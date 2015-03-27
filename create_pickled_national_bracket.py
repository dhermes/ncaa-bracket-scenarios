import pickle

from game_tree_classes import GameSlots
from game_tree_classes import Team
from game_tree_classes import WinnerOf


def main():
    game_slots = GameSlots()
    for slot_id in xrange(64):
        # NOTE: This relies on the assumption from get_team_mapping.py
        #       that the team ID is 1 more than the slot ID.
        team = Team(slot_id + 1)
        game_slots.add_slot(slot_id, team)

    prev_first, first_index = 0, 64
    for round_size in (32, 16, 8, 4, 2, 1):
        for slot_offset in xrange(round_size):
            slot_id = slot_offset + first_index
            prev_slot1 = prev_first + 2 * slot_offset
            prev_slot2 = prev_first + 2 * slot_offset + 1
            winner_of = WinnerOf(prev_slot1, prev_slot2)
            game_slots.add_slot(slot_id, winner_of)
        prev_first, first_index = first_index, first_index + round_size
    game_slots.save('base_bracket.pkl')


if __name__ == '__main__':
    main()
