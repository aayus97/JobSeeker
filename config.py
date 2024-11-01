# config.py
import os

# Database file
DATABASE_FILE = "job_applications.db"

# Email settings
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "paudelaayus@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "Monochromo123")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
EMAIL_RECIPIENTS = [EMAIL_ADDRESS]  # Add multiple recipients if needed
