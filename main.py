# main.py

from gui import JobTrackerApp
from db_manager import create_tables
from email_reminder import check_for_reminders

if __name__ == "__main__":
    create_tables()
    check_for_reminders()  # Sends email reminders if any follow-up dates match today
    app = JobTrackerApp()
    app.mainloop()
