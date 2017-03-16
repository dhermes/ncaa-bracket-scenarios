import os

import local_settings


BRACKET_LINKS_FILE = os.path.join(
    local_settings.YEAR, 'bracket_links.json')
TEAM_MAP_FILENAME = os.path.join(
    local_settings.YEAR, 'team_map.json')


def prepare_directory(dirname):
    if not os.path.isdir(dirname):
        msg = 'Creating {}'.format(dirname)
        print(msg)
        os.mkdir(dirname)
    else:
        msg = 'Already exists: {}'.format(dirname)
        print(msg)
