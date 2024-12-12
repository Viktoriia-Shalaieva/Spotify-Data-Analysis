import streamlit as st
import pandas as pd
from modules import components
import yaml
import os
import plotly.express as px


components.set_page_layout()
st.sidebar.markdown("# **Albums Analysis** 📀️ ")

components.set_page_header("Albums Analysis", "📀️")

with open('config/path_config.yaml', 'r') as config_file:
    path_config = yaml.safe_load(config_file)

data_dir = path_config['data_dir'][0]
raw_dir = path_config['raw_dir'][0]
file_paths = {file_name: os.path.join(data_dir, file_name) for file_name in path_config['files_names']}

albums_path = str(file_paths['albums.csv'])
albums = pd.read_csv(albums_path, sep='~')

playlists_path = str(file_paths['playlists.csv'])
playlists_table = pd.read_csv(playlists_path, sep="~")

fig_histogram = px.histogram(
    albums,
    x='album_popularity',
    title='Distribution of Album Popularity',
    labels={'album_popularity': 'Album Popularity'},
    nbins=20,
)
fig_histogram.update_layout(
    yaxis_title='Count',
)
st.plotly_chart(fig_histogram)

top_10_albums_popularity = (
    albums.nlargest(n=10, columns='album_popularity')
    .sort_values(by='album_popularity', ascending=True)
)
min_x = top_10_albums_popularity['album_popularity'].min() - 3
max_x = top_10_albums_popularity['album_popularity'].max() + 1

fig_top_10_popularity = px.bar(
    top_10_albums_popularity,
    x='album_popularity',
    y='album_name',
    orientation='h',
    title='Top 10 Most Popular Albums',
    labels={'album_popularity': 'Popularity', 'album_name': 'Album'},
    text='album_popularity',
    range_x=[min_x, max_x],
)
fig_top_10_popularity.update_traces(textposition='outside')
st.plotly_chart(fig_top_10_popularity)

# The 'errors="coerce"' argument replaces invalid date entries with NaT (Not a Time),
# ensuring the column can be processed without raising errors for incorrect formats.
albums['album_release_date'] = pd.to_datetime(albums['album_release_date'], errors='coerce')

albums['release_month'] = albums['album_release_date'].dt.month

monthly_releases = albums['release_month'].value_counts().reset_index()
monthly_releases.columns = ['Month', 'Release Count']

month_names = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December'
}
monthly_releases['Month Name'] = monthly_releases['Month'].map(month_names)

monthly_releases = monthly_releases.sort_values(by='Month')


fig = px.bar(
    monthly_releases,
    x='Month Name',
    y='Release Count',
    title='Seasonality of Album Releases',
    labels={'Release Count': 'Number of Releases', 'Month Name': 'Month'},
    text='Release Count'
)
fig.update_traces(textposition='outside')

st.plotly_chart(fig)

albums['release_year'] = albums['album_release_date'].dt.year

yearly_releases = albums['release_year'].value_counts().sort_index().reset_index()
yearly_releases.columns = ['Year', 'Release Count']

fig_yearly = px.line(
    yearly_releases,
    x='Year',
    y='Release Count',
    title='Number of Album Releases by Year',
    labels={'Year': 'Release Year', 'Release Count': 'Number of Releases'},
    markers=True,  # Add markers to the line for better visualization
    text='Release Count',
    log_y=True,
)

fig_yearly.update_traces(textposition='top center')

st.plotly_chart(fig_yearly)

fig_pie_album_type = px.pie(
    albums,
    names='album_type',
    title='Distribution of Album Types',
)

fig_pie_album_type.update_traces(
    textinfo='percent+label',
)
fig_pie_album_type.update_layout(showlegend=False)

st.plotly_chart(fig_pie_album_type)

fig_box = px.box(
    albums,
    x='album_type',
    y='album_popularity',
    title='Distribution of Album Popularity by Album Type',
    labels={
        'album_type': 'Album Type',
        'album_popularity': 'Album Popularity'
    },
)
st.plotly_chart(fig_box)

fig_tracks_vs_popularity = px.scatter(
    albums,
    x='album_total_tracks',
    y='album_popularity',
    title='Impact of Track Count on Album Popularity',
    labels={
        'album_total_tracks': 'Total Tracks',
        'album_popularity': 'Album Popularity'
    },
)
