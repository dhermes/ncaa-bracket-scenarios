from __future__ import print_function

import argparse
import json


FILENAME_TEMPLATE = 'brackets_html/%s.json'
with open('team_map.json', 'r') as fh:
    TEAM_MAP = json.load(fh)
# Convert string keys to integers.
TEAM_MAP = {int(key): val for key, val in TEAM_MAP.items()}
ROUND_BREAKS = frozenset([64, 96, 112, 120, 124, 126, 127])


def main():
    parser = argparse.ArgumentParser(
        description='Check correctness of parse_brackets_html.py')
    parser.add_argument('--entry-id', dest='entry_id', required=True)
    args = parser.parse_args()
    bracket_filename = FILENAME_TEMPLATE % (args.entry_id,)

    with open(bracket_filename, 'r') as fh:
        winners = json.load(fh)
    winners = {int(key): val for key, val in winners.items()}

    for game_id in sorted(winners.keys()):
        if game_id in ROUND_BREAKS:
            print('=' * 60)
        winner_of = winners[game_id]
        winner_name = TEAM_MAP[winner_of]
        msg = '{:3d} -> {}'.format(game_id, winner_name)
        print(msg)


if __name__ == '__main__':
    main()
