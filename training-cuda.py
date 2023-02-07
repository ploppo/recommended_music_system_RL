import networkx as nx
import numpy as np
import torch
import cupy as cp
import pykeen_emb
import constant
from torch import norm
from sklearn.preprocessing import normalize
import graph_construction

# finishing importing
print('training initialization begin')
Graph = graph_construction.G
data = graph_construction.data
n_artist = graph_construction.n_artist
n_song = graph_construction.n_song
node = list(Graph.nodes)

# get matrix and normalize to do transition probabilities matrix
M = nx.to_scipy_sparse_array(Graph)
M = normalize(M, norm='l1', axis=1)
# row_sums = np.asarray(M.sum(axis=1))
# M = M / row_sums[:, np.newaxis]

# function that change transition pro
def transition_prob(teta_pass, row_state, matrix):
    possible_action = list((M.getrow(row_state)).nonzero()[1])  # starting state
    den = 0
    for act in possible_action:
        if n_artist - 1 < act < (n_artist + n_song):
            features_song = np.squeeze(np.array(data[data['spotify_song_id'] == node[act]].iloc[:, 3:9]))
            h = np.dot(teta_pass, constant.rbf_vec(features=features_song))
            den = den + np.exp(h)
    for act in possible_action:
        if n_artist - 1 < act < (n_artist + n_song):
            features_num = np.squeeze(np.array(data[data['spotify_song_id'] == node[act]].iloc[:, 3:9]))
            h_num = np.dot(teta_pass, constant.rbf_vec(features=features_num))
            num = np.exp(h_num)
            matrix[row_state,act] = num / den
    return matrix

# parameter initialization
teta = np.zeros(6)
alpha = 1 / np.power(2, 13)
features = {}
sequence_state = [10, 10, 10]
old_songs = [1, 2, 3]
new_songs = [4,5,2]
episode = 0
max_reward = 0
still_same_max = 0
print('training initialization end')

print('training begin')
while episode < 100:
    # initialization for each episode
    episode += 1
    old_songs = new_songs
    state = 7310 # starting song
    new_state = 7310
    sequence_state = [36567, state] # starting sequence
    reward = []
    features[state] = np.squeeze(np.array(data[data['spotify_song_id'] == node[new_state]].iloc[:, 3:9]))
    # starting vector V
    V_forward = pykeen_emb.entity_embedding_tensor[pykeen_emb.tf.entity_to_id['user0']].cuda()
    V_forward = torch.add(V_forward, pykeen_emb.relation_embedding_tensor[pykeen_emb.tf.relation_to_id['listen_to']])
    state_concatenation = V_forward
    V_backward = torch.zeros(10).cuda()
    calculate_reward = 0
    loop_state = []
    while sum(map(lambda x: n_artist - 1 < x < (n_artist + n_song), sequence_state)) < 5:
        action = list((M.getrow(state)).nonzero()[1])
        for el in loop_state:
            if el in action: action.remove(el)
        num_action = len(action)
        # exclude to go back on the already visited nodes
        count = 0
        loop = 0
        forward = 0
        backward = 0
        while new_state in set(sequence_state) or new_state in loop_state:
            num = M.getrow(state).todense()[0]
            p = num[action] / np.sum(num[action])
            if len(action) > 0:
                new_state = np.random.choice(action, p=p.data)
                action.remove(new_state)
            count += 1
            if count > len(action):
                loop = 1
                loop_state.append(state)
                sequence_state.remove(state)
                state = sequence_state[len(sequence_state) - 1]
                action = list((M.getrow(state)).nonzero()[1])
                for el in loop_state:
                    if el in action: action.remove(el)
                count = 0
        # case 1: (from...) to song
        if n_artist - 1 < new_state < (n_artist + n_song):
            calculate_reward = 1
            features[new_state] = np.squeeze(np.array(data[data['spotify_song_id'] == node[new_state]].iloc[:, 3:9]))
            # song
            if n_artist <= state < (n_artist + n_song):
                forward = 1
                edge_embeddings_forward = pykeen_emb.relation_embedding_tensor[
                    pykeen_emb.tf.relation_to_id['song_similar_to']]
            # artist
            if state < n_artist:
                backward = 1
                edge_embeddings_backward = pykeen_emb.relation_embedding_tensor[
                    pykeen_emb.tf.relation_to_id['is_make_by']]
            # user
            if state >= (n_artist + n_song):
                forward = 1
                edge_embeddings_forward = pykeen_emb.relation_embedding_tensor[pykeen_emb.tf.relation_to_id['listen_to']]
        else:
            calculate_reward = 0
        # case 2: song to (...)
        if n_artist <= state < (n_artist + n_song):
            # to artist
            if new_state < n_artist:
                forward = 1
                edge_embeddings_forward = pykeen_emb.relation_embedding_tensor[pykeen_emb.tf.relation_to_id['is_make_by']]
            # to user
            if new_state >= (n_artist + n_song):
                backward = 1
                edge_embeddings_backward = pykeen_emb.relation_embedding_tensor[pykeen_emb.tf.relation_to_id['listen_to']]
        if backward == 1:
            V_backward = torch.add(V_backward,edge_embeddings_backward)
        if forward == 1:
            V_forward = torch.add(V_forward,edge_embeddings_forward)
        state = new_state
        sequence_state.append(state)
        V_backward = torch.add(V_backward, (pykeen_emb.entity_embedding_tensor[pykeen_emb.tf.entity_to_id[node[new_state]]]))
        similarity = (torch.dot(V_forward, V_backward) / (norm(V_forward) * norm(V_backward)))
        reward.append(cp.asarray(100*similarity.detach()))

    # gradient ascent
    new_songs = []
    for el in sequence_state:
        if n_artist - 1 < el < (n_artist + n_song):
            new_songs.append(el)
    for i in range(len(new_songs)):
        G = float(sum(reward[i:len(new_songs)]))
        teta = teta + alpha * G * (constant.rbf_vec(features[new_songs[i]]))
        M = transition_prob(teta_pass=teta, row_state=new_songs[i], matrix=M)

    # keeping memory of the best sequence
    if max_reward < float(sum(reward[0:len(new_songs)])):
        max_reward = float(sum(reward[0:len(new_songs)]))
        best_sequence = sequence_state
        still_same_max = 0
    else:
        still_same_max += 1

    print(episode)
    print(sequence_state)

print('training end')

for el in best_sequence:
    if n_artist - 1 < el < (n_artist + n_song):
        print(data[data['spotify_song_id'] == node[el]][['song_name','artist_name']].values[0][0],
              data[data['spotify_song_id'] == node[el]][['song_name','artist_name']].values[0][1])
print(best_sequence)