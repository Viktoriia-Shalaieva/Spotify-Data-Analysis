import streamlit as st


def navbar():
    with st.sidebar:
        st.page_link('streamlit_app.py', label='Home', icon='🏠')
        st.page_link('pages/data_preview.py', label='Data Preview', icon='🧮')
        st.page_link('pages/playlists_analysis.py', label='Playlists Analysis', icon='📋️')
        st.page_link('pages/tracks_analysis.py', label='Tracks Analysis', icon='🎵')
        st.page_link('pages/artists_analysis.py', label='Artists Analysis', icon='👩‍🎤')
        st.page_link('pages/albums_analysis.py', label='Albums Analysis', icon='📀')

