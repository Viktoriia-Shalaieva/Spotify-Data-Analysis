import streamlit as st
import pandas as pd
from modules import components
import yaml
import os
import plotly.express as px
import re
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go


components.set_page_layout()
st.sidebar.markdown("# **Artists Analysis** 👩‍🎤 ")

components.set_page_header("Artists Analysis", " 👩‍🎤")


with open('config/path_config.yaml', 'r') as config_file:
    path_config = yaml.safe_load(config_file)

data_dir = path_config['data_dir'][0]
raw_dir = path_config['raw_dir'][0]
file_paths = {file_name: os.path.join(data_dir, file_name) for file_name in path_config['files_names']}

artists_genres_full_unknown_path = str(file_paths['artists_genres_full_unknown.csv'])
artists_genres_full_unknown = pd.read_csv(artists_genres_full_unknown_path, sep='~')

playlists_path = str(file_paths['playlists.csv'])
playlists_table = pd.read_csv(playlists_path, sep="~")

with open('./data/genres/genres.yaml', 'r', encoding='utf-8') as file:
    all_genres_with_subgenres = yaml.safe_load(file)

st.dataframe(artists_genres_full_unknown)


fig_popularity_distribution = px.histogram(
    artists_genres_full_unknown,
    x='artist_popularity',
    title='Distribution of Artist Popularity',
    labels={'artist_popularity': 'Popularity'},
    nbins=10,
)


st.plotly_chart(fig_popularity_distribution)

top_10_artists_popularity = (
    artists_genres_full_unknown.nlargest(n=10, columns='artist_popularity')
    .sort_values(by='artist_popularity', ascending=True)
)
min_x = top_10_artists_popularity['artist_popularity'].min() - 3
max_x = top_10_artists_popularity['artist_popularity'].max() + 1

fig_top_10_popularity = px.bar(
    top_10_artists_popularity,
    x='artist_popularity',
    y='artist_name',
    orientation='h',
    title='Top 10 Most Popular Artists',
    labels={'artist_popularity': 'Popularity', 'artist_name': 'Artist'},
    text='artist_popularity',
    range_x=[min_x, max_x],
)
fig_top_10_popularity.update_traces(textposition='outside')
st.plotly_chart(fig_top_10_popularity)

top_10_artists_followers = (
    artists_genres_full_unknown.nlargest(n=10, columns='artist_followers')
    .sort_values(by='artist_followers', ascending=True)
)
# min_x = top_10_artists_followers['artist_followers'].min()
# max_x = top_10_artists_followers['artist_followers'].max()

fig_top_10_followers = px.bar(
    top_10_artists_followers,
    x='artist_followers',
    y='artist_name',
    orientation='h',
    title='Top 10 Artists by Followers',
    labels={'artist_followers': 'Followers', 'artist_name': 'Artist'},
    # text='artist_followers',
    # range_x=[min_x, max_x],
)
# fig_top_10_followers.update_traces(textposition='outside')
st.plotly_chart(fig_top_10_followers)

artists_genres_full_unknown['followers_bin'] = pd.cut(
    artists_genres_full_unknown['artist_followers'],
    bins=[0, 1e6, 5e6, 10e6, 50e6, 100e6, 150e6],
    labels=['<1M', '1-5M', '5-10M', '10-50M', '50-100M', '>100M'],
    ordered=True
)

bin_counts = artists_genres_full_unknown['followers_bin'].value_counts(sort=False)
st.dataframe(bin_counts)
st.dataframe(artists_genres_full_unknown)
fig = px.bar(
    bin_counts,
    x=bin_counts.index,
    y=bin_counts.values,
    title='Artists by Follower Groups',
    labels={'x': 'Follower Group', 'y': 'Number of Artists'},
)

fig.update_layout(
    xaxis_title='Follower Group',
    yaxis_title='Number of Artists',
)

st.plotly_chart(fig)

# artists_genres_full_unknown['artist_genres'] = artists_genres_full_unknown['artist_genres'] \
#     .str.lower() \
#     .str.strip()
#
# st.dataframe(artists_genres_full_unknown)

artists_genres_full_unknown['artist_genres'] = artists_genres_full_unknown['artist_genres'].str.split(', ')
st.dataframe(artists_genres_full_unknown)

st.write('-expanded__artists---------')
expanded_artists_genres = artists_genres_full_unknown.explode('artist_genres')

# r"[\"\'\[\]]": Regular expression to match the characters.
# regex=True : Indicates using a regular expression for matching.
expanded_artists_genres['artist_genres'] = (expanded_artists_genres['artist_genres']
                                            .str.replace(r"[\"\'\[\]]", '', regex=True))


expanded_artists_genres['artist_genres'] = expanded_artists_genres['artist_genres'].str.lower()
st.dataframe(expanded_artists_genres)


# Update classification logic based on the provided detailed genre structure
def classify_genres_detailed_structure(genre):
    # genre = genre.lower().strip()
    for parent_genre, subgenres in all_genres_with_subgenres.items():
        if genre in subgenres:
            return parent_genre
    return 'Other'


expanded_artists_genres['artist_genres'] = (expanded_artists_genres['artist_genres']
                                            .str.replace(r'&\s*country', 'country', regex=True))

genre_counts = expanded_artists_genres['artist_genres'].value_counts(sort=False).reset_index()
st.dataframe(genre_counts)
expanded_artists_genres['parent_genre'] = (expanded_artists_genres['artist_genres']
                                           .apply(classify_genres_detailed_structure))

# Group by main genres and count occurrences
main_genre_counts = expanded_artists_genres['parent_genre'].value_counts(sort=False).reset_index()
main_genre_counts.columns = ['parent_genre', 'artist_count']

st.dataframe(expanded_artists_genres)
st.dataframe(main_genre_counts)

st.subheader('Genres Distribution')
fig_polar = px.line_polar(
    main_genre_counts,
    r='artist_count',
    theta='parent_genre',
    line_close=True,
    # template="plotly_dark",
    # hover_data={'artist_count': True, 'parent_genre': True},
    # text='artist_count',
)
fig_polar.update_traces(
    mode='lines+markers',
    fill='toself',
    marker=dict(size=8)
)

fig_polar.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, title="Artist Count", showticklabels=True)
    )
)

st.plotly_chart(fig_polar)

expanded_artists_genres = expanded_artists_genres.merge(
    playlists_table[['artist_id', 'country']],
    on='artist_id',
    how='left'
)

st.subheader('Genre Frequency Across Countries')
# Group data by country and parent_genre
genre_country_counts = expanded_artists_genres.groupby(['country', 'parent_genre']).size().reset_index(name='count')
st.dataframe(genre_country_counts)

# select_all = st.checkbox("Select All Countries", value=True)
# all_countries = genre_country_counts['country'].unique()
#
# selected_countries = st.multiselect(
#     "Select Countries",
#     options=all_countries,
#     default=all_countries if select_all else []
# )
#
# select_all = st.checkbox("Select All", value=True)

with st.popover("Select countries for analysis", icon="🌍"):
    select_all = st.checkbox("Select All Countries", value=True,
                             help="Check to select all countries. Uncheck to choose specific ones.")

    if select_all:
        selected_countries = genre_country_counts['country'].unique()
    else:
        selected_countries = st.multiselect(
            "Select Specific Countries",
            options=genre_country_counts['country'].unique(),
            default=[]
        )

# select_all_genres = st.checkbox("Select All Genres", value=True)
# all_genres = genre_country_counts['parent_genre'].unique()
#
# selected_genres = st.multiselect(
#     "Select Genres",
#     options=all_genres,
#     default=all_genres if select_all_genres else []
# )

with st.popover("Select genres for analysis", icon="🎵"):
    select_all = st.checkbox("Select All Genres", value=True,
                             help="Check to select all genres. Uncheck to choose specific ones.")

    if select_all:
        selected_genres = genre_country_counts['parent_genre'].unique()
    else:
        selected_genres = st.multiselect(
            "Select Specific Countries",
            options=genre_country_counts['parent_genre'].unique(),
            default=[]
        )

filtered_genre_country_counts = genre_country_counts[
    (genre_country_counts['country'].isin(selected_countries)) &
    (genre_country_counts['parent_genre'].isin(selected_genres))
]

fig_heatmap = px.density_heatmap(
    filtered_genre_country_counts,
    x='parent_genre',
    y='country',
    z='count',
    labels={'parent_genre': 'Genre', 'country': 'Country', 'count': 'Frequency'},
)

fig_heatmap.update_layout(
    xaxis=dict(tickangle=45),
    height=600,
    coloraxis_colorbar=dict(title="Frequency"),
)

st.plotly_chart(fig_heatmap)
