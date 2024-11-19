import streamlit as st
from modules.nav import navbar

st.set_page_config(
    page_title="Spotify Data Analysis",
    page_icon="🎵")

st.sidebar.image("images/music.png", width=150)

navbar()
st.sidebar.divider()
st.sidebar.markdown("# **Artists Analysis** 👩‍🎤 ")

st.title("Artists Analysis 👩‍🎤 ")
st.divider()
