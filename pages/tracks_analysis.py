import streamlit as st
from modules import components
from modules import plots
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
import numpy as np


components.set_page_layout()
st.sidebar.markdown("**Tracks Analysis** 🎵")

components.set_page_header("Tracks Analysis", "🎵")


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


@st.cache_data
def load_artists_data():
    artists_path = str(file_paths['artists_genres_full_unknown.csv'])
    return pd.read_csv(artists_path, sep='~')


playlists_table = load_playlists_data()
tracks_table = load_tracks_data()
artists_table = load_artists_data()

playlists_table = playlists_table.rename(columns={
    'playlist_id': 'Playlist ID',
    'playlist_name': 'Playlist Name',
    'country': 'Country',
    'playlist_followers_total': 'Playlist Total Followers',
    'track_id': 'Track ID',
    'album_id': 'Album ID',
    'artist_id': 'Artist ID'
})

artists_table = artists_table.rename(columns={
    'artist_id': 'Artist ID',
    'artist_name': 'Artist Name',
    'artist_followers': 'Artist Total Followers',
    'artist_genres': 'Artist Genres',
    'artist_popularity': 'Artist Popularity'
})

tracks_table = tracks_table.rename(columns={
    'track_id': 'Track ID',
    'track_name': 'Track Name',
    'track_duration_ms': 'Duration (ms)',
    'track_explicit': 'Explicit Content',
    'track_popularity': 'Track Popularity'
})

# fig_popularity_distribution = px.histogram(
#     tracks_table,
#     x='Track Popularity',
#     title='Distribution of Track Popularity',
#     labels={'Track Popularity': 'Popularity'},
#     nbins=10,
# )
#
# st.plotly_chart(fig_popularity_distribution)

st.subheader('Distribution of Track Popularity')
plots.create_histogram(
    data=tracks_table,
    x='Track Popularity',
)

merged_playlists_tracks = pd.merge(
    playlists_table[['Track ID', 'Artist ID']],
    tracks_table,
    on='Track ID',
    how='left'
)
merged_playlists_tracks.loc[:, 'Artist ID'] = merged_playlists_tracks['Artist ID'].str.split(', ')
expanded_tracks_artists = merged_playlists_tracks.explode('Artist ID')
tracks_artists_name = expanded_tracks_artists.merge(
    artists_table[['Artist ID', 'Artist Name']],
    on='Artist ID',
    how='left'
)

tracks_artists_grouped = tracks_artists_name.groupby('Track ID').agg({
    'Track Name': 'first',   # Keep the first occurrence of the track name
    'Artist Name': lambda x: ', '.join(x.dropna().unique()),  # Concatenate unique artist names, separated by commas
    'Duration (ms)': 'first',
    'Explicit Content': 'first',
    'Track Popularity': 'first',
}).reset_index()

# tracks_artists_grouped = tracks_artists_grouped.rename(columns={
#     'Track ID': 'Track ID',
#     'Track Name': 'Track Name',
#     'Artist Name': 'Artists',
#     'Duration (ms)': 'Duration (ms)',
#     'Explicit Content': 'Explicit Content',
#     'Track Popularity': 'Popularity'
# })

top_10_tracks_popularity = (
    tracks_artists_grouped.nlargest(n=10, columns='Track Popularity')
    .sort_values(by='Track Popularity', ascending=True)
)

min_x = top_10_tracks_popularity['Track Popularity'].min() - 3
max_x = top_10_tracks_popularity['Track Popularity'].max()

# fig_top_10 = px.bar(
#     top_10_tracks_popularity,
#     x='Track Popularity',
#     y='Track Name',
#     orientation='h',
#     title='Top 10 Most Popular Tracks',
#     text='Track Popularity',
#     range_x=[min_x, max_x],
#     hover_data={'Artist Name': True},
# )
#
# fig_top_10.update_traces(textposition='outside')
# st.plotly_chart(fig_top_10)

st.subheader('Top 10 Most Popular Tracks')
plots.create_bar_plot(
    data=top_10_tracks_popularity,
    x='Track Popularity',
    y='Track Name',
    orientation='h',
    text='Track Popularity',
    range_x=[min_x, max_x],
    hover_data={'Artist Name': True},
)

tracks_artists_grouped['Explicit Status'] = tracks_artists_grouped['Explicit Content'].map({True: 'Explicit', False: 'Non-Explicit'})

# fig_pie_explicit = px.pie(tracks_artists_grouped,
#                           names='Explicit Status',
#                           title='Distribution of Explicit and Non-Explicit Tracks',
#                           )
#
# fig_pie_explicit.update_traces(
#     textinfo='percent+label',
# )
# fig_pie_explicit.update_layout(showlegend=False)
#
# st.plotly_chart(fig_pie_explicit)

st.subheader('Distribution of Explicit and Non-Explicit Tracks')
plots.create_pie_chart(
    data=tracks_artists_grouped,
    names='Explicit Status',
)

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

explicit_popularity = tracks_artists_grouped[tracks_artists_grouped['Explicit Status'] == 'Explicit']['Track Popularity']
non_explicit_popularity = tracks_artists_grouped[tracks_artists_grouped['Explicit Status'] == 'Non-Explicit']['Track Popularity']

t_stat, p_value = ttest_ind(explicit_popularity, non_explicit_popularity)

tab1_visualizations, tab2_results, tab3_interpretation = st.tabs(
    ['Visualizations', 'Statistical Results',  'Interpretation'])

with tab1_visualizations:
    st.subheader("Visualizations")
    tab1_boxplot, tab2_histogram = st.tabs(['Box Plot', 'Histogram'])

    with tab1_boxplot:
        # fig_box = px.box(
        #     tracks_artists_grouped,
        #     x='Explicit Status',
        #     y='Track Popularity',
        #     # color='explicit_label',
        #     # labels={'track_popularity': 'Track Popularity', 'track_explicit': 'Explicit Status'}
        # )
        # st.plotly_chart(fig_box)

        plots.create_boxplot(
            data=tracks_artists_grouped,
            x='Explicit Status',
            y='Track Popularity',
        )

    with tab2_histogram:
        fig_histogram = px.histogram(
            tracks_artists_grouped,
            x='Track Popularity',
            color='Explicit Status',
            barmode='overlay',
            # labels={'track_popularity': 'Track Popularity'}
        )
        fig_histogram.update_layout(legend_title_text='Explicit Status')
        st.plotly_chart(fig_histogram)

        plots.create_histogram(
            data=tracks_artists_grouped,
            x='Track Popularity',
            color='Explicit Status',
            legend_title='Explicit Status',
        )

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

tracks_artists_grouped['Track Duration (minutes)'] = tracks_artists_grouped['Duration (ms)'] / 60000

fig_scatter = px.scatter(
    tracks_artists_grouped,
    x='Track Duration (minutes)',
    y='Track Popularity',
    color='Explicit Status',
    title='Track Popularity vs. Duration',
    # labels={'track_duration_minutes': 'Track Duration (minutes)', 'track_popularity': 'Track Popularity'},
    hover_data=['Track Name'],
    symbol='Explicit Status',
    marginal_x="histogram",
    # marginal_y="rug",
    trendline="ols",
    opacity=0.8,
)

fig_scatter.update_layout(
    # legend_title_text='Explicit Status',
    height=700,
)

st.plotly_chart(fig_scatter)

fig_facet = px.scatter(
    tracks_artists_grouped,
    x='Track Duration (minutes)',
    y='Track Popularity',
    facet_col='Explicit Status',
    color='Explicit Status',
    title='Track Popularity vs. Duration (Separated by Explicit Status)',
    trendline='ols'
)
st.plotly_chart(fig_facet)

fig_violin = px.violin(
    tracks_artists_grouped,
    x='Explicit Status',
    y='Track Popularity',
    color='Explicit Status',
    box=True,
    points='all',
    title='Track Popularity Distribution with Density by Explicit Status'
)

fig_violin.update_layout(
    # legend_title_text='Explicit Status',
    height=700,
)

st.plotly_chart(fig_violin)

fig_scatter = px.scatter(
    tracks_artists_grouped,
    x='Track Duration (minutes)',
    y='Track Popularity',
    color='Explicit Status',
    title='Track Popularity vs. Duration',
    hover_data=['Track Name'],
    opacity=0.6,
    size_max=8,
    symbol='Explicit Status',
)


x = tracks_artists_grouped['Track Duration (minutes)']
y = tracks_artists_grouped['Track Popularity']
z = np.polyfit(x, y, 1)
p = np.poly1d(z)

fig_scatter.add_trace(
    go.Scatter(
        x=x,
        y=p(x),
        mode='lines',
        name='Trend Line',
        line=dict(color='red', width=2, dash='dot')
    )
)

fig_scatter.update_traces(marker=dict(size=6, line=dict(width=1, color='DarkSlateGrey')))
fig_scatter.update_layout(
    xaxis=dict(title='Track Duration (minutes)', gridcolor='lightgray'),
    yaxis=dict(title='Track Popularity', gridcolor='lightgray'),
    legend_title_text='Explicit Status',
    height=600,
    template='simple_white'
)

st.plotly_chart(fig_scatter)


st.subheader("Analysis of Correlation Between Track Duration and Popularity")

correlation, p_value = pearsonr(tracks_table['Duration (ms)'], tracks_table['Track Popularity'])

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
