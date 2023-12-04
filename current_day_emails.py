import imaplib, email
import time
import datetime as dt
from os import path
from datetime import timezone
import os
from dotenv import load_dotenv

load_dotenv()

user = os.environ.get('USER')
password = os.environ.get('PASSWORD')
imap_url = os.environ.get('IMAP_URL')

def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)

conn = imaplib.IMAP4_SSL(imap_url)
conn.login(user, password)
conn.select('INBOX')


lastDayDateTime = dt.datetime.now() - dt.timedelta(days=1)
dates = lastDayDateTime.strftime('%d-%b-%Y')

resp, items = conn.uid('search', None, f'(SENTSINCE {dates})')  # resp="OK", "items" is collection of email uids

if items[0]:
    # Get the UID of the latest email
    email_uids = items[0].split()

    if len(email_uids) > 0:
        f1 = open("gmail_mails.txt", "w+")
        email_count = 1

        for euid in email_uids:
            # Fetch the latest email using its UID
            result, data = conn.uid('fetch', euid, '(RFC822)')

            # Check if the fetch command was successful
            if result == 'OK':
                # Process the email as needed
                email_content = data[0][1].decode('utf-8')  # Assuming UTF-8 encoding
                raw = email.message_from_bytes(data[0][1])
                f1.write(f'Email no: {str(email_count)} \n')
                f1.write('Date: ' + raw['Date'] + '\n')
                f1.write('From: ' + raw['From'] + '\n')
                f1.write('Subject: ' + raw['Subject'] + '\n')
                normal_string = get_body(raw).decode('utf-8')
                f1.write('\nContent: \n' + normal_string + '\n')
                email_count += 1
            f1.write('\n'*10)

f1.close()
conn.logout()
