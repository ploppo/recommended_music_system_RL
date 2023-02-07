import pickle
import pandas as pd

f = open('old/song_artist_dict.obj', 'rb')
song_artist_dict = pickle.load(f)  # dictionary with key song_id and value artist_id
f.close()

f = open('old/artist_name.obj', 'rb')
artist_name = pickle.load(f)  # dictionary with key artist_id and value artist_name
f.close()

f = open('old/song_name.obj', 'rb')
song_name = pickle.load(f)  # dictionary with key song_id and value song_name
f.close()

# creating final dictionary with non-null values
song_artist_dict_def = {}
for key in song_name.keys():
    if song_name[key]:
        if artist_name[song_artist_dict[key]]:
            song_artist_dict_def[key] = song_artist_dict[key]

# creating dataset 4 column [artist_id, song_id, song_name, artist_name
data = pd.DataFrame(song_artist_dict_def, index=['artist_id'])
data = data.T
data['song_id'] = data.index
data.index = range(0, len(song_artist_dict_def.keys()))
for el in data.index:
    data.at[el, 'song_name'] = song_name[data.at[el, 'song_id']]
    data.at[el, 'artist_name'] = artist_name[data.at[el, 'artist_id']]

# saving in file
fnew = open('old/dataset_medium.obj', 'wb')
pickle.dump(data, fnew)
