import datetime as dt


def latest_mail_reading_date():
    with open("gmail_time.txt") as f:
        latest_mail_reader_date = f.readlines()
        # print("Latest gmail reading time:", latest_mail_reader_date)
        f1 = open("gmail_time.txt", "w+")
        
        if len(latest_mail_reader_date) > 0:
            # print("Not empty!")
            # print("file_stored_current_date:", latest_mail_reader_date)
            modified_date = dt.datetime.strptime(f'{latest_mail_reader_date[0]}', "%d-%b-%Y").date() - dt.timedelta(days=1)
            modified_date = modified_date.strftime('%d-%b-%Y')
            # print("Modified date:", modified_date)
            f1.write(modified_date)
            # f.close()   # While using the "with" statement, explicitly defining the file closing is optional. The "with" statement ensures the file is properly closed.
            return modified_date
        else:
            current_date_time = dt.datetime.now().date()
            current_date_time = current_date_time.strftime('%d-%b-%Y')
            # print("Empty!")
            # print("Current datetime:", current_date_time)
            f1.write(current_date_time)
            # f.close()   # While using the "with" statement, explicitly defining the file closing is optional. The "with" statement ensures the file is properly closed.
            return current_date_time
        

# print(latest_mail_reading_date())