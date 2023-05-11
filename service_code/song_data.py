import os
import pickle


def song_dict_creation(f):
    song_set = pickle.load(f)
    song_dict = {}
    for root, dirs, files in os.walk('users'):
        for file in files:
            f = open('users/' + str(file), 'r')
            user = str(file).strip('.txt')
            for lines in f.readlines():
                line = lines.split()
                song_id = line[1]
                if song_id in song_set:
                    if song_id not in song_dict.keys():
                        song_dict[song_id] = {}
                        song_dict[song_id][user + '_count'] = 1
                        song_dict[song_id]['artist_id'] = line[0]
                    else:
                        if user + '_count' in song_dict[song_id].keys():
                            song_dict[song_id][user + '_count'] = song_dict[song_id][user + '_count'] + 1
                        else:
                            song_dict[song_id][user + '_count'] = 1

    songObj = open('song_dict.obj', 'wb')
    pickle.dump(song_dict, songObj)
    songObj.close()
