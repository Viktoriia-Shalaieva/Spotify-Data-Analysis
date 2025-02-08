import streamlit as st

from streamlit_utils import data_processing, layouts, plots


layouts.set_page_layout()
st.sidebar.markdown("**Tracks Analysis** 🎵")

layouts.set_page_header("Tracks Analysis", "🎵")

data = data_processing.load_and_process_data("config/path_config.yaml")

playlists_table = data["playlists"]
artists_table = data["artists"]
tracks_table = data["tracks"]

data_tracks = data_processing.process_tracks_data(playlists_table, tracks_table, artists_table)
top_10_tracks_by_popularity = data_tracks["top_10_tracks"]
tracks_artists_grouped = data_tracks["grouped_tracks"]

help_popularity = "The value of popularity will be between 0 and 100, with 100 being the most popular"

st.subheader("Distribution of Track Popularity", help=help_popularity)
plots.create_histogram(
    data=tracks_table,
    x="Track Popularity",
)

min_x = top_10_tracks_by_popularity["Track Popularity"].min() - 3
max_x = top_10_tracks_by_popularity["Track Popularity"].max()

st.subheader("Top 10 Most Popular Tracks", help=help_popularity)
plots.create_bar_plot(
    data=top_10_tracks_by_popularity,
    x="Track Popularity",
    y="Track Name",
    orientation="h",
    text="Track Popularity",
    range_x=[min_x, max_x],
    hover_data={"Artist Name": True},
)

st.subheader("Analysis of Track Popularity for Explicit and Non-Explicit Tracks", help=help_popularity)


tab1_boxplot, tab2_histogram = st.tabs(["Box Plot", "Histogram"])

with tab1_boxplot:
    plots.create_boxplot(
        data=tracks_artists_grouped,
        x="Explicit Status",
        y="Track Popularity",
        color_discrete_map={
            "Explicit": "red",
            "Non-Explicit": "green"
        },
    )

with tab2_histogram:
    plots.create_histogram(
        data=tracks_artists_grouped,
        x="Track Popularity",
        color="Explicit Status",
        color_discrete_map={
            "Explicit": "red",
            "Non-Explicit": "green"
        },
    )

help_trendline = ("""Trendlines show the overall relationship between track duration and popularity 
                  for Explicit and Non-Explicit tracks.""")

st.subheader("Relationship Between Track Duration and Popularity with Trendlines", help=help_trendline)
plots.create_scatter_plot(
    data=tracks_artists_grouped,
    x="Track Duration (minutes)",
    y="Track Popularity",
    color="Explicit Status",
    hover_data=["Track Name"],
    symbol="Explicit Status",
    color_map={
                "Explicit": "red",
                "Non-Explicit": "green"
            },
)

show_explanation = st.checkbox("Show more details", value=False)

if show_explanation:
    st.info("""
        **Trendlines**:
        - These lines show the overall trend for each category using the LOWESS (Locally Weighted Scatterplot 
        Smoothing) method.
        - They help identify patterns in the data without assuming a strict linear relationship.
        - For example, a rising trendline indicates that longer tracks in that category tend to be more popular.
    """)
