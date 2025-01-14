import streamlit as st
import pandas as pd
import inflection
import plotly.express as px
import os

def rename_columns(dataframe):
	df = dataframe.copy()
	title = lambda x: inflection.titleize(x)
	snakecase = lambda x: inflection.underscore(x)
	spaces = lambda x: x.replace(" ", "")
	cols_old = list(df.columns)
	cols_old = list(map(title, cols_old))
	cols_old = list(map(spaces, cols_old))
	cols_new = list(map(snakecase, cols_old))
	df.columns = cols_new
	return df

def country_name(country_id):
	return COUNTRIES[country_id]

def create_price_tye(price_range):
	if price_range == 1:
		return "cheap"
	elif price_range == 2:
		return "normal"
	elif price_range == 3:
		return "expensive"
	else:
		return "gourmet"

def color_name(color_code):
	return COLORS[color_code]

COUNTRIES = {
	1: "India",
	14: "Australia",
	30: "Brazil",
	37: "Canada",
	94: "Indonesia",
	148: "New Zeland",
	162: "Philippines",
	166: "Qatar",
	184: "Singapure",
	189: "South Africa",
	191: "Sri Lanka",
	208: "Turkey",
	214: "United Arab Emirates",
	215: "England",
	216: "United States of America",
}
COLORS = {
	"3F7E00": "darkgreen",
	"5BA829": "green",
	"9ACD32": "lightgreen",
	"CDD614": "orange",
	"FFBA00": "red",
	"CBCBC8": "darkred",
	"FF7800": "darkred",
}


def process_data():
	pathCsv = os.path.abspath(os.getcwd())
	file_path = pathCsv + '/data/zomato.csv'
	df = pd.read_csv(file_path)
	df = rename_columns(df)
	df['country_name'] = df['country_code'].apply(country_name)
	df['price_type'] = df['price_range'].apply(create_price_tye)
	df["cuisines"] = df["cuisines"].fillna("").apply(lambda x: x.split(",")[0])
	df = df[df['aggregate_rating'] > 0]

	return df

def sidebar_filters(df):
	st.sidebar.markdown('## Filtros')
	country_options = st.sidebar.multiselect(
		'Escolha os países que deseja visualizar os restaurantes',
		options=df['country_name'].unique(),
		default=['Brazil', 'Canada', 'South Africa', 'England', 'Australia']
	)
	return country_options


def chart_bar(df, title, label1, label2):
    fig = px.bar(
        df,
        x=df.columns[0],
        y=df.columns[1],
        text=df.columns[1],
        title=title,
        labels={df.columns[0]: label1, df.columns[1]: label2},
        category_orders={
            df.columns[0]: df[df.columns[0]].tolist()
        }
    )
    fig.update_traces(textposition='inside', texttemplate='%{text:.2f}')
    for trace in fig.data:
        if any(len(str(text)) > 5 for text in trace.text):
            trace.textposition = 'outside'
    return fig

def plot_top_cities(df, title, label1, label2):
	fig = px.bar(
		df,
		x=df.columns[0],
		y=df.columns[1],
		title=title,
		text=df.columns[1],
		labels={df.columns[0]: label1, df.columns[1]: label2, 'country_name': 'País'},
		color='country_name'
	)
	fig.update_traces(textposition='inside')
	fig.update_layout(height=500)
	return fig