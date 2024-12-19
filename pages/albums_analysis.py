import streamlit as st
import pandas as pd
from modules import components
import yaml
import os
import plotly.express as px
from modules import plots
import numpy as np
import plotly.graph_objects as go


components.set_page_layout()
st.sidebar.markdown("# **Albums Analysis** 📀️ ")

components.set_page_header("Albums Analysis", "📀️")

with open('config/path_config.yaml', 'r') as config_file:
    path_config = yaml.safe_load(config_file)

data_dir = path_config['data_dir'][0]
raw_dir = path_config['raw_dir'][0]
file_paths = {file_name: os.path.join(data_dir, file_name) for file_name in path_config['files_names']}

albums_path = str(file_paths['albums.csv'])
albums_table = pd.read_csv(albums_path, sep='~')

playlists_path = str(file_paths['playlists.csv'])
playlists_table = pd.read_csv(playlists_path, sep="~")

artists_genres_full_unknown_path = str(file_paths['artists_genres_full_unknown.csv'])
artists_genres_full_unknown = pd.read_csv(artists_genres_full_unknown_path, sep='~')

albums_table = albums_table.rename(columns={
    'album_id': 'Album ID',
    'album_name': 'Album Name',
    'album_type': 'Album Type',
    'album_release_date': 'Release Date',
    'album_total_tracks': 'Total Tracks',
    'album_label': 'Label',
    'album_popularity': 'Album Popularity'
})

playlists_table = playlists_table.rename(columns={
    'playlist_id': 'Playlist ID',
    'playlist_name': 'Playlist Name',
    'country': 'Country',
    'playlist_followers_total': 'Playlist Total Followers',
    'track_id': 'Track ID',
    'album_id': 'Album ID',
    'artist_id': 'Artist ID'
})

artists_table = artists_genres_full_unknown.rename(columns={
    'artist_id': 'Artist ID',
    'artist_name': 'Artist Name',
    'artist_followers': 'Artist Total Followers',
    'artist_genres': 'Artist Genres',
    'artist_popularity': 'Artist Popularity'
})

# fig_histogram = px.histogram(
#     albums_table,
#     x='Album Popularity',
#     title='Distribution of Album Popularity',
#     # labels={'album_popularity': 'Album Popularity'},
#     nbins=20,
# )
# fig_histogram.update_layout(
#     yaxis_title='Count',
# )
# st.plotly_chart(fig_histogram)

st.subheader('Distribution of Album Popularity',)
plots.create_histogram(
            data=albums_table,
            x='Album Popularity',
        )

top_10_albums_popularity = (
    albums_table.nlargest(n=10, columns='Album Popularity')
    )
min_x = top_10_albums_popularity['Album Popularity'].min() - 3
max_x = top_10_albums_popularity['Album Popularity'].max()

# fig_top_10_popularity = px.bar(
#     top_10_albums_popularity,
#     x='Album Popularity',
#     y='Album Name',
#     orientation='h',
#     title='Top 10 Most Popular Albums',
#     # labels={'album_popularity': 'Popularity', 'album_name': 'Album'},
#     text='Album Popularity',
#     range_x=[min_x, max_x],
# )
# fig_top_10_popularity.update_traces(textposition='outside')
# st.plotly_chart(fig_top_10_popularity)

merged_playlists_albums = pd.merge(
    top_10_albums_popularity,
    playlists_table[['Album ID', 'Artist ID']],
    on='Album ID',
    how='left'
)
merged_playlists_albums.loc[:, 'Artist ID'] = merged_playlists_albums['Artist ID'].str.split(', ')
expanded_albums_artists = merged_playlists_albums.explode('Artist ID')
albums_artists_name = expanded_albums_artists.merge(
    artists_table[['Artist ID', 'Artist Name']],
    on='Artist ID',
    how='left'
)
# st.dataframe(merged_playlists_albums)

top_10_albums_artists_grouped = albums_artists_name.groupby('Album ID').agg({
    'Album Name': 'first',   # Keep the first occurrence of the track name
    'Artist Name': lambda x: ', '.join(x.dropna().unique()),  # Concatenate unique artist names, separated by commas
    'Album Popularity': 'first',
}).reset_index()

top_10_albums_artists_sorted = top_10_albums_artists_grouped.sort_values(by='Album Popularity', ascending=True)

st.subheader('Top 10 Most Popular Albums')
plots.create_bar_plot(
    data=top_10_albums_artists_sorted,
    x='Album Popularity',
    y='Album Name',
    orientation='h',
    text='Album Popularity',
    range_x=[min_x, max_x],
    hover_data={'Artist Name': True},
)

# The 'errors="coerce"' argument replaces invalid date entries with NaT (Not a Time),
# ensuring the column can be processed without raising errors for incorrect formats.
albums_table['Release Date'] = pd.to_datetime(albums_table['Release Date'], errors='coerce')

albums_table['release_month'] = albums_table['Release Date'].dt.month

monthly_releases = albums_table['release_month'].value_counts().reset_index()
monthly_releases.columns = ['Month', 'Release Count']

month_names = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December'
}
monthly_releases['Month Name'] = monthly_releases['Month'].map(month_names)

monthly_releases = monthly_releases.sort_values(by='Month')


# fig = px.bar(
#     monthly_releases,
#     x='Month Name',
#     y='Release Count',
#     title='Seasonality of Album Releases',
#     labels={'Release Count': 'Number of Releases', 'Month Name': 'Month'},
#     text='Release Count'
# )
# fig.update_traces(textposition='outside')
#
# st.plotly_chart(fig)

st.subheader('Seasonality of Album Releases')
plots.create_bar_plot(
    data=monthly_releases,
    x='Month Name',
    y='Release Count',
    text='Release Count',
)

albums_table['release_year'] = albums_table['Release Date'].dt.year

yearly_releases = albums_table['release_year'].value_counts().sort_index().reset_index()
yearly_releases.columns = ['Release Year', 'Release Count']

st.subheader('Number of Album Releases by Year')
# fig_yearly = px.line(
#     yearly_releases,
#     x='Release Year',
#     y='Release Count',
#     # labels={'Year': 'Release Year', 'Release Count': 'Number of Releases'},
#     markers=True,
#     text='Release Count',
#     log_y=True,
#     color_discrete_sequence=['#109618'],
# )
#
# fig_yearly.update_traces(
#     textposition='top center',
#     textfont=dict(size=12, color='black'),
#     line=dict(width=3, color='rgba(0, 0, 255, 0.3)'),
#     marker=dict(size=8, color='green', opacity=1),
# )
# fig_yearly.update_layout(
#     yaxis_title='Number of Releases (log scale)',
# )
# st.plotly_chart(fig_yearly)

plots.create_line_chart(
    data=yearly_releases,
    x='Release Year',
    y='Release Count',
    text='Release Count',
    yaxis_title='Number of Releases (log scale)',
    log_y=True,
)
# fig_pie_album_type = px.pie(
#     albums_table,
#     names='Album Type',
#     title='Distribution of Album Types',
# )
#
# fig_pie_album_type.update_traces(
#     textinfo='percent+label',
# )
# fig_pie_album_type.update_layout(showlegend=False)
#
# st.plotly_chart(fig_pie_album_type)

st.subheader('Distribution of Album Types')
plots.create_pie_chart(
    data=albums_table,
    names='Album Type',
)

# fig_box = px.box(
#     albums_table,
#     x='Album Type',
#     y='Album Popularity',
#     title='Distribution of Album Popularity by Album Type',
#     # labels={
#     #     'album_type': 'Album Type',
#     #     'album_popularity': 'Album Popularity'
#     # },
# )
# st.plotly_chart(fig_box)

st.subheader('Distribution of Album Popularity by Album Type')
plots.create_boxplot(
    data=albums_table,
    x='Album Type',
    y='Album Popularity',
    color_discrete_sequence=px.colors.qualitative.Vivid,
)

# fig_tracks_vs_popularity = px.scatter(
#     albums_table,
#     x='Total Tracks',
#     y='Album Popularity',
#     title='Impact of Track Count on Album Popularity',
#     labels={
#         'Total Tracks': 'Total Tracks',
#         'Album Popularity': 'Album Popularity'
#     },
# )
# st.plotly_chart(fig_tracks_vs_popularity)


fig_tracks_vs_popularity = px.scatter(
    albums_table,
    x='Total Tracks',
    y='Album Popularity',
    size='Total Tracks',
    title='Impact of Track Count on Album Popularity',
    hover_data=['Album Name'],
    marginal_x="histogram",
    # marginal_y="rug",
    # trendline="ols",
    trendline="lowess",
    # opacity=0.5,
    color_discrete_sequence=['#008000']
)
fig_tracks_vs_popularity.update_layout(
    height=700,
)
st.plotly_chart(fig_tracks_vs_popularity)
