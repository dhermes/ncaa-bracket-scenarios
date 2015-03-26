# ncaa-bracket-scenarios
Toy Project to Parse NCAA Group and Create Scenarios

## Pipeline For Computing Scenarios

1. Get the current year's field by running `get_team_mapping.py`. This
   may require updating the `NATIONAL_BRACKET` and the HTML parsers
   which pick out the teams. This creates `team_map.json` and a `.html`
   file with a filename corresponding to `NATIONAL_BRACKET`.

2. Run `get_bracket_pool.py` to download the HTML listing all of the
   pages of brackets in the pool. This will run a Selenium server since
   ESPN does not provide query parameters to page through the pool. This
   creates `.html` files in the `links_html/` folder with filenames
   corresponding to the bracket `GROUP_ID` (defined in `local_settings`).

3. Run `parse_bracket_links.py` to parse the HTML downloaded in step 2 and
   retrieve the bracket names and entry IDs. These will be stored in
   `bracket_links.json`.

## Install Instructions

pip install --upgrade selenium
