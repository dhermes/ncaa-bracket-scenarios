import json
import logging

from google.appengine.ext import deferred
from google.appengine.ext import ndb
import webapp2

from base_handler import BaseHandler
from game_tree_classes import WinnerOf
from main import BracketContainer
from utils import all_possible_outcomes
from utils import get_scenario


with open('team_map.json.data', 'r') as fh:
    TEAM_MAP = json.load(fh)


class AdminPage(BaseHandler):

    def get(self):
        self.render_response('admin.templ')


class SelectLast(BaseHandler):

    def handle_get(self, how_many):
        kwargs = {'incorrect_url': False, 'finished': False}

        last_how_many = BracketContainer.get_or_insert_n(how_many)
        if last_how_many.bracket is not None:
            kwargs['finished'] = True
            kwargs['message'] = 'Last %d already selected' % how_many
        else:
            # Need this to move on
            one_more = BracketContainer.get_or_insert_n(how_many + 1)
            if one_more.bracket is None:
                kwargs['not_possible'] = True
                kwargs['message'] = ('No Last %d Bracket to go '
                                     'off of' % (how_many + 1))
            else:
                bracket = one_more.bracket
                undecided = get_undecided(bracket, range(120, 124))
                if len(undecided) + 3 != how_many:
                    kwargs['not_possible'] = True
                    kwargs['message'] = ('Last %d Bracket has wrong amount '
                                         'undecided' % (how_many + 1))
                else:
                    kwargs['how_many'] = how_many
                    kwargs['matchups'] = get_matchups(bracket, undecided)
        self.render_response('select_last.templ', **kwargs)

    def get(self, how_many):
        how_many = how_many.strip()
        if how_many not in ('4', '5', '6', '7'):
            self.render_response('select_last.templ', incorrect_url=True)
            return
        self.handle_get(int(how_many))

    def handle_post(self, how_many):
        one_more = BracketContainer.get_or_insert_n(how_many + 1)
        if one_more.bracket is not None:
            bracket = one_more.bracket.copy()
            undecided = get_undecided(bracket, range(120, 124))
            selected = {}
            for game_slot in undecided:
                value = self.request.params.get(str(game_slot))
                if value != 'null':
                    selected[str(game_slot)] = value
            if len(selected) == 1:
                slot_choices = map(int, selected.keys())
                validated = check_values(bracket, selected, slot_choices)
                for slot, team in validated.iteritems():
                    logging.info((slot, TEAM_MAP[team.team_id]))
                    bracket.reset_slot(slot, team)
                last_how_many = BracketContainer.get_or_insert_n(how_many)
                last_how_many.bracket = bracket
                last_how_many.put()
                run_it_all(last_how_many)
        self.redirect('/select-last-%d' % how_many)

    def post(self, how_many):
        how_many = how_many.strip()
        if how_many not in ('4', '5', '6', '7'):
            self.redirect('/')
            return
        self.handle_post(int(how_many))


class SelectElite8(BaseHandler):

    def get(self):
        kwargs = {'still_pending': True}
        elite_8 = BracketContainer.get_or_insert_n(8)
        if elite_8.bracket is not None:
            kwargs['still_pending'] = False
        else:
            sweet_16 = BracketContainer.get_or_insert_n(16)
            bracket = sweet_16.bracket
            if bracket is None:
                self.response.clear()
                self.response.set_status(500)
                return
            kwargs['matchups'] = get_matchups(bracket, range(112, 120))
        self.render_response('select_elite8.templ', **kwargs)

    def post(self):
        sweet_16 = BracketContainer.get_or_insert_n(16)
        if sweet_16.bracket is not None:
            bracket = sweet_16.bracket.copy()
            validated = check_values(bracket, self.request.params,
                                     range(112, 120))
            if validated is not None:
                for slot, team in validated.iteritems():
                    logging.info((slot, TEAM_MAP[team.team_id]))
                    bracket.reset_slot(slot, team)
                elite_8 = BracketContainer.get_or_insert_n(8)
                elite_8.bracket = bracket
                elite_8.put()
                run_it_all(elite_8)
        self.redirect('/select-elite-8')


def run_it_all(bracket_container, defer_now=True):
    if defer_now:
        deferred.defer(run_it_all, bracket_container, defer_now=False)
        return

    unfinished_game_slots = bracket_container.bracket
    all_outcomes = all_possible_outcomes(unfinished_game_slots)
    all_scenarios = [get_scenario(unfinished_game_slots, outcome)
                     for outcome in all_outcomes]
    bracket_container.scenarios = ''.join(all_scenarios)
    bracket_container.put()


def check_values(bracket, request_params, slot_choices):
    slots = {}
    for game_slot in slot_choices:
        value = request_params.get(str(game_slot))

        winner_of = bracket.get_slot(game_slot)
        team1 = bracket.get_slot(winner_of.game_slot1)
        team2 = bracket.get_slot(winner_of.game_slot2)
        if team1.team_id == value:
            slots[game_slot] = team1
        elif team2.team_id == value:
            slots[game_slot] = team2
        else:
            return None
    return slots


def get_matchups(bracket, slot_choices):
    matchups = []
    for game_slot in slot_choices:
        winner_of = bracket.get_slot(game_slot)
        team1 = bracket.get_slot(winner_of.game_slot1)
        team2 = bracket.get_slot(winner_of.game_slot2)
        team1_name = TEAM_MAP[team1.team_id]
        team2_name = TEAM_MAP[team2.team_id]
        matchup = (game_slot,
                   team1.team_id, team1_name,
                   team2.team_id, team2_name)
        matchups.append(matchup)
    return matchups


def get_undecided(bracket, slot_choices):
    undecided = []
    for game_slot in slot_choices:
        potential = bracket.get_slot(game_slot)
        if isinstance(potential, WinnerOf):
            undecided.append(game_slot)
    return undecided


routes = [
    ('/admin', AdminPage),
    ('/select-elite-8', SelectElite8),
    ('/select-last-(.*)', SelectLast),
]
app = webapp2.WSGIApplication(routes, debug=True)
