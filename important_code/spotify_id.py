from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pickle

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
          scope="user-read-recently-played user-read-private user-top-read user-read-currently-playing"))

# auth_manager = SpotifyClientCredentials()
# spotify = spotipy.Spotify(auth_manager=auth_manager)

# opening dataset
f = open('database3.obj', 'rb')
database = pickle.load(f)
f.close()


for el in database.index[30000:]:  # for each element query to get the features needed
        query = ('track:' + database.at[el, 'song_name'].replace(" ", "+") + ' ' + 'artist:' + database.at[
            el, 'artist_name'].replace(" ", "+"))
        result = spotify.search(q=database.at[el, 'song_name'] + " " + database.at[el, 'artist_name'], type='track',
                                limit=1)  # result from spotipy
        if len(result['tracks']['items']) > 0:
            i = 0
            if result['tracks']['items'][i]['name'].upper()[0:int(len(database.at[el, 'song_name'])/4)] != database.at[el, 'song_name'].upper().replace("’", "'")[0:int(len(database.at[el, 'song_name'])/4)]:
                database = database.drop(el)
            elif result['tracks']['items'][i]['id'] is not None:
                print(el)
                database.at[el, 'spotify_song_id'] = result['tracks']['items'][i]['id']  # spotify_id
                database.at[el, 'spotify_artist_id'] = result['tracks']['items'][i]['artists'][0]['id']
                features = spotify.audio_features(database.at[el, 'spotify_song_id'])[0]
                if features is not None:  # setting the features
                    database.at[el, 'danceability'] = features['danceability']
                    database.at[el, 'energy'] = features['energy']
                    database.at[el, 'speechiness'] = features['speechiness']
                    database.at[el, 'acousticness'] = features['acousticness']
                    database.at[el, 'valence'] = features['valence']
                    database.at[el, 'instrumentalness'] = features['instrumentalness']
        else:
            database = database.drop(el)
        fnew = open('databaseend.obj', 'wb')
        pickle.dump(database, fnew)
        fnew.close()

fnew = open('databaseend.obj', 'wb')
database = database.drop_duplicates(subset="spotify_song_id")
database.index = range(0, len(database.index))
pickle.dump(database, fnew)
fnew.close()
