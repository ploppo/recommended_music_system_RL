import pickle

def open_file():
    print('open file begin')

    f = open('dataset_medium.obj', 'rb')
    data = pickle.load(f)
    data = data.dropna(subset='spotify_artist_id')
    data = data.dropna(subset='spotify_song_id')
    data['spotify_artist_id'] = data['spotify_artist_id'].astype(str)
    data['spotify_song_id'] = data['spotify_song_id'].astype(str)
    f.close()

    f = open('old/edges_song_list_medium.obj', 'rb')
    edge_song = pickle.load(f)
    edge_song = [x for x in edge_song if str(x[1]) != 'nan' and str(x[0]) != 'nan']
    f.close()

    f = open('old/edges_user_song_list_medium.obj', 'rb')
    edge_user = pickle.load(f)
    edge_user = [x for x in edge_user if str(x[1]) != 'nan' and str(x[0]) != 'nan' ]
    f.close()

    f = open('old/edges_artist_song_list_medium.obj', 'rb')
    edge_artist = pickle.load(f)
    edge_artist = [x for x in edge_artist if str(x[1]) != 'nan' and str(x[0]) != 'nan']
    f.close()

    print('open file end')
    return edge_artist, edge_user, edge_song, data

