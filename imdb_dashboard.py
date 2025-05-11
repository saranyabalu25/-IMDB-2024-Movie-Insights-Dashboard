import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Page Configuration
st.set_page_config(page_title="IMDB 2024 Movie Insights", layout="wide", page_icon="🎬")

# Title
st.markdown("""
    <h1 style='text-align: center; color: #FF4B4B;'>🎬 IMDB 2024 Movie Insights Dashboard</h1>
    <hr style='border: 1px solid #f63366;'>
""", unsafe_allow_html=True)

# Vote & Duration Parsers
def parse_duration(duration):
    if pd.isna(duration): return 0
    hours, minutes = 0, 0
    if 'h' in duration:
        parts = duration.split('h')
        hours = int(parts[0].strip())
        if 'm' in parts[1]:
            minutes = int(parts[1].replace('m', '').strip())
    elif 'm' in duration:
        minutes = int(duration.replace('m', '').strip())
    return hours * 60 + minutes

def parse_votes(vote_str):
    try:
        vote_str = vote_str.replace('(', '').replace(')', '').strip().upper()
        if 'K' in vote_str:
            return int(float(vote_str.replace('K', '')) * 1000)
        elif 'M' in vote_str:
            return int(float(vote_str.replace('M', '')) * 1_000_000)
        return int(vote_str)
    except:
        return 0

# Load Data from CSV Files
@st.cache_data
def load_data():
    genre_files = {
        "Adventure": r"C:\Users\HP\Downloads\adventure_2024_raw.csv",
        "Animation": r"C:\Users\HP\Downloads\animation_2024_raw.csv",
        "Family": r"C:\Users\HP\Downloads\family_2024_raw.csv",
        "Fantasy": r"C:\Users\HP\Downloads\fantasy_2024_raw.csv",
        "Horror": r"C:\Users\HP\Downloads\horror_2024_raw.csv",
        "All Genres": r"C:\Users\HP\Downloads\all_genres_2024_raw.csv"
    }

    dfs = []
    for genre, file in genre_files.items():
        if os.path.exists(file):
            df = pd.read_csv(file)
            if 'Genre' not in df.columns:
                df['Genre'] = genre
            dfs.append(df)
        else:
            st.error(f"File not found: {file}")  # Display error message if file doesn't exist

    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df['Votes'] = combined_df['Votes'].apply(parse_votes)
    combined_df['Duration (min)'] = combined_df['Duration'].apply(parse_duration)
    return combined_df

# Load dataset
df = load_data()

# Sidebar Filters
st.sidebar.header("📊 Filters")
selected_genres = st.sidebar.multiselect("🎭 Select Genre(s)", df['Genre'].dropna().unique())
min_rating = st.sidebar.slider("⭐ Minimum Rating", 0.0, 10.0, 0.0, 0.1)
min_votes = st.sidebar.slider("🗳️ Minimum Votes", 0, int(df['Votes'].max()), 0, 1000)
duration_option = st.sidebar.selectbox("⏱️ Duration (minutes)", ['All', '< 90 mins', '90–120 mins', '> 120 mins'])

# Applying Filters
filtered_df = df.copy()
if selected_genres:
    filtered_df = filtered_df[filtered_df['Genre'].isin(selected_genres)]
if min_rating:
    filtered_df = filtered_df[filtered_df['Rating'] >= min_rating]
if min_votes:
    filtered_df = filtered_df[filtered_df['Votes'] >= min_votes]
if duration_option == '< 90 mins':
    filtered_df = filtered_df[filtered_df['Duration (min)'] < 90]
elif duration_option == '90–120 mins':
    filtered_df = filtered_df[(filtered_df['Duration (min)'] >= 90) & (filtered_df['Duration (min)'] <= 120)]
elif duration_option == '> 120 mins':
    filtered_df = filtered_df[filtered_df['Duration (min)'] > 120]

# To Display Filtered Data
st.subheader("🎯 Filtered Movies")
st.dataframe(filtered_df[['Title', 'Genre', 'Rating', 'Votes', 'Duration']], use_container_width=True, height=350)

# 1. Top 10 Movies by Rating & Votes
st.subheader("🏅 Top 10 Movies by Rating & Votes")
top_movies = filtered_df.sort_values(by=['Rating', 'Votes'], ascending=False).head(10)
fig1 = px.bar(top_movies, x='Title', y='Rating', color='Votes', title="Top 10 Movies by Rating",
              labels={"Rating": "IMDb Ratings", "Votes": "Vote Count"},
              color_continuous_scale='reds')
st.plotly_chart(fig1, use_container_width=True)

# 2. Genre Distribution
st.subheader("📊 Genre Distribution")
genre_counts = filtered_df['Genre'].value_counts().reset_index()
genre_counts.columns = ['Genre', 'count']
fig2 = px.bar(genre_counts, x='Genre', y='count', title="Number of Movies by Genre",
              color='count', color_continuous_scale='blues')
st.plotly_chart(fig2, use_container_width=True)

# 3. Average Duration by Genre
st.subheader("⏱️ Average Duration by Genre (mins)")
avg_duration = filtered_df.groupby('Genre')['Duration (min)'].mean().sort_values()
fig3 = px.bar(avg_duration, x=avg_duration.index, y=avg_duration.values, title="Average Duration by Genre",
              labels={"x": "Genre", "y": "Average Duration (mins)"}, color=avg_duration.values, color_continuous_scale='Viridis')
st.plotly_chart(fig3, use_container_width=True)

# 4. Average Voting by Genre
st.subheader("🗳️ Average Votes by Genre")
avg_votes = filtered_df.groupby('Genre')['Votes'].mean().sort_values()
fig4 = px.bar(avg_votes, x=avg_votes.index, y=avg_votes.values, title="Average Votes by Genre",
              labels={"x": "Genre", "y": "Average Votes"}, color=avg_votes.values, color_continuous_scale='YlOrRd')
st.plotly_chart(fig4, use_container_width=True)

# 5. Rating Distribution
st.subheader("⭐ Rating Distribution")
fig5 = px.histogram(filtered_df, x='Rating', nbins=10, title="Rating Distribution",
                    labels={"Rating": "IMDb Ratings"}, color_discrete_sequence=["green"])
st.plotly_chart(fig5, use_container_width=True)

# 6. Top-Rated Movies by Genre
if not filtered_df.empty:
    st.subheader("🏆 Top-Rated Movies by Genre")
    top_by_genre = filtered_df.loc[filtered_df.groupby('Genre')['Rating'].idxmax()]
    st.dataframe(top_by_genre[['Genre', 'Title', 'Rating']], use_container_width=True)
else:
    st.warning("⚠️ No data to display top-rated movies.")

# 7. Most Popular Genres by Votes (Pie Chart)
if not filtered_df.empty:
    st.subheader("🥧 Most Popular Genres by Votes")
    total_votes = filtered_df.groupby('Genre')['Votes'].sum().reset_index()
    fig7 = px.pie(total_votes, names='Genre', values='Votes', title="Total Votes per Genre",
                  color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig7, use_container_width=True)

# Footer
st.markdown("""
---
<div style='text-align: center;'>
    <em>📌 Made using Streamlit | IMDb 2024 Data</em>
</div>
""", unsafe_allow_html=True)