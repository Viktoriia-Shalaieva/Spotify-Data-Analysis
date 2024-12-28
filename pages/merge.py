# albums
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

# artists
expanded_artists_genres = expanded_artists_genres.merge(
    playlists_table[['Artist ID', 'Country']],
    on='Artist ID',
    how='left'
)

# playlists
merged_playlists_tracks = pd.merge(
    playlists_table,
    tracks_table,
    on='Track ID',
    how='left'
)

tracks_data = top_track_counts_sorted.merge(
    tracks_table[['Track ID', 'Track Name', 'Track Popularity', 'Explicit Content']],
    on='Track ID',
    how='left'
)
tracks_artists = tracks_data.merge(
    playlists_table[['Track ID', 'Artist ID']],
    on='Track ID',
    how='left'
)
tracks_artists_cleaned = tracks_artists.drop_duplicates(subset=['Track ID'])

tracks_artists_cleaned.loc[:, 'Artist ID'] = tracks_artists_cleaned['Artist ID'].str.split(', ')

expanded_tracks_artists = tracks_artists_cleaned.explode('Artist ID')

tracks_artists_name = expanded_tracks_artists.merge(
    artists_table[['Artist ID', 'Artist Name']],
    on='Artist ID',
    how='left'
)

tracks_artists_grouped = tracks_artists_name.groupby('Track ID').agg({
    'Track Name': 'first',   # Keep the first occurrence of the track name
    'Artist Name': lambda x: ', '.join(x.dropna().unique()),  # Concatenate unique artist names, separated by commas
    'count': 'first',
    'Track Popularity': 'first',
    'Explicit Content': 'first'
}).reset_index()

top_10_artists_full = top_10_artists.merge(
    artists_table[['Artist ID', 'Artist Name', 'Artist Total Followers', 'Artist Popularity', 'Artist Genres']],
    on='Artist ID',
    how='left'
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
playlists_table['Artist ID'] = playlists_table['Artist ID'].str.split(', ')

# tracks
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
