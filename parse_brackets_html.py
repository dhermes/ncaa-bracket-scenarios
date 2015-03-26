from BeautifulSoup import BeautifulSoup
import json
import os

import get_brackets_html
import get_team_mapping


def get_team_info(data_tag):
    # Modeled after get_team_mapping.get_data_slot_tags
    slot_id = int(data_tag['data-slotindex'])
    team_id = int(data_tag['data-teamid'])
    return slot_id, team_id


def get_slots(filename):
    with open(filename, 'r') as fh:
        soup = BeautifulSoup(fh.read())

    data_tags = soup.findAll(get_team_mapping.get_data_slot_tags)
    if len(data_tags) != 127:
        raise ValueError('Expected 127 slots in the bracket.')

    tag_info = [get_team_info(tag) for tag in data_tags]
    slot_winners = {}
    for slot_id, team_id in tag_info:
        if slot_id < 64:
            # Check assumption from get_team_mapping.py that
            # the team ID is 1 more than the slot ID.
            if slot_id + 1 != team_id:
                raise ValueError('Expected team ID to be 1 more than slot ID')
        else:
            slot_winners[slot_id] = team_id

    if sorted(slot_winners.keys()) != range(64, 127):
        raise ValueError('Expected winner slots to be [64 .. 126]')

    return slot_winners


def main():
    for entry_id in get_brackets_html.get_bracket_ids():
        json_filename = os.path.join(get_brackets_html.BRACKETS_DIR,
                                     str(entry_id) + '.json')
        if os.path.exists(json_filename):
            print 'Exists:', json_filename
            continue

        html_filename = os.path.join(get_brackets_html.BRACKETS_DIR,
                                     str(entry_id) + '.html')
        slot_winners = get_slots(html_filename)
        with open(json_filename, 'w') as fh:
            print 'Creating', json_filename
            json.dump(slot_winners, fh, indent=2, sort_keys=True,
                      separators=(',', ': '))


if __name__ == '__main__':
    main()
