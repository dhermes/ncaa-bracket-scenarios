from google.cloud import datastore

from local_settings import DATASET_ID


def main():
    client = datastore.Client(project=DATASET_ID)
    with open('complete_bracket_sweet_16.pkl', 'rb') as fh:
        pickle_contents = fh.read()

    key = client.key('BracketContainer', 'sweet16')
    entity = datastore.Entity(key, exclude_from_indexes=('bracket',))
    entity['bracket'] = pickle_contents
    entity['year'] = 2017
    client.put(entity)


if __name__ == '__main__':
    main()
