import streamlit as st
from utils.utils import process_data, sidebar_filters, chart_bar

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
st.write('# 🌎 Visão Países')

df_country = df['country_name'].value_counts().reset_index()
df_country = df_country.sort_values(by='count', ascending=False)

fig = chart_bar(df_country, 'Quantidade de Restaurantes por País', 'Países', 'Quantidade de Restaurantes')
st.plotly_chart(fig)


df_country_city = df.groupby('country_name')['city'].nunique().reset_index()
df_country_city = df_country_city.sort_values(by='city', ascending=False)

fig = chart_bar(df_country_city, 'Quantidade de Cidades por País', 'Países', 'Quantidade de Cidades')
st.plotly_chart(fig)

col1, col2 = st.columns(2)

with col1:
	df_avg_votes = df.groupby('country_name')['votes'].mean().reset_index()
	df_avg_votes = df_avg_votes.sort_values(by='votes', ascending=False)
	fig = chart_bar(df_avg_votes, 'Média de Avaliações por País', 'Países', 'Média de Avaliações')
	fig.update_layout(height=500)
	st.plotly_chart(fig)

with col2:
	df_avg_price = df.groupby('country_name')['average_cost_for_two'].mean().reset_index()
	df_avg_price = df_avg_price.sort_values(by='average_cost_for_two', ascending=False)
	fig = chart_bar(df_avg_price, 'Média de Preço por País', 'Países', 'Média de Preço para  Duas Pessoas')
	fig.update_layout(height=500)
	st.plotly_chart(fig)
