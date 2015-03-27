import json

from gcloud.credentials import get_for_service_account_json
from gcloud import datastore

from local_settings import DATASET_ID
from local_settings import KEY_NAME

CREDS = get_for_service_account_json(KEY_NAME, datastore.SCOPE)
CNXN = datastore.Connection(CREDS)
datastore.set_defaults(dataset_id=DATASET_ID, connection=CNXN)


with open('winning_scores.json', 'r') as fh:
    ALL_OUTCOMES = json.load(fh)
with open('bracket_links.json', 'r') as fh:
    BRACKETS = json.load(fh)
ENTRY_TO_NAME = {str(val): key for key, val in BRACKETS.items()}
PAGE_SIZE = 100


def to_entity(key, outcomes):
    lowest, highest = outcomes[key]
    lowest_scores = [pair[0] for pair in lowest]
    lowest_names = [ENTRY_TO_NAME[pair[1]] for pair in lowest]
    highest_scores = [pair[0] for pair in highest]
    highest_names = [ENTRY_TO_NAME[pair[1]] for pair in highest]

    ds_key = datastore.Key('PotentialBracket', key)
    entity = datastore.Entity(ds_key)
    entity['lowest_scores'] = lowest_scores
    entity['lowest_names'] = lowest_names
    entity['highest_scores'] = highest_scores
    entity['highest_names'] = highest_names

    return entity


def store_entities():
    # Page 100 items at a time.
    base_index = 0

    # Use sorted so it is deterministic.
    keys = sorted(ALL_OUTCOMES.keys())
    num_keys = len(keys)
    while base_index < num_keys:
        max_index = min(num_keys, base_index + PAGE_SIZE)
        entities = [to_entity(keys[i], ALL_OUTCOMES)
                    for i in xrange(base_index, max_index)]
        datastore.put(entities)
        base_index += PAGE_SIZE
        print 'Completed', base_index


if __name__ == '__main__':
    store_entities()
