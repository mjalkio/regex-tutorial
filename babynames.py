"""Baby Names exercise.

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
"""

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import re


def extract_names(filename):
    """
    Extract names from an HTML file.

    Given a file name for baby.html, returns a list starting with the year
    string followed by the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
    """
    with open(filename) as f:
        file_contents = f.read()

    year_match = re.search(pattern='Popularity in (?P<year>\d+)',
                           string=file_contents)
    year = year_match.group('year')

    name_pattern = ('<td>(?P<rank>\d+)</td><td>'
                    '(?P<boy_name>[A-Z][a-z]+)</td>'
                    '<td>(?P<girl_name>[A-Z][a-z]+)</td>')
    names_match = re.findall(pattern=name_pattern, string=file_contents)
    ranks = {}
    for rank, boy_name, girl_name in names_match:
        rank = int(rank)
        # Names can be boy names and girl names at the same time
        # Want to make entries of rank unique, and choose the smallest rank
        if boy_name not in ranks or rank < ranks[boy_name]:
            ranks[boy_name] = rank
        if girl_name not in ranks or rank < ranks[girl_name]:
            ranks[girl_name] = rank

    return [year]


def main():
    """Run the code (previously did command line parsing...I removed that."""
    extracted_names = extract_names('baby1990.html')
    print('\n'.join(extracted_names))

if __name__ == '__main__':
    main()
