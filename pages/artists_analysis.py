import streamlit as st
import pandas as pd
from streamlit_utils import plots, layouts, data_processing
import yaml
import os


layouts.set_page_layout()
st.sidebar.markdown("# **Artists Analysis** 👩‍🎤 ")

layouts.set_page_header("Artists Analysis", " 👩‍🎤")


# with open('config/path_config.yaml', 'r') as config_file:
#     path_config = yaml.safe_load(config_file)

with open('./data/genres/genres.yaml', 'r', encoding='utf-8') as file:
    all_genres_with_subgenres = yaml.safe_load(file)

# data_dir = path_config['data_dir'][0]
# file_paths = {file_name: os.path.join(data_dir, file_name) for file_name in path_config['files_names']}
#
# artists_genres_full_unknown_path = str(file_paths['artists_genres_full_unknown.csv'])
# artists_genres_full_unknown = pd.read_csv(artists_genres_full_unknown_path, sep='~')
#
# playlists_path = str(file_paths['playlists.csv'])
# playlists_table = pd.read_csv(playlists_path, sep="~")

data = data_processing.load_and_process_data('config/path_config.yaml')

playlists_table = data["playlists"]
artists_table = data["artists"]

st.subheader('Distribution of Artist Popularity',)
plots.create_histogram(
            data=artists_table,
            x='Artist Popularity',
        )

top_10_artists_popularity = (
    artists_table.nlargest(n=10, columns='Artist Popularity')
    .sort_values(by='Artist Popularity', ascending=True)
)
min_x = top_10_artists_popularity['Artist Popularity'].min() - 3
max_x = top_10_artists_popularity['Artist Popularity'].max()

st.subheader('Top 10 Most Popular Artists')
plots.create_bar_plot(
    data=top_10_artists_popularity,
    x='Artist Popularity',
    y='Artist Name',
    orientation='h',
    text='Artist Popularity',
    range_x=[min_x, max_x],
)

top_10_artists_followers = (
    artists_table.nlargest(n=10, columns='Artist Total Followers')
    .sort_values(by='Artist Total Followers', ascending=True)
)

top_10_artists_followers['Artist Total Followers (formatted)'] = (
    plots.format_number_text(
        top_10_artists_followers['Artist Total Followers']
    )
)

st.subheader('Top 10 Artists by Followers')
plots.create_bar_plot(
    data=top_10_artists_followers,
    x='Artist Total Followers',
    y='Artist Name',
    orientation='h',
    text='Artist Total Followers (formatted)',
)

artists_table['Follower Group'] = pd.cut(
    artists_table['Artist Total Followers'],
    bins=[0, 1e6, 5e6, 10e6, 50e6, 100e6, 150e6],
    labels=['<1M', '1-5M', '5-10M', '10-50M', '50-100M', '>100M'],
    ordered=True
)

bin_counts = artists_table['Follower Group'].value_counts(sort=False)

st.subheader('Number of Artists by Follower Groups')
plots.create_bar_plot(
    data=bin_counts,
    x=bin_counts.index,
    y=bin_counts.values,
    labels={'y': 'Number of Artists'},
    showticklabels=True
)

artists_table['Artist Genres'] = artists_table['Artist Genres'].str.split(', ')

expanded_artists_genres = artists_table.explode('Artist Genres')

# r"[\"\'\[\]]": Regular expression to match the characters.
# regex=True : Indicates using a regular expression for matching.
expanded_artists_genres['Artist Genres'] = (expanded_artists_genres['Artist Genres']
                                            .str.replace(r"[\"\'\[\]]", '', regex=True))


expanded_artists_genres['Artist Genres'] = expanded_artists_genres['Artist Genres'].str.lower()


# Update classification logic based on the provided detailed genre structure
def classify_genres_detailed_structure(genre):
    for parent_genre, subgenres in all_genres_with_subgenres.items():
        if genre in subgenres:
            return parent_genre
    return 'Other'


expanded_artists_genres['Artist Genres'] = (expanded_artists_genres['Artist Genres']
                                            .str.replace(r'&\s*country', 'country', regex=True))

genre_counts = expanded_artists_genres['Artist Genres'].value_counts(sort=False).reset_index()

expanded_artists_genres['Parent Genre'] = (expanded_artists_genres['Artist Genres']
                                           .apply(classify_genres_detailed_structure))

# Group by main genres and count occurrences
main_genre_counts = expanded_artists_genres['Parent Genre'].value_counts(sort=False).reset_index()
main_genre_counts.columns = ['Parent Genre', 'Number of Artists']

st.subheader('Genres Distribution')
plots.create_polar_chart(
    data=main_genre_counts,
    r='Number of Artists',
    theta='Parent Genre',
)

expanded_artists_genres = expanded_artists_genres.merge(
    playlists_table[['Artist ID', 'Country']],
    on='Artist ID',
    how='left'
)

st.subheader('Genre Frequency Across Countries')
# Group data by country and parent_genre
genre_country_counts = expanded_artists_genres.groupby(['Country', 'Parent Genre']).size().reset_index(name='count')

with st.popover("Select countries for analysis", icon="🌍"):
    select_all = st.checkbox("Select All Countries", value=True,
                             help="Check to select all countries. Uncheck to choose specific ones.")

    if select_all:
        selected_countries = genre_country_counts['Country'].unique()
    else:
        selected_countries = st.multiselect(
            "Select Specific Countries",
            options=genre_country_counts['Country'].unique(),
            default=[]
        )

with st.popover("Select genres for analysis", icon="🎵"):
    select_all = st.checkbox("Select All Genres", value=True,
                             help="Check to select all genres. Uncheck to choose specific ones.")

    if select_all:
        selected_genres = genre_country_counts['Parent Genre'].unique()
    else:
        selected_genres = st.multiselect(
            "Select Specific Countries",
            options=genre_country_counts['Parent Genre'].unique(),
            default=[]
        )

filtered_genre_country_counts = genre_country_counts[
    (genre_country_counts['Country'].isin(selected_countries)) &
    (genre_country_counts['Parent Genre'].isin(selected_genres))
]

plots.create_heatmap(
    data=filtered_genre_country_counts,
    x='Parent Genre',
    y='Country',
    z='count',
    label_z='Genre Count'
)
