from open_file import open_file

edge_artist, edge_user, edge_song, data = open_file()

f = open('triplets_medium.tsv', 'w')

for el in edge_artist:
    f.write(str(el[0])+'\tis_make_by\t'+str(el[1])+'\n')

for el in edge_user:
    f.write(str(el[0])+'\tlisten_to\t'+str(el[1])+'\n')

for el in edge_song:
    f.write(str(el[0])+'\tsong_similar_to\t'+str(el[1])+'\n')

f.close()
