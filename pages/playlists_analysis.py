import os
import yaml
import pandas as pd
import plotly.express as px
import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from scipy.stats import shapiro, skew
from streamlit_utils import plots, layouts, data_processing


layouts.set_page_layout()
st.sidebar.markdown("# **Playlists Analysis** 📋️ ")

layouts.set_page_header("Playlists Analysis", "📋️")

data = data_processing.load_and_process_data('config/path_config.yaml')

playlists_table = data["playlists"]
artists_table = data["artists"]
tracks_table = data["tracks"]

country_coords_df = data_processing.load_country_coords('config/country_coords.yaml')

st.subheader("Map of Countries for Playlist Analysis")

plots.create_choropleth_map(
    data=country_coords_df,
    locations='Country',
    location_mode='country names',
    color='Country',
    color_discrete_sequence=px.colors.qualitative.Light24,
    hover_name='Country',
    legend_title='Country',
)

countries_for_map = playlists_table['Country'].unique()

max_followers_playlist = playlists_table.sort_values(by='Playlist Total Followers', ascending=False).iloc[0]
min_followers_playlist = playlists_table.sort_values(by='Playlist Total Followers').iloc[0]

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("### 🏆 Playlist with Maximum Followers")
        st.write(f"🎶**Playlist Name:** {max_followers_playlist['Playlist Name']}")
        st.write(f"👥**Number of Followers:** {max_followers_playlist['Playlist Total Followers']:,}")

with col2:
    with st.container(border=True):
        st.markdown("### 🛑 Playlist with Minimum Followers")
        st.write(f"🎶**Playlist Name:** {min_followers_playlist['Playlist Name']}")
        st.write(f"👥**Number of Followers:** {min_followers_playlist['Playlist Total Followers']:,}")

st.divider()

st.subheader('Number of Followers per Playlist')
select_all = st.checkbox("Select All", value=True)

with st.popover("Select countries for analysis", icon="🌍"):
    select_all_countries = st.checkbox("Select All", value=True,
                                       help="Check to select all countries. Uncheck to choose specific ones.")

    if select_all_countries:
        selected_countries = countries_for_map
    else:
        selected_countries = st.multiselect(
            "Select Specific Countries",
            options=countries_for_map,
            default=[]
        )

followers_data = playlists_table[['Country', 'Playlist Total Followers']].drop_duplicates()
followers_data = followers_data[followers_data['Country'].isin(selected_countries)]
followers_data = followers_data.sort_values(by='Playlist Total Followers', ascending=False)
followers_data['Playlist Total Followers (formatted)'] = (
    plots.format_number_text(followers_data['Playlist Total Followers'])
)

plots.create_bubble_plot(
    data=followers_data,
    x='Country',
    y='Playlist Total Followers',
    size='Playlist Total Followers',
    text='Playlist Total Followers (formatted)',
    log_y=True,
    hover_data={'Playlist Total Followers (formatted)': False},
    yaxis_title="Total Followers (log scale)",
)

merged_playlists_tracks = pd.merge(
    playlists_table,
    tracks_table,
    on='Track ID',
    how='left'
)

help_popularity = 'The value of popularity will be between 0 and 100, with 100 being the most popular'

median_popularity = (
    merged_playlists_tracks
    .groupby('Country')['Track Popularity']
    .median()
)
median_popularity_df = median_popularity.reset_index()

median_popularity_df.columns = ['Country', 'Median Popularity']

median_popularity_df = median_popularity_df.sort_values(by='Median Popularity', ascending=False)

sorted_countries = median_popularity_df['Country'].tolist()

st.subheader('Distribution of Track Popularity by Country and Overall (Sorted by Median, Descending Order)',
             help=help_popularity)

plots.create_boxplot_subplots(
    x=merged_playlists_tracks['Country'],
    y=merged_playlists_tracks['Track Popularity'],
    y2=tracks_table['Track Popularity'],
    title="Track Popularity",
    categoryarray=sorted_countries
)

st.subheader("Country-wise Track Popularity Analysis", help=help_popularity)

selected_country = st.selectbox("Select a Country", countries_for_map)
filtered_data = merged_playlists_tracks[merged_playlists_tracks['Country'] == selected_country]

# Shapiro-Wilk Test for normality
shapiro_stat, shapiro_p_value = shapiro(filtered_data['Track Popularity'])
skewness = skew(filtered_data['Track Popularity'])

popularity_stats, std_ranges, perc_within_std = data_processing.calculate_std_dev_ranges_and_percentages(
    filtered_data['Track Popularity']
)

if shapiro_p_value >= 0.05 and abs(skewness) <= 0.5:
    st.success("The data is approximately normally distributed. Building a histogram with standard deviations.")
    plots.create_histogram_normal_distribution(
        data=filtered_data,
        x='Track Popularity',
        country=selected_country,
        mean=popularity_stats['mean'],
        median=popularity_stats['median'],
        one_std_dev=std_ranges['1_std'],
        two_std_dev=std_ranges['2_std'],
        three_std_dev=std_ranges['3_std'],
    )

else:
    st.warning("The data is not normally distributed. Building a standard histogram.")
    plots.create_histogram(
        data=filtered_data,
        x='Track Popularity',
        title=f"Track Popularity Distribution in Top 50 - {selected_country}",
    )

show_explanation = st.checkbox('Show more details', value=False)

if show_explanation:
    if shapiro_p_value >= 0.05 and abs(skewness) <= 0.5:
        st.success("The data is approximately normally distributed. Proceeding with the Empirical Rule.")
        st.info(f"""
            ### Statistical Analysis of Track Popularity
            
            - **Shapiro-Wilk Test for Normality**:
              - **Test Statistic (W)**: {shapiro_stat:.4f}
                - Values close to **1** indicate that the data closely follows a normal distribution.
                - Values close to **0** suggest significant deviations from normality.
                
              - **p-value**: {shapiro_p_value:.4f}
                - A p-value ≥ 0.05 implies that the data does not significantly deviate from a normal distribution.

            - **Skewness**: **{skewness:.2f}**  
              - Skewness close to 0 (between -0.5 and 0.5) indicates symmetric data.  
              - Positive skewness (> 0.5): Data is right-skewed.  
              - Negative skewness (< -0.5): Data is left-skewed.

            - **Descriptive Statistics**:  
              - Mean: **{popularity_stats['mean']:.2f}**  
              - Median: **{popularity_stats['median']:.2f}**  
              - Standard Deviation: **{popularity_stats['std']:.2f}**  

            ### Empirical Rule Interpretation
            For normally distributed data, the Empirical Rule applies:
            - **68%** of the data falls within 1 standard deviation from the mean.
            - **95%** of the data falls within 2 standard deviations from the mean.
            - **99.7%** of the data falls within 3 standard deviations from the mean.

            #### Data Distribution:
            - Percentage of data within **1 standard deviation**: **{perc_within_std['within_1_std']:.2f}%**  
            - Percentage of data within **2 standard deviations**: **{perc_within_std['within_2_std']:.2f}%**  
            - Percentage of data within **3 standard deviations**: **{perc_within_std['within_3_std']:.2f}%**

            The percentages closely match the Empirical Rule, indicating a strong approximation to a normal 
            distribution.
        """)
    else:
        st.warning("The data does not appear to follow a normal distribution.")
        st.info(f"""
            ### Statistical Analysis of Track Popularity
            - **Shapiro-Wilk Test for Normality**:
              - **Test Statistic (W)**: {shapiro_stat:.4f}
                - Values close to **1** indicate that the data closely follows a normal distribution.
                - Values close to **0** suggest significant deviations from normality.
                
              - **p-value**: {shapiro_p_value:.4f}
                - A p-value < 0.05 indicates significant deviation from normality.

            - **Skewness**: **{skewness:.2f}**  
              - Positive skewness (> 0.5): Data is right-skewed.  
              - Negative skewness (< -0.5): Data is left-skewed.

            - **Descriptive Statistics**:  
              - Mean: **{popularity_stats['mean']:.2f}**  
              - Median: **{popularity_stats['median']:.2f}**  
              - Standard Deviation: **{popularity_stats['std']:.2f}**  
        """)
#
# track_counts = playlists_table['Track ID'].value_counts().reset_index()
#
# # track_counts_sorted = track_counts.sort_values(by='count', ascending=False)
# # top_track_counts_sorted = track_counts_sorted.head(10)
#
# top_track_counts_sorted = track_counts.nlargest(n=10, columns='count')
#
# tracks_data = top_track_counts_sorted.merge(
#     tracks_table[['Track ID', 'Track Name', 'Track Popularity', 'Explicit Content']],
#     on='Track ID',
#     how='left'
# )
# tracks_artists = tracks_data.merge(
#     playlists_table[['Track ID', 'Artist ID']],
#     on='Track ID',
#     how='left'
# )
# tracks_artists_cleaned = tracks_artists.drop_duplicates(subset=['Track ID'])
#
# tracks_artists_cleaned.loc[:, 'Artist ID'] = tracks_artists_cleaned['Artist ID'].str.split(', ')
#
# expanded_tracks_artists = tracks_artists_cleaned.explode('Artist ID')
#
# tracks_artists_name = expanded_tracks_artists.merge(
#     artists_table[['Artist ID', 'Artist Name']],
#     on='Artist ID',
#     how='left'
# )
#
# # Grouping the data by 'track_id' and aggregating values
# tracks_artists_grouped = tracks_artists_name.groupby('Track ID').agg({
#     'Track Name': 'first',   # Keep the first occurrence of the track name
#     'Artist Name': lambda x: ', '.join(x.dropna().unique()),  # Concatenate unique artist names, separated by commas
#     'count': 'first',
#     'Track Popularity': 'first',
#     'Explicit Content': 'first'
# }).reset_index()
#
# tracks_full = tracks_artists_grouped[['Track Name', 'Artist Name', 'count', 'Track Popularity', 'Explicit Content']]
#
# tracks_full.columns = ['Track Name', 'Artists', 'Frequency in Playlists', 'Popularity', 'Explicit']

top_10_tracks = data_processing.prepare_top_tracks_data(playlists_table, tracks_table, artists_table)

st.subheader("Top 10 Tracks by Frequency in Playlists")
tab1_tracks, tab2_tracks, tab3_tracks, tab4_tracks = st.tabs(["Frequency Distribution",
                                                              "Data Table", "Popularity Plot", "Map"])

with tab1_tracks:
    tracks_full_sorted_asc = top_10_tracks.sort_values(by='Frequency in Playlists', ascending=True)
    plots.create_bar_plot(
        data=tracks_full_sorted_asc,
        x='Frequency in Playlists',
        y='Track Name',
        orientation='h',
        text='Frequency in Playlists',
        hover_data={'Artists': True},
    )
with tab2_tracks:
    tracks_full_sorted_desc = top_10_tracks.sort_values(by='Frequency in Playlists', ascending=False)
    st.dataframe(tracks_full_sorted_desc, width=680, hide_index=True)

with tab3_tracks:
    tracks_popularity = top_10_tracks.sort_values(by='Popularity', ascending=False)
    min_y_popularity_track = tracks_popularity['Popularity'].min() - 5
    max_y_popularity_track = tracks_popularity['Popularity'].max()
    plots.create_bar_plot(
        data=tracks_popularity,
        x='Track Name',
        y='Popularity',
        title='Popularity of Top 10 Tracks',
        text='Popularity',
        range_y=[min_y_popularity_track, max_y_popularity_track],
        hover_data={'Artists': True},
        showticklabels=True,
    )
with tab4_tracks:
    selected_track = st.selectbox(
        "Select a Track",
        options=top_10_tracks['Track Name']
    )
    # Filter the data to include only rows for the selected track
    filtered_tracks = merged_playlists_tracks[merged_playlists_tracks['Track Name'] == selected_track]

    filtered_countries = country_coords_df[country_coords_df['Country'].isin(filtered_tracks['Country'])]

    artists_for_selected_track = top_10_tracks.loc[
        top_10_tracks["Track Name"] == selected_track, "Artists"
    ].iloc[0]

    plots.create_choropleth_map(
        data=filtered_countries,
        locations='Country',
        location_mode='country names',
        color='Country',
        color_discrete_sequence=px.colors.qualitative.Light24,
        hover_name='Country',
        title=f'Countries with Playlists Containing "{selected_track}" ({artists_for_selected_track})',
        legend_title='Country',
    )

st.subheader("Top 10 Artists by Frequency in Playlists")

playlists_table['Artist ID'] = playlists_table['Artist ID'].str.split(', ')

# Expand the playlists table so that each artist in the 'artist_id' list gets its own row
expanded_playlists_artists = playlists_table.explode('Artist ID')

# Group by country and artist_id to count how often each artist appears in playlists for each country
artist_per_playlist = (
    expanded_playlists_artists
    .groupby('Country')['Artist ID']
    .value_counts()
    .reset_index()
)

artist_counts = expanded_playlists_artists['Artist ID'].value_counts().reset_index()

# artist_counts_sorted = artist_counts.sort_values(by='count', ascending=False)
# top_10_artists = artist_counts_sorted.head(10)

top_10_artists = artist_counts.nlargest(n=10, columns='count')

top_10_artists_full = top_10_artists.merge(
    artists_table[['Artist ID', 'Artist Name', 'Artist Total Followers', 'Artist Popularity', 'Artist Genres']],
    on='Artist ID',
    how='left'
)

top_10_artists_full = top_10_artists_full[
    ['Artist Name', 'count', 'Artist Total Followers', 'Artist Popularity', 'Artist Genres']
]

top_10_artists_full.columns = ['Artist Name', 'Number of songs in playlists',
                               'Followers', 'Artist Popularity', 'Artist Genres']

# top_10_artists_full['Artist Genres'] = top_10_artists_full['Artist Genres'].str.split(', ')
#
# expanded_artists_genres = top_10_artists_full.explode('Artist Genres')
#
# # r"[\"\'\[\]]": Regular expression to match the characters.
# # regex=True : Indicates using a regular expression for matching.
# expanded_artists_genres['Artist Genres'] = (expanded_artists_genres['Artist Genres']
#                                             .str.replace(r"[\"\'\[\]]", '', regex=True))
#
# expanded_artists_genres['Artist Genres'] = expanded_artists_genres['Artist Genres'].str.lower()
#
#
# # Update classification logic based on the provided detailed genre structure
# def classify_genres_detailed_structure(genre):
#     for parent_genre, subgenres in all_genres_with_subgenres.items():
#         if genre in subgenres:
#             return parent_genre
#     return 'Other'
#
#
# expanded_artists_genres['Artist Genres'] = (expanded_artists_genres['Artist Genres']
#                                             .str.replace(r'&\s*country', 'country', regex=True))
# expanded_artists_genres['Parent Genre'] = (expanded_artists_genres['Artist Genres']
#                                            .apply(classify_genres_detailed_structure))


expanded_artists_genres = data_processing.expand_and_classify_artists_genres(top_10_artists_full)

# Grouping the data by 'Artist Name' and aggregating values
top_10_artists_grouped = expanded_artists_genres.groupby('Artist Name').agg({
    'Number of songs in playlists': 'first',
    'Followers': 'first',
    'Artist Popularity': 'first',
    'Parent Genre': lambda x: ', '.join(x.dropna().unique()),  # Concatenate genres, separated by commas
}).reset_index(drop=False)

tab1_artists, tab2_artists, tab3_artists, tab4_artists = st.tabs(["Frequency Distribution", "Data Table",
                                                                  "Popularity Plot", "Map"])

with tab1_artists:
    top_10_artists_full = top_10_artists_full.sort_values(by='Number of songs in playlists', ascending=True)
    plots.create_bar_plot(
        data=top_10_artists_full,
        x='Number of songs in playlists',
        y='Artist Name',
        orientation='h',
        title='Top 10 Artists by Frequency in Playlists',
        text='Number of songs in playlists',
        )

with tab2_artists:
    top_10_artists_grouped = top_10_artists_grouped.sort_values(by='Number of songs in playlists', ascending=False)
    st.dataframe(top_10_artists_grouped, width=680, hide_index=True)

with tab3_artists:
    top_10_artists_full = top_10_artists_full.sort_values(by='Artist Popularity', ascending=False)
    min_y_popularity_art = top_10_artists_full['Artist Popularity'].min()-5
    max_y_popularity_art = top_10_artists_full['Artist Popularity'].max()+3

    plots.create_bar_plot(
        data=top_10_artists_full,
        x='Artist Name',
        y='Artist Popularity',
        title='Popularity of Top 10 Artists',
        range_y=[min_y_popularity_art, max_y_popularity_art],
        text='Artist Popularity',
        showticklabels=True
    )

with tab4_artists:
    selected_artist = st.selectbox(
        "Select an Artist",
        options=top_10_artists_full['Artist Name']
    )
    artist_data = artist_per_playlist.merge(
        artists_table[['Artist ID', 'Artist Name']],
        on='Artist ID',
        how='left'
    )
    filtered_artist_data = artist_data[artist_data['Artist Name'] == selected_artist]
    artist_country_map_data = filtered_artist_data.merge(
        country_coords_df,
        on='Country',
        how='left'
    )
    col1, col2 = st.columns([0.75, 0.25], vertical_alignment="center")
    with col1:
        plots.create_choropleth_map(
                data=artist_country_map_data,
                locations='Country',
                location_mode='country names',
                color='count',
                color_continuous_scale='Turbo',
                hover_name='Country',
                title=f'Playlists Containing "{selected_artist}"',
                labels={'count': 'Songs in playlist'},
            )
    with col2:
        countries_list = ', '.join(filtered_artist_data['Country'].tolist())
        st.write("**Countries where the artist is present:**")

        filtered_artist_data_map = filtered_artist_data[['Country', 'count']].sort_values(['count'], ascending=False)
        filtered_artist_data_map.columns = ['Country', 'Number of songs in playlist']

        st.dataframe(filtered_artist_data_map, hide_index=True)
