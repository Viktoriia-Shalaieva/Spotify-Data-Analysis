import streamlit as st

from streamlit_utils import data_processing, layouts, plots


layouts.set_page_layout()
st.sidebar.markdown("# **Artists Analysis** 👩‍🎤 ")

layouts.set_page_header("Artists Analysis", " 👩‍🎤")

data = data_processing.load_and_process_data("config/path_config.yaml")

playlists_table = data["playlists"]
artists_table = data["artists"]

data_artists = data_processing.process_artists_data(artists_table)
top_10_artists_by_popularity = data_artists["top_10_artists_by_popularity"]
top_10_artists_by_followers = data_artists["top_10_artists_by_followers"]
bin_counts_followers = data_artists["bin_counts_followers"]

help_popularity = "The value of popularity will be between 0 and 100, with 100 being the most popular"

st.subheader("Distribution of Artist Popularity", help=help_popularity)
plots.create_histogram(
            data=artists_table,
            x="Artist Popularity",
        )

min_x = top_10_artists_by_popularity["Artist Popularity"].min() - 3
max_x = top_10_artists_by_popularity["Artist Popularity"].max()

st.subheader("Top 10 Most Popular Artists", help=help_popularity)
plots.create_bar_plot(
    data=top_10_artists_by_popularity,
    x="Artist Popularity",
    y="Artist Name",
    orientation="h",
    text="Artist Popularity",
    range_x=[min_x, max_x],
)

st.subheader("Top 10 Artists by Followers")
plots.create_bar_plot(
    data=top_10_artists_by_followers,
    x="Artist Total Followers",
    y="Artist Name",
    orientation="h",
    text="Artist Total Followers (formatted)",
)

st.subheader("Number of Artists by Follower Groups")
plots.create_bar_plot(
    data=bin_counts_followers,
    x=bin_counts_followers.index,
    y=bin_counts_followers.values,
    labels={"y": "Number of Artists"},
    showticklabels=True
)

expanded_artists_genres = data_processing.expand_and_classify_artists_genres(artists_table)
expanded_artists_genres_unknown = expanded_artists_genres[expanded_artists_genres["Parent Genre"] == "Other"]

# Group by main genres and count occurrences
main_genre_counts = expanded_artists_genres["Parent Genre"].value_counts(sort=False).reset_index()
main_genre_counts.columns = ["Parent Genre", "Number of Artists"]

st.subheader("Genres Distribution")
plots.create_polar_chart(
    data=main_genre_counts,
    r="Number of Artists",
    theta="Parent Genre",
)

expanded_artists_genres = expanded_artists_genres.merge(
    playlists_table[["Artist ID", "Country"]],
    on="Artist ID",
    how="left"
)

st.subheader("Genre Frequency Across Countries")

# Group data by country and parent_genre
genre_country_counts = expanded_artists_genres.groupby(["Country", "Parent Genre"]).size().reset_index(name="count")

with st.popover("Select countries for analysis", icon="🌍"):
    select_all = st.checkbox("Select All Countries", value=True,
                             help="Check to select all countries. Uncheck to choose specific ones.")

    if select_all:
        selected_countries = genre_country_counts["Country"].unique()
    else:
        selected_countries = st.multiselect(
            "Select Specific Countries",
            options=genre_country_counts["Country"].unique(),
            default=[]
        )

with st.popover("Select genres for analysis", icon="🎵"):
    select_all = st.checkbox("Select All Genres", value=True,
                             help="Check to select all genres. Uncheck to choose specific ones.")

    if select_all:
        selected_genres = genre_country_counts["Parent Genre"].unique()
    else:
        selected_genres = st.multiselect(
            "Select Specific Countries",
            options=genre_country_counts["Parent Genre"].unique(),
            default=[]
        )

filtered_genre_country_counts = genre_country_counts[
    (genre_country_counts["Country"].isin(selected_countries)) &
    (genre_country_counts["Parent Genre"].isin(selected_genres))
]

plots.create_heatmap(
    data=filtered_genre_country_counts,
    x="Parent Genre",
    y="Country",
    z="count",
    label_z="Genre Count"
)
