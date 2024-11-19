import streamlit as st
from modules.nav import navbar


def main():
    navbar()

    st.title(f'🛡️ Competition Checker')


if __name__ == '__main__':
    main()
#
# st.markdown("# Home 🏘️")
# st.sidebar.markdown("# Home 🏘️ 🏠")
#
# st.title("Welcome to the Spotify Data Analysis App 👋")
# st.divider()
# st.write("""
# This application provides interactive visualizations and analyses of Spotify data,
# including track popularity, audio features, artist genres, and more.
#
# **👈 Use the navigation menu** to explore different sections.
# """)
#
