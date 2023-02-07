import numpy as np
from open_file import open_file

edge_artist, edge_user, edge_song, data = open_file()

center_state = np.array([np.mean(data['danceability']), np.mean(data['energy']), np.mean(data['speechiness']),
                         np.mean(data['acousticness']), np.mean(data['valence']), np.mean(data['instrumentalness'])])

features_width = np.array([np.var(data['danceability']), np.var(data['energy']), np.var(data['speechiness']),
                           np.var(data['acousticness']), np.var(data['valence']), np.var(data['instrumentalness'])])


def rbf_vec(features):
    x = np.zeros(6)
    for i in range(6):
        num = np.linalg.norm(features - center_state[i])
        x[i] = np.exp(-(num * num) / (2 * features_width[i]))

    return x
