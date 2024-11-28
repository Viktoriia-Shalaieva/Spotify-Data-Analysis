import streamlit as st
import pandas as pd
from modules.nav import navbar
import yaml
import os
import plotly.express as px
import re
import requests
from bs4 import BeautifulSoup

st.set_page_config(
    page_title="Spotify Data Analysis",
    page_icon="🎵")

st.sidebar.image("images/music.png", width=150)

navbar()
st.sidebar.divider()
st.sidebar.markdown("# **Artists Analysis** 👩‍🎤 ")

st.title("Artists Analysis 👩‍🎤 ")
st.divider()


with open('config/path_config.yaml', 'r') as config_file:
    path_config = yaml.safe_load(config_file)

data_dir = path_config['data_dir'][0]
raw_dir = path_config['raw_dir'][0]
file_paths = {file_name: os.path.join(data_dir, file_name) for file_name in path_config['files_names']}

artists_genres_full_unknown_path = str(file_paths['artists_genres_full_unknown.csv'])

artists_genres_full_unknown = pd.read_csv(artists_genres_full_unknown_path, sep='~')

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

fig_followers_distribution = px.histogram(
    artists_genres_full_unknown,
    x='artist_followers',
    title='Distribution of Artist Followers',
    labels={'artist_followers': 'Followers'},
    nbins=10,
    log_y=True,
)

st.plotly_chart(fig_followers_distribution)

fig = px.box(
    artists_genres_full_unknown,
    y='artist_followers',
    title='Box Plot of Artist Followers',
    labels={'artist_followers': 'Followers'},
)

st.plotly_chart(fig)

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


url = 'https://www.chosic.com/list-of-music-genres/'


headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    )
}

response = requests.get(url, headers=headers)
print(response)

soup = BeautifulSoup(response.text, 'html.parser')


def get_parent_genres(soup_response):
    genres_parent = {}
    d = 1
    for i in soup_response.select(".genre-term-basic"):
        genres_parent[i.text] = d
        d += 1
    return genres_parent


def get_all_subgenres(soup_response, parent_genres_number):
    genre_subgenres = {}

    for main_genre, data_parent_value in parent_genres_number.items():
        subgenre_list = soup_response.find('ul', {'data-parent': str(data_parent_value)})

        subgenres = []
        if subgenre_list:
            # Iterate through all <a> tags with the href attribute in subgenre_list
            for subgenre in subgenre_list.select('.capital-letter.genre-term'):
            # for subgenre in subgenre_list.find_all('a', href=True):
                # Extract the text from the element and remove any extra spaces
                subgenre_name = subgenre.text.strip()
                subgenres.append(subgenre_name)

        genre_subgenres[main_genre] = subgenres

    return genre_subgenres


parent_genres = get_parent_genres(soup)
all_genres_with_subgenres = get_all_subgenres(soup, parent_genres)
print(all_genres_with_subgenres)


# Update classification logic based on the provided detailed genre structure
def classify_genres_detailed_structure(genre):
    genre = genre.lower().strip()
    for parent_genre, subgenres in all_genres_with_subgenres.items():
        if any(subgenre.lower() in genre.lower() for subgenre in subgenres):
            return parent_genre
    return 'Other'


expanded_artists_genres['parent_genre'] = (expanded_artists_genres['artist_genres']
                                           .apply(classify_genres_detailed_structure))

# Group by main genres and count occurrences
main_genre_counts = expanded_artists_genres['parent_genre'].value_counts(sort=False).reset_index()
main_genre_counts.columns = ['parent_genre', 'artist_count']

st.dataframe(expanded_artists_genres)
st.dataframe(main_genre_counts)

# main_genre_counts['theta'] = main_genre_counts['main_genre']

# Create the line polar chart
fig_polar = px.line_polar(
    main_genre_counts,
    r='artist_count',      # Radius is the count of artists
    theta='parent_genre',         # Theta is the main genre
    title="Genres Distribution",  # Chart title
    line_close=True,       # Close the line to form a complete loop
    # template="plotly_dark"
)

# Customize layout
fig_polar.update_layout(
    polar=dict(
        radialaxis=dict(title="Artist Count", showticklabels=True)
    )
)

# Display the polar chart
st.plotly_chart(fig_polar)


