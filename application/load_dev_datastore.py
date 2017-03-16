from __future__ import print_function

import json
import pickle

from google.appengine.ext import ndb


class PotentialBracket(ndb.Model):
    year = ndb.IntegerProperty(default=2017, indexed=False)
    highest_names = ndb.StringProperty(repeated=True, indexed=False)
    highest_scores = ndb.IntegerProperty(repeated=True, indexed=False)
    lowest_names = ndb.StringProperty(repeated=True, indexed=False)
    lowest_scores = ndb.IntegerProperty(repeated=True, indexed=False)


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

    return PotentialBracket(
        id=key, lowest_scores=lowest_scores, lowest_names=lowest_names,
        highest_scores=highest_scores, highest_names=highest_names)


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
        ndb.put_multi(entities)
        base_index += PAGE_SIZE
        msg = 'Completed {}'.format(base_index)
        print(msg)


def store_sweet16():
    class BracketContainer(ndb.Model):
        year = ndb.IntegerProperty(default=2017, indexed=False)
        bracket = ndb.PickleProperty()

    with open('complete_bracket_sweet_16.pkl', 'r') as fh:
        pickled_obj = pickle.load(fh)

    entity = BracketContainer(id='sweet16', bracket=pickled_obj)
    ndb.put_multi([entity])


def main():
    store_entities()
    store_sweet16()
