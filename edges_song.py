import pickle
import numpy as np
from numpy.linalg import norm

# getting the dataset
f = open('dataset_medium.obj', 'rb')
database = pickle.load(f)
f.close()

n_rows = database.shape[0]  # length of the dataset
edge_list = []  # list of the song-song edge

len = 600
for el in database.index[len-100:len]:
    a = np.array(
        [database.iat[el, 3], database.iat[el, 4], database.iat[el, 5], database.iat[el, 6], database.iat[el, 7],
         database.iat[el, 8]])
    for i in range(el + 1, n_rows):
        print(str(el)+'-'+str(i))
        b = np.array(
            [database.iat[i, 3], database.iat[i, 4], database.iat[i, 5], database.iat[i, 6], database.iat[i, 7],
             database.iat[i, 8]])
        cosine = np.dot(a, b) / (norm(a) * norm(b))
        if cosine >= 0.999:  # eps = 0.999
            print('similar')
            edge_list.append((database.at[el, 'spotify_song_id'], database.at[i, 'spotify_song_id']))
            edge_list.append((database.at[i, 'spotify_song_id'], database.at[el, 'spotify_song_id']))

fnew = open('edges_song_list_medium_'+str(len)+'.obj', 'wb')
pickle.dump(edge_list, fnew)
fnew.close()