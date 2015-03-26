import json
import pickle

from game_tree_classes import GameSlots
from game_tree_classes import Team


def main():
    game_slots = GameSlots()
    for slot_id in xrange(64):
        # NOTE: This relies on the assumption from get_team_mapping.py
        #       that the team ID is 1 more than the slot ID.
        team = Team(slot_id + 1)
        game_slots.add_slot(slot_id, team)
    game_slots.save()


if __name__ == '__main__':
    main()
