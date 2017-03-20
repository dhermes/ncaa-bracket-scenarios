from google.cloud import datastore

import local_settings
import utils


def main():
    client = datastore.Client(project=local_settings.DATASET_ID)
    with open(utils.SWEET16_PICKLE, 'rb') as fh:
        pickle_contents = fh.read()

    key = client.key('BracketContainer', 'sweet16')
    entity = datastore.Entity(key, exclude_from_indexes=('bracket',))
    entity['bracket'] = pickle_contents
    entity['year'] = 2017
    client.put(entity)


if __name__ == '__main__':
    main()
