import streamlit as st
from utils.utils import process_data, sidebar_filters, plot_top_cities

############################################
# LEITURA DO CSV E CONFIGURAÇÃO INICIAL
############################################
df = process_data()
st.set_page_config(page_title='Countries', page_icon='🌍', layout='wide', initial_sidebar_state='expanded')

##########################
#BARRA LATERAL NO STREAMLIT
##########################

country_options = sidebar_filters(df)
df = df[df['country_name'].isin(country_options)]

##########################
#LAYOUT NO STREAMLIT
##########################
st.write('# 🌇 Visão Cidades')

df_city = df['city'].value_counts().reset_index()
df_city.columns = ['city', 'count']
df_city = df_city.sort_values(by='count', ascending=False)
df_city = df_city.head(10)

df_city = df_city.merge(df[['city', 'country_name']].drop_duplicates(), on='city', how='left')

df_city = df['city'].value_counts().reset_index()
df_city.columns = ['city', 'count']
df_city = df_city.sort_values(by='count', ascending=False)
df_city = df_city.head(10)

df_city = df_city.merge(df[['city', 'country_name']].drop_duplicates(), on='city', how='left')

fig = plot_top_cities(df_city, 'Top 10 Cidades com Mais Restaurantes', 'Cidades', 'Quantidade de Restaurantes')
st.plotly_chart(fig)

col1, col2 = st.columns(2)

with col1:
	df_city_rating = df[df['aggregate_rating'] > 4]['city'].value_counts().reset_index()
	df_city_rating.columns = ['city', 'count']
	df_city_rating = df_city_rating.head(7)
	df_city_rating = df_city_rating.merge(df[['city', 'country_name']].drop_duplicates(), on='city', how='left')
	fig = plot_top_cities(df_city_rating, 'Top 7 Cidades com Restaurantes com Média Acima de 4', 'Cidades', 'Quantidade de Restaurantes')
	st.plotly_chart(fig)

with col2:
	df_city_rating = df[df['aggregate_rating'] < 2.5]['city'].value_counts().reset_index()
	df_city_rating.columns = ['city', 'count']
	df_city_rating = df_city_rating.head(7)
	df_city_rating = df_city_rating.merge(df[['city', 'country_name']].drop_duplicates(), on='city', how='left')
	fig = plot_top_cities(df_city_rating, 'Top 7 Cidades com Restaurantes com Média Abaixo de 4', 'Cidades', 'Quantidade de Restaurantes')
	st.plotly_chart(fig)

df_city_cuisine = df.groupby('city')['cuisines'].nunique().reset_index()
df_city_cuisine.columns = ['city', 'count']
df_city_cuisine = df_city_cuisine.sort_values(by='count', ascending=False)
df_city_cuisine = df_city_cuisine.head(10)
df_city_cuisine = df_city_cuisine.merge(df[['city', 'country_name']].drop_duplicates(), on='city', how='left')
fig = plot_top_cities(df_city_cuisine, 'Top 10 Cidades com Mais Tipos de Culinária Distintos', 'Cidades', 'Quantidade de Tipos de Culinária')
st.plotly_chart(fig)