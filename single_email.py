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

# date_time = dt.datetime.now()

# f = open("gmail_time.txt", "r")
# a = f.read()
# f.close()

# # print('a:', a)
# # print('Type:', type(a))
# # print('Length:', len(a))
# if len(a) == 0:
#     # print('Current Time:', dt.datetime.now())
#     a = str(dt.datetime.now())
#     print("dt.datetime.strptime()", dt.datetime.strptime(a, '%a, %d %b %Y %H:%M:%S %z'))
# else:
#     print('Time from "gmail_time.txt" file:', a)

# b = str(dt.datetime.now())
# b_formatted = dt.datetime.strptime(b, '%a, %d %b %Y %H:%M:%S %z')
# print('Current Time:', b_formatted)

# a = dt.datetime.strptime(a, '%a, %d %b %Y %H:%M:%S %z')

# date_time.replace(tzinfo=timezone.utc)

# date_time = date_time.replace(tzinfo=timezone.utc).isoformat()

# date_time = dt.datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%S.%f%z')

# lastDayDateTime = date_time - a

conn = imaplib.IMAP4_SSL(imap_url)
conn.login(user, password)
conn.select('INBOX')

# dates = (dt.datetime.now() - lastDayDateTime).strftime('%d-%b-%Y')
# dates = (dt.datetime.now() - lastDayDateTime).strftime('%d-%b-%Y')

lastDayDateTime = dt.datetime.now() - dt.timedelta(days=1)
dates = lastDayDateTime.strftime('%d-%b-%Y')

resp, items = conn.uid('search', None, f'(SENTSINCE {dates})')

if items[0]:
    # Get the UID of the latest email
    latest_email_uid = items[0].split()[-1]

    # Fetch the latest email using its UID
    result, data = conn.uid('fetch', latest_email_uid, '(RFC822)')

    # Check if the fetch command was successful
    if result == 'OK':
        # Process the email as needed
        email_content = data[0][1].decode('utf-8')  # Assuming UTF-8 encoding
        # print("Email Content:", email_content)
        raw = email.message_from_bytes(data[0][1])
        # print('Email Content:', raw)
        f1 = open("gmail_mails.txt", "w+")
        f1.write('Date: ' + raw['Date'] + '\n')
        f1.write('From: ' + raw['From'] + '\n')
        f1.write('Subject: ' + raw['Subject'] + '\n')
        normal_string = get_body(raw).decode('utf-8')
        f1.write('\nContent: \n' + normal_string + '\n')
        # f1.write('Content = ' + str(get_body(raw)) + '\n')
        # f1.write(' ')
        f1.close()
        conn.logout()
# print(conn.uid())
# resp, items = conn.uid('search', None, '(SENTSINCE {dates})'.format(date=dates))
# print(items)


# dates = '02-Dec-2023'
# resp, items = conn.uid('search', None, '(SENTSINCE {dates})'.format(date=dates))

# a = items
# b = a[0].decode('utf-8')
# b = b.split(" ")
# f1 = open("gmail_mails.txt", "w+")


# for value in b:
#     late = int(value) - 801
#     late = str(late)
#     result, data = conn.fetch(late, '(RFC822)')
#     raw = email.message_from_bytes(data[0][1])
#     print(raw['Date'])
#     print(raw['From'])
#     print(raw['Body'])
#     f1.write('Date =', raw['Date'] + ' ')
#     f1.write('From =', raw['From'] + ' ')
#     f1.write('Subject =', raw['Subject'] + ' ')
#     f1.write('Body =', str(get_body(raw)) + ' ')
#     f1.write(' ')
# f1.close()
# f2 = open('gmail_time.txt', 'w+')
# f2.write(raw['Date'])
# f2.close()
# conn.logout()
