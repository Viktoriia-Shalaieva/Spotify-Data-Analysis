import streamlit as st


def set_page_layout(page_title="Spotify Data Analysis", page_icon="🎵"):
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.sidebar.image("images/music.png", width=150)
    navbar()
    st.sidebar.divider()


def set_page_header(header_title: str, header_icon: str = "🏠"):
    st.title(f"{header_title} {header_icon}")
    st.divider()


def navbar():
    with st.sidebar:
        st.page_link('streamlit_app.py', label='Home', icon='🏠')
        st.page_link('pages/data_preview.py', label='Data Preview', icon='🧮')
        st.page_link('pages/playlists_analysis.py', label='Playlists Analysis', icon='📋️')
        st.page_link('pages/tracks_analysis.py', label='Tracks Analysis', icon='🎵')
        st.page_link('pages/artists_analysis.py', label='Artists Analysis', icon='👩‍🎤')
        st.page_link('pages/albums_analysis.py', label='Albums Analysis', icon='📀')
