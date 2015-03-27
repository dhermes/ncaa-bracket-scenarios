import json
import os
import pickle

from game_tree_classes import Team
import get_brackets_html


with open('base_bracket.pkl', 'r') as fh:
    BASE_BRACKET = pickle.load(fh)


def get_complete_bracket(slot_winners, game_slots):
    result = game_slots.copy()
    for slot_id in xrange(64, 127):
        winner_of = result.get_slot(slot_id)
        winning_team = slot_winners[str(slot_id)]

        team_id1 = result.get_slot(winner_of.game_slot1).team_id
        team_id2 = result.get_slot(winner_of.game_slot2).team_id

        if str(winning_team) not in (team_id1, team_id2):
            raise ValueError('Winner is not possible.')
        result.reset_slot(slot_id, Team(winning_team))

    if not result.complete:
        raise ValueError('Expected bracket to be complete.')
    return result.reduced


def main():
    to_store = {}
    for entry_id in get_brackets_html.get_bracket_ids():
        json_filename = os.path.join(get_brackets_html.BRACKETS_DIR,
                                     str(entry_id) + '.json')
        with open(json_filename, 'r') as fh:
            slot_winners = json.load(fh)

        bracket_reduced = get_complete_bracket(slot_winners, BASE_BRACKET)
        to_store[entry_id] = bracket_reduced

    filename = 'reduced_all_filled_out.json'
    with open(filename, 'w') as fh:
        json.dump(to_store, fh, indent=2, sort_keys=True,
                  separators=(',', ': '))
    print 'Created', filename


if __name__ == '__main__':
    main()
