import datetime as dt

with open("gmail_time.txt") as f:
    latest_mail_reader_date = f.readlines()
    # print("Latest gmail reading time:", latest_mail_reader_date)
    if len(latest_mail_reader_date) > 0:
        print("Not empty!")
        print("Current datetime:", latest_mail_reader_date)
    else:
        current_date_time = dt.datetime.now().date()
        current_date_time = current_date_time.strftime('%d-%b-%Y')
        print("Empty!")
        print("Current datetime:", current_date_time)

        f1 = open("gmail_time.txt", "w+")
        f1.write(current_date_time)
        f1.close()



f.close()