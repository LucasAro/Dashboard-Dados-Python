import streamlit as st
from streamlit_folium import folium_static
from utils.utils import process_data, color_name, sidebar_filters
import folium
from folium.plugins import MarkerCluster
import streamlit as st
from utils.utils import process_data, sidebar_filters


##########################
# LEITURA DO CSV E CONFIGURAÇÃO INICIAL
##########################
st.set_page_config(page_title='Main Page', page_icon=':truck:', layout='wide', initial_sidebar_state='expanded')
df = process_data()

##########################
#BARRA LATERAL NO STREAMLIT
##########################

st.sidebar.markdown('# Fome Zero')
country_options = sidebar_filters(df)
st.sidebar.markdown('## Dados Tratados')

if st.sidebar.button('Download'):
	df.to_csv('zomato_tratado.csv', index=False)
	st.sidebar.markdown('Download Realizado com Sucesso!')

df_filter = df[df['country_name'].isin(country_options)]

##########################
#LAYOUT NO STREAMLIT
##########################

st.write('# Fome Zero!')
st.write('## O Melhor lugar para encontrar seu mais novo restaurante favorito!')
st.write('### Temos as seguintes marcas dentro da nossa plataforma:')

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
	unique_restaurants = df['restaurant_id'].nunique()
	st.metric('Restaurantes Cadastrados', unique_restaurants)

with col2:
	unique_countries = df['country_code'].nunique()
	st.metric('Países Cadastrados', unique_countries)

with col3:
	unique_city = df['city'].nunique()
	st.metric('Cidades Cadastradas', unique_city)

with col4:
	sum_avg = df['votes'].sum()
	sum_avg = '{:,}'.format(sum_avg)
	st.metric('Avaliações Feitas na Plataforma', sum_avg)

with col5:
	unique_cuisines = df['cuisines'].nunique()
	st.metric('Tipos de Culinária Cadastrados', unique_cuisines)

mapa = folium.Map(location=[df_filter['latitude'].mean(), df_filter['longitude'].mean()], zoom_start=3)
cluster = MarkerCluster().add_to(mapa)

for row in df_filter.itertuples():
	folium.Marker(
		location=[row.latitude, row.longitude],
		popup=folium.Popup(
			f"<b>Nome:</b> {row.restaurant_name}<br><b>Preço Para Dois:</b> {row.average_cost_for_two} , {row.currency} <br><b>Culinária:</b> {row.cuisines}<br><b>Avaliação:</b> {row.aggregate_rating}",
			max_width=300
		),
		icon=folium.Icon(color=color_name(row.rating_color))
	).add_to(cluster)

folium_static(mapa, width=1000, height=500)
