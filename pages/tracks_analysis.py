import streamlit as st
from modules.nav import navbar
import pandas as pd
import yaml
import os
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from scipy import stats
from scipy.stats import ttest_ind


st.set_page_config(
    page_title="Spotify Data Analysis",
    page_icon="🎵")

st.sidebar.image("images/music.png", width=150)

navbar()
st.sidebar.divider()
st.sidebar.markdown("# **Tracks Analysis** 🎵 ")

st.title("Tracks Analysis 🎵 ")
st.divider()

with open('config/path_config.yaml', 'r') as config_file:
    path_config = yaml.safe_load(config_file)

data_dir = path_config['data_dir'][0]
raw_dir = path_config['raw_dir'][0]
file_paths = {file_name: os.path.join(data_dir, file_name) for file_name in path_config['files_names']}


@st.cache_data
def load_playlists_data():
    playlists_path = str(file_paths['playlists.csv'])
    return pd.read_csv(playlists_path, sep="~")


@st.cache_data
def load_tracks_data():
    tracks_path = str(file_paths['tracks.csv'])
    return pd.read_csv(tracks_path, sep='~')


playlists_table = load_playlists_data()
tracks_table = load_tracks_data()

fig_popularity_distribution = px.histogram(
    tracks_table,
    x='track_popularity',
    title='Distribution of Track Popularity',
    labels={'track_popularity': 'Popularity'},
    nbins=10,
)

st.plotly_chart(fig_popularity_distribution)

top_10_tracks_popularity = (
    tracks_table.nlargest(n=10, columns='track_popularity')
    .sort_values(by='track_popularity', ascending=True)
)
min_x = top_10_tracks_popularity['track_popularity'].min() - 3
max_x = top_10_tracks_popularity['track_popularity'].max() + 1

fig_top_10 = px.bar(
    top_10_tracks_popularity,
    x='track_popularity',
    y='track_name',
    orientation='h',
    title='Top 10 Most Popular Tracks',
    labels={'track_popularity': 'Popularity', 'track_name': 'Track Name'},
    text='track_popularity',
    range_x=[min_x, max_x],
)
fig_top_10.update_traces(textposition='outside')
st.plotly_chart(fig_top_10)

fig_pie_explicit = px.pie(tracks_table,
                          names='track_explicit',
                          title='Distribution of Explicit and Non-Explicit Tracks')

fig_pie_explicit.update_layout(
    legend_title_text='Explicit Status'
)

st.plotly_chart(fig_pie_explicit)

# st.subheader('Track Popularity Distribution for Explicit and Non-Explicit Tracks')
# tab1_tracks, tab2_tracks = st.tabs(['Bar Plot', 'Histogram'])
#
# with tab1_tracks:
#     fig_box = px.box(tracks_table,
#                      x='track_explicit',
#                      y='track_popularity',
#                      color='track_explicit',
#                      # title='Track Popularity Distribution for Explicit and Non-Explicit Tracks',
#                      labels={'track_popularity': 'Track Popularity', 'track_explicit': 'Explicit Status'},
#                      )
#
#     st.plotly_chart(fig_box)
#
# with tab2_tracks:
#     fig_histogram = px.histogram(tracks_table,
#                                  x='track_popularity',
#                                  color='track_explicit',
#                                  barmode='overlay',
#                                  # title='Track Popularity Distribution for Explicit and Non-Explicit Tracks',
#                                  labels={'track_popularity': 'Track Popularity'},
#                                  )
#     fig_histogram.update_layout(
#         legend_title_text='Explicit Status'
#     )
#     st.plotly_chart(fig_histogram)

st.subheader('Analysis of Track Popularity for Explicit and Non-Explicit Tracks')

explicit_popularity = tracks_table[tracks_table['track_explicit']]['track_popularity']
non_explicit_popularity = tracks_table[~tracks_table['track_explicit']]['track_popularity']

t_stat, p_value = ttest_ind(explicit_popularity, non_explicit_popularity)

tab1_visualizations, tab2_results, tab3_interpretation = st.tabs(
    ['Visualizations', 'Statistical Results',  'Interpretation'])

with tab1_visualizations:
    st.subheader("Visualizations")
    tab1_boxplot, tab2_histogram = st.tabs(['Box Plot', 'Histogram'])

    with tab1_boxplot:
        fig_box = px.box(
            tracks_table,
            x='track_explicit',
            y='track_popularity',
            color='track_explicit',
            labels={'track_popularity': 'Track Popularity', 'track_explicit': 'Explicit Status'}
        )
        st.plotly_chart(fig_box)

    with tab2_histogram:
        fig_histogram = px.histogram(
            tracks_table,
            x='track_popularity',
            color='track_explicit',
            barmode='overlay',
            labels={'track_popularity': 'Track Popularity'}
        )
        fig_histogram.update_layout(legend_title_text='Explicit Status')
        st.plotly_chart(fig_histogram)

with tab2_results:
    st.subheader("Statistical Results")
    st.write(f"T-statistic: {t_stat:.2f}")
    st.write(f"P-value: {p_value:.2f}")

with tab3_interpretation:
    st.subheader("Interpretation")
    st.write("""
        **Key Insights:**
        **T-statistic:** Indicates the magnitude of the difference between the mean popularity of tracks with explicit content and those without.

        **P-value:** If the P-value is less than 0.05, the difference in popularity between the two groups is considered statistically significant.

        **Conclusion:**
        - If the results show statistical significance and a noticeable difference in the visualizations, explicit content could play a role in track popularity. 
        Otherwise, its impact might be negligible.
    """)


# fig_violin = px.violin(tracks_table,
#                        x='track_explicit',
#                        y='track_popularity',
#                        box=True,
#                        points='all',
#                        color='track_explicit',
#                        title='Track Popularity Distribution for Explicit and Non-Explicit Tracks',
#                        labels={'track_explicit': 'Explicit', 'track_popularity': 'Track Popularity'},
#                        )
# st.plotly_chart(fig_violin)
#
# fig = go.Figure()
#
# fig.add_trace(go.Violin(
#     x=tracks_table['track_explicit'][tracks_table['track_explicit']],
#     y=tracks_table['track_popularity'][tracks_table['track_explicit']],
#     points='all',
#     legendgroup='Explicit', scalegroup='Explicit', name='Explicit',
#     side='negative',
#     line_color='blue'
# ))
#
# fig.add_trace(go.Violin(
#     x=tracks_table['track_explicit'][~tracks_table['track_explicit']],
#     y=tracks_table['track_popularity'][~tracks_table['track_explicit']],
#     points='all',
#     legendgroup='Non-Explicit', scalegroup='Non-Explicit', name='Non-Explicit',
#     side='positive',
#     line_color='orange'
# ))
#
# fig.update_traces(meanline_visible=True)
# fig.update_layout(
#     title="Distribution of Track Popularity by Explicit Status",
#     violingap=0,
#     violinmode='overlay'
# )
# st.plotly_chart(fig)

tracks_table['track_duration_minutes'] = tracks_table['track_duration_ms'] / 60000

st.dataframe(tracks_table, height=210, hide_index=True)

fig_scatter = px.scatter(
    tracks_table,
    x='track_duration_minutes',
    y='track_popularity',
    color='track_explicit',
    title='Track Popularity vs. Duration',
    labels={'track_duration_minutes': 'Track Duration (minutes)', 'track_popularity': 'Track Popularity'},
    hover_data=['track_name']
)
fig_scatter.update_layout(
    legend_title_text='Explicit Status'
)
st.plotly_chart(fig_scatter)

st.subheader("Analysis of Correlation Between Track Duration and Popularity")

correlation, p_value = pearsonr(tracks_table['track_duration_ms'], tracks_table['track_popularity'])

tab1_correlation, tab2_correlation = st.tabs(["Results", "Interpretation"])

with tab1_correlation:
    st.write(f"Pearson Correlation Coefficient: {correlation:.2f}")
    st.write(f"P-value: {p_value:.2f}")
with tab2_correlation:
    st.write("""
        **Pearson Correlation Coefficient:**
        - Values range between -1 and 1.
        - A value close to 1 indicates a strong positive correlation.
        - A value close to -1 indicates a strong negative correlation.
        - A value close to 0 indicates no correlation.

        **P-value:**
        - Indicates the significance of the correlation.
        - A p-value less than 0.05 typically suggests a statistically significant correlation.

        **What this means:**
        - Use the correlation coefficient to determine the strength and direction of the relationship.
        - The p-value helps assess whether the relationship is statistically significant.
    """)

# res = stats.pearsonr(tracks_table['track_duration_ms'], tracks_table['track_popularity'])
# st.write(res)

# Calculate the number of artists for each track in the playlist table
playlists_table['num_artists'] = playlists_table['artist_id'].apply(lambda x: len(x.split(',')))
st.dataframe(playlists_table)

# Merge the number of artists from playlists_table with the tracks_table
tracks_with_artists = tracks_table.merge(
    playlists_table[['track_id', 'num_artists']],
    on='track_id',
    how='left'
)

st.dataframe(tracks_with_artists)

tracks_with_artists = tracks_with_artists.drop_duplicates(subset=['track_id'])

st.dataframe(tracks_with_artists)

# correlation = tracks_with_artists[['num_artists', 'track_popularity']].corr().iloc[0, 1]

# Calculate the Pearson correlation coefficient and p-value between the number of artists and track popularity
correlation, p_value = pearsonr(tracks_with_artists['num_artists'], tracks_with_artists['track_popularity'])
st.write(f"Pearson Correlation Coefficient: {correlation:.2f}")
st.write(f"P-value: {p_value:.2f}")

# Calculate the average popularity of tracks grouped by the number of artists
popularity_by_artists = tracks_with_artists.groupby('num_artists')['track_popularity'].mean().reset_index()
popularity_by_artists.rename(columns={'track_popularity': 'avg_track_popularity'}, inplace=True)
st.dataframe(popularity_by_artists)
min_y = popularity_by_artists['avg_track_popularity'].min() - 5
max_y = popularity_by_artists['avg_track_popularity'].max()

fig = px.bar(
    popularity_by_artists,
    x='num_artists',
    y='avg_track_popularity',
    title='Average Track Popularity by Number of Artists',
    labels={'num_artists': 'Number of Artists', 'track_popularity': 'Average Popularity'},
    range_y=[min_y, max_y],
)

st.plotly_chart(fig)

# Analyze the distribution of tracks by the number of artists
artist_distribution = tracks_with_artists['num_artists'].value_counts().reset_index()
artist_distribution.columns = ['num_artists', 'track_count']

artist_distribution.sort_values(by='num_artists', inplace=True)

st.dataframe(artist_distribution)

fig = px.bar(
    artist_distribution,
    x='num_artists',
    y='track_count',
    title='Distribution of Tracks by Number of Artists',
    labels={'num_artists': 'Number of Artists', 'track_count': 'Number of Tracks'},
)

st.plotly_chart(fig)
