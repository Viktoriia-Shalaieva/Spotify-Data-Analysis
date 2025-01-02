import os
import yaml
import pandas as pd
from logs.logger_config import logger
from source import utils
from source.api import secrets_functions, spotify
from source.preprocessing import data_prep
from source.web_scraping import chosic
import random
from source.preprocessing import data_prep


pd.set_option('display.max_columns', None)
# Get configs
config = utils.load_config('config/config.yaml')
path_config = utils.load_config('config/path_config.yaml')

# Handle paths
data_dir = path_config['data_dir'][0]
raw_dir = path_config['raw_dir'][0]
genres_dir = path_config['genres_dir'][0]
file_paths = {file_name: os.path.join(data_dir, file_name) for file_name in path_config['files_names']}

artists_path = str(file_paths['artists.csv'])
artists_genres_discogs_path = str(file_paths['artists_genres_discogs.csv'])
artists_genres_full_unknown_path = str(file_paths['artists_genres_full_unknown.csv'])
tracks_path = str(file_paths['tracks.csv'])
artists_full_path = str(file_paths['artists_full.csv'])

artists_df = pd.read_csv(artists_path, sep='~')

print(artists_df)
artists_genres_discogs = pd.read_csv(artists_genres_discogs_path, sep='~')

artists = artists_df.merge(artists_genres_discogs, on='artist_name', how='left')

# Fill missing values in the 'artist_genres' column with corresponding values from the 'artist_genre' column.
artists['artist_genres'] = artists['artist_genres'].fillna(artists['artist_genre'])
artists = artists.drop(columns=['artist_genre'])

artists = data_prep.process_artist_genres(
    artists_df=artists,
    path=artists_full_path,
    save=True
)
# artists['artist_genres'] = artists_df['artist_genres'].replace('[]', pd.NA)
#
# artists['artist_genres'] = artists['artist_genres'].str.strip("[]").str.replace("'", "")
#
# genre_counts = artists['artist_genres'].str.split(', ').explode().value_counts()
# genres_list = genre_counts.index.tolist()
# weights = genre_counts.tolist()
#
# known_genres_table = artists[~pd.isna(artists['artist_genres'])]
#
# unknown_indices = artists[artists['artist_genres'].isna()].index
#
# # Generate random genres using the weights
# random_genres = random.choices(
#     population=genres_list,
#     weights=weights,
#     k=len(unknown_indices)
# )
#
# artists.loc[unknown_indices, 'artist_genres'] = random_genres
#
#
# artists.to_csv(artists_full_path, index=False, sep="~")

print(artists)
