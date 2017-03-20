import os

import local_settings


BRACKET_LINKS_FILE = os.path.join(
    local_settings.YEAR, 'bracket_links.json')
TEAM_MAP_FILENAME = os.path.join(
    local_settings.YEAR, 'team_map.json')
BASE_BRACKET_PICKLE = os.path.join(
    local_settings.YEAR, 'base_bracket.pkl')
SWEET16_PICKLE = os.path.join(
    local_settings.YEAR, 'complete_bracket_sweet_16.pkl')
REDUCED_SCENARIOS = os.path.join(
    local_settings.YEAR, 'reduced_completed_scenarios.json')


def prepare_directory(dirname):
    if not os.path.isdir(dirname):
        msg = 'Creating {}'.format(dirname)
        print(msg)
        os.mkdir(dirname)
    else:
        msg = 'Already exists: {}'.format(dirname)
        print(msg)
