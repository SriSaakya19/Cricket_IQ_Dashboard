import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cricket IQ Analytics", layout="wide")
st.title("🏏 Cricket IQ Analytics Dashboard")

# Google Drive FILE IDs
MATCHES_FILE_ID = "1Hd1SMxjtgPMhXfwonUmkY9fsokn0qF5J"
DELIVERIES_FILE_ID = "1h0kIMBu2Zy9i6P5Z3Ip7v-7NUGcbbmpe"

@st.cache_data
def load_data():
    matches_url = f'https://drive.google.com/uc?export=download&id={MATCHES_FILE_ID}'
    deliveries_url = f'https://drive.google.com/uc?export=download&id={DELIVERIES_FILE_ID}'
    
    matches = pd.read_csv(matches_url)
    deliveries = pd.read_csv(deliveries_url)
    return matches, deliveries

try:
    matches, deliveries = load_data()
    st.success("✅ Data loaded successfully from Google Drive!")
    
    st.header("Matches Data")
    st.dataframe(matches.head())
    
    st.header("Deliveries Data") 
    st.dataframe(deliveries.head())

    # Example chart - nee original dashboard code ikkada pettu
    st.header("Sample Chart")
    fig = px.bar(matches, x='season', y='id', title='Matches per Season')
    st.plotly_chart(fig)

except Exception as e:
    st.error(f"Error loading data: {e}")