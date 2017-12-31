"""
Tutorial on Python regular expressions with Pandas.

Taken from: https://www.dataquest.io/blog/regular-expressions-data-scientists/
"""
import email
import re

import pandas as pd


def get_sender_data(fraud_email):
    """Return a dictionary with sender data for the email."""
    # Step 1: find the whole line beginning with "From:".
    sender = re.search(r"From:.*", fraud_email)

    # Step 2: find the email address and name.
    if sender is not None:
        sender_email = re.search(r"\w\S*@.*\w", sender.group())
        sender_name = re.search(r":.*<", sender.group())
    else:
        sender_email = None
        sender_name = None

    # Step 3A: assign email address as string to a variable.
    if sender_email is not None:
        sender_email = sender_email.group()

    # Step 3B: remove unwanted substrings, assign to variable.
    if sender_name is not None:
        # Remove the colon and any whitespace characters
        sender_name = re.sub(":\s*", "", sender_name.group())
        # Remove whitespace characters and the angle bracket on the other side
        sender_name = re.sub("\s*<", "", sender_name)
        # Remove the quotes too...
        sender_name = sender_name.strip('"')

    return {
        'sender_name': sender_name,
        'sender_email': sender_email,
    }

email_data = []

with open('test_emails.txt', 'r') as f:
    content = f.read()

emails = re.split("From r", content)
emails.pop(0)  # Remove the first empty string

for fraud_email in emails:
    data = {}
    data.update(get_sender_data(fraud_email))
    print(data)
