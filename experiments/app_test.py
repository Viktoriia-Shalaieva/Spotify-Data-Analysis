
from pprint import pprint
import json
import pandas as pd
from experiments import api_calls_test

import yaml
import os

pd.set_option('display.max_columns', None)


token = api_calls_test.get_spotify_access_token()
print(token)

print('--------------------Marilyn Manson')
marilyn_manson_id = '2VYQTNDsvvKN9wmU5W7xpj'
artist_json_manson = api_calls_test.get_artist(marilyn_manson_id, token)
pprint(artist_json_manson)
#
# print('--------------------track SAY10 Marilyn Manson')
# mm_say10_id = '3sxNhARfL8uj7NlMqwF61p'
# track_json_mm_say10 = api_calls_test.get_track(mm_say10_id, token)
# pprint(track_json_mm_say10)
#
# print('--------------------track KILL4ME Marilyn Manson')
# mm_kill4me_id = '6UIo6YbaXihIZ72MWUpcGb'
# market = 'UA'
# track_json_mm_say10 = api_calls_test.get_track_market(mm_kill4me_id, market, token)
# pprint(track_json_mm_say10)
# #
# print('--------------------album WE ARE CHAOS Marilyn Manson')
# mm_we_are_chaos_id = '3VOlp4Dion1qjjvhmuDZvV'
# album_json_mm_we_are_chaos_id = api_calls.get_album(mm_we_are_chaos_id, token)
# pprint(album_json_mm_we_are_chaos_id)
#
# print('--------------------Available Genre Seeds')
# genre_seeds = api_calls.get_genre_recom(token)
# pprint(genre_seeds)
#
# print('--------------------Tracks')
# more_tracks = api_calls.get_more_tracks(token)
# pprint(more_tracks)
#
# print('--------------------Tracks_MARKET')
# more_tracks_market = api_calls.get_more_tracks_market(token, 'UA')
# pprint(more_tracks_market)
#
# print('--------------------OLD Recommendations')
# old_artist_id = '2VYQTNDsvvKN9wmU5W7xpj'
# old_genre = 'rock'
# old_track = '3sxNhARfL8uj7NlMqwF61p'
# old_recommendations = api_calls_test.get_recommendations_old(token, old_artist_id, old_genre, old_track)
# pprint(old_recommendations)
# #
# # print('--------------------Recommendations')
# # artist_id = '2VYQTNDsvvKN9wmU5W7xpj'
# # genre = 'hard rock'
# # track = '3sxNhARfL8uj7NlMqwF61p'
# # recommendations = api_calls.get_recommendations(token, artist_id, genre, track)
# # pprint(recommendations)
# #
# print('--------------------50 ARTISTS')
# artists_50 = api_calls_test.get_50_artists(token)
# pprint(artists_50)
# #
#
#
# # Discogs
# print('--------------------Discogs')
# discogs_api_token = 'EaALIPVnUVkCSfqeUhhWzcdXZfgXNvERIHfabBFh'
#
# # print('--------------------Discogs track The Emptiness Machine Linkin Park')
# track_title_lp = 'The Emptiness Machine'
# artist_name_lp = 'Linkin Park'
# track_release_lp = api_calls.get_track_discogs(discogs_api_token, track_title_lp, artist_name_lp)
# pprint(track_release_lp)
#
# print('--------------------Discogs genre The Emptiness Machine Linkin Park')
# genre = api_calls.get_genre(discogs_api_token, track_title_lp, artist_name_lp)
# pprint(genre)
#
# print('--------------------Discogs genre Театр Klavdia Petrivna')
# track_title_kp = 'Театр'
# artist_name_kp = 'Klavdia Petrivna'
# genre_kp = api_calls.get_genre(discogs_api_token, track_title_kp, artist_name_kp)
# pprint(genre_kp)
#
#
# print('--------------------Discogs track_discogs Барабан Klavdia Petrivna Артём Пивоваров')
# track_title_ap_ = 'Барабан'
# artist_name_ap_ = 'Klavdia Petrivna', 'Артём Пивоваров'
# genre_ap_ = api_calls.get_track_discogs(discogs_api_token, track_title_ap_, artist_name_ap_)
# pprint(genre_ap_)
#
# print('--------------------Discogs track_discogs Барабан Klavdia Petrivna Artem Pivovarov')
# track_title_ap_ = 'Барабан'
# artist_name_ap_ = 'Klavdia Petrivna', 'Artem Pivovarov'
# genre_ap_ = api_calls.get_track_discogs(discogs_api_token, track_title_ap_, artist_name_ap_)
# pprint(genre_ap_)
#
# print('--------------------Discogs track_discogs Барабан Klavdia Petrivna Artem Pivovarov + album')
# track_title_ap_ = 'Барабан'
# artist_name_ap_ = 'Klavdia Petrivna', 'Artem Pivovarov'
# album_ap_ = 'THE BEST'
# genre_ap_ = api_calls.get_track_discogs_album(discogs_api_token, track_title_ap_, artist_name_ap_, album_ap_)
# pprint(genre_ap_)
#
# print('--------------------Discogs genre Барабан Klavdia Petrivna')
# track_title_ap = 'Барабан'
# artist_name_ap = 'Klavdia Petrivna'
# genre_ap = api_calls.get_genre(discogs_api_token, track_title_ap, artist_name_ap)
# pprint(genre_ap)
#
# print('--------------------Discogs  track Барабан Klavdia Petrivna')
# track_title_ap = 'Барабан'
# artist_name_ap = 'Klavdia Petrivna'
# genre_ap = api_calls.get_track_discogs(discogs_api_token, track_title_ap, artist_name_ap)
# pprint(genre_ap)
#
# print('--------------------Discogs genre KEEP UP Odetari')
# track_title_o = 'KEEP UP'
# artist_name_o = 'Odetari'
# genre_o = api_calls.get_genre(discogs_api_token, track_title_o, artist_name_o)
# pprint(genre_o)
#
# print('--------------------SAY10 Marilyn Manson')
# track_title_say = 'SAY10'
# artist_name_say = 'Marilyn Manson'
# genre_say = api_calls.get_track_discogs(discogs_api_token, track_title_say, artist_name_say)
# pprint(genre_say)
#
print('--------------------smells like teen spirit Nirvana')
smells_like_teen_spirit_id = '5ghIJDpPoe3CfHMGu71E6T'
smells_like_teen_spirit = api_calls_test.get_track(smells_like_teen_spirit_id, token)
pprint(smells_like_teen_spirit)
#
# print('--------------------Discogs isrc SAY10 Marilyn Manson')
# isrc = 'USC4R1702226'
# genre_say = api_calls.get_track_discogs_isrc(discogs_api_token, isrc)
# pprint(genre_say)
#
# print('--------------------Discogs isrc smells like teen spirit Nirvana')
# isrc_smells_like_teen_spirit = 'USGF19942501'
# genre_smells_like_teen_spirit = api_calls.get_track_discogs_isrc(discogs_api_token, isrc_smells_like_teen_spirit)
# pprint(genre_smells_like_teen_spirit)
#
# print('--------------------Discogs isrc KILL4ME Marilyn Manson')
# isrc_KILL4ME = 'USC4R1702226'
# genre_KILL4ME = api_calls.get_track_discogs_isrc(discogs_api_token, isrc_KILL4ME)
# pprint(genre_KILL4ME)
#
# print('--------------------TOP 50 - UKRAINE')
# pl_top_50_ua_id = '37i9dQZEVXbKkidEfWYRuD'
# playlist_top_50_ua = api_calls.get_playlist(token, pl_top_50_ua_id)
# pprint(playlist_top_50_ua)
#
# print('--------------------TOP 50 - UKRAINE')
# pl_top_50_ua_id = '37i9dQZEVXbKkidEfWYRuD'
# playlist_top_50_ua = api_calls.get_playlist(token, pl_top_50_ua_id)
# pprint(playlist_top_50_ua)
#
# # Defines the path to the file where the playlist data will be saved in JSON format
# file_pl_top_50_ua = 'C:/Users/vgrec/Desktop/Spotify_Songs/Spotify-Songs-Analysis/data/raw/pl_top_50_ua.json'
# # Opens the file for writing and saves the retrieved playlist data in JSON format
# with open(file_pl_top_50_ua, 'w') as file:
#     # Uses json.dump to write the playlist data to the specified file in JSON format
#     json.dump(playlist_top_50_ua, file)
#
# print('--------------------TOP 50 - UKRAINE Playlist Items')
# pl_items_top_50_ua_id = '37i9dQZEVXbKkidEfWYRuD'
# playlist_items_top_50_ua = api_calls.get_playlist_items(token, pl_items_top_50_ua_id)
# pprint(playlist_items_top_50_ua)
#
# table_data = []
# playlist_name_top_50_ua = playlist_top_50_ua['name']
# print(playlist_name_top_50_ua)
# playlist_followers_total_top_50_ua = playlist_top_50_ua['followers']['total']
# print(playlist_followers_total_top_50_ua)
# playlist_id_top_50_ua = playlist_top_50_ua['id']
# print(playlist_id_top_50_ua)
#
# file_pl_items_top_50_ua = '../data/raw/pl_items_top_50_ua.json'
# with open(file_pl_items_top_50_ua, 'w') as file:
#      json.dump(playlist_items_top_50_ua, file)
#
# # Using df2 = pd.DataFrame(playlist_items_top_50_ua) is not appropriate
# # because playlist_items_top_50_ua contains nested structures.
# df2 = pd.DataFrame(playlist_items_top_50_ua)
# print(df2)
#
# # normalized_data = api_calls.normalize_json(playlist_top_50_ua)
# # # print(normalized_data)
# # print('--------------------------------------------------')
# # keys = normalized_data.keys()
# # keys_to_remove = []
# #
# # for key in normalized_data:
# #     if "available_markets" in key:
# #         keys_to_remove.append(key)
# #
# # for key in keys_to_remove:
# #     del normalized_data[key]
#
# # print(normalized_data)
#
# # print(keys)
#
# print('------------------------------------df_top_50_ua')
# df_top_50_ua = api_calls.create_playlist(playlist_top_50_ua)
# print(df_top_50_ua.head(10))
# print(df_top_50_ua.describe(include=['object']))
# print(df_top_50_ua.info())
#
# print('------------------------------------df_top_50_ua_2')
# df_top_50_ua_2 = api_calls.create_playlist_2(playlist_top_50_ua)
# print(df_top_50_ua_2.head(10))
# print(df_top_50_ua_2.describe(include=['object']))
# print(df_top_50_ua_2.info())
#
#
#
# # all_playlists = []
# #
# # for playlist_id in playlist_ids:
# #     playlist_data = api_calls.get_playlist(token, playlist_id)
# #     df_playlist = api_calls.create_playlist_table(playlist_data)
# #     # print(f'---------------------------------------------------{playlist_id}')
# #     # print(df_playlist.head(10))
# #     all_playlists.append(df_playlist)
# #
# # # print(all_playlists)
# #
# # playlists_df = pd.concat(all_playlists, ignore_index=True)
# # print(playlists_df)
#
# with open('config_test.yaml', 'r') as file:
#     config = yaml.safe_load(file)
#
# pprint(config)
# playlists_id = config['playlists_id']
# playlists_df = api_calls.create_all_playlists(token, playlists_id)
# print(playlists_df)
#
# file_path_playlists = '../data/preprocessed/playlists_df.csv'
# playlists_df.to_csv(file_path_playlists, index=False)
