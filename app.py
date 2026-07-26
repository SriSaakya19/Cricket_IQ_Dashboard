import streamlit as st
import pandas as pd

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

st.write("**Columns:**", list(deliveries.columns))
st.dataframe(deliveries.head(20), use_container_width=True)