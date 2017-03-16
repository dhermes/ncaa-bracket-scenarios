from __future__ import print_function

import base64
import codecs
import os
import time

from selenium import webdriver

from local_settings import GROUP_ID


BASE_URI = ('http://games.espn.com/tournament-challenge-bracket/'
            '2017/en/group?groupID=')
GROUP_URI = '%s%d' % (BASE_URI, GROUP_ID)

LINKS_DIR = 'links_html'
BASE_FILENAME = os.path.join(LINKS_DIR, base64.b64encode(GROUP_URI))


def prepare_directory():
    if not os.path.isdir(LINKS_DIR):
        msg = 'Creating {}'.format(LINKS_DIR)
        print(msg)
        os.mkdir(LINKS_DIR)
    else:
        msg = 'Already exists: {}'.format(LINKS_DIR)
        print(msg)


def _write_content(driver, page_number):
    filename = '%s-%02d.html' % (BASE_FILENAME, page_number)
    with codecs.open(filename, 'w', 'utf-8') as fh:
        msg = 'Writing to {}'.format(filename)
        print(msg)
        fh.write(driver.page_source)


def _get_current_page(driver):
    try:
        pg_num_elts = driver.find_elements_by_class_name('pageNumber')
        curr_page, = [elt for elt in pg_num_elts
                      if elt.tag_name == 'strong']
        return int(curr_page.text)
    except:
        # In the case that the driver becomes unattached partway through,
        # we catch any possible exception.
        return -1


def _click_next(driver, page_number):
    """Clicks next page link (JS only).

    Returns boolean indicating if another page exists.
    """
    curr_page = _get_current_page(driver)
    if curr_page != page_number:
        raise ValueError('Expected page number to match.')

    next_page_links = driver.find_elements_by_class_name('nextPage')
    if len(next_page_links) == 0:
        return False
    elif len(next_page_links) != 1:
        raise ValueError('Expected exactly one next page link.')

    # Increment before clicking.
    page_number += 1
    next_page_links[0].click()
    while _get_current_page(driver) != page_number:
        print('New page has not loaded. Sleeping 0.5 seconds.')
        time.sleep(0.5)

    return True


def _get_all_pages(driver):
    driver.get(GROUP_URI)

    page_number = 1
    _write_content(driver, page_number)

    while _click_next(driver, page_number):
        page_number += 1
        _write_content(driver, page_number)


def get_all_pages():
    driver = webdriver.Firefox()
    try:
        _get_all_pages(driver)
    finally:
        driver.close()


if __name__ == '__main__':
    prepare_directory()
    get_all_pages()
