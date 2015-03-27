import itertools
import json
import pickle

from game_tree_classes import WinnerOf


with open('complete_bracket_first_half_of_elite_8.pkl', 'r') as fh:
    SLOTS_BEFORE = pickle.load(fh)


def complete_bracket(game_slots, choice_slots, choices):
    result = game_slots.copy()
    for slot_id, choice_val in zip(choice_slots, choices):
        winner_of = result.get_slot(slot_id)
        if choice_val not in (winner_of.game_slot1, winner_of.game_slot2):
            raise ValueError('Choice does not match available.')
        winning_team = result.get_slot(choice_val)
        result.reset_slot(slot_id, winning_team)

    if not result.complete:
        raise ValueError('Expected bracket to be complete.')
    return result.reduced


def main():
    choice_slots = []
    choice_vals = []
    for slot_id in xrange(127):
        value = SLOTS_BEFORE.get_slot(slot_id)
        if isinstance(value, WinnerOf):
            choice_slots.append(slot_id)
            choice_vals.append((value.game_slot1, value.game_slot2))

    print len(choice_slots), 'choices left'
    reduced_vals = []
    for choice_tuple in itertools.product(*choice_vals):
        reduced_vals.append(
            complete_bracket(SLOTS_BEFORE, choice_slots, choice_tuple))

    filename = 'reduced_completed_scenarios.json'
    with open(filename, 'w') as fh:
        json.dump(reduced_vals, fh, indent=2, sort_keys=True,
                  separators=(',', ': '))
    print 'Created', filename


if __name__ == '__main__':
    main()
