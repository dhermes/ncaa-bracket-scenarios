from BeautifulSoup import BeautifulSoup
import base64
import json
import os
import requests


NATIONAL_BRACKET = ('http://games.espn.com/tournament-challenge-bracket/'
                    '2017/en/entry?entryID=115703')
FILENAME = base64.b64encode(NATIONAL_BRACKET) + '.html'
SLOT_KEY = 'data-slotindex'


def get_national_bracket():
    if not os.path.exists(FILENAME):
        response = requests.get(NATIONAL_BRACKET)
        with open(FILENAME, 'w') as fh:
            fh.write(response.content)
        response.close()
    with open(FILENAME, 'r') as fh:
        return fh.read()


def get_team_info(data_tag):
    """Returns ({teamID}, {team name}) from a node."""
    name_span, = data_tag.findAll('span', {'class': 'name'})
    team_name = name_span.text
    slot_id = int(data_tag[SLOT_KEY])
    # NOTE: Assumes the team ID is 1 more than the slot ID.
    team_id = slot_id + 1
    return team_id, team_name


def get_data_slot_tags(tag):
    if tag.name != 'a':
        return False
    return tag.has_key(SLOT_KEY)


def parse_teams():
    bracket_html = get_national_bracket()
    soup = BeautifulSoup(bracket_html)

    data_tags = soup.findAll(get_data_slot_tags)
    opening_round_tags = [tag for tag in data_tags
                          if int(tag[SLOT_KEY]) < 64]
    assert len(opening_round_tags) == 64
    team_info = [get_team_info(data_tag) for data_tag in
                 opening_round_tags]
    team_info = dict(set(team_info))

    with open('team_map.json', 'w') as fh:
        json.dump(team_info, fh, indent=2, sort_keys=True,
                  separators=(',', ': '))


if __name__ == '__main__':
    parse_teams()
