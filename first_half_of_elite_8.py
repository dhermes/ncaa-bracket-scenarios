import json
import pickle


with open('team_map.json', 'r') as fh:
    TEAM_MAP = json.load(fh)


def choose_winner(winner_of, game_slots):
    prev_team1 = game_slots.get_slot(winner_of.game_slot1)
    prev_team2 = game_slots.get_slot(winner_of.game_slot2)

    team_name1 = TEAM_MAP[prev_team1.team_id]
    team_name2 = TEAM_MAP[prev_team2.team_id]

    message = '%s [y] or %s [n]? ' % (team_name1, team_name2)
    choice = raw_input(message)
    response = choice.strip().lower()
    if response == '':
        return
    elif response == 'y':
        return prev_team1
    else:
        return prev_team2



def main():
    with open('complete_bracket_sweet_16.pkl', 'r') as fh:
        slots_before = pickle.load(fh)

    game_slots = slots_before.copy()
    winners_added = 0
    for slot_id in xrange(64 + 32 + 16, 64 + 32 + 16 + 8):
        winner_of = game_slots.get_slot(slot_id)
        winning_team = choose_winner(winner_of, game_slots)
        if winning_team is not None:
            winners_added += 1
            game_slots.reset_slot(slot_id, winning_team)
    if winners_added != 4:
        raise ValueError('Expected to add 4 winners after the first'
                         'half of the Elite 8.')
    game_slots.save('complete_bracket_first_half_of_elite_8.pkl')


if __name__ == '__main__':
    main()
