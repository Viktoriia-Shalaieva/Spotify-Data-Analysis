import streamlit as st
from modules.nav import navbar


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
