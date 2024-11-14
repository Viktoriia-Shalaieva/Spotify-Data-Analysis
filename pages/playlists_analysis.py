import streamlit as st
from modules.nav import navbar
import pandas as pd
import yaml
import os
import plotly.express as px


st.set_page_config(
    page_title="Spotify Data Analysis",
    page_icon="🎵")

st.sidebar.image("images/music.png", width=150)

navbar()
st.sidebar.divider()
st.sidebar.markdown("# **Playlists Analysis** 📋️ ")

st.title("Playlists Analysis 📋️ ")
st.divider()


with open('config/country_coords.yaml', 'r') as config_file:
    country_coords = yaml.safe_load(config_file)

countries = []
latitudes = []
longitudes = []

for country, coords in country_coords['countries'].items():
    countries.append(country)
    latitudes.append(coords['latitude'])
    longitudes.append(coords['longitude'])

country_coords_df = pd.DataFrame({
    'country': countries,
    'latitude': latitudes,
    'longitude': longitudes
})

st.subheader("Map of Countries for Playlist Analysis")

fig = px.choropleth(
    country_coords_df,
    locations='country',  # Name of the column containing country names
    locationmode='country names',  # This mode allows country names to be used for mapping
    color='country',
    hover_name="country",
    title="Countries for Playlist Analysis"
)

st.plotly_chart(fig)

with open('config/path_config.yaml', 'r') as config_file:
    path_config = yaml.safe_load(config_file)

data_dir = path_config['data_dir'][0]
raw_dir = path_config['raw_dir'][0]
file_paths = {file_name: os.path.join(data_dir, file_name) for file_name in path_config['files_names']}

playlists_path = str(file_paths['playlists.csv'])
playlists_table = pd.read_csv(playlists_path, sep="~")

playlist_names = playlists_table['playlist_name'].unique()
total_playlists = playlists_table['playlist_id'].nunique()
average_followers = playlists_table['playlist_followers_total'].mean()
total_unique_tracks = playlists_table['track_id'].nunique()
min_followers = playlists_table['playlist_followers_total'].min()
max_followers = playlists_table['playlist_followers_total'].max()

max_followers_playlist = playlists_table.sort_values(by='playlist_followers_total', ascending=False).iloc[0]
min_followers_playlist = playlists_table.sort_values(by='playlist_followers_total').iloc[0]

st.subheader("Playlists Analysis - Overview Statistics")

st.metric(label="Total Number of Playlists", value=total_playlists)
st.metric(label="Average Number of Followers per Playlist", value=f"{average_followers:.0f}")
st.metric(label="Total Number of Unique Tracks", value=total_unique_tracks)

st.subheader("Playlist with Maximum Followers")
st.write(f"Playlist Name: {max_followers_playlist['playlist_name']}")
st.write(f"Number of Followers: {max_followers_playlist['playlist_followers_total']}")

st.subheader("Playlist with Minimum Followers")
st.write(f"Playlist Name: {min_followers_playlist['playlist_name']}")
st.write(f"Number of Followers: {min_followers_playlist['playlist_followers_total']}")

select_all = st.checkbox("Select All", value=True)

selected_playlists = st.multiselect(
    "Select Playlists",
    options=playlist_names,
    default=playlist_names if select_all else []
)

followers_data = playlists_table[['playlist_name', 'playlist_followers_total']].drop_duplicates()
followers_data.columns = ['Playlist Name', 'Number of Followers']
followers_data = followers_data[followers_data['Playlist Name'].isin(selected_playlists)]
followers_data = followers_data.sort_values(by='Number of Followers', ascending=False)

fig_followers = px.bar(followers_data,
                       x='Playlist Name',
                       y='Number of Followers',
                       color="Playlist Name",
                       title='Number of Followers per Playlist',
                       log_y=True)
st.plotly_chart(fig_followers)

fig_pie_followers = px.pie(
    followers_data,
    names='Playlist Name',
    values='Number of Followers',
    title='Proportion of Followers per Playlist',
    height=400
)
st.plotly_chart(fig_pie_followers)

avg_popularity = playlists_table.groupby('playlist_name')['track_popularity'].mean().reset_index()
avg_popularity.columns = ['Playlist', 'Average Popularity']
avg_popularity = avg_popularity.sort_values(by='Average Popularity', ascending=False)

fig = px.bar(avg_popularity,
             x='Playlist',
             y='Average Popularity',
             title='Average Track Popularity Across Playlists')

st.plotly_chart(fig)

fig_violin = px.violin(
    playlists_table,
    x='playlist_name',
    y='track_popularity',
    points="all",
    title='Distribution of Track Popularity Across Playlists',
    labels={'playlist_name': 'Playlist', 'track_popularity': 'Track Popularity'},
    color='playlist_name',
    height=700,
)

fig_violin.update_layout(
    xaxis_title='Playlist',
    yaxis_title='Track Popularity',
    showlegend=False
)

st.plotly_chart(fig_violin)

selected_playlist = st.selectbox("Select a Playlist", playlist_names)
filtered_data = playlists_table[playlists_table['playlist_name'] == selected_playlist]

st.write(f"Data for {selected_playlist}:")
st.dataframe(filtered_data, height=210, hide_index=True)

fig_track_popularity = px.histogram(filtered_data,
                                    x='track_popularity',
                                    nbins=20,
                                    labels={'track_popularity': 'Track Popularity'},
                                    title=f"Track Popularity Distribution in {selected_playlist}")
st.plotly_chart(fig_track_popularity)


