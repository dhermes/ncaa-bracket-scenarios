import os
import glob
import json

from BeautifulSoup import BeautifulSoup

import get_bracket_pool
import utils


def get_links(links, filename):
    """Updates links with those found in filename."""
    with open(filename, 'r') as fh:
        soup = BeautifulSoup(fh.read())

    entry_links = soup.findAll('a', {'class': 'entry'})
    for anchor in entry_links:
        bracket_name = anchor.text
        if bracket_name in links:
            raise KeyError(bracket_name, 'already exists')

        bracket_link = anchor['href']
        before, entry_id = bracket_link.split('entry?entryID=', 1)
        if before != '':
            raise ValueError('Expected link to begin with entry?...')
        entry_id = int(entry_id)
        links[bracket_name] = entry_id


def get_all_bracket_links():
    all_filenames = glob.glob(get_bracket_pool.BASE_FILENAME + '*')
    links = {}
    for filename in all_filenames:
        get_links(links, filename)

    # check_unique_entries
    if len(set(links.values())) != len(links):
        raise ValueError('Link entry IDs not unique.')

    return links


if __name__ == '__main__':
    links = get_all_bracket_links()
    with open(utils.BRACKET_LINKS_FILE, 'w') as fh:
        json.dump(links, fh, indent=2, sort_keys=True,
                  separators=(',', ': '))
