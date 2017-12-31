"""
Tutorial on Python regular expressions with Pandas.

Taken from: https://www.dataquest.io/blog/regular-expressions-data-scientists/
"""
import re
from email import message_from_string as email_message_from_string

import pandas as pd


def _parse_name_and_email(line):
    email = re.search(r"\w\S*@.*\w", line)
    if email is not None:
        email = email.group()

    name = re.search(r":.*<", line)
    if name is not None:
        # Remove the colon and any whitespace characters
        name = re.sub(":\s*", "", name.group())
        # Remove whitespace characters and the angle bracket on the other side
        name = re.sub("\s*<", "", name)
        # Remove the quotes too...
        name = name.strip('"')

    return (name, email)


def get_sender_data(fraud_email):
    """Return a dictionary with sender data for the email."""
    sender = re.search("From:.*", fraud_email)
    if sender is not None:
        sender_name, sender_email = _parse_name_and_email(sender.group())
    else:
        sender_name, sender_email = None, None

    return {
        'sender_name': sender_name,
        'sender_email': sender_email,
    }


def get_recipient_data(fraud_email):
    """Return a dictionary with recipient data for the email."""
    recipient = re.search("To:.*", fraud_email)
    if recipient is not None:
        line = recipient.group()
        recipient_name, recipient_email = _parse_name_and_email(line)

    return {
        'recipient_name': recipient_name,
        'recipient_email': recipient_email,
    }


def get_date_sent_data(fraud_email):
    """Return a dictionary with the date data for the email."""
    date = re.search(r"Date:.*", fraud_email)
    if date is not None:
        # \d is any decimal digit
        # + matches 1 or more of the preceding regex
        # 1+ digit, one whitespace, 1+ alphanumeric, one whitespace, 1+ digit
        date = re.search(r"\d+\s\w+\s\d+", date.group())
        if date is not None:
            date = date.group()

    return {'date_sent': date}


def get_subject_data(fraud_email):
    """Return a dictionary with the subject data for the email."""
    subject = re.search(r"Subject: .*", fraud_email)

    if subject is not None:
        subject = re.sub(r"Subject: ", "", subject.group())

    return {'subject': subject}


def get_email_body(fraud_email):
    """Return a dictionary with the email body for the email."""
    full_email = email_message_from_string(fraud_email)
    body = full_email.get_payload()
    return {'email_body': body}


def get_emails_from_domains(emails_df, domains):
    """Return subset of emails_df where the sender's domain is in domains."""
    # The bar is a regex "OR"
    domains = '|'.join(domains)
    return emails_df[emails_df['sender_email'].str.contains(domains)]

if __name__ == '__main__':
    email_data = []

    with open('test_emails.txt', 'r') as f:
        content = f.read()

    emails = re.split("From r", content)
    emails.pop(0)  # Remove the first empty string

    for fraud_email in emails:
        data = {}
        for fn in (get_sender_data, get_recipient_data, get_date_sent_data,
                   get_subject_data, get_email_body):
            data.update(fn(fraud_email))
        email_data.append(data)

    emails_df = pd.DataFrame(email_data)

    print(emails_df.head(n=3))
    print(get_emails_from_domains(emails_df=emails_df,
                                  domains=['maktoob', 'spinfinder']))
