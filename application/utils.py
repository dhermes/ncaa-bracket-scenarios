import itertools
import json
import logging

from google.appengine.ext import ndb

from game_tree_classes import GameSlots
from game_tree_classes import Team
from game_tree_classes import WinnerOf


with open('team_map.json.data', 'r') as fh:
    TEAM_MAP = json.load(fh)
BOTTOM_BAR = ('=' * 30) + '\n\n'


class PotentialBracket(ndb.Model):
    year = ndb.IntegerProperty(default=2017, indexed=False)
    highest_names = ndb.StringProperty(repeated=True, indexed=False)
    highest_scores = ndb.IntegerProperty(repeated=True, indexed=False)
    lowest_names = ndb.StringProperty(repeated=True, indexed=False)
    lowest_scores = ndb.IntegerProperty(repeated=True, indexed=False)


def all_possible_outcomes(unfinished_game_slots):
    undecided_slots = []
    for game_slot in range(127):
        if isinstance(unfinished_game_slots.get_slot(game_slot), WinnerOf):
            undecided_slots.append(game_slot)

    all_outcomes = [GameSlots.copy(unfinished_game_slots)]
    for undecided_slot in undecided_slots:
        # Assume all GameSlots in the list have yet to
        # decide who wins "undecided_slot"
        initial_game = all_outcomes[0]
        winner_of = initial_game.get_slot(undecided_slot)

        # We will branch each GameSlots entry in all_outcomes to
        # two different GameSlots entries with a WinnerOf member
        # swapped out for a Team instance, and will ditch
        new_outcomes = []
        for outcome in all_outcomes:
            team1 = outcome.get_slot(winner_of.game_slot1)
            slot1_winner = GameSlots.copy(outcome)
            slot1_winner.reset_slot(undecided_slot, team1)

            team2 = outcome.get_slot(winner_of.game_slot2)
            slot2_winner = GameSlots.copy(outcome)
            slot2_winner.reset_slot(undecided_slot, team2)

            new_outcomes.extend([slot1_winner, slot2_winner])

        all_outcomes = new_outcomes

    return all_outcomes


def assumed_winners(unfinished_master_game_slots, guess_slots):
    assumptions = []
    for game_slot in range(127):
        if not isinstance(unfinished_master_game_slots.get_slot(game_slot),
                          Team):
            winner_of = unfinished_master_game_slots.get_slot(game_slot)
            opponent_ids = [
                guess_slots.get_slot(winner_of.game_slot1).team_id,
                guess_slots.get_slot(winner_of.game_slot2).team_id
            ]

            winning_team_id = guess_slots.get_slot(game_slot).team_id
            losing_team_ids = [id_ for id_ in opponent_ids
                               if id_ != winning_team_id]
            if len(losing_team_ids) != 1:
                raise Exception('Losing team not a single ID: %s' % game_slot)
            losing_team_id = losing_team_ids[0]

            message = '%s over %s' % (TEAM_MAP[winning_team_id],
                                      TEAM_MAP[losing_team_id])
            assumptions.append(message)

    return assumptions


def pretty_print(assumptions, winners, last_place):
    winners_row_messages = [
        '%d: %s - %d' % (index + 1, bracket_name, score)
        for index, (bracket_name, score) in enumerate(winners)
    ]
    winners_message = '\n'.join(winners_row_messages)
    last_place_row_messages = [
        'Last: %s - %d' % (bracket_name, score)
        for bracket_name, score in last_place
    ]
    last_place_message = '\n'.join(last_place_row_messages)
    assumptions_message = '\n'.join(['Assumptions:'] + assumptions)

    return '%s\n%s\n\n%s\n\n%s' % (winners_message, last_place_message,
                                   assumptions_message, BOTTOM_BAR)


def get_scenario(unfinished_master_game_slots, potential_finished_slots):
    assumptions = assumed_winners(unfinished_master_game_slots,
                                  potential_finished_slots)

    reduced = potential_finished_slots.reduced
    all_data = PotentialBracket.get_by_id(reduced)
    winners = zip(all_data.highest_names, all_data.highest_scores)
    # Pretty print actually expects the winners to be in the reverse
    # order they are stored.
    winners = reversed(winners)
    last_place = zip(all_data.lowest_names, all_data.lowest_scores)
    return pretty_print(assumptions, winners, last_place)
