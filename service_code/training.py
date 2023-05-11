import networkx as nx
import numpy as np
import torch
import pykeen_emb
import constant
from torch.linalg import norm
import graph_construction

# finishing importing
print('training initialization begin')
Graph = graph_construction.G
data = graph_construction.data
n_artist = graph_construction.n_artist
n_song = graph_construction.n_song

# get matrix and normalize
M = nx.to_numpy_array(Graph)
row_sums = np.asarray(M.sum(axis=1))
M = M / row_sums[:, np.newaxis]


def transiction_prob(teta_pass, row_state, matrix):
    possible_action = np.where(matrix[row_state] != 0)[0]
    den = 0
    for act in possible_action:
        features_song = np.squeeze(np.array(data[data['spotify_song_id'] == node[act]].iloc[:, 3:9]))
        h = np.dot(teta_pass, constant.rbf_vec(features=features_song))
        den = den + np.exp(h)
    for act in possible_action:
        features_num = np.squeeze(np.array(data[data['spotify_song_id'] == node[act]].iloc[:, 3:9]))
        h_num = np.dot(teta_pass, constant.rbf_vec(features=features_num))
        num = np.exp(h_num)
        matrix[row_state][act] = num / den
    return matrix


T = 7
stateartist = 0
node = list(Graph.nodes)
teta = np.zeros(6)
alpha = 1 / np.power(2, 13)
features = {}

# for i in range(n_artist):
#     features_artist = np.zeros(6)
#     new_action = np.where(M[i] != 0)[0]
#     for el in new_action:
#         song_id = node[el]
#         features_new_songs = np.squeeze(np.array(data[data['spotify_song_id'] == song_id].iloc[:, 6:12]))
#         features_artist += features_new_songs
#     features[i] = features_artist / len(new_action)
#
# for i in range(n_artist + n_song, len(node)):
#     features_user = np.zeros(6)
#     new_action = np.where(M[i] != 0)[0]
#     for el in new_action:
#         song_id = node[el]
#         features_new_songs = np.squeeze(np.array(data[data['spotify_song_id'] == song_id].iloc[:, 6:12]))
#         features_user += features_new_songs
#     features[i] = features_user / len(new_action)

sequence_state = [10, 10, 10]
old_songs = [1, 2, 3]
new_songs = [4, 5, 2]
episode = 0
max_reward = 0
small_change = 0
still_same_max = 0
print('training initialization end')

print('training begin')
while episode < 1000:  # and set(old_songs) != set(new_songs):
    episode += 1
    # alpha = 1 / (np.log(episode+1))
    old_songs = new_songs
    state = 36567
    new_state = 36567  # 897
    sequence_state = [state]
    reward = []
    V_forward = pykeentry.entity_embedding_tensor[pykeentry.tf.entity_to_id['user0']]
    state_concatenation = V_forward
    V_backward = torch.empty(50)
    calculate_reward = 0
    loop_state = []
    while sum(map(lambda x: n_artist - 1 < x < (n_artist + n_song), sequence_state)) < 5:
        # for i in range(T):
        action = list(np.where(M[state] != 0)[0])
        num_action = len(action)
        M = transiction_prob(teta_pass=teta, row_state=state, matrix=M)
        # exclude to go back on the already visited nodes
        count = 0
        loop = 0
        forward = 0
        backward = 0
        while new_state in set(sequence_state) or new_state in loop_state:
            p = M[state, action] / np.sum(M[state, action])
            if len(action) > 0:
                new_state = np.random.choice(action, p=p)
                action.remove(new_state)
            count += 1
            if count > num_action:
                loop = 1
                loop_state.append(state)
                sequence_state.remove(state)
                state = sequence_state[len(sequence_state) - 1]
                action = list(np.where(M[state] != 0)[0])
                count = 0
        # case 1: (from...) to song
        if n_artist - 1 < new_state < (n_artist + n_song):
            calculate_reward = 1
            features[new_state] = np.squeeze(np.array(data[data['spotify_song_id'] == node[new_state]].iloc[:, 3:9]))
            # song
            if n_artist <= state < (n_artist + n_song):
                forward = 1
                edge_embeddings_forward = pykeentry.relation_embedding_tensor[
                    pykeentry.tf.relation_to_id['song_similar_to']]
            # artist
            if state < n_artist:
                backward = 1
                edge_embeddings_backward = pykeentry.relation_embedding_tensor[
                    pykeentry.tf.relation_to_id['is_make_by']]
            # user
            if state >= (n_artist + n_song):
                forward = 1
                edge_embeddings_forward = pykeentry.relation_embedding_tensor[pykeentry.tf.relation_to_id['listen_to']]
        else:
            calculate_reward = 0
        # case 2: song to (...)
        if n_artist <= state < (n_artist + n_song):
            # to artist
            if new_state < n_artist:
                forward = 1
                edge_embeddings_forward = pykeentry.relation_embedding_tensor[pykeentry.tf.relation_to_id['is_make_by']]
            # to user
            if new_state >= (n_artist + n_song):
                backward = 1
                edge_embeddings_backward = pykeentry.relation_embedding_tensor[pykeentry.tf.relation_to_id['listen_to']]
        if backward == 1:
            V_backward = V_backward.add(edge_embeddings_backward)
        if forward == 1:
            V_forward = V_forward.add(edge_embeddings_forward)
        state = new_state
        sequence_state.append(state)
        # print('state embeddings \n', pykeentry.entity_embedding_tensor[pykeentry.tf.entity_to_id[node[new_state]]])
        # print('V_backward prima \n', V_backward)
        V_backward = torch.add(V_backward,
                               (pykeentry.entity_embedding_tensor[pykeentry.tf.entity_to_id[node[new_state]]]))
        # print('V_backward dopo \n',V_backward)
        similarity = (torch.dot(V_forward, V_backward) / (norm(V_forward) * norm(V_backward)))
        reward.append(np.array(100 * similarity.detach()))

    new_songs = []
    for el in sequence_state:
        if n_artist - 1 < el < (n_artist + n_song):
            new_songs.append(el)

    old_teta_norm = np.linalg.norm(teta)

    for i in range(len(new_songs)):
        G = float(sum(reward[i:len(new_songs)]))
        teta = teta + alpha * G * (constant.rbf_vec(features[new_songs[i]]))
        M = transiction_prob(teta_pass=teta, row_state=new_songs[i], matrix=M)

    if max_reward < float(sum(reward[0:len(new_songs)])):
        max_reward = float(sum(reward[0:len(new_songs)]))
        best_sequence = sequence_state
        still_same_max = 0
    else:
        still_same_max += 1
    # max_reward = max(max_reward,(sum(reward[0:len(new_songs)])))

    new_teta_norm = np.linalg.norm(teta)
    if abs(new_teta_norm - old_teta_norm) < 0.001:
        small_change += 1
    else:
        small_change = 0

    print(sequence_state)
    print(episode)
    episode += 1
    print(sequence_state)
    print(episode)
# for el in new_songs:
#     print(data)
print('training end')
