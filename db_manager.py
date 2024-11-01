# db_manager.py

import sqlite3
from config import DATABASE_FILE

def create_tables():
    """Create job applications table if it doesn't exist."""
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_title TEXT,
                company TEXT,
                location TEXT,
                salary_range TEXT,
                application_date TEXT,
                status TEXT,
                follow_up_date TEXT,
                notes TEXT
            )
        """)
        # Create profile table
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS profile (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        skills TEXT,
                        experience INTEGER,
                        preferred_location TEXT,
                        preferred_roles TEXT
                    )
                """)
        conn.commit()

def add_application(job_title, company, location, salary_range, application_date, status, follow_up_date, notes):
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO applications (job_title, company, location, salary_range, application_date, status, follow_up_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (job_title, company, location, salary_range, application_date, status, follow_up_date, notes))
        conn.commit()

def update_application(application_id, job_title, company, location, salary_range, application_date, status, follow_up_date, notes):
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE applications
            SET job_title = ?, company = ?, location = ?, salary_range = ?, application_date = ?, status = ?, follow_up_date = ?, notes = ?
            WHERE id = ?
        """, (job_title, company, location, salary_range, application_date, status, follow_up_date, notes, application_id))
        conn.commit()

def get_all_applications():
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM applications")
        return cursor.fetchall()

# def delete_application(application_id):
#     with sqlite3.connect(DATABASE_FILE) as conn:
#         cursor = conn.cursor()
#         cursor.execute("DELETE FROM applications WHERE id = ?", (application_id,))
#         conn.commit()

def delete_application(application_id):
    """Delete an application by its ID from the database."""
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM applications WHERE id = ?", (application_id,))
        conn.commit()


def save_profile(name, skills, experience, preferred_location, preferred_roles):
    """Save or update profile information in the database."""
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()

        # Check if profile already exists
        cursor.execute("SELECT id FROM profile")
        existing_profile = cursor.fetchone()

        # If a profile exists, update it; otherwise, insert a new profile
        if existing_profile:
            cursor.execute("""
                UPDATE profile SET name = ?, skills = ?, experience = ?, preferred_location = ?, preferred_roles = ?
                WHERE id = ?
            """, (name, skills, experience, preferred_location, preferred_roles, existing_profile[0]))
        else:
            cursor.execute("""
                INSERT INTO profile (name, skills, experience, preferred_location, preferred_roles)
                VALUES (?, ?, ?, ?, ?)
            """, (name, skills, experience, preferred_location, preferred_roles))

        conn.commit()

def get_profile():
    """Fetch profile information from the database."""
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM profile")
        return cursor.fetchone()


