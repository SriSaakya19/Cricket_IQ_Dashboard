import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cricket IQ Analytics", layout="wide")
st.title("🏏 Cricket IQ Analytics Dashboard")

DELIVERIES_FILE_ID = "1h0kIMBu2Zy9i6P5Z3Ip7v-7NUGcbbmpe"

@st.cache_data
def load_data():
    deliveries_url = f'https://drive.google.com/uc?export=download&id={DELIVERIES_FILE_ID}'
    deliveries = pd.read_csv(deliveries_url)
    return deliveries

deliveries = load_data()
st.success("✅ Data Loaded!")

st.header("📋 First 10 Rows")
st.dataframe(deliveries.head(10), use_container_width=True)

# 1. Top 10 Run Scorers - Capital B, Total_Runs
st.header("🔥 Top 10 Run Scorers")
top_batters = deliveries.groupby('Batter')['Total_Runs'].sum().sort_values(ascending=False).head(10)
fig1 = px.bar(x=top_batters.index, y=top_batters.values, title='Top 10 Run Scorers')
fig1.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig1, use_container_width=True)

# 2. Top 10 Wicket Takers
st.header("⚡ Top 10 Wicket Takers")
wickets = deliveries[deliveries['Is_Wicket'] == 1]
top_bowlers = wickets.groupby('Bowler')['Is_Wicket'].sum().sort_values(ascending=False).head(10)
fig2 = px.bar(x=top_bowlers.index, y=top_bowlers.values, title='Top 10 Wicket Takers')
fig2.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig2, use_container_width=True)