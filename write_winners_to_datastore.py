from __future__ import print_function

import json

from google.cloud import datastore

import local_settings
import utils


with open(utils.WINNING_SCORES, 'r') as fh:
    ALL_OUTCOMES = json.load(fh)
with open(utils.BRACKET_LINKS_FILE, 'r') as fh:
    BRACKETS = json.load(fh)
ENTRY_TO_NAME = {str(val): key for key, val in BRACKETS.items()}
PAGE_SIZE = 100


def to_entity(key, client, outcomes):
    lowest, highest = outcomes[key]
    lowest_scores = [pair[0] for pair in lowest]
    lowest_names = [ENTRY_TO_NAME[pair[1]] for pair in lowest]
    highest_scores = [pair[0] for pair in highest]
    highest_names = [ENTRY_TO_NAME[pair[1]] for pair in highest]

    ds_key = client.key('PotentialBracket', key)
    entity = datastore.Entity(ds_key)
    entity['year'] = 2017
    entity['lowest_scores'] = lowest_scores
    entity['lowest_names'] = lowest_names
    entity['highest_scores'] = highest_scores
    entity['highest_names'] = highest_names

    return entity


def store_entities():
    client = datastore.Client(project=local_settings.DATASET_ID)

    # Page 100 items at a time.
    base_index = 0

    # Use sorted so it is deterministic.
    keys = sorted(ALL_OUTCOMES.keys())
    num_keys = len(keys)
    while base_index < num_keys:
        max_index = min(num_keys, base_index + PAGE_SIZE)
        entities = [to_entity(keys[i], client, ALL_OUTCOMES)
                    for i in xrange(base_index, max_index)]
        client.put_multi(entities)
        base_index += PAGE_SIZE
        msg = 'Completed {}'.format(base_index)
        print(msg)


if __name__ == '__main__':
    store_entities()
