# import matplotlib.pyplot as plt
import networkx as nx
from open_file import open_file

edge_artist, edge_user, edge_song, data = open_file()

print('graph construction begin')
# graph construction
G = nx.DiGraph()
# adding nodes
G.add_nodes_from((set(data['spotify_artist_id'])))  # 0 - 240
G.add_nodes_from(set(data['spotify_song_id']))  # 241 - 896
# number of artist and song in the graph
n_artist = len(set(data['spotify_artist_id']))
n_song = len(set(data['spotify_song_id']))
# undirected edge to let the agent visiting the graph
n_edge_user = len(edge_user)
for i in range(n_edge_user):
    edge_user.append((edge_user[i][1], edge_user[i][0]))
n_edge_artist = len(edge_artist)
for i in range(n_edge_artist):
    edge_artist.append((edge_artist[i][1], edge_artist[i][0]))
# add edge
G.add_edges_from(edge_artist) # song to artist and viceversa
G.add_edges_from(edge_song)   # songo to song based on similarity
G.add_edges_from(edge_user)   # user to song and viceversa
print('graph construction end')

# nx.draw(G)
# plt.draw()
# plt.show()
