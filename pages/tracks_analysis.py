import streamlit as st
from modules.nav import navbar
import pandas as pd
import yaml
import os
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt


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

tracks_path = str(file_paths['tracks.csv'])
tracks_table = pd.read_csv(tracks_path, sep='~')

fig_pie_explicit = px.pie(tracks_table,
                          names='track_explicit',
                          title='Distribution of Explicit and Non-Explicit Tracks')

fig_pie_explicit.update_layout(
    legend_title_text='Explicit Status'
)

st.plotly_chart(fig_pie_explicit)

fig_histogram = px.histogram(tracks_table,
                             x='track_popularity',
                             color='track_explicit',
                             barmode='overlay',
                             title='Track Popularity Distribution for Explicit and Non-Explicit Tracks',
                             labels={'track_popularity': 'Track Popularity'},
                             )
fig_histogram.update_layout(
    legend_title_text='Explicit Status'
)
st.plotly_chart(fig_histogram)

fig_box = px.box(tracks_table,
                 x='track_explicit',
                 y='track_popularity',
                 color='track_explicit',
                 title='Track Popularity Distribution for Explicit and Non-Explicit Tracks',
                 labels={'track_popularity': 'Track Popularity', 'track_explicit': 'Explicit Status'},
                 )

st.plotly_chart(fig_box)

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
