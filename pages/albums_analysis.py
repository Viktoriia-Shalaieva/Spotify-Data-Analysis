import streamlit as st

from streamlit_utils import data_processing, layouts, plots


layouts.set_page_layout()
st.sidebar.markdown("# **Albums Analysis** 📀️ ")

layouts.set_page_header("Albums Analysis", "📀️")

data = data_processing.load_and_process_data("config/path_config.yaml")

playlists_table = data["playlists"]
artists_table = data["artists"]
tracks_table = data["tracks"]
albums_table = data["albums"]

data_albums = data_processing.process_albums_data(albums_table, playlists_table, artists_table)
top_10_albums_by_popularity = data_albums["top_10_albums_by_popularity"]
top_10_albums_artists_sorted = data_albums["top_10_albums_artists_sorted"]
monthly_releases = data_albums["monthly_releases"]
yearly_releases = data_albums["yearly_releases"]
albums_table_with_year_release = data_albums["albums_table"]

help_popularity = "The value of popularity will be between 0 and 100, with 100 being the most popular"

st.subheader("Distribution of Album Popularity", help=help_popularity)
plots.create_histogram(
            data=albums_table,
            x="Album Popularity",
        )

min_x = top_10_albums_by_popularity["Album Popularity"].min() - 3
max_x = top_10_albums_by_popularity["Album Popularity"].max()

st.subheader("Top 10 Most Popular Albums", help=help_popularity)
plots.create_bar_plot(
    data=top_10_albums_artists_sorted,
    x="Album Popularity",
    y="Album Name",
    orientation="h",
    text="Album Popularity",
    range_x=[min_x, max_x],
    hover_data={"Artist Name": True},
)

st.subheader("Seasonality of Album Releases")
plots.create_bar_plot(
    data=monthly_releases,
    x="Month Name",
    y="Release Count",
    text="Release Count",
    showticklabels=True,
)

st.subheader("Album Releases Timeline")

plots.create_line_chart(
    data=yearly_releases,
    x="Release Year",
    y="Release Count",
    text="Release Count",
    yaxis_title="Number of Releases (log scale)",
    log_y=True,
)

st.subheader("Distribution of Album Types")
plots.create_pie_chart(
    data=albums_table_with_year_release,
    names="Album Type",
)
