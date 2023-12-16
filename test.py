import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta

# Your email credentials
email_address = "tanjim.ashraf.doer.bp@gmail.com"
email_password = "tusa zabz pngh jqxi"

# IMAP server settings
imap_server = "imap.gmail.com"
mailbox = "inbox"

# Date to filter emails (replace 'your_date' with the actual date)
target_date = "08-Nov-2023"
target_date_obj = datetime.strptime(target_date, "%d-%b-%Y")

# Convert the date string to a datetime object
# target_date_obj = datetime.strptime(target_date_obj, "%Y-%m-%d")

# Connect to the IMAP server using SSL
mail = imaplib.IMAP4_SSL(imap_server)

# Log in to your email account
mail.login(email_address, email_password)

# Select the desired mailbox
mail.select(mailbox)

# Define the search criteria for the specified date
# search_criteria = f'(SINCE "{target_date}" BEFORE "{(target_date_obj + timedelta(days=1)).strftime("%Y-%m-%d")}")'
search_criteria = f'(SINCE "{target_date}" BEFORE "{(target_date_obj + timedelta(days=1)).strftime("%d-%b-%Y")}")'


# Search for emails based on the criteria
status, messages = mail.search(None, search_criteria)

# Get the list of email IDs
email_ids = messages[0].split()

# Fetch and print the details of each email
for email_id in email_ids:
    status, msg_data = mail.fetch(email_id, "(RFC822)")
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            email_message = email.message_from_bytes(response_part[1])
            subject, encoding = decode_header(email_message["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")
            from_address, encoding = decode_header(email_message.get("From", ""))[0]
            if isinstance(from_address, bytes):
                from_address = from_address.decode(encoding or "utf-8")
            date_sent = email.utils.parsedate(email_message["Date"])
            date_sent_obj = datetime(*date_sent[:6])
            
            # Check if the email date matches the target date
            if date_sent_obj.date() == target_date_obj.date():
                print("Subject:", subject)
                print("From:", from_address)
                print("Date:", date_sent)
                print("=" * 40)

# Logout from the email server
mail.logout()
