import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cricket IQ Analytics", layout="wide")
st.title("🏏 Cricket IQ Analytics Dashboard")
st.markdown("IPL Data Analysis using Matches and Deliveries Dataset")

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

    # Sidebar filters
    st.sidebar.header("Filters")
    seasons = st.sidebar.multiselect("Select Season", options=sorted(matches['season'].unique()), default=sorted(matches['season'].unique()))
    
    filtered_matches = matches[matches['season'].isin(seasons)]
    filtered_deliveries = deliveries[deliveries['match_id'].isin(filtered_matches['id'])]

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "🏆 Teams", "🔥 Players"])

    with tab1:
        st.header("Matches Data")
        st.dataframe(filtered_matches.head(10), use_container_width=True)

        st.header("Deliveries Data") 
        st.dataframe(filtered_deliveries.head(10), use_container_width=True)

        st.subheader("📊 Matches per Season")
        if 'season' in filtered_matches.columns:
            season_counts = filtered_matches['season'].value_counts().sort_index()
            fig2 = px.line(x=season_counts.index, y=season_counts.values, markers=True, title='Matches per Season')
            st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        st.subheader("🏆 Most Matches Won by Team")
        # 'winner' lekunte 'winning_team' try chey
        win_col = 'winner' if 'winner' in filtered_matches.columns else 'winning_team'
        if win_col in filtered_matches.columns:
            winners = filtered_matches[win_col].value_counts().head(10)
            fig1 = px.bar(x=winners.index, y=winners.values, title='Top 10 Winning Teams')
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.warning(f"Winner column dorakaledu")

        st.subheader("Toss Winner vs Match Winner")
        if 'toss_winner' in filtered_matches.columns and win_col in filtered_matches.columns:
            toss_win_match_win = (filtered_matches['toss_winner'] == filtered_matches[win_col]).sum()
            st.metric("Toss Win = Match Win", f"{toss_win_match_win} times")

    with tab3:
        st.subheader("🔥 Top 10 Run Scorers")
        if 'batter' in filtered_deliveries.columns and 'batsman_runs' in filtered_deliveries.columns:
            top_batters = filtered_deliveries.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(10)
            fig3 = px.bar(x=top_batters.index, y=top_batters.values, title='Top 10 Run Scorers')
            st.plotly_chart(fig3, use_container_width=True)

        st.subheader("⚡ Top 10 Wicket Takers")
        if 'bowler' in filtered_deliveries.columns and 'is_wicket' in filtered_deliveries.columns:
            wickets = filtered_deliveries[filtered_deliveries['is_wicket'] == 1]
            top_bowlers = wickets['bowler'].value_counts().head(10)
            fig4 = px.bar(x=top_bowlers.index, y=top_bowlers.values, title='Top 10 Wicket Takers')
            st.plotly_chart(fig4, use_container_width=True)

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Check if Google Drive links are public and FILE_IDs are correct")