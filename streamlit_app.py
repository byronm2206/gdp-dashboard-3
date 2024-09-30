import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Función para limpiar la pantalla
def limpiar_pantalla():
    st.session_state.clear()

# Título de la aplicación
st.subheader("Simulación de Punto de Equilibrio y Utilidad")
st.subheader("Autor: Byron Méndez")

# Selección de tipo de cálculo
tipo_calculo = st.radio(
    "Seleccione el tipo de cálculo:",
    ('Cálculo con unidades', 'Cálculo con porcentaje de costo variable', 'Cálculo con total de gastos y ventas', 'Cálculo con total de ventas y % costo variable')
)

# Inputs y cálculos según la selección
if tipo_calculo == 'Cálculo con unidades':
    # Parámetros de entrada
    gastos_fijos = st.number_input('Ingrese los gastos generales ($)', min_value=0, value=0000, step=100, key="gastos_fijos")
    costo_variable = st.number_input('Ingrese el costo variable por unidad ($)', min_value=0.0, value=1.00, step=0.1, key="costo_variable")
    precio_venta = st.number_input('Ingrese el precio de venta por unidad ($)', min_value=0.0, value=2.00, step=0.1, key="precio_venta")
    unidades_producir = st.number_input('Unidades a producir', min_value=0, value=0, step=10, key="unidades_producir")

    # Calcular el punto de equilibrio y la utilidad
    if precio_venta > costo_variable:
        punto_equilibrio = gastos_fijos / (precio_venta - costo_variable)
        ingresos_totales = precio_venta * unidades_producir
        costos_variables_totales = costo_variable * unidades_producir
        utilidad = ingresos_totales - (gastos_fijos + costos_variables_totales)

        # Mostrar las salidas
        st.write(f"Punto de Equilibrio: **{punto_equilibrio:.2f} unidades**")
        st.write(f"Total de Ventas: **${ingresos_totales:.2f}**")
        st.write(f"Costos Variables Totales: **${costos_variables_totales:.2f}**")
        st.write(f"Gastos Generales: **${gastos_fijos:.2f}**")
        st.write(f"Utilidad: **${utilidad:.2f}**")

        # Generar gráfica
        if st.button("Mostrar Gráfica"):
            cantidades = np.arange(0, (punto_equilibrio*2), 1) 
            ingresos_totales_graf = precio_venta * cantidades
            costos_totales_graf = gastos_fijos + (costo_variable * cantidades)

            plt.figure(figsize=(10,6))
            plt.fill_between(cantidades, costos_totales_graf, ingresos_totales_graf, where=(cantidades < punto_equilibrio), color='red', alpha=0.3, label='Pérdidas')
            plt.fill_between(cantidades, costos_totales_graf, ingresos_totales_graf, where=(cantidades >= punto_equilibrio), color='green', alpha=0.3, label='Ganancias')
            plt.plot(cantidades, ingresos_totales_graf, label='Ingresos Totales', color='blue')
            plt.plot(cantidades, costos_totales_graf, label='Costos Totales', color='orange')
            plt.axvline(x=punto_equilibrio, color='red', linestyle='--', label=f'Punto de Equilibrio: {punto_equilibrio:.2f} unidades')
            plt.axvline(x=unidades_producir, color='black', linestyle='-.', label=f'Unidades a Producir: {unidades_producir} unidades')
            plt.xlabel('Cantidad vendida')
            plt.ylabel('Total Gastos($)')
            plt.title('Gráfico del Punto de Equilibrio: Pérdidas y Ganancias')
            plt.legend()
            plt.grid(True)
            st.pyplot(plt)

elif tipo_calculo == 'Cálculo con porcentaje de costo variable':
    # Inputs adicionales para este caso
    total_gastos = st.number_input('Ingrese el total de gastos ($)', min_value=0, value=0, step=100, key="total_gastos")
    porcentaje_costo_variable = st.number_input('Ingrese el porcentaje del costo variable (%)', min_value=0.0, max_value=100.0, value=10.0, step=0.1, key="porcentaje_costo_variable") / 100

    # Calcular total de ventas
    total_ventas = total_gastos / (1 - porcentaje_costo_variable)

    # Mostrar el resultado
    st.write(f"Total de Ventas Necesarias: **${total_ventas:.2f}**")

    # Gráfico con punto de equilibrio
    if st.button("Mostrar Gráfica"):
        punto_equilibrio = total_gastos / (1 - porcentaje_costo_variable)
        cantidades = np.arange(0, (punto_equilibrio*2), 1)
        ingresos_totales_graf = total_ventas * (cantidades / punto_equilibrio)
        costos_totales_graf = total_gastos + (porcentaje_costo_variable * total_ventas * cantidades / punto_equilibrio)

        plt.figure(figsize=(10,6))
        plt.fill_between(cantidades, costos_totales_graf, ingresos_totales_graf, where=(cantidades < punto_equilibrio), color='red', alpha=0.3, label='Pérdidas')
        plt.fill_between(cantidades, costos_totales_graf, ingresos_totales_graf, where=(cantidades >= punto_equilibrio), color='green', alpha=0.3, label='Ganancias')
        plt.plot(cantidades, ingresos_totales_graf, label='Ingresos Totales', color='blue')
        plt.plot(cantidades, costos_totales_graf, label='Costos Totales', color='orange')
        plt.axvline(x=punto_equilibrio, color='red', linestyle='--', label=f'Punto de Equilibrio $: {punto_equilibrio:.2f}')
        plt.xlabel('Ventas Necesarias$')
        plt.ylabel('Total Gastos($)')
        plt.title('Gráfico del Punto de Equilibrio con Porcentaje de Costo Variable')
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)

elif tipo_calculo == 'Cálculo con total de gastos y ventas':
    # Inputs
    total_gastos = st.number_input('Ingrese el total de gastos ($)', min_value=0, value=10, step=100, key="total_gastos")
    total_ventas = st.number_input('Ingrese el total de ventas ($)', min_value=0, value=20, step=100, key="total_ventas")

    # Calcular porcentaje de costos variables
    porcentaje_costo_variable = (total_ventas-total_gastos)/total_ventas
    
    # Mostrar el resultado
    st.write(f"Porcentaje del Costo Variable: **{porcentaje_costo_variable*100:.2f}%**")

    # Gráfico corregido para este cálculo
    if st.button("Mostrar Gráfica"):
        plt.figure(figsize=(10,6))
        plt.bar(['Total Gastos', 'Total Ventas'], [total_gastos, total_ventas], color=['orange', 'blue'])
        plt.title('Comparación de Gastos y Ventas')
        plt.ylabel('Dinero ($)')
        st.pyplot(plt)

elif tipo_calculo == 'Cálculo con total de ventas y % costo variable':
    # Inputs
    total_ventas = st.number_input('Ingrese el total de ventas ($)', min_value=0, value=0, step=100, key="total_ventas")
    porcentaje_costo_variable = st.number_input('Ingrese el porcentaje del costo variable (%)', min_value=0.0, max_value=100.0, value=10.0, step=0.1, key="porcentaje_costo_variable") / 100

    # Calcular total de gastos correctamente
    total_gastos = total_ventas * (1-porcentaje_costo_variable)

    # Mostrar el resultado
    st.write(f"Total de Gastos: **${total_gastos:.2f}**")

    # Gráfico para este cálculo
    if st.button("Mostrar Gráfica"):
        plt.figure(figsize=(10,6))
        plt.pie([total_gastos, total_ventas-total_gastos], labels=['Gastos', 'Costo de ventas'], autopct='%1.1f%%', colors=['orange', 'green'])
        plt.title('Distribución de Gastos y Costo de Ventas')
        st.pyplot(plt)

# Botón para limpiar la pantalla
if st.button("Limpiar Pantalla"):
    limpiar_pantalla()
