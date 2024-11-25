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

countries_for_map = []
latitudes = []
longitudes = []

for country, coords in country_coords['countries'].items():
    countries_for_map.append(country)
    latitudes.append(coords['latitude'])
    longitudes.append(coords['longitude'])

country_coords_df = pd.DataFrame({
    'country': countries_for_map,
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
fig.update_layout(
    legend_title_text='Country'
)
st.plotly_chart(fig)

with open('config/path_config.yaml', 'r') as config_file:
    path_config = yaml.safe_load(config_file)

data_dir = path_config['data_dir'][0]
raw_dir = path_config['raw_dir'][0]
file_paths = {file_name: os.path.join(data_dir, file_name) for file_name in path_config['files_names']}

playlists_path = str(file_paths['playlists.csv'])
artists_genres_full_unknown_path = str(file_paths['artists_genres_full_unknown.csv'])
tracks_path = str(file_paths['tracks.csv'])

playlists_table = pd.read_csv(playlists_path, sep="~")
artists_genres_full_unknown = pd.read_csv(artists_genres_full_unknown_path, sep='~')
tracks_table = pd.read_csv(tracks_path, sep='~')

playlist_names = playlists_table['playlist_name'].unique()
countries_for_map = playlists_table['country'].unique()
min_followers = playlists_table['playlist_followers_total'].min()
max_followers = playlists_table['playlist_followers_total'].max()

max_followers_playlist = playlists_table.sort_values(by='playlist_followers_total', ascending=False).iloc[0]
min_followers_playlist = playlists_table.sort_values(by='playlist_followers_total').iloc[0]

st.subheader("Playlist with Maximum Followers")
st.write(f"Playlist Name: {max_followers_playlist['playlist_name']}")
st.write(f"Number of Followers: {max_followers_playlist['playlist_followers_total']}")

st.subheader("Playlist with Minimum Followers")
st.write(f"Playlist Name: {min_followers_playlist['playlist_name']}")
st.write(f"Number of Followers: {min_followers_playlist['playlist_followers_total']}")

select_all = st.checkbox("Select All", value=True)

selected_countries = st.multiselect(
    "Select Countries",
    options=countries_for_map,
    default=countries_for_map if select_all else []
)

followers_data = playlists_table[['country', 'playlist_followers_total']].drop_duplicates()
followers_data.columns = ['Country', 'Number of Followers']
followers_data = followers_data[followers_data['Country'].isin(selected_countries)]
followers_data = followers_data.sort_values(by='Number of Followers', ascending=False)

fig_followers = px.bar(followers_data,
                       x='Country',
                       y='Number of Followers',
                       # color="Country",
                       title='Number of Followers per Playlist',
                       log_y=True)
st.plotly_chart(fig_followers)

merged_playlists_tracks = pd.merge(
    playlists_table,
    tracks_table,
    on='track_id',
    how='left'
)

help_input = (
    '''The popularity of the track across different countries. 
    The value will be between 0 and 100, with 100 being the most popular.'''
)
st.subheader("Average Track Popularity Across Playlists", help=help_input)

avg_popularity = merged_playlists_tracks.groupby('country')['track_popularity'].mean().reset_index()
avg_popularity.columns = ['Country', 'Average Popularity']
avg_popularity = avg_popularity.sort_values(by='Average Popularity', ascending=False)
min_y = avg_popularity['Average Popularity'].min() - 5
max_y = avg_popularity['Average Popularity'].max() + 5

fig = px.bar(avg_popularity,
             x='Country',
             y='Average Popularity',
             # title='Average Track Popularity Across Playlists',
             range_y=[min_y, max_y])

st.plotly_chart(fig)

fig_violin = px.violin(
    merged_playlists_tracks,
    x='country',
    y='track_popularity',
    points="all",
    box=True,
    title='Distribution of Track Popularity Across Playlists',
    labels={'country': 'Country', 'track_popularity': 'Track Popularity'},
    color='country',
    height=700,
)

fig_violin.update_layout(
    xaxis_title='Country',
    yaxis_title='Track Popularity',
    showlegend=False
)

st.plotly_chart(fig_violin)

st.subheader("Country-wise Track Popularity Analysis", help=help_input)

selected_country = st.selectbox("Select a Country", countries_for_map)
filtered_data = merged_playlists_tracks[merged_playlists_tracks['country'] == selected_country]

# st.write(f"Data for {selected_playlist}:")
# st.dataframe(filtered_data, height=210, hide_index=True)

mean_popularity = filtered_data['track_popularity'].mean()
median_popularity = filtered_data['track_popularity'].median()
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

tab1_histogram, tab2_interpretation = st.tabs(["Histogram", "Interpretation"])

with tab1_histogram:
    fig_track_popularity = px.histogram(
        filtered_data,
        x='track_popularity',
        nbins=20,
        labels={'track_popularity': 'Track Popularity'},
        title=f"Track Popularity Distribution in Top 50 - {selected_country}",
        opacity=0.7,
        # marginal="box"
        )

    fig_track_popularity.add_vline(
        x=mean_popularity,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Mean: {mean_popularity:.2f}",
        annotation_position="top right",
        annotation_font_color="blue"
    )

    fig_track_popularity.add_vline(
        x=median_popularity,
        line_dash="dot",
        line_color="green",
        annotation_text=f"Median: {median_popularity:.2f}",
        annotation_position="bottom left",
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
        annotation_font_color="blue",
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

with tab2_interpretation:
    # st.write(f"Percentage of data within 1 standard deviation: {within_one_std_dev:.2f}%")
    # st.write(f"Percentage of data within 2 standard deviations: {within_two_std_dev:.2f}%")
    # st.write(f"Percentage of data within 3 standard deviations: {within_three_std_dev:.2f}%")
    #
    # st.subheader("Interpretation of Results")
    # st.markdown("""
    # If the percentage of data within 1, 2, and 3 standard deviations is approximately 68%, 95%, and 99.7%, respectively,
    # this indicates that the data is approximately normally distributed.
    #
    # Significant deviations from these values may indicate that the data is skewed, has outliers,
    # or other anomalies in its distribution.
    # """)
    st.subheader("Interpretation of Results")
    st.write(f"Percentage of data within 1 standard deviation: {within_one_std_dev:.2f}%")
    st.write(f"Percentage of data within 2 standard deviations: {within_two_std_dev:.2f}%")
    st.write(f"Percentage of data within 3 standard deviations: {within_three_std_dev:.2f}%")
    st.markdown("""
    If the percentage of data within 1, 2, and 3 standard deviations is approximately 68%, 95%, 
    and 99.7%, it suggests a normal distribution (Empirical Rule):

    - **1 Std Dev (68%)**: About 68% of data falls within 1 standard deviation of the mean.
    - **2 Std Dev (95%)**: Around 95% of data lies within 2 standard deviations.
    - **3 Std Dev (99.7%)**: Nearly all data falls within 3 standard deviations.

    Significant deviations may indicate skewness, outliers, or other anomalies:
    - **Skewness**: Data may have a long tail if heavily skewed.
    - **Outliers**: Extreme values far from the mean may indicate rare cases.

    Shaded regions in the chart show these ranges, helping assess data normality and identify trends or anomalies.
    """)

st.dataframe(merged_playlists_tracks)
# playlists_tracks_data_tab = merged_playlists_tracks['track_name']
track_counts = merged_playlists_tracks['track_id'].value_counts().reset_index()
st.dataframe(track_counts)

tracks_data_tab = track_counts.merge(
    tracks_table[['track_id', 'track_name', 'track_popularity', 'track_explicit']],
    on='track_id',
    how='left'
)
st.dataframe(tracks_data_tab)

tracks_data_tab = tracks_data_tab[['track_name', 'count', 'track_popularity', 'track_explicit']]
top_10_tracks = tracks_data_tab.head(10)
top_10_tracks.columns = ['Track Name', 'Frequency in Playlists', 'Popularity', 'Explicit']
top_10_tracks = top_10_tracks.sort_values(by='Frequency in Playlists', ascending=True)
st.dataframe(top_10_tracks, hide_index=True)


st.subheader("Top 10 Tracks by Frequency in Playlists")
tab1_tracks, tab2_tracks, tab3_tracks, tab4_tracks = st.tabs(["Bar Plot", "Data Table", "Popularity Graph", "Map"])

with tab1_tracks:
    fig = px.bar(
        top_10_tracks,
        x='Frequency in Playlists',
        y='Track Name',
        orientation='h',
        title='Top 10 Tracks by Frequency in Playlists',
        color='Frequency in Playlists',
    )
    st.plotly_chart(fig)

with tab2_tracks:
    st.subheader("Data Table of Top 10 Tracks")
    top_10_tracks_data_tab = top_10_tracks.sort_values(by='Frequency in Playlists', ascending=False)
    st.dataframe(top_10_tracks_data_tab, hide_index=True)

with tab3_tracks:
    min_y_popularity_track = top_10_tracks['Popularity'].min() - 5
    max_y_popularity_track = top_10_tracks['Popularity'].max()

    fig_popularity = px.bar(top_10_tracks,
                            x='Track Name',
                            y='Popularity',
                            title='Popularity of Top 10 Tracks',
                            labels={'Popularity': 'Track Popularity', 'Track Name': 'Track Name'},
                            color='Popularity',
                            range_y=[min_y_popularity_track, max_y_popularity_track],
                            )
    fig_popularity.update_layout(xaxis={'categoryorder': 'total descending'})
    st.plotly_chart(fig_popularity)

with tab4_tracks:
    selected_track = st.selectbox(
        "Select a Track",
        options=top_10_tracks['Track Name']
    )

    # Filter the data to include only rows for the selected track
    filtered_tracks = merged_playlists_tracks[merged_playlists_tracks['track_name'] == selected_track]

    # Extract the unique list of countries where the track is present
    track_countries = filtered_tracks['country'].unique()

    # Filter the country coordinates table to include only countries from the track_countries list
    filtered_countries = country_coords_df[country_coords_df['country'].isin(track_countries)]

    fig_map = px.choropleth(
        filtered_countries,
        locations='country',
        locationmode='country names',
        color='country',
        hover_name='country',
        title=f'Countries with Playlists Containing "{selected_track}"'
    )

    fig_map.update_layout(
        legend_title_text='Country',
        # geo=dict(
        #     showcountries=True,
        #     countrycolor="LightGray",
        #     showcoastlines=True,
        #     coastlinecolor="RebeccaPurple"
        # )
    )
    st.plotly_chart(fig_map)

st.subheader("Top 10 Artists by Frequency in Playlists")

playlists_table['artist_id'] = playlists_table['artist_id'].str.split(', ')
st.dataframe(playlists_table)

st.write('-expanded_playlists_artists---------')
expanded_playlists_artists = playlists_table.explode('artist_id')
st.dataframe(expanded_playlists_artists)

st.write('-artist_per_playlist---------')
artist_per_playlist = expanded_playlists_artists.groupby(['country', 'artist_id'])['artist_id'].count().reset_index(name='count')
st.dataframe(artist_per_playlist)


st.write('-artist_counts---------')
artist_counts = expanded_playlists_artists['artist_id'].value_counts().reset_index()
artist_counts.columns = ['artist_id', 'Count']
st.dataframe(artist_counts)

st.write('top_10_artists-----------------')
top_10_artists = artist_counts.head(10)
top_10_artists = top_10_artists.merge(
    artists_genres_full_unknown[['artist_id', 'artist_name', 'artist_followers', 'artist_popularity', 'artist_genres']],
    on='artist_id',
    how='left'
)

st.dataframe(top_10_artists, hide_index=True)

st.write('top_10_artists_full-----------------')
top_10_artists_full = top_10_artists[['artist_name', 'Count', 'artist_followers', 'artist_popularity', 'artist_genres']]
st.dataframe(top_10_artists_full, hide_index=True)

st.write(' renamed columns top_10_artists_full-----------------')
top_10_artists_full.columns = ['Artist', 'Frequency in Playlists',  'Followers', 'Popularity', 'Genres']
st.dataframe(top_10_artists_full, hide_index=True)

tab1_artists, tab2_artists, tab3_artists, tab4_artists = st.tabs(["Bar Plot", "Data Table", "Popularity Graph", "Map"])

with tab1_artists:
    fig = px.bar(top_10_artists_full,
                 x='Frequency in Playlists',
                 y='Artist',
                 orientation='h',
                 title='Top 10 Artists by Frequency in Playlists',
                 color='Frequency in Playlists')
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig)

with tab2_artists:
    st.dataframe(top_10_artists_full, hide_index=True)

with tab3_artists:
    min_y_popularity_art = top_10_artists_full['Popularity'].min()-5
    max_y_popularity_art = top_10_artists_full['Popularity'].max()

    fig_popularity = px.bar(top_10_artists_full,
                            x='Artist',
                            y='Popularity',
                            title='Popularity of Top 10 Artists',
                            color='Popularity',
                            range_y=[min_y_popularity_art, max_y_popularity_art],
                            )
    fig_popularity.update_layout(xaxis={'categoryorder': 'total descending'})
    st.plotly_chart(fig_popularity)

with tab4_artists:
    selected_artist = st.selectbox(
        "Select an Artist",
        options=top_10_artists_full['Artist']
    )

    artist_data = artist_per_playlist.merge(
        artists_genres_full_unknown[['artist_id', 'artist_name']],
        on='artist_id',
        how='left'
    )

    filtered_artist_data = artist_data[artist_data['artist_name'] == selected_artist]

    artist_country_map_data = filtered_artist_data.merge(
        country_coords_df,
        on='country',
        how='left'
    )

    fig_map = px.choropleth(
        artist_country_map_data,
        locations='country',
        locationmode='country names',
        color='count',
        hover_name='country',
        title=f'Countries with Playlists Containing "{selected_artist}"',
        labels={'count': 'Frequency'},
        color_continuous_scale=px.colors.sequential.Plasma,
    )

    fig_map.update_layout(
        legend_title_text='Frequency',
    )

    st.plotly_chart(fig_map)

    countries_list = ', '.join(filtered_artist_data['country'].tolist())
    st.write("**Countries where the artist is present:**")

    filtered_artist_data_map = filtered_artist_data[['country', 'count']].sort_values(['count'], ascending=False)
    filtered_artist_data_map.columns = ['Country', 'Frequency in Playlists']

    st.dataframe(filtered_artist_data_map, hide_index=True)
