from gcloud import datastore
import setup_gcloud


def main():
    with open('complete_bracket_sweet_16.pkl', 'rb') as fh:
        pickle_contents = fh.read()

    key = datastore.Key('BracketContainer', 'sweet16')
    entity = datastore.Entity(key, exclude_from_indexes=('bracket',))
    entity['bracket'] = pickle_contents
    datastore.put([entity])


if __name__ == '__main__':
    main()
