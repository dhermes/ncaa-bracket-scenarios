import json
import pickle

import local_settings
import utils


with open(utils.TEAM_MAP_FILENAME, 'r') as fh:
    TEAM_MAP = json.load(fh)


def choose_winner(winner_of, game_slots):
    prev_team1 = game_slots.get_slot(winner_of.game_slot1)
    prev_team2 = game_slots.get_slot(winner_of.game_slot2)

    team_name1 = TEAM_MAP[prev_team1.team_id]
    team_name2 = TEAM_MAP[prev_team2.team_id]

    message = '%s [y] or %s [n]? ' % (team_name1, team_name2)
    choice = raw_input(message)
    if choice.strip().lower() == 'y':
        return prev_team1
    else:
        return prev_team2



def main():
    with open(utils.BASE_BRACKET_PICKLE, 'r') as fh:
        slots_before = pickle.load(fh)

    game_slots = slots_before.copy()
    for slot_id in xrange(64, 64 + 32 + 16):
        winner_of = game_slots.get_slot(slot_id)
        winning_team = choose_winner(winner_of, game_slots)
        game_slots.reset_slot(slot_id, winning_team)
    game_slots.save(utils.SWEET16_PICKLE)


if __name__ == '__main__':
    main()
