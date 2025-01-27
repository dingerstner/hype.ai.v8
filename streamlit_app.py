import streamlit as st
import pandas as pd
from datetime import timedelta, datetime
import altair as alt

#######################
# Page configuration

st.set_page_config(page_title="home", layout="wide",initial_sidebar_state="expanded")
st.logo("images/logo.png")

alt.themes.enable("dark")
#######################
# --- HIDE STREAMLIT BRANDING ---

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- LOAD DATA ---

@st.cache_data

def load_data():
 data = pd.read_csv("data.csv")
 data['DATE'] = pd.to_datetime(data['DATE'])
 return data

def format_with_commas(number):
    return f"{number:,}"

def create_metric_chart(df, column, color, height=150):
    chart_df = df[["DATE", column]].set_index("DATE")
    return st.area_chart(chart_df, color=color, height=height)

def display_metric(col, title, value, df, column, color):
    with col:
        with st.container(border=True):
            st.metric(title, format_with_commas(value))
            create_metric_chart(df, column, color)

# Load data
df = load_data()
df_cumulative = df.copy()
for column in ['WORTH','SCORE']:
    df_cumulative[column] = df_cumulative[column].cumsum()

with st.sidebar:
    st.header("⚙️ Settings")
    start_date = st.date_input("Start date", df['DATE'].min())
    end_date = st.date_input("End date", df['DATE'].max())
    time_frame = st.selectbox("Select time frame", ("Daily", "Cumulative"))

st.subheader("Key Metrics")
st.caption("All-Time Statistics")


metrics = [
("Total worth", "WORTH", '#29b5e8'),
("Total score", "SCORE", '#FF9F36'),    
]

cols = st.columns(2)
for col, (title, column, color) in zip(cols, metrics):
    display_metric(col, title, df[column].sum(), 
                   df_cumulative if time_frame == "Cumulative" else df, 
                   column, color)

# Selected Duration Metrics
st.caption("Selected Duration")
df_filtered = df_cumulative if time_frame == "Cumulative" else df
mask = (df_filtered['DATE'].dt.date >= start_date) & (df_filtered['DATE'].dt.date <= end_date)
df_filtered = df_filtered.loc[mask]

cols = st.columns(2)
for col, (title, column, color) in zip(cols, metrics):
    display_metric(col, title.split()[-1], df_filtered[column].sum(), 
                   df_filtered, column, color)

# DataFrame display

st.dataframe(df)