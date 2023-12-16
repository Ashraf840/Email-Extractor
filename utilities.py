import imaplib, email
import os
from dotenv import load_dotenv
import datetime as dt
from check_last_read_mail_date import latest_mail_reading_date
from datetime import datetime, timedelta

load_dotenv()


def get_environment_variables():
    email_address = os.environ.get('EMAIL_ADDRESS')
    password = os.environ.get('PASSWORD')
    imap_url = os.environ.get('IMAP_URL')
    return email_address, password, imap_url


class EmailExtractor:
    def __init__(self, mailbox_type):
        self.email_address, self.password, self.imap_url = get_environment_variables()
        # Use a try/catch block for different edge cases (auth-fail; net-conn-error)
        self.conn = imaplib.IMAP4_SSL(self.imap_url)
        self.conn.login(self.email_address, self.password)
        self.conn.select(mailbox_type)
        # print("Welcome to email extractor!")
    
    def mail_logout(self):
        self.conn.logout()

    def get_body(self, msg):
        if msg.is_multipart():
            return self.get_body(msg.get_payload(0))
        else:
            return msg.get_payload(None, True)
    
    def config_date(self):
        lastDayDateTime = dt.datetime.now()
        dates = lastDayDateTime.strftime('%d-%b-%Y')
        return dates

    def extract_emails(self, dates):
        email_list = []     # NB: Might require to use pandas.series while working in big thing
        # dates = self.config_date()
        
        print("date:", dates)
        dates_obj = datetime.strptime(dates, "%d-%b-%Y")

        # # [Can make a separate method]
        # resp, items = self.conn.uid('search', None, f'(SENTSINCE {dates})')   # Original: OK
        

        # resp, items = self.conn.uid(None, search_criteria)
        # resp, items = self.conn.uid('search', None, f'(SENTSINCE {dates} BEFORE "{(dates_obj + timedelta(days=1)).strftime("%d-%b-%Y")}")')


        # # [Can make a separate method]
        search_criteria = f'(SENTSINCE "{dates}" BEFORE "{(dates_obj + timedelta(days=1)).strftime("%d-%b-%Y")}")'
        print("Search criteria:", search_criteria)
        resp, items = self.conn.uid('search', None, search_criteria)

        if resp == "OK":
            email_uids = items[0].split()
            if len(email_uids) > 0:
                for euid in email_uids:
                    result, data = self.conn.uid('fetch', euid, '(RFC822)')
                    if result == 'OK':
                        email_content = data[0][1].decode('utf-8')
                        raw = email.message_from_bytes(data[0][1])
                        normal_string = self.get_body(raw).decode('utf-8')
                        email_dict = dict(UID = euid, Date = raw['Date'], From = raw['From'], Subject = raw['Subject'], Content = normal_string)
                        email_list.append(email_dict)
        self.mail_logout()
        return email_list


# # Uncomment while executing this file only
# ee = EmailExtractor("INBOX")

# emails_list = ee.extract_emails(latest_mail_reading_date())
# print("list length:", len(emails_list))

# for el in emails_list:
#     print("Email Subject:", el['Subject'])
