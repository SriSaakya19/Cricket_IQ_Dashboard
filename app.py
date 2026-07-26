import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cricket IQ Analytics", layout="wide")
st.title("🏏 Cricket IQ Analytics Dashboard")

MATCHES_FILE_ID = "1Hd1SMxjtgPMhXfwonUmkY9fsokn0qF5J"
DELIVERIES_FILE_ID = "1h0kIMBu2Zy9i6P5Z3Ip7v-7NUGcbbmpe"

@st.cache_data
def load_data():
    matches_url = f'https://drive.google.com/uc?export=download&id={MATCHES_FILE_ID}'
    deliveries_url = f'https://drive.google.com/uc?export=download&id={DELIVERIES_FILE_ID}'
    matches = pd.read_csv(matches_url)
    deliveries = pd.read_csv(deliveries_url)
    return matches, deliveries

matches, deliveries = load_data()
st.success("✅ Data loaded!")

st.dataframe(matches.head(10), use_container_width=True)

# Winner find cheyadam
st.subheader("🏆 Top 10 Winning Teams")
win_col = None
for col in matches.columns:
    if 'win' in col.lower() or 'winner' in col.lower():
        win_col = col
        break

if win_col:
    winners = matches[win_col].value_counts().head(10)
    fig1 = px.bar(x=winners.index, y=winners.values, title='Top 10 Winning Teams')
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.write("Matches columns:", list(matches.columns))

# Top batsmen
st.subheader("🔥 Top 10 Run Scorers")
if 'batter' in deliveries.columns and 'batsman_runs' in deliveries.columns:
    top_batters = deliveries.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(10)
    fig2 = px.bar(x=top_batters.index, y=top_batters.values, title='Top 10 Run Scorers')
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.write("Deliveries columns:", list(deliveries.columns))