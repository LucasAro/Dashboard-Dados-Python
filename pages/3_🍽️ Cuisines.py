import streamlit as st
from utils.utils import process_data, sidebar_filters, chart_bar
import os

############################################
# LEITURA DO CSV E CONFIGURAÇÃO INICIAL
############################################
st.set_page_config(page_title='Countries', page_icon='🌍', layout='wide', initial_sidebar_state='expanded')
df = process_data()
#df = process_data('../data/zomato.csv')


##########################
#BARRA LATERAL NO STREAMLIT
##########################

country_options = sidebar_filters(df)

num_restaurants = st.sidebar.slider('Número de Restaurantes', min_value=1, max_value=20, value=10)

cuisine_options = df['cuisines'].unique()
cuisine_options = st.sidebar.multiselect('Selecione o Tipo de Culinária', cuisine_options, default=cuisine_options[:5])

df_filter = df[df['country_name'].isin(country_options)]
df_filter = df[df['cuisines'].isin(cuisine_options)]

##########################
#LAYOUT NO STREAMLIT
##########################

st.write('# 🍽️ Visão Tipos de Cosinhas')

st.write('## Melhores Restaurantes dos Principais Tipos Culinários')
col1, col2, col3, col4, col5 = st.columns(5)

cuisines = ['North Indian', 'Arabian', 'Brazilian', 'Pizza', 'Italian']
columns = [col1, col2, col3, col4, col5]

for cuisine, col in zip(cuisines, columns):
	df_cuisine = df[df['cuisines'].isin([cuisine])].sort_values('aggregate_rating', ascending=False).drop_duplicates('cuisines')[['restaurant_name', 'cuisines', 'aggregate_rating', 'country_name', 'city', 'average_cost_for_two']].head(1)
	for index, row in df_cuisine.iterrows():
		col.metric(
			label=f"{row['cuisines']}: {row['restaurant_name']}",
			value=f"{row['aggregate_rating']}/5.0",
			delta=None,
			help=f"Country: {row['country_name']}, City: {row['city']}, Average cost for two: {row['average_cost_for_two']}"
		)

st.write(f'## Top {num_restaurants} Restaurantes com Melhor Avaliação')
df_top = df_filter.sort_values('aggregate_rating', ascending=False).drop_duplicates('restaurant_id')[['restaurant_name', 'cuisines', 'aggregate_rating', 'country_name', 'city', 'average_cost_for_two', 'votes']].head(num_restaurants)
st.dataframe(df_top, width=1800)

col1, col2 = st.columns(2)

with col1:
	df_cuisine = df_filter.groupby('cuisines')['aggregate_rating'].mean().reset_index()
	df_cuisine = df_cuisine.sort_values(by='aggregate_rating', ascending=False)
	df_cuisine = df_cuisine.head(num_restaurants)
	fig = chart_bar(df_cuisine, f'Top {num_restaurants} Tipos de Culinária com Melhor Avaliação', 'Tipo de Culinária', 'Média de Avaliação')
	fig.update_layout(height=500)
	st.plotly_chart(fig)

with col2:
	df_bottom = df_filter.sort_values('aggregate_rating', ascending=True).drop_duplicates('restaurant_id')[['restaurant_name', 'cuisines', 'aggregate_rating', 'country_name', 'city', 'average_cost_for_two', 'votes']].head(num_restaurants)
	df_cuisine = df_filter.groupby('cuisines')['aggregate_rating'].mean().reset_index()
	df_cuisine = df_cuisine.sort_values(by='aggregate_rating', ascending=True)
	df_cuisine = df_cuisine.head(num_restaurants)
	fig = chart_bar(df_cuisine, f'Top {num_restaurants} Tipos de Culinária com Pior Avaliação', 'Tipo de Culinária', 'Média de Avaliação')
	fig.update_layout(height=500)

	st.plotly_chart(fig)