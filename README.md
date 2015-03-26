# ncaa-bracket-scenarios
Toy Project to Parse NCAA Group and Create Scenarios

## Pipeline For Computing Scenarios

1. Get the current year's field by running `get_team_mapping.py`. This
   may require updating the `NATIONAL_BRACKET` and the HTML parsers
   which pick out the teams. This creates `team_map.json` and a `.html`
   file with a filename corresponding to `NATIONAL_BRACKET`.

1. Run `get_bracket_pool.py` to download the HTML listing all of the
   pages of brackets in the pool. This will run a Selenium server since
   ESPN does not provide query parameters to page through the pool. This
   creates `.html` files in the `links_html/` folder with filenames
   corresponding to the bracket `GROUP_ID` (defined in `local_settings`).

1. Run `parse_bracket_links.py` to parse the HTML downloaded in step 2 and
   retrieve the bracket names and entry IDs. These will be stored in
   `bracket_links.json`.

1. Run `get_brackets_html.py` to download the HTML for all the entries in the
   pool. These will be stored as `brackets_html/012345.html` where `012345`
   is a stand-in for the entry ID (which is unique for each year).

1. Run `parse_brackets_html.py` to parse each bracket's HTML to determine the
   winners of each game (slots 64 through 126). These will be stored as
   `brackets_html/012345.json` where `012345` is a stand-in for the entry
   ID (which is unique for each year).

   The correctness of this parser can be checked by running
   `python check_parse_brackets.py --entry-id=012345`.

1. Run `create_pickled_national_bracket.py` to create a bare bracket before
   any results have been recorded. This will create
   `complete_bracket_thru_63.pkl`.

## Install Instructions

pip install --upgrade selenium
