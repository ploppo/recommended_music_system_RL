import pickle
import pandas as pd

f = open('old/number_listening.obj', 'rb')
listening = pickle.load(f)
f.close()
f = open('dataset_medium.obj', 'rb')
data = pickle.load(f)
f.close()
edge_list = []

for el in data.index:
    if pd.isna(data.at[el, 'artist_id']):
        edge_list.append(('user0', data.at[el,'spotify_song_id']))


for key in list(listening.keys())[:100]:
    print(key)
    for keys in listening[key]:
        for el in data.index:
            if keys == data.at[el, 'song_id']:
                edge_list.append((key, data.at[el, 'spotify_song_id']))

fnew = open('edges_user_song_list_medium'+str(100)+'.obj', 'wb')
pickle.dump(edge_list, fnew)
fnew.close()
