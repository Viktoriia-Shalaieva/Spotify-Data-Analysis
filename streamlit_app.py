import streamlit as st

from streamlit_utils import layouts


layouts.set_page_layout()
st.sidebar.markdown("# Home 🏘️ ")

layouts.set_page_header("🎵 Welcome to the Spotify Data Analysis App", "👋")

st.write("""
This application is designed to explore and analyze Spotify's Top 50 playlists, including country-specific playlists 
and the global Top 50 playlist, using an interactive and visually appealing application that functions as a dashboard. 
Each playlist corresponds to a specific country or the global category, helping users understand how music trends differ 
by region or resonate globally. 


## 🤔 Purpose of the Project
The goal of this project is to uncover trends and insights in global music preferences.
 
Visualize global music preferences by analyzing Spotify's Top 50 playlists, combining data from country-specific 
playlists and the global playlist. This project aims to identify key trends in track, artist, and album popularity 
through interactive analysis of data retrieved from the Spotify API. The primary goal is to explore how music 
preferences vary across countries and within a global context, while providing a tool for comparing regional and 
global music trends.


## 👥 Who is this for?
- **Music Enthusiasts**: Discover popular tracks, artists, and albums from around the world.
- **Data Analysts**: Explore and interpret music data through advanced visualizations and statistical summaries.
- **Marketers and Producers**: Identify trends and patterns to support data-driven decisions in the music industry.

## 🌍 What You Can Do
- Compare the popularity of tracks, artists, and albums across various countries.
- Analyze music trends over time, such as release seasonality.
- Use dynamic filters and interactive visualizations to tailor the insights to your specific interests.

## 🔧 Features
- **Data Preview**: View and summarize the raw data powering these analyses.
- **Playlists Analysis**: Visualize playlist followers, track contributions, and geographical distributions.
- **Tracks Analysis**: Discover trends in track popularity, duration, and explicit content.
- **Artists Analysis**: Analyze artist popularity, follower distribution, and genre classifications.
- **Albums Analysis**: Explore album popularity, release patterns, and types.

## 🔍 How to Use
- **👈 Navigate**: Use the sidebar to explore various sections, including Data Preview, Playlists, Tracks, Artists, 
and Albums Analysis.
- **📈 Interact**: Hover over charts for additional details or filter data with dropdowns and checkboxes.
- **📚 Learn**: Gain insights from statistical summaries, visual patterns, and explanations provided within each 
analysis.

**Ready to dive into the world of music data? Use the navigation menu on the left to get started!**
""")
