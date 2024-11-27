import streamlit as st
import pandas as pd
from modules.nav import navbar
import yaml
import os
import plotly.express as px


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
