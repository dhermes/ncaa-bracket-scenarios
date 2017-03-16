from __future__ import print_function

import json
import os
import requests

import utils


BASE_URI = ('http://games.espn.com/tournament-challenge-bracket/'
            '2017/en/entry?entryID=')
BRACKETS_DIR = 'brackets_html'


def get_bracket_ids():
    with open('bracket_links.json', 'r') as fh:
        bracket_dict = json.load(fh)
    return bracket_dict.values()


def download_bracket(entry_id):
    filename = os.path.join(BRACKETS_DIR,
                            str(entry_id) + '.html')
    if os.path.exists(filename):
        msg = 'Exists: {}'.format(filename)
        print(msg)
        return

    uri = '%s%d' % (BASE_URI, entry_id)
    response = requests.get(uri)
    if response.status_code != 200:
        raise ValueError('Failed', response, entry_id)
    with open(filename, 'w') as fh:
        msg = 'Writing {}'.format(filename)
        print(msg)
        fh.write(response.content)
    response.close()


if __name__ == '__main__':
    utils.prepare_directory(BRACKETS_DIR)
    for entry_id in get_bracket_ids():
        download_bracket(entry_id)
