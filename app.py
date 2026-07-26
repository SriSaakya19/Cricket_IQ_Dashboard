import pandas as pd
import streamlit as st
import plotly.express as px
import os

st.set_page_config(page_title="Cricket IQ - IPL Analytics", layout="wide")

@st.cache_data
def load_data():
    matches_path = r"c:\Users\user\Downloads\archive (4)\matches.csv"
    deliveries_path = r"c:\Users\user\Downloads\archive (4)\deliveries.csv"
    matches = pd.read_csv(matches_path)
    deliveries = pd.read_csv(deliveries_path)
    return matches, deliveries

matches, deliveries = load_data()
st.success(f"✅ Loaded {len(deliveries):,} balls and {len(matches):,} matches")

st.title("🏏 Cricket IQ - IPL Analytics Dashboard")

# SIDEBAR
st.sidebar.header("Filters")
season = st.sidebar.multiselect("Select Season", options=sorted(matches['season'].unique()), default=sorted(matches['season'].unique()))
all_teams = sorted(set(matches['team1'].unique()) | set(matches['team2'].unique()))
team = st.sidebar.multiselect("Select Team", options=all_teams)

filtered_matches = matches[matches['season'].isin(season)]
filtered_deliveries = deliveries[deliveries['match_id'].isin(filtered_matches['id'])]

if team:
    filtered_matches = filtered_matches[(filtered_matches['team1'].isin(team)) | (filtered_matches['team2'].isin(team))]
    filtered_deliveries = deliveries[deliveries['match_id'].isin(filtered_matches['id'])]

tab1, tab2, tab3 = st.tabs(["📊 Overview", "👑 Top Players", "🏆 Team Stats"])

with tab1:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Matches", len(filtered_matches))
    col2.metric("Total Runs", f"{filtered_deliveries['total_runs'].sum():,}")
    col3.metric("Total Wickets", filtered_deliveries['player_dismissed'].count())
    
    runs_df = filtered_deliveries.merge(filtered_matches[['id', 'season']], left_on='match_id', right_on='id', how='inner')
    runs_per_season = runs_df.groupby('season')['total_runs'].sum().reset_index()
    fig = px.bar(runs_per_season, x='season', y='total_runs', title="Total Runs per Season")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # AUTO DETECT COLUMN NAME
    if 'batsman' in filtered_deliveries.columns:
        bat_col = 'batsman'
    elif 'batter' in filtered_deliveries.columns:
        bat_col = 'batter'
    else:
        st.error("No batsman/batter column found")
        bat_col = None
    
    if bat_col:
        top_batsman = filtered_deliveries.groupby(bat_col)['total_runs'].sum().sort_values(ascending=False).head(10).reset_index()
        fig1 = px.bar(top_batsman, x=bat_col, y='total_runs', title="Top 10 Run Scorers")
        fig1.update_xaxes(tickangle=45)
        st.plotly_chart(fig1, use_container_width=True)
    
    wickets = filtered_deliveries[filtered_deliveries['player_dismissed'].notna()]
    top_bowler = wickets.groupby('bowler')['player_dismissed'].count().sort_values(ascending=False).head(10).reset_index()
    fig2 = px.bar(top_bowler, x='bowler', y='player_dismissed', title="Top 10 Wicket Takers")
    fig2.update_xaxes(tickangle=45)
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    win_counts = filtered_matches['winner'].value_counts().head(10).reset_index()
    win_counts.columns = ['Team', 'Wins']
    fig3 = px.bar(win_counts, x='Team', y='Wins', title="Most Wins by Team")
    fig3.update_xaxes(tickangle=45)
    st.plotly_chart(fig3, use_container_width=True)