import streamlit as st
from modules import components
from modules import plots
import pandas as pd
import yaml
import os
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from modules import data_processing
from scipy.stats import shapiro, skew


components.set_page_layout()
st.sidebar.markdown("# **Playlists Analysis** 📋️ ")

components.set_page_header("Playlists Analysis", "📋️")

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
# country_coords_df['random_value'] = np.random.rand(len(country_coords_df))
unique_countries = country_coords_df['country'].unique()
n_countries = len(unique_countries)

# https://plotly.com/python-api-reference/generated/plotly.express.colors.html
colors = px.colors.sample_colorscale("speed", n_countries)
# The zip() function returns a zip object, which is an iterator of tuples where the first item in each passed
# iterator is paired together, and then the second item in each passed iterator are paired together etc.
# zip combines two lists (unique_countries and colors) into pairs, e.g.
# dict converts these pairs into a dictionary where the keys are unique_countries and values are colors.
color_map = dict(zip(unique_countries, colors))

plots.create_choropleth_map(
    data=country_coords_df,
    locations='country',
    location_mode='country names',
    color='country',
    color_discrete_map=color_map,
    hover_name='country',
    title='Countries for Playlist Analysis',
    legend_title='Country'
)
# fig = px.choropleth(
#     country_coords_df,
#     locations='country',  # Name of the column containing country names
#     locationmode='country names',  # This mode allows country names to be used for mapping
#     color='country',
#     # color='random_value',
#     # color_discrete_sequence=px.colors.qualitative.Set3,
#     color_discrete_map=color_map,
#     hover_name="country",
#     # title="Countries for Playlist Analysis"
# )
# fig.update_layout(
#     legend_title_text='Country',
#     legend=dict(
#         y=0.5,
#     ),
#     width=1000,
#     height=700,
# )
# st.plotly_chart(fig)

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

# st.subheader("Playlist with Maximum Followers")
# st.write(f"Playlist Name: {max_followers_playlist['playlist_name']}")
# st.write(f"Number of Followers: {max_followers_playlist['playlist_followers_total']}")
#
# st.subheader("Playlist with Minimum Followers")
# st.write(f"Playlist Name: {min_followers_playlist['playlist_name']}")
# st.write(f"Number of Followers: {min_followers_playlist['playlist_followers_total']}")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("### 🏆 Playlist with Maximum Followers")
        st.write(f"🎶**Playlist Name:** {max_followers_playlist['playlist_name']}")
        st.write(f"👥**Number of Followers:** {max_followers_playlist['playlist_followers_total']:,}")

with col2:
    with st.container(border=True):
        st.markdown("### 🛑 Playlist with Minimum Followers")
        st.write(f"🎶**Playlist Name:** {min_followers_playlist['playlist_name']}")
        st.write(f"👥**Number of Followers:** {min_followers_playlist['playlist_followers_total']:,}")

st.divider()

# selected_countries = st.multiselect(
#     "Select Countries",
#     options=countries_for_map,
#     default=countries_for_map if select_all else []
# )

st.subheader('Number of Followers per Playlist')
select_all = st.checkbox("Select All", value=True)

with st.popover("Select countries for analysis", icon="🌍"):
    select_all = st.checkbox("Select All", value=True,
                             help="Check to select all countries. Uncheck to choose specific ones.")

    if select_all:
        selected_countries = countries_for_map
    else:
        selected_countries = st.multiselect(
            "Select Specific Countries",
            options=countries_for_map,
            default=[]
        )


followers_data = playlists_table[['country', 'playlist_followers_total']].drop_duplicates()
followers_data.columns = ['Country', 'Number of Followers']
followers_data = followers_data[followers_data['Country'].isin(selected_countries)]
followers_data = followers_data.sort_values(by='Number of Followers', ascending=False)
followers_data['Number of Followers (formatted)'] = data_processing.format_number_text(followers_data['Number of Followers'])

st.dataframe(followers_data)

# plots.create_bar_plot(
#     data=followers_data,
#     x='Country',
#     y='Number of Followers',
#     text='Number of Followers',
#     log_y=True
# )

plots.create_bubble_plot(
    data=followers_data,
    x='Country',
    y='Number of Followers',
    size='Number of Followers',
    text='Number of Followers (formatted)',
    log_y=True,
    hover_data={'Number of Followers (formatted)': False},
)



#
# fig_followers = px.bar(followers_data,
#                        x='Country',
#                        y='Number of Followers',
#                        # color="Country",
#                        # title='Number of Followers per Playlist',
#                        log_y=True)
# st.plotly_chart(fig_followers)

show_explanation = st.checkbox('Show explanation', value=False)

if show_explanation:
    st.info(
        """
        This chart displays the **Number of Followers per Playlist** for selected countries.

        **How to interpret:**
        - The x-axis represents the **countries**.
        - The y-axis (logarithmic scale) shows the **total number of followers** for playlists originating from each 
        country.
        - Countries with higher bars indicate playlists with larger followings, reflecting their popularity.

        **Logarithmic Scale:**
        - A logarithmic scale is used for the y-axis to better represent the data when there is a significant 
        difference between the highest and lowest values.
        - This helps visualize countries with smaller follower counts more effectively.

        **Filtering Options:**
        - Use the 'Select All' checkbox to choose all countries.
        - If you want to analyze specific countries, uncheck 'Select All' and use the dropdown to select 
        individual countries.

        **Purpose:**
        - This chart displays the number of followers for different countries and the Global playlist.
        """)

merged_playlists_tracks = pd.merge(
    playlists_table,
    tracks_table,
    on='track_id',
    how='left'
)

help_popularity = 'The value of popularity will be between 0 and 100, with 100 being the most popular'

st.subheader("Average Track Popularity Across Playlists", help=help_popularity)

avg_popularity = merged_playlists_tracks.groupby('country')['track_popularity'].mean().reset_index()
avg_popularity.columns = ['Country', 'Average Popularity']
avg_popularity = avg_popularity.sort_values(by='Average Popularity', ascending=False)
avg_popularity['Average Popularity (formatted)'] = avg_popularity['Average Popularity'].round(1)
min_y = avg_popularity['Average Popularity'].min() - 5
max_y = avg_popularity['Average Popularity'].max() + 5

plots.create_bar_plot(
    data=avg_popularity,
    x='Country',
    y='Average Popularity',
    text='Average Popularity (formatted)',
    range_y=[min_y, max_y],
    hover_data={'Average Popularity (formatted)': False},
)

# fig = px.bar(avg_popularity,
#              x='Country',
#              y='Average Popularity',
#              # title='Average Track Popularity Across Playlists',
#              range_y=[min_y, max_y])
#
# st.plotly_chart(fig)

fig = make_subplots(
    rows=1, cols=2,
    shared_yaxes=True,
    horizontal_spacing=0.02,
    column_widths=[0.94, 0.06],
)

fig.add_trace(
    go.Violin(
        x=merged_playlists_tracks['country'],
        y=merged_playlists_tracks['track_popularity'],
        # name=merged_playlists_tracks['country'],
        box=dict(visible=True),
        meanline=dict(visible=True),
        points="all",
    ),
    row=1, col=1
)

fig.add_trace(
    go.Violin(
        y=tracks_table['track_popularity'],
        name="Overall",
        box=dict(visible=True),
        meanline=dict(visible=True),
        points="all",
    ),
    row=1, col=2
)

fig.update_layout(
    height=700,
    showlegend=False,
    title_text="Distribution of Track Popularity by Country and Overall",
    yaxis=dict(title="Track Popularity"),
)
st.plotly_chart(fig)

fig = make_subplots(
    rows=1, cols=2,  # Один рядок, дві колонки
    shared_yaxes=True,  # Спільна вісь Y
    horizontal_spacing=0.02,  # Відстань між графіками
    column_widths=[0.94, 0.06],

)

fig.add_trace(
    go.Box(
        x=merged_playlists_tracks['country'],
        y=merged_playlists_tracks['track_popularity'],
    ),
    row=1, col=1
)

fig.add_trace(
    go.Box(
        y=tracks_table['track_popularity'],
        name="Overall",
    ),
    row=1, col=2
)

fig.update_layout(
    height=700,
    showlegend=False,
    title_text="Distribution of Track Popularity by Country and Overall",
    yaxis=dict(title="Track Popularity"),
)

st.plotly_chart(fig)

col1, col2 = st.columns([0.75, 0.25])

with col1:
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

with col2:
    fig_popularity_distribution = px.violin(
        tracks_table,
        y='track_popularity',
        title='Distribution of Track Popularity',
        labels={'track_popularity': 'Popularity'},
        box=True,  # Додаємо відображення коробчастого графіка (опціонально)
        points='all',  # Відображення всіх точок (опціонально)
        color_discrete_sequence=["#636EFA"],  # Колір для графіка
        height=700,
    )

    # Налаштування макета
    fig_popularity_distribution.update_layout(
        yaxis_title='Popularity',  # Підпис осі Y
        xaxis_title='',  # Видаляємо підпис осі X
        violingap=0,  # Відстань між скрипками (неактуально для одного графіка)
        violingroupgap=0.1  # Проміжок між групами
    )

    st.plotly_chart(fig_popularity_distribution)

st.subheader("Country-wise Track Popularity Analysis", help=help_popularity)

selected_country = st.selectbox("Select a Country", countries_for_map)
filtered_data = merged_playlists_tracks[merged_playlists_tracks['country'] == selected_country]

# st.write(f"Data for {selected_playlist}:")
# st.dataframe(filtered_data, height=210, hide_index=True)

mean_popularity = filtered_data['track_popularity'].mean()
median_popularity = filtered_data['track_popularity'].median()
std_popularity = filtered_data['track_popularity'].std()

# Shapiro-Wilk Test for normality
shapiro_stat, shapiro_p_value = shapiro(filtered_data['track_popularity'])
skewness = skew(filtered_data['track_popularity'])

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

# show_explanation = st.checkbox('Show explanation', value=False, key='histogram_explanation_checkbox')
#
# if show_explanation:
#     st.info(f"""
#         ### Interpretation of Results
#         - Percentage of data within 1 standard deviation: **{within_one_std_dev:.2f}%**"
#         - Percentage of data within 2 standard deviations: **{within_two_std_dev:.2f}%**"
#         - Percentage of data within 3 standard deviations: **{within_three_std_dev:.2f}%**"
#         If the percentage of data within 1, 2, and 3 standard deviations is approximately 68%, 95%,
#         and 99.7%, it suggests a normal distribution (Empirical Rule):
#
#         - **1 Std Dev (68%)**: About 68% of data falls within 1 standard deviation of the mean.
#         - **2 Std Dev (95%)**: Around 95% of data lies within 2 standard deviations.
#         - **3 Std Dev (99.7%)**: Nearly all data falls within 3 standard deviations.
#
#         Significant deviations may indicate skewness, outliers, or other anomalies:
#         - **Skewness**: Data may have a long tail if heavily skewed.
#         - **Outliers**: Extreme values far from the mean may indicate rare cases.
#
#         Shaded regions in the chart show these ranges, helping assess data normality and identify trends or anomalies.
#         """
#             )

# if show_explanation:
#     mean_median_difference = abs(mean_popularity - median_popularity)
#
#     normal_distribution_message = (
#         "It suggests a normal distribution (Empirical Rule):"
#         if mean_median_difference < 0.1 * mean_popularity
#         else "It may not follow a normal distribution due to significant difference between mean and median."
#     )
#
#     st.info(f"""
#         ### Interpretation of Results
#         - Percentage of data within 1 standard deviation: **{within_one_std_dev:.2f}%**
#         - Percentage of data within 2 standard deviations: **{within_two_std_dev:.2f}%**
#         - Percentage of data within 3 standard deviations: **{within_three_std_dev:.2f}%**
#
#         If the percentage of data within 1, 2, and 3 standard deviations is approximately 68%, 95%, and 99.7%, {normal_distribution_message}
#
#         - **1 Std Dev (68%)**: About 68% of data falls within 1 standard deviation of the mean.
#         - **2 Std Dev (95%)**: Around 95% of data lies within 2 standard deviations.
#         - **3 Std Dev (99.7%)**: Nearly all data falls within 3 standard deviations.
#
#         **Mean and Median Analysis:**
#         - **Mean**: {mean_popularity:.2f}
#         - **Median**: {median_popularity:.2f}
#         - Difference between mean and median: {mean_median_difference:.2f}
#
#         Significant deviations may indicate skewness, outliers, or other anomalies:
#         - **Skewness**: Data may have a long tail if heavily skewed.
#         - **Outliers**: Extreme values far from the mean may indicate rare cases.
#
#         Shaded regions in the chart show these ranges, helping assess data normality and identify trends or anomalies.
#     """)

show_explanation = st.checkbox('Show explanation', value=False, key='histogram_explanation_checkbox')

if show_explanation:
    if shapiro_p_value >= 0.05 and abs(skewness) <= 0.5:
        st.success("The data is approximately normally distributed. Proceeding with the Empirical Rule.")
        st.info(f"""
            ### Interpretation of Results
            - Percentage of data within 1 standard deviation: **{within_one_std_dev:.2f}%**
            - Percentage of data within 2 standard deviations: **{within_two_std_dev:.2f}%**
            - Percentage of data within 3 standard deviations: **{within_three_std_dev:.2f}%**

            **Empirical Rule**:
            - **68%** of data is within 1 standard deviation.
            - **95%** of data is within 2 standard deviations.
            - **99.7%** of data is within 3 standard deviations.
        """)
    else:
        st.warning("The data does not appear to follow a normal distribution. The Empirical Rule may not be applicable.")
        st.write("Consider transformations or alternative visualizations to assess the distribution.")

st.write('track_counts')

track_counts = playlists_table['track_id'].value_counts().reset_index()
st.dataframe(track_counts)

st.write('track_counts_sorted')
track_counts_sorted = track_counts.sort_values(by='count', ascending=False)
st.dataframe(track_counts_sorted)

st.write('top_track_counts_sorted')
top_track_counts_sorted = track_counts_sorted.head(10)
st.dataframe(top_track_counts_sorted)

st.write('track_data')
tracks_data = top_track_counts_sorted.merge(
    tracks_table[['track_id', 'track_name', 'track_popularity', 'track_explicit']],
    on='track_id',
    how='left'
)
st.dataframe(tracks_data)

st.write('tracks_artists')
tracks_artists = tracks_data.merge(
    playlists_table[['track_id', 'artist_id']],
    on='track_id',
    how='left'
)
st.dataframe(tracks_artists)

st.write('tracks_artists_cleaned')
tracks_artists_cleaned = tracks_artists.drop_duplicates(subset=['track_id'])
st.dataframe(tracks_artists_cleaned)

tracks_artists_cleaned.loc[:, 'artist_id'] = tracks_artists_cleaned['artist_id'].str.split(', ')
# tracks_artists_cleaned['artist_id'] = tracks_artists_cleaned['artist_id'].str.split(', ')
st.dataframe(tracks_artists_cleaned)

st.write('-expanded_tracks_artists---------')
expanded_tracks_artists = tracks_artists_cleaned.explode('artist_id')
st.dataframe(expanded_tracks_artists)

st.write('tracks_artists_name---------')
tracks_artists_name = expanded_tracks_artists.merge(
    artists_genres_full_unknown[['artist_id', 'artist_name']],
    on='artist_id',
    how='left'
)
st.dataframe(tracks_artists_name)

st.write('tracks_artists_grouped---------')
# Grouping the data by 'track_id' and aggregating values
tracks_artists_grouped = tracks_artists_name.groupby('track_id').agg({
    'track_name': 'first',   # Keep the first occurrence of the track name
    'artist_name': lambda x: ', '.join(x.dropna().unique()),  # Concatenate unique artist names, separated by commas
    'count': 'first',
    'track_popularity': 'first',
    'track_explicit': 'first'
}).reset_index()
st.dataframe(tracks_artists_grouped)

st.write('tracks_full---------')
tracks_full = tracks_artists_grouped[['track_name', 'artist_name', 'count', 'track_popularity', 'track_explicit']]
st.dataframe(tracks_full)

tracks_full.columns = ['Track Name', 'Artists', 'Frequency in Playlists', 'Popularity', 'Explicit']
st.dataframe(tracks_full)

# tracks_full = tracks_full.sort_values(by='Frequency in Playlists', ascending=False)


st.subheader("Top 10 Tracks by Frequency in Playlists")
tab1_tracks, tab2_tracks, tab3_tracks, tab4_tracks = st.tabs(["Frequency Distribution",
                                                              "Data Table", "Popularity Plot", "Map"])

with tab1_tracks:
    tracks_full = tracks_full.sort_values(by='Frequency in Playlists', ascending=True)
    plots.create_bar_plot(
        data=tracks_full,
        x='Frequency in Playlists',
        y='Track Name',
        orientation='h',
        text='Frequency in Playlists',
        hover_data={'Artists': True},

        # color='Frequency in Playlists',
    )
    # fig = px.bar(
    #     tracks_full,
    #     x='Frequency in Playlists',
    #     y='Track Name',
    #     orientation='h',
    #     # title='Top 10 Tracks by Frequency in Playlists',
    #     color='Frequency in Playlists',
    # )
    # st.plotly_chart(fig)

with tab2_tracks:
    # st.subheader("Data Table of Top 10 Tracks")
    tracks_full = tracks_full.sort_values(by='Frequency in Playlists', ascending=False)
    st.dataframe(tracks_full, hide_index=True)

with tab3_tracks:
    tracks_full = tracks_full.sort_values(by='Popularity', ascending=False)
    # tracks_full['Track Name'] = tracks_full['Track Name'].astype('category')
    # tracks_full['Track Name'] = tracks_full['Track Name'].cat.set_categories(tracks_full['Track Name'].unique())

    min_y_popularity_track = tracks_full['Popularity'].min() - 5
    max_y_popularity_track = tracks_full['Popularity'].max()

    plots.create_bar_plot(
        data=tracks_full,
        x='Track Name',
        y='Popularity',
        title='Popularity of Top 10 Tracks',
        labels={'Popularity': 'Track Popularity', 'Track Name': 'Track Name'},
        text='Popularity',
        # color='Popularity',
        range_y=[min_y_popularity_track, max_y_popularity_track],
        hover_data={'Artists': True},
    )

    # fig_popularity = px.bar(tracks_full,
    #                         x='Track Name',
    #                         y='Popularity',
    #                         title='Popularity of Top 10 Tracks',
    #                         labels={'Popularity': 'Track Popularity', 'Track Name': 'Track Name'},
    #                         color='Popularity',
    #                         range_y=[min_y_popularity_track, max_y_popularity_track],
    #                         )
    # fig_popularity.update_layout(xaxis={'categoryorder': 'total descending'})
    # st.plotly_chart(fig_popularity)

with tab4_tracks:
    selected_track = st.selectbox(
        "Select a Track",
        options=tracks_full['Track Name']
    )

    # Filter the data to include only rows for the selected track
    filtered_tracks = merged_playlists_tracks[merged_playlists_tracks['track_name'] == selected_track]

    # Extract the unique list of countries where the track is present
    track_countries = filtered_tracks['country'].unique()

    # Filter the country coordinates table to include only countries from the track_countries list
    filtered_countries = country_coords_df[country_coords_df['country'].isin(track_countries)]
    artists_for_selected_track = tracks_full.loc[
        tracks_full["Track Name"] == selected_track, "Artists"
    ].iloc[0]

    plots.create_choropleth_map(
        data=filtered_countries,
        locations='country',
        location_mode='country names',
        color='country',
        color_discrete_map=color_map,
        hover_name='country',
        title=f'Countries with Playlists Containing "{selected_track}" ({artists_for_selected_track})',
        legend_title='Country',
        hover_data={'country': False},

    )
    # fig_map = px.choropleth(
    #     filtered_countries,
    #     locations='country',
    #     locationmode='country names',
    #     color='country',
    #     color_discrete_map=color_map,
    #     hover_name='country',
    #     title=f'Countries with Playlists Containing "{selected_track}"'
    # )
    #
    # fig_map.update_layout(
    #     legend_title_text='Country',
    #     legend=dict(
    #         y=0.5,
    #     ),
    #     width=1200,
    #     height=600,
    # )
    # st.plotly_chart(fig_map)

st.subheader("Top 10 Artists by Frequency in Playlists")

st.write('playlists_table---------')
# Split the 'artist_id' column values (which are strings of comma-separated IDs) into lists of IDs
playlists_table['artist_id'] = playlists_table['artist_id'].str.split(', ')
st.dataframe(playlists_table)

st.write('-expanded_playlists_artists---------')
# Expand the playlists table so that each artist in the 'artist_id' list gets its own row
expanded_playlists_artists = playlists_table.explode('artist_id')
st.dataframe(expanded_playlists_artists)

st.write('-artist_per_playlist---------')
# Group by country and artist_id to count how often each artist appears in playlists for each country
artist_per_playlist = (
    expanded_playlists_artists
    .groupby('country')['artist_id']
    .value_counts()
    .reset_index()
)
st.dataframe(artist_per_playlist)


st.write('-artist_counts---------')
artist_counts = expanded_playlists_artists['artist_id'].value_counts().reset_index()
st.dataframe(artist_counts)

st.write('artist_counts_sorted')
artist_counts_sorted = artist_counts.sort_values(by='count', ascending=False)
st.dataframe(artist_counts_sorted)

st.write('top_10_artists-----------------')
top_10_artists = artist_counts_sorted.head(10)
st.dataframe(top_10_artists)

st.write('top_10_artists_full-----------------')
top_10_artists_full = top_10_artists.merge(
    artists_genres_full_unknown[['artist_id', 'artist_name', 'artist_followers', 'artist_popularity', 'artist_genres']],
    on='artist_id',
    how='left'
)
st.dataframe(top_10_artists_full)

st.write('top_10_artists_full-2---------------')
top_10_artists_full = top_10_artists_full[
    ['artist_name', 'count', 'artist_followers', 'artist_popularity', 'artist_genres']
]
st.dataframe(top_10_artists_full)

st.write(' renamed columns top_10_artists_full-----------------')
top_10_artists_full.columns = ['Artist', 'Number of songs in playlists',  'Followers', 'Popularity', 'Genres']
st.dataframe(top_10_artists_full)

tab1_artists, tab2_artists, tab3_artists, tab4_artists = st.tabs(["Frequency Distribution", "Data Table",
                                                                  "Popularity Plot", "Map"])

with tab1_artists:
    top_10_artists_full = top_10_artists_full.sort_values(by='Number of songs in playlists', ascending=True)
    plots.create_bar_plot(
        data=top_10_artists_full,
        x='Number of songs in playlists',
        y='Artist',
        orientation='h',
        title='Top 10 Artists by Frequency in Playlists',
        # color='Frequency in Playlists',
        text='Number of songs in playlists',
        )

    # fig = px.bar(top_10_artists_full,
    #              x='Frequency in Playlists',
    #              y='Artist',
    #              orientation='h',
    #              title='Top 10 Artists by Frequency in Playlists',
    #              color='Frequency in Playlists',
    #              text='Frequency in Playlists',
    #              )
    # fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    # fig.update_traces(textposition='outside')
    # st.plotly_chart(fig)

with tab2_artists:
    st.dataframe(top_10_artists_full, hide_index=True)

with tab3_artists:
    top_10_artists_full = top_10_artists_full.sort_values(by='Popularity', ascending=False)
    min_y_popularity_art = top_10_artists_full['Popularity'].min()-5
    max_y_popularity_art = top_10_artists_full['Popularity'].max()+3

    plots.create_bar_plot(
        data=top_10_artists_full,
        x='Artist',
        y='Popularity',
        title='Popularity of Top 10 Artists',
        # color='Popularity',
        range_y=[min_y_popularity_art, max_y_popularity_art],
        text='Popularity',
    )
    # fig_popularity = px.bar(top_10_artists_full,
    #                         x='Artist',
    #                         y='Popularity',
    #                         title='Popularity of Top 10 Artists',
    #                         color='Popularity',
    #                         range_y=[min_y_popularity_art, max_y_popularity_art],
    #                         text='Popularity',
    #                         )
    # fig_popularity.update_layout(xaxis={'categoryorder': 'total descending'})
    # fig_popularity.update_traces(textposition='outside')
    # st.plotly_chart(fig_popularity)

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

    col1, col2 = st.columns([0.75, 0.25], vertical_alignment="center")
    with col1:
        plots.create_choropleth_map(
                data=artist_country_map_data,
                locations='country',
                location_mode='country names',
                color='count',
                color_continuous_scale='speed',
                hover_name='country',
                title=f'Playlists Containing "{selected_artist}"',
                labels={'count': 'Songs in playlist'},
                hover_data={'country': False},
            )

        #     fig_map = px.choropleth(
        #     artist_country_map_data,
        #     locations='country',
        #     locationmode='country names',
        #     color='count',
        #     color_continuous_scale='speed',
        #     hover_name='country',
        #     title=f'Countries with Playlists Containing "{selected_artist}"',
        #     labels={'count': 'Frequency'},
        # )
        #
        # fig_map.update_layout(
        #     legend_title_text='Frequency',
        #     legend=dict(
        #         y=0.5,
        #     ),
        #     width=1000,
        #     height=600,
        # )

        # st.plotly_chart(fig_map)

    with col2:
        countries_list = ', '.join(filtered_artist_data['country'].tolist())
        st.write("**Countries where the artist is present:**")

        filtered_artist_data_map = filtered_artist_data[['country', 'count']].sort_values(['count'], ascending=False)
        filtered_artist_data_map.columns = ['Country', 'Number of songs in playlist']

        st.dataframe(filtered_artist_data_map, hide_index=True)


