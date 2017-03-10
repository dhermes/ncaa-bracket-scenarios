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
   any results have been recorded. This will create `base_bracket.pkl`.
   (This file does not depend on the teams in the field, so this step
    can be skipped, as the file will be checked in to the repository.)

1. Run `update_national_bracket.py` to enter winners through the Sweet 16.
   This will create `complete_bracket_sweet_16.pkl`.

1. Run `first_half_of_elite_8.py` to enter winners from the first day of
   the Elite 8. This creates `complete_bracket_first_half_of_elite_8.pkl`.
   Note this leaves 4 games left in the Sweet 16, then 4 in Elite 8, then
   2, then 1. In total, there are 11 left, with 2**11 = 2048 possible
   outcomes left.

1. Run `run_all_scenarios.py` to compute all possible remaining outcomes
   (should be 2048). Creates the outcomes serialized as
   `reduced_completed_scenarios.json`.

1. Run `entries_as_reduced.py` to store all the entries in the bracket pool
   in reduced form (same serialization as in previous step). This will
   create `reduced_all_filled_out.json`.

1. Run `compute_all_winners.py` to actually compute the top scores and lowest
   scores for each possible scenario. This creates the file
   `winning_scores.json`.

1. Run `write_winners_to_datastore.py`. This will write all the possible
   outcomes to the datastore. Requires setting the string `DATASET_ID` in
   the file `local_settings.py` (and making sure auth works with
   `google-cloud-python`).

1. Run `write_sweet16_to_datastore.py`. This will write the bracket
   to the datastore using `complete_bracket_sweet_16.pkl`. This is then used
   in the GUI to select the Elite 8. (Note we already know half the teams in
   the Elite 8, this allowed us to only have to compute 2048 outcomes.
   However, it is easiest to use the existing admin UI to select Elite 8 from
   the Sweet 16 games.)

## Deploy Instructions

```
$ gcloud app deploy path/to/application/app.yaml --version ${CURRENT_YEAR}
```

## Install Instructions

```
pip install --upgrade selenium google-cloud-datastore requests BeautifulSoup
```
