import streamlit as st
from modules.nav import navbar
import pandas as pd
import yaml
import os
import plotly.express as px
import numpy as np


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
    # title="Countries for Playlist Analysis"
)

st.plotly_chart(fig)

with open('config/path_config.yaml', 'r') as config_file:
    path_config = yaml.safe_load(config_file)

data_dir = path_config['data_dir'][0]
raw_dir = path_config['raw_dir'][0]
file_paths = {file_name: os.path.join(data_dir, file_name) for file_name in path_config['files_names']}

playlists_path = str(file_paths['playlists.csv'])
tracks_path = str(file_paths['tracks.csv'])
playlists_table = pd.read_csv(playlists_path, sep="~")
tracks_table = pd.read_csv(tracks_path, sep='~')

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

merged_playlists_tracks = pd.merge(
    playlists_table,
    tracks_table,
    on='track_id',
    how='left'
)

avg_popularity = merged_playlists_tracks.groupby('playlist_name')['track_popularity'].mean().reset_index()
avg_popularity.columns = ['Playlist', 'Average Popularity']
avg_popularity = avg_popularity.sort_values(by='Average Popularity', ascending=False)

fig = px.bar(avg_popularity,
             x='Playlist',
             y='Average Popularity',
             title='Average Track Popularity Across Playlists')

st.plotly_chart(fig)

fig_violin = px.violin(
    merged_playlists_tracks,
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
filtered_data = merged_playlists_tracks[merged_playlists_tracks['playlist_name'] == selected_playlist]

# st.write(f"Data for {selected_playlist}:")
# st.dataframe(filtered_data, height=210, hide_index=True)

mean_popularity = filtered_data['track_popularity'].mean()
std_popularity = filtered_data['track_popularity'].std()

one_std_dev = (mean_popularity - std_popularity, mean_popularity + std_popularity)
two_std_dev = (mean_popularity - 2 * std_popularity, mean_popularity + 2 * std_popularity)
three_std_dev = (mean_popularity - 3 * std_popularity, mean_popularity + 3 * std_popularity)

total_values = len(filtered_data['track_popularity'])
within_one_std_dev = len(filtered_data
                         [(filtered_data['track_popularity'] >= one_std_dev[0]) &
                          (filtered_data['track_popularity'] <= one_std_dev[1])]) / total_values * 100
within_two_std_dev = len(filtered_data
                         [(filtered_data['track_popularity'] >= two_std_dev[0]) &
                          (filtered_data['track_popularity'] <= two_std_dev[1])]) / total_values * 100
within_three_std_dev = len(filtered_data
                           [(filtered_data['track_popularity'] >= three_std_dev[0]) &
                            (filtered_data['track_popularity'] <= three_std_dev[1])]) / total_values * 100

fig_track_popularity = px.histogram(
    filtered_data,
    x='track_popularity',
    nbins=20,
    labels={'track_popularity': 'Track Popularity'},
    title=f"Track Popularity Distribution in {selected_playlist}",
    opacity=0.7,
    # marginal="box"
)

mean_popularity = filtered_data['track_popularity'].mean()
fig_track_popularity.add_vline(
    x=mean_popularity,
    line_dash="dash",
    line_color="red",
    annotation_text=f"Mean: {mean_popularity:.2f}",
    annotation_position="top left",
    annotation_font_color="blue"
)

median_popularity = filtered_data['track_popularity'].median()
fig_track_popularity.add_vline(
    x=median_popularity,
    line_dash="dot",
    line_color="green",
    annotation_text=f"Median: {median_popularity:.2f}",
    annotation_position="top right",
    annotation_font_color="blue",
)

fig_track_popularity.update_layout(
    xaxis_title="Track Popularity",
    yaxis_title="Count",
    bargap=0.1,
    template="plotly_dark"
)

fig_track_popularity.add_vrect(
    x0=one_std_dev[0], x1=one_std_dev[1],
    fillcolor="blue", opacity=0.1,
    layer="below", line_width=0,
    annotation_text="1 Std Dev",
    annotation_position="top left",
    annotation_font_color = "blue",
)
fig_track_popularity.add_vrect(
    x0=two_std_dev[0], x1=two_std_dev[1],
    fillcolor="green", opacity=0.1,
    layer="below", line_width=0,
    annotation_text="2 Std Dev",
    annotation_position="top left",
    annotation_font_color="blue",
)
fig_track_popularity.add_vrect(
    x0=three_std_dev[0], x1=three_std_dev[1],
    fillcolor="yellow", opacity=0.1,
    layer="below", line_width=0,
    annotation_text="3 Std Dev",
    annotation_position="top left",
    annotation_font_color="blue",
)

st.plotly_chart(fig_track_popularity)

st.write(f"Percentage of data within 1 standard deviation: {within_one_std_dev:.2f}%")
st.write(f"Percentage of data within 2 standard deviations: {within_two_std_dev:.2f}%")
st.write(f"Percentage of data within 3 standard deviations: {within_three_std_dev:.2f}%")

st.subheader("Interpretation of Results")
st.markdown("""
If the percentage of data within 1, 2, and 3 standard deviations is approximately 68%, 95%, and 99.7%, respectively, 
this indicates that the data is approximately normally distributed.

Significant deviations from these values may indicate that the data is skewed, has outliers, 
or other anomalies in its distribution.
""")
