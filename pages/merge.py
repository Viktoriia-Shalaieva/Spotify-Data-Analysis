top_10_albums_by_popularity = (
    albums_table.nlargest(n=10, columns='Album Popularity')
    )

merged_playlists_albums = pd.merge(
    top_10_albums_by_popularity,
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

top_10_albums_artists_grouped = albums_artists_name.groupby('Album ID').agg({
    'Album Name': 'first',   # Keep the first occurrence of the track name
    'Artist Name': lambda x: ', '.join(x.dropna().unique()),  # Concatenate unique artist names, separated by commas
    'Album Popularity': 'first',
}).reset_index()

top_10_albums_artists_sorted = top_10_albums_artists_grouped.sort_values(by='Album Popularity', ascending=True)

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

albums_table['release_year'] = albums_table['Release Date'].dt.year

yearly_releases = albums_table['release_year'].value_counts().sort_index().reset_index()
yearly_releases.columns = ['Release Year', 'Release Count']


