# email_reminder.py

import smtplib
from email.message import EmailMessage
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT, EMAIL_RECIPIENTS
from db_manager import get_all_applications
from datetime import datetime
import threading
import time

def send_email_reminder(subject, body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = ", ".join(EMAIL_RECIPIENTS)
    msg.set_content(body)

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def check_for_reminders():
    """Check for applications that need follow-up reminders."""
    applications = get_all_applications()
    today = datetime.now().date()

    for app in applications:
        follow_up_date = app[7]  # Follow-up date is the 8th column in the row
        if follow_up_date and datetime.strptime(follow_up_date, "%Y-%m-%d").date() == today:
            send_email_reminder(
                subject=f"Follow-Up Reminder for {app[1]} at {app[2]}",
                body=f"Don't forget to follow up for the {app[1]} position at {app[2]}.\nNotes: {app[8]}"
            )

def start_reminder_thread():
    def reminder_task():
        while True:
            check_for_reminders()
            time.sleep(86400)  # Check once every 24 hours

    reminder_thread = threading.Thread(target=reminder_task)
    reminder_thread.daemon = True  # Allows thread to exit when the main program exits
    reminder_thread.start()
