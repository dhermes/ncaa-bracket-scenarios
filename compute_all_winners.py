from __future__ import print_function

import json
import os

from game_tree_classes import _BASE64_ALPHABET
from game_tree_classes import Team
import get_brackets_html


def get_brackets():
    filename = 'reduced_all_filled_out.json'
    with open(filename, 'r') as fh:
        return json.load(fh)


def get_scenarios():
    filename = 'reduced_completed_scenarios.json'
    with open(filename, 'r') as fh:
        return json.load(fh)


def score_bracket(master, guess):
    if len(master) != 127 or len(guess) != 127:
        raise ValueError('Expected 127 slots.')
    if (master[:64] != _BASE64_ALPHABET or
        guess[:64] != _BASE64_ALPHABET):
        raise ValueError('Expected identical first 64 slots.')

    score = 0
    game_value = 10
    base_index = 64
    for games_per_round in (32, 16, 8, 4, 2, 1):
        next_index = base_index + games_per_round
        for position in xrange(base_index, next_index):
            if guess[position] == master[position]:
                score += game_value

        base_index = next_index
        # Double the score per game.
        game_value *= 2

    return score


def get_lowest(pair_list):
    """Gets the pairs with the lowest score.

    Assumes pair_list[0] has the lowest score and the score
    is the first element of the pair.
    """
    low_score = pair_list[0][0]
    result = []

    index = 0
    while pair_list[index][0] == low_score:
        result.append(pair_list[index])
        index += 1

    return result


def get_highest9(pair_list):
    """Gets the pairs with the highest 9 scores.

    If there is a tie for the 9th highest score, will return all that
    match it.

    Assumes pair_list[0] has the lowest score and the score
    is the first element of the pair.
    """
    cutoff_score = pair_list[-9][0]
    result = pair_list[-9:]

    index = -10
    while pair_list[index][0] == cutoff_score:
        result.insert(0, pair_list[index])
        index -= 1

    return result


def get_all_scores(master, brackets):
    results = []
    for entry_id, guess in brackets.items():
        curr_score = score_bracket(master, guess)
        results.append((curr_score, entry_id))
    results.sort(key=lambda pair: pair[0])

    lowest = get_lowest(results)
    highest = get_highest9(results)
    return lowest, highest


def main():
    brackets = get_brackets()
    scenarios = get_scenarios()

    to_store = {}
    count = 0
    for master in scenarios:
        count += 1
        if master in to_store:
            raise KeyError(master, 'already exists')
        lowest, highest = get_all_scores(master, brackets)
        to_store[master] = [lowest, highest]
        if count % 25 == 0:
            msg = 'Count: {}'.format(count)
            print(msg)

    filename = 'winning_scores.json'
    with open(filename, 'w') as fh:
        json.dump(to_store, fh, indent=2, sort_keys=True,
                  separators=(',', ': '))
    msg = 'Created {}'.format(filename)
    print(msg)


if __name__ == '__main__':
    main()
