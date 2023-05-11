import pickle
import spotipy
from spotipy.oauth2 import SpotifyOAuth

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="user-read-recently-played user-read-private user-top-read user-read-currently-playing"))

f = open('user0.txt', 'r')
fdata = open('dataset_small2.obj', 'rb')
data = pickle.load(fdata)
fdata.close()

for lines in f.readlines():
    line = lines.split()
    artist_id = line[0]
    song_id = line[1]
    if song_id not in data['spotify_song_id']:
        row = len(data.index)
        print(row)
        data.at[row, 'spotify_artist_id'] = artist_id
        data.at[row, 'spotify_song_id'] = song_id
        artist_info = spotify.artist(artist_id=artist_id)
        data.at[row, 'artist_name'] = artist_info['name']
        song_info = spotify.track(track_id=song_id)
        data.at[row, 'song_name'] = song_info['name']
        features = spotify.audio_features(data.at[row, 'spotify_song_id'])[0]
        if features is not None:  # setting the features
            data.at[row, 'danceability'] = features['danceability']
            data.at[row, 'energy'] = features['energy']
            data.at[row, 'speechiness'] = features['speechiness']
            data.at[row, 'acousticness'] = features['acousticness']
            data.at[row, 'valence'] = features['valence']
            data.at[row, 'instrumentalness'] = features['instrumentalness']
            fnew = open('dataset_small2.obj', 'wb')
            pickle.dump(data, fnew)
            fnew.close()
