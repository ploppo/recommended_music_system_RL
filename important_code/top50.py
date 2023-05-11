import os
from collections import Counter
import pickle

song_set = set()
artist_set = set()
number_listening = {}
song_artist_dict = {}
total_seen = set()
song_artist_dict_real ={}
for root, dirs, files in os.walk('users'):
    for file in files:
        f = open('users/' + str(file), 'r')
        user = str(file).strip('.txt')
        number_listening[user] = {}
        seen = set()
        for lines in f.readlines():
            line = lines.split()
            song_id = line[1]
            artist_id = line[0]
            if song_id not in seen:
                seen.add(song_id)
                number_listening[user][song_id] = 1
            else:
                number_listening[user][song_id] = number_listening[user][song_id] + 1
            if song_id not in total_seen:
                total_seen.add(song_id)
                song_artist_dict[song_id] = artist_id
        d = Counter(number_listening[user])
        number_listening[user] = dict(d.most_common(50))
        for song_id in number_listening[user].keys():
            song_artist_dict_real[song_id] = song_artist_dict[song_id]
            if song_id not in song_set:
                song_set.add(song_id)
            if song_artist_dict[song_id] not in artist_set:
                artist_set.add(song_artist_dict[song_id])

song_artist_dict_file = open('song_artist_dict_small.obj','wb')
pickle.dump(song_artist_dict_real, song_artist_dict_file)

artist_file = open('artist_set_small.obj', 'wb')
pickle.dump(artist_set, artist_file)

song_file = open('song_set_small.obj', 'wb')
pickle.dump(song_set, song_file)

number_listening_file = open('number_listening_small.obj', 'wb')
pickle.dump(number_listening, number_listening_file)
