import streamlit as st
from modules import components
import plotly.express as px


components.set_page_layout()
st.sidebar.markdown("# Home 🏘️ ")

components.set_page_header("Welcome to the Spotify Data Analysis App", "👋")

st.write("""
This application provides interactive visualizations and analyses of Spotify data,
including track popularity, audio features, artist genres, and more.

**👈 Use the navigation menu** to explore different sections.
""")
fig = px.colors.sequential.swatches_continuous()
st.plotly_chart(fig)

# import pandas as pd
# import yaml
# import os
# import plotly.express as px
#

# st.set_page_config(
#     page_title="Spotify Data Analysis",
#     page_icon="🎵")

# st.set_page_config(page_title="Spotify Data Explorer")

# home = st.Page("pages/1_🏘️_home.py", title="Home")
# data_preview = st.Page("pages/data_preview.py", title="Data Preview")
# playlists_analysis = st.Page("pages/playlists_analysis.py", title="Playlists Analysis")
# tracks_analysis = st.Page("pages/tracks_analysis.py", title="Tracks Analysis")
# artists_analysis = st.Page("pages/artists_analysis.py", title="Artists Analysis")
# albums_analysis = st.Page("pages/albums_analysis.py", title="Albums Analysis")
# recommendations = st.Page("pages/recommendations.py", title="Recommendations")
#
# pg = st.navigation([home, data_preview, playlists_analysis, tracks_analysis, artists_analysis, albums_analysis,
#                     recommendations])
# st.set_page_config(page_title="Spotify Data Analysis")
# pg.run()


# st.title("Welcome to the Spotify Data Analysis App")
# st.write("Select a section from the navigation panel to continue.")
#

