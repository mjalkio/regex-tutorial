"""
Tutorial on Python regular expressions.

Taken from: https://www.dataquest.io/blog/regular-expressions-data-scientists/
"""
import re


def print_separator(section=None):
    """Print a separator for the tutorial sections."""
    sec = " {sec} ".format(sec=section) if section is not None else ''
    print("\n====={sec}=====".format(sec=sec))

with open('test_emails.txt', 'r') as f:
    test_emails = f.read()

print_separator("'From:' lines with plain Python")
for line in test_emails.split("\n"):
    if "From:" in line:
        print(line)

print_separator("'From:' lines using regex")
# . matches any character that isn't a newline
# * matches 0 or more of the preceding pattern
# re.findall returns a list of all matches
from_lines = re.findall(pattern="From:.*", string=test_emails)
for line in from_lines:
    print(line)

print_separator("Isolating the name")
for line in from_lines:
    # Original line: `print(re.findall("\".*\"", line))`
    # Match any string contained in quotes
    print(re.findall(pattern='".*"', string=line))

print_separator("Isolate the emails")
for line in from_lines:
    # \w matches alphanumeric characters...and the underscore
    # \S matches any non-whitespace character
    # These two follow the general pattern of lowercase letters matching
    # something, and uppercase letters matching the opposite.

    # The regex here is making the assumption that emails must start and end
    # with alphanumeric characters, so that it can avoid grabbing the <>
    # Honestly this doesn't seem like the ideal regex for this, but it works
    # I would probably write the pattern as "<.*>" and then trim the <>
    print(re.findall(pattern="\w\S*@.*\w", string=line))

print_separator("Understanding re.search")
# re.search returns the first match as a match object
match = re.search(pattern="From:.*", string=test_emails)
print(type(match))
print(type(match.group()))
# Fun fact: in Python3 this prints more info than in 2
print(match)
# Group does some crazy stuff
# The default is group(0), which returns the full match
# group(i) returns the ith match group
# You can even name groups!
print(match.group())

print_separator("re.split")
for item in from_lines:
    for line in re.findall("\w\S*@.*\w", item):
        # Not really doing anything worthy of regex here...
        username, domain = re.split("@", line)
        print("{username}, {domain}".format(username=username, domain=domain))

print_separator("re.sub")
address = match.group()
# Again, not really worthy of the regex here
email = re.sub(pattern="From", repl="Email", string=address)
print(address)
print(email)
