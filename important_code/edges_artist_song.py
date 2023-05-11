import pickle

f = open('dataset_medium.obj', 'rb')
data = pickle.load(f)
f.close()

edge_list = []

for el in data.index:
    edge_list.append((data.at[el, 'spotify_song_id'],data.at[el, 'spotify_artist_id']))

fnew = open('old/edges_artist_song_list_medium.obj', 'wb')
pickle.dump(edge_list, fnew)
fnew.close()
