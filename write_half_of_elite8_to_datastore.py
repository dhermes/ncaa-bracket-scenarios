from gcloud import datastore
import setup_gcloud


def main():
    with open('complete_bracket_first_half_of_elite_8.pkl', 'rb') as fh:
        pickle_contents = fh.read()

    key = datastore.Key('BracketContainer', 'half-elite8')
    entity = datastore.Entity(key)
    entity['bracket'] = pickle_contents
    datastore.put([entity])


if __name__ == '__main__':
    main()
