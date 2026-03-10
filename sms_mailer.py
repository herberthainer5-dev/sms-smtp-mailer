import smtplib
import json
import csv
from email.mime.text import MIMEText

print("SMTP SMS Mailer")

subject = input("Enter subject: ")

with open("smtp_config.json") as f:
    smtp = json.load(f)

with open("message.txt","r",encoding="utf8") as f:
    message_body = f.read()

server = smtplib.SMTP(smtp["host"], smtp["port"])
server.starttls()
server.login(smtp["username"], smtp["password"])

with open("numbers.csv") as f:
    reader = csv.DictReader(f)

    for row in reader:

        number = row["phone"]
        carrier = row["carrier"]

        address = f"{number}@{carrier}"

        msg = MIMEText(message_body)
        msg["From"] = smtp["username"]
        msg["To"] = address
        msg["Subject"] = subject

        try:
            server.sendmail(
                smtp["username"],
                address,
                msg.as_string()
            )

            print("Sent to", number)

        except Exception as e:
            print("Failed:", number, e)

server.quit()

print("Finished")
