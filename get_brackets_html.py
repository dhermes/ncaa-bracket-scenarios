import json
import os
import requests


BASE_URI = ('http://games.espn.go.com/tournament-challenge-bracket/'
            '2016/en/entry?entryID=')
BRACKETS_DIR = 'brackets_html'


def prepare_directory():
    if not os.path.isdir(BRACKETS_DIR):
        print 'Creating', BRACKETS_DIR
        os.mkdir(BRACKETS_DIR)
    else:
        print 'Already exists:', BRACKETS_DIR


def get_bracket_ids():
    with open('bracket_links.json', 'r') as fh:
        bracket_dict = json.load(fh)
    return bracket_dict.values()


def download_bracket(entry_id):
    filename = os.path.join(BRACKETS_DIR,
                            str(entry_id) + '.html')
    if os.path.exists(filename):
        print 'Exists:', filename
        return

    uri = '%s%d' % (BASE_URI, entry_id)
    response = requests.get(uri)
    if response.status_code != 200:
        raise ValueError('Failed', response, entry_id)
    with open(filename, 'w') as fh:
        print 'Writing', filename
        fh.write(response.content)
    response.close()


if __name__ == '__main__':
    prepare_directory()
    for entry_id in get_bracket_ids():
        download_bracket(entry_id)
