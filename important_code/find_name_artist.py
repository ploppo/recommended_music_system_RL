import pickle
import time
import musicbrainzngs

start_time = time.time()

f = open('old/artist_set.obj', 'rb')
artis_set = pickle.load(f)

musicbrainzngs.set_useragent('my app', '1.0.0', contact='fenix7@live.it')

result = {}


def name_search(el):
    ris = []
    try:
        result = musicbrainzngs.get_artist_by_id(el)
    except musicbrainzngs.WebServiceError as exc:
        print("Something went wrong with the request: %s" % exc)
    else:
        ris = result["artist"]['name']
    return ris


if __name__ == '__main__':
    for el in artis_set:
        ris = name_search(el)
        result[el] = ris
    fnew = open('artist_name.obj', 'wb')
    pickle.dump(result, fnew)
    fnew.close()
    print("--%s seconds ---" % (time.time() - start_time))
