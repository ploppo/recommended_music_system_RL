# Reccomended Music System using reinforcement learning
The goal of this project is to create a personalised playlist on Spotify for a chosen user. In the explanation I’m going to put in brackets the most important section of the relative code that I developed.

I used historical listening data from 1055 user, obtained on musicbrainz (https://musicbrainz.org/doc/MusicBrainz_Database/Download), and added my personal data (add_spotify_data.py) to the problem. 

For each user I got the most 50 listened song and then create a  pandas dataframe to work with (top50.py, create_dataset.py). I had to use also the Spotify’s api (spotify_id.py)  to retrieve the values for each song of 6 features (danceability, energy, speechness, acousticness, valence and instrumentalness), so I had to solve also the problem of linking the database of musicbrainz and Spotify (find_name_artist.py, find_name_song.py). 

After all this process of organizing the data I created a knowledge graph between users, artists and songs (graph_construction.py, edges_user_song.py, edges_artist_song.py, edges_song.py). Then created the embeddings of the graph using two different methods, TransE and TransR (make_triplets_tsv.py, pykeen_emb.py).

Finally exploring the graph using the best policy obtained from Monte Carlo policy gradient using soft-max action with linear action preferences. The result is the best sequence of song as a playlist (training-cuda.py)
