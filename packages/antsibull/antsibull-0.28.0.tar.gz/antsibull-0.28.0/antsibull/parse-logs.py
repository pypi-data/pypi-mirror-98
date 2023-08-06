#!/usr/bin/python3 -tt

# Script to parse the antsibull log and gather the number of times each of the macros were used in
# a run of the docs build.

import json
import re
from collections import Counter


# The standard format of the log file is structured data:
#
# 2021-01-05T17:45:43Z:INFO:antsibull:counts={'italic': 0, 'bold': 0, 'module': 0, 'url': 0, 'ref': 0, 'link': 0, 'const': 0, 'ruler': 0}:func=html_ify:mod=antsibull.jinja2.filters|Number of macros converted to rst equivalents
#
# We could write a parser for it but this regex is sufficient to grab the data field that we're
# interested in for now.

content = re.compile('^.*INFO:antsibull:counts=({.*}):func=.*')

totals = Counter()
with open('macros-data', 'r') as f:
    for line in f:
        data = content.match(line)
        if not data:
            # Right now, the only thing that we log is information that we're interested in.  Once the
            # logs are expanded in the future, we'll need to ignore the extraneous lines instead of
            # raising an exception.
            raise Exception(f'Line with no data: {line}')

        data = data.group(1)
        # Want to use json to parse the data so we need to change single quotes to double quotes
        data = data.translate({ord("'"): '"'})
        new_counts = Counter(json.loads(data))
        totals += new_counts

print(totals)
