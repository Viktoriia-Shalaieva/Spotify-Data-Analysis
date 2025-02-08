import streamlit as st


def set_page_layout(page_title="Spotify Data Analysis", page_icon="🎵"):
    """
    Configure the Streamlit app layout, including the page title, icon, and sidebar setup.
    It also adds a custom image and navigation bar to the sidebar.
    """
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
    """Set up the page header for the Streamlit application."""
    st.title(f"{header_title} {header_icon}")
    st.divider()


def navbar():
    """
    Set up the navigation bar in the Streamlit sidebar.

    This function creates links to various pages of the Streamlit application,
    displayed in the sidebar with labels and icons for easy navigation.
    """
    with st.sidebar:
        st.page_link("streamlit_app.py", label="Home", icon="🏠")
        st.page_link("pages/data_preview.py", label="Data Preview", icon="🧮")
        st.page_link("pages/playlists_analysis.py", label="Playlists Analysis", icon="📋️")
        st.page_link("pages/tracks_analysis.py", label="Tracks Analysis", icon="🎵")
        st.page_link("pages/artists_analysis.py", label="Artists Analysis", icon="👩‍🎤")
        st.page_link("pages/albums_analysis.py", label="Albums Analysis", icon="📀")
