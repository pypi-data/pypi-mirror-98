#!/usr/bin/env python3
"""Update and sort the creators list of the zenodo record.

This script was originally developed by the nipreps developers.

For the full LICENSE and terms of use, see
https://github.com/nipreps/dmriprep/blob/master/LICENSE

"""
import sys
import shutil
from pathlib import Path
import json
from rapidfuzz import fuzz, process
import subprocess as sp

# These ORCIDs should go last
CREATORS_FIRST = ["Richie-Halford, Adam"]
CREATORS_LAST = ["Rokem, Ariel"]
# for entries not found in line-contributions
MISSING_ENTRIES = [
    {
        "affiliation": "Stanford University",
        "name": "Narayan, Manjari",
        "orcid": "0000-0001-5348-270X",
    },
    {
        "affiliation": "Stanford University",
        "name": "Yeatman, Jason",
        "orcid": "0000-0002-2686-1293",
    },
    {
        "affiliation": "The University of Washington",
        "name": "Simon, Noah",
        "orcid": "0000-0002-8985-2474",
    },
]

if __name__ == "__main__":
    contrib_file = Path("line-contributors.txt")
    lines = []
    if contrib_file.exists():
        print("WARNING: Reusing existing line-contributors.txt file.", file=sys.stderr)
        lines = contrib_file.read_text().splitlines()

    git_line_summary_path = shutil.which("git-summary")
    if not lines and git_line_summary_path:
        print("Running git-line-summary on the repo")
        lines = sp.check_output([git_line_summary_path]).decode().splitlines()
        contrib_file.write_text("\n".join(lines))

    if not lines:
        raise RuntimeError(
            """Could not find line-contributors from git repository.%s"""
            % """git-line-summary not found, please install git-extras. """
            * (git_line_summary_path is None)
        )

    data = [" ".join(line.strip().split()[1:-1]) for line in lines if "%" in line]

    # load zenodo from main
    zenodo_file = Path(".zenodo.json")
    zenodo = json.loads(zenodo_file.read_text())
    zen_names = [
        " ".join(val["name"].split(",")[::-1]).strip() for val in zenodo["creators"]
    ]
    total_names = len(zen_names) + len(MISSING_ENTRIES)

    name_matches = []
    position = 1 + len(CREATORS_FIRST)
    for ele in data:
        match = process.extractOne(
            ele, zen_names, scorer=fuzz.token_sort_ratio, score_cutoff=80
        )

        if match:
            val = zenodo["creators"][zen_names.index(match[0])]
        else:
            # skip unmatched names
            print("No entry to sort:", ele)
            continue

        if val not in name_matches:
            if val["name"] not in CREATORS_LAST and val["name"] not in CREATORS_FIRST:
                val["position"] = position
                position += 1
            elif val["name"] in CREATORS_LAST:
                val["position"] = total_names + CREATORS_LAST.index(val["name"])
            elif val["name"] in CREATORS_FIRST:
                val["position"] = CREATORS_FIRST.index(val["name"])
            name_matches.append(val)

    for missing in MISSING_ENTRIES:
        missing["position"] = position
        position += 1
        name_matches.append(missing)

    zenodo["creators"] = sorted(name_matches, key=lambda k: k["position"])
    # Remove position
    for creator in zenodo["creators"]:
        del creator["position"]

    zenodo_file.write_text("%s\n" % json.dumps(zenodo, indent=2, sort_keys=True))
