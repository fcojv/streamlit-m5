# source streamlit-env/bin/activate
# streamlit run employees.py --server.enableCORS false -- server.enableXsrfProtection false
# DSA05 Reto
# Francisco Moises Jimenez Vasconcelos

# Se importan librerías
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# Se establecen lo valores de las variables
DATA_URL = 'Employees.csv'
select_hometown = ''
select_unit = ''
select_educationLevel = 0

# Se crea función para leer datos en un dataframe
@st.cache
def datosCargados(numeroFilas):
  data = pd.read_csv(DATA_URL, nrows = numeroFilas)
  lowercase = lambda x: str(x).lower()
  data.rename(lowercase, axis='columns', inplace=True)
  return data

def filter_data_by_employee_id(id):
    filtered_data_employee_id = data[data['employee_id'].str.upper().str.contains(id)]
    return filtered_data_employee_id

def filter_data_by_hometown(hometown):
    filtered_data_hometown = data[data['hometown'].str.upper().str.contains(hometown)]
    return filtered_data_hometown

def filter_data_by_unit(unit):
    filtered_data_unit = data[data['unit'].str.upper()==(unit)]
    return filtered_data_unit

def filter_data_by_education_level(educationLevel):
    filtered_data_education_level = data[data['education_level']==educationLevel]
    return filtered_data_education_level

def filter_data(data_filter,count_row):
    st.write(f"Total de empleados mostrados : {count_row}")
    st.write(data_filter)

st.set_page_config(page_title="DSA05 Reto | Análisis de deserción de empleados", page_icon="icon_IA.png")

st.title("DSA05 Reto | Análisis de deserción de empleados")
st.markdown("_El sitio muestra información del Hackathon HackerEarth 2020 sobre la deserción de empleados, se realiza un análisis para intentar explicar este fenómeno_")

data = datosCargados(500) 

st.sidebar.image("icon_IA.png",width=80)

if st.sidebar.checkbox('Mostrar todos los datos'):
  count_row = data.shape[0]
  st.subheader(f'Información que se está utilizando ({count_row} registros)')
  st.write(data)

idempleado = st.sidebar.text_input('ID del empleado:')
btnBuscarID = st.sidebar.button('Buscar ID')
hometown = st.sidebar.text_input('Ciudad del empleado:')
btnBuscarHometown = st.sidebar.button('Buscar Ciudad')
unit = st.sidebar.text_input('Unidad del empleado:')
btnBuscarUnit = st.sidebar.button('Buscar Unidad')

select_hometown = st.sidebar.selectbox("Selecciona una ciudad",options=data['hometown'].unique())
select_unit = st.sidebar.selectbox("Selecciona una unidad", options=data['unit'].unique())
select_educationLevel = st.sidebar.selectbox("Selecciona un nivel de estudios", options=data['education_level'].unique())


if (btnBuscarID):
   data_filter = filter_data_by_employee_id(idempleado.upper())
   count_row = data_filter.shape[0]  # Gives number of rows
   st.subheader(f'Filtros de texto')
   filter_data(data_filter,count_row)

if (btnBuscarHometown):
   data_filter = filter_data_by_hometown(hometown.upper())
   count_row = data_filter.shape[0]  # Gives number of rows
   st.subheader(f'Filtros de texto')
   filter_data(data_filter,count_row)

if (btnBuscarUnit):
   data_filter = filter_data_by_unit(unit.upper())
   count_row = data_filter.shape[0]  # Gives number of rows
   st.subheader(f'Filtros de texto')
   filter_data(data_filter,count_row)

if (select_hometown or select_unit or select_educationLevel):
   data_filter = filter_data_by_hometown(select_hometown.upper()).merge(filter_data_by_unit(select_unit.upper())).merge(filter_data_by_education_level(select_educationLevel))
   count_row = data_filter.shape[0]  # Gives number of rows
   st.subheader(f'Filtros de combo')
   filter_data(data_filter,count_row)

hist_edad, ax = plt.subplots()
ax.hist(data['age'], bins=[10,20,25,30,35,40,45,50,55,60,65,70])
ax.set_xlabel("Edad")
st.subheader("Histograma de empleados por edad")
st.pyplot(hist_edad)

employees_by_unit = data[['employee_id','unit']].groupby('unit').count()
st.subheader("Número de empleados por unidad")
st.bar_chart(employees_by_unit)

employees_by_hometown = data[['employee_id','hometown','attrition_rate']].groupby('hometown')
employees_by_hometown = employees_by_hometown['attrition_rate'].sum()/employees_by_hometown['employee_id'].count()
st.subheader("Ciudades con mayor índice de deserción")
st.line_chart(employees_by_hometown)

data.plot(kind='scatter', x='age', y='attrition_rate')

st.subheader("Relación Edad - Tasa de deserción")
scatter_edad = px.scatter(data, x="age", y="attrition_rate",color="attrition_rate")
st.plotly_chart(scatter_edad)

st.subheader("Relación Tiempo de servicio - Tasa de deserción")
scatter_servicio = px.scatter(data, x="time_of_service", y="attrition_rate", color="attrition_rate")
st.plotly_chart(scatter_servicio)
