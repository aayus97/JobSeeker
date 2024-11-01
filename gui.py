# gui.py

# import requests
# from spacy.matcher import Matcher
# from textblob import TextBlob
# import spacy
# import tkinter as tk
# from tkinter import messagebox, ttk
# from db_manager import add_application, update_application, get_all_applications, delete_application
# from db_manager import save_profile, get_profile
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import matplotlib.pyplot as plt
# from nltk.tokenize import sent_tokenize
# from transformers import pipeline
#
# import nltk
#
# # Check and download 'punkt' if not already available
# try:
#     nltk.data.find('tokenizers/punkt')
# except LookupError:
#     nltk.download('punkt')
#
# from email_reminder import start_reminder_thread
# from dashboard import create_status_pie_chart, create_applications_over_time_chart
#
#
# # Load spaCy model
# nlp = spacy.load("en_core_web_sm")
#
# # Initialize the Hugging Face zero-shot classification pipeline
# classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
#
#
# # Define the function to extract job details using zero-shot classification
# def extract_job_details_nlp(email_content):
#     # Split the email content into individual sentences
#     sentences = sent_tokenize(email_content)
#
#     # Define the labels (job detail categories) we want to classify each sentence into
#     labels = ["Job Title", "Company", "Location", "Salary", "Application Date", "Status", "Follow-Up Date", "Notes"]
#
#     # Initialize an empty dictionary to store classified job details
#     job_details = {label: "" for label in labels}
#     job_details["Notes"] = email_content  # Default the notes to the entire email
#
#     # Classify each sentence
#     for sentence in sentences:
#         # Get classification results for the sentence
#         result = classifier(sentence, labels)
#         best_label = result["labels"][0]
#         best_score = result["scores"][0]
#
#         # Threshold for confidence; only assign the label if the score is above this threshold
#         confidence_threshold = 0.5
#
#         if best_score > confidence_threshold:
#             # If the job detail for this label is empty, assign the sentence
#             if job_details[best_label] == "":
#                 job_details[best_label] = sentence
#             else:
#                 # Otherwise, append it to any existing content
#                 job_details[best_label] += " " + sentence
#
#     # Display final classified job details
#     for label, content in job_details.items():
#         print(f"{label}: {content}")
#
#     return job_details



import nltk
import requests
from spacy.matcher import Matcher
from textblob import TextBlob
import spacy
import tkinter as tk
from tkinter import messagebox, ttk
from db_manager import add_application, update_application, get_all_applications, delete_application
from db_manager import save_profile, get_profile
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from transformers import pipeline

import os

from nltk.tokenize import sent_tokenize
from email_reminder import start_reminder_thread
from dashboard import create_status_pie_chart, create_applications_over_time_chart

# Specify the directory for nltk_data
nltk_data_path = '/Users/pratistha99/nltk_data'
if not os.path.exists(nltk_data_path):
    os.makedirs(nltk_data_path)

# Add the path to nltk's data path
nltk.data.path.append(nltk_data_path)

# Force download 'punkt' directly
nltk.download('punkt', download_dir=nltk_data_path)



# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize the Hugging Face zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


# Define the function to extract job details using zero-shot classification
def extract_job_details_nlp(email_content):
    # Ensure 'punkt' is downloaded
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

    # Split the email content into individual sentences
    sentences = sent_tokenize(email_content)

    # Define the labels (job detail categories) we want to classify each sentence into
    labels = ["Job Title", "Company", "Location", "Salary", "Application Date", "Status", "Follow-Up Date", "Notes"]

    # Initialize an empty dictionary to store classified job details
    job_details = {label: "" for label in labels}
    job_details["Notes"] = email_content  # Default the notes to the entire email

    # Classify each sentence
    for sentence in sentences:
        # Get classification results for the sentence
        result = classifier(sentence, labels)
        best_label = result["labels"][0]
        best_score = result["scores"][0]

        # Threshold for confidence; only assign the label if the score is above this threshold
        confidence_threshold = 0.5

        if best_score > confidence_threshold:
            # If the job detail for this label is empty, assign the sentence
            if job_details[best_label] == "":
                job_details[best_label] = sentence
            else:
                # Otherwise, append it to any existing content
                job_details[best_label] += " " + sentence

    # Display final classified job details
    for label, content in job_details.items():
        print(f"{label}: {content}")

    return job_details


class JobTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Job Application Tracker")
        self.geometry("1000x800")

        # Set up Frames for better layout organization
        self.setup_frames()

        # Configure treeview for displaying applications
        self.setup_treeview()

        # Set up the profile form for personal details
        self.setup_profile_form()

        # Set up the form for adding new applications
        self.setup_form()

        # Set up search functionality
        self.setup_search()

        # Load initial data
        self.display_applications()

        # Display Dashboard
        self.display_dashboard()

        self.setup_email_content_extraction()



    def fetch_relevant_jobs(self):
        """Fetch relevant jobs based on profile using the JSearch API on RapidAPI."""
        # Get profile data from form fields
        profile = {
            "skills": self.skills_var.get(),
            "preferred_location": self.preferred_location_var.get()
        }

        # Fetch jobs using JSearch API
        jobs = fetch_jobs_from_api(profile)

        # Format the job list for display
        if jobs:
            job_text = "\n\n".join(
                [f"{job['title']} at {job['company']} ({job['location']})\nApply here: {job['link']}" for job in jobs]
            )
        else:
            job_text = "No matching jobs found!"

        # Show the relevant jobs in a message box
        messagebox.showinfo("Recommended Jobs", job_text)


    def setup_frames(self):
        """Create frames to organize the layout."""
        # Top frame for search and filter
        self.top_frame = tk.Frame(self, padx=10, pady=5)
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Center frame for application list (treeview)
        self.center_frame = tk.Frame(self, padx=10, pady=5)
        self.center_frame.grid(row=1, column=0, sticky="nsew")

        # Right frame for dashboard
        self.dashboard_frame = tk.Frame(self, padx=10, pady=5, relief=tk.GROOVE, bd=2)
        self.dashboard_frame.grid(row=1, column=1, sticky="nsew")

        # Bottom frame for the form
        self.bottom_frame = tk.Frame(self, padx=10, pady=10, relief=tk.SUNKEN, bd=1)
        self.bottom_frame.grid(row=2, column=0, columnspan=2, sticky="ew")


        # Allow resizing
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)


    def setup_email_content_extraction(self):
        """Add a multi-line text field and a button to populate fields from email content."""
        # Label for email content
        tk.Label(self.bottom_frame, text="Paste Email Content Here:").grid(row=10, column=0, sticky="w", padx=5, pady=5)

        # Text widget for multi-line input
        self.email_content_text = tk.Text(self.bottom_frame, wrap="word", width=50, height=10)
        self.email_content_text.grid(row=11, column=0, columnspan=2, padx=5, pady=5)

        # Button to extract and populate job details
        extract_button = tk.Button(self.bottom_frame, text="Extract Job Details",
                                   command=self.extract_and_populate, bg="white", fg="blue")
        extract_button.grid(row=12, column=1, pady=10, sticky="e")


    def extract_and_populate(self):
        """Extract job details from pasted email content and populate form fields."""
        email_content = self.email_content_text.get("1.0", tk.END).strip()
        job_details = extract_job_details_nlp(email_content)

        self.form_vars["Job Title"].set(job_details.get("job_title", ""))
        self.form_vars["Company"].set(job_details.get("company", ""))
        self.form_vars["Location"].set(job_details.get("location", ""))
        self.form_vars["Salary"].set(job_details.get("salary", ""))
        self.form_vars["Application Date"].set(job_details.get("application_date", ""))
        self.form_vars["Status"].set(job_details.get("status", ""))
        self.form_vars["Follow-Up Date"].set(job_details.get("follow_up_date", ""))
        self.form_vars["Notes"].set(job_details.get("notes", ""))

        messagebox.showinfo("Extracted", "Job details populated from email content.")

    def setup_profile_form(self):
        """Set up a form in the bottom frame for entering profile details."""
        profile_frame = tk.Frame(self.bottom_frame, padx=10, pady=10, relief=tk.GROOVE, bd=2)
        profile_frame.grid(row=0, column=2, rowspan=10, padx=10, pady=10, sticky="n")

        tk.Label(profile_frame, text="Profile Information", font=("Arial", 12, "bold")).grid(row=0, column=0,
                                                                                             columnspan=2, pady=5)

        tk.Label(profile_frame, text="Name:").grid(row=1, column=0, sticky="w")
        self.name_var = tk.StringVar()
        tk.Entry(profile_frame, textvariable=self.name_var).grid(row=1, column=1)

        tk.Label(profile_frame, text="Skills (comma-separated):").grid(row=2, column=0, sticky="w")
        self.skills_var = tk.StringVar()
        tk.Entry(profile_frame, textvariable=self.skills_var).grid(row=2, column=1)

        tk.Label(profile_frame, text="Experience (years):").grid(row=3, column=0, sticky="w")
        self.experience_var = tk.IntVar()
        tk.Entry(profile_frame, textvariable=self.experience_var).grid(row=3, column=1)

        tk.Label(profile_frame, text="Preferred Location:").grid(row=4, column=0, sticky="w")
        self.preferred_location_var = tk.StringVar()
        tk.Entry(profile_frame, textvariable=self.preferred_location_var).grid(row=4, column=1)

        tk.Label(profile_frame, text="Preferred Roles (comma-separated):").grid(row=5, column=0, sticky="w")
        self.preferred_roles_var = tk.StringVar()
        tk.Entry(profile_frame, textvariable=self.preferred_roles_var).grid(row=5, column=1)

        # Save Profile Button
        tk.Button(profile_frame, text="Save Profile", command=self.save_profile_info, bg="white", fg="blue").grid(row=6,
                                                                                                                  column=0,
                                                                                                                  columnspan=2,
                                                                                                                  pady=10)

        # Show Recommended Jobs Button
        tk.Button(profile_frame, text="Show Recommended Jobs", command=self.fetch_relevant_jobs, bg="white",
                  fg="blue").grid(row=7, column=0, columnspan=2, pady=5)

        # Load any existing profile data
        self.load_profile()

    def save_profile_info(self):
        """Save profile details to the database."""
        name = self.name_var.get()
        skills = self.skills_var.get()
        experience = self.experience_var.get()
        preferred_location = self.preferred_location_var.get()
        preferred_roles = self.preferred_roles_var.get()

        # Save profile data to the database
        save_profile(name, skills, experience, preferred_location, preferred_roles)
        messagebox.showinfo("Success", "Profile information saved successfully!")

    def load_profile(self):
        """Load profile details from the database into the form."""
        profile = get_profile()
        if profile:
            self.name_var.set(profile[1])
            self.skills_var.set(profile[2])
            self.experience_var.set(profile[3])
            self.preferred_location_var.set(profile[4])
            self.preferred_roles_var.set(profile[5])



    def fetch_relevant_jobs(self):
        """Fetch relevant jobs based on profile."""
        # Get profile data from form fields
        profile = {
            "skills": self.skills_var.get(),
            "preferred_location": self.preferred_location_var.get()
        }

        # Debugging: Print profile data
        print("Profile data:", profile)

        # Simulate job search based on profile
        # jobs = filter_jobs_based_on_profile(profile)
        jobs = fetch_jobs_from_api(profile)

        # Debugging: Print filtered jobs
        print("Filtered jobs:", jobs)
        # Format the job list for display
        if jobs:
            job_text = "\n\n".join([f"{job['title']} at {job['company']} ({job['location']})" for job in jobs])
        else:
            job_text = "No matching jobs found!"

        # Show the relevant jobs in a message box
        messagebox.showinfo("Recommended Jobs", job_text)




    def setup_treeview(self):
        """Set up the treeview widget in the center frame and add a delete button below it."""
        # Define columns for the treeview
        columns = ["ID", "Job Title", "Company", "Location", "Salary", "Application Date", "Status", "Follow-Up Date",
                   "Notes"]

        # Create the treeview widget inside the center frame
        self.tree = ttk.Treeview(self.center_frame, columns=columns, show="headings", height=15)

        # Configure each column heading and width
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        # Pack the treeview with a vertical scrollbar
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Add a vertical scrollbar to the treeview
        self.tree_scroll = tk.Scrollbar(self.center_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.tree_scroll.set)
        self.tree_scroll.pack(side=tk.RIGHT, fill="y")

        delete_button = tk.Button(
            self.center_frame,
            text="Delete Selected",
            command=self.delete_selected_application,
            bg="#ff4d4d",  # Custom red background color
            fg="#2196f3"  # White text color
        )
        delete_button.pack(side=tk.TOP, pady=10)


    def setup_search(self):
        """Set up the search bar at the top."""
        tk.Label(self.top_frame, text="Search:").grid(row=0, column=0, sticky="w", padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.top_frame, textvariable=self.search_var, width=40)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        self.search_entry.bind("<KeyRelease>", self.display_applications)

    def setup_form(self):
        """Set up the form in the bottom frame for adding new applications."""
        form_labels = ["Job Title", "Company", "Location", "Salary", "Application Date", "Status", "Follow-Up Date",
                       "Notes"]
        self.form_vars = {}

        for idx, label_text in enumerate(form_labels):
            tk.Label(self.bottom_frame, text=label_text + ":").grid(row=idx, column=0, sticky="w", padx=5, pady=2)
            entry_var = tk.StringVar()
            entry = tk.Entry(self.bottom_frame, textvariable=entry_var, width=40)
            entry.grid(row=idx, column=1, padx=5, pady=2)
            self.form_vars[label_text] = entry_var

        # Buttons for adding and updating applications
        button_frame = tk.Frame(self.bottom_frame)
        button_frame.grid(row=len(form_labels), column=0, columnspan=2, pady=10)

        tk.Button(button_frame, text="Add Application", command=self.add_application, bg="white", fg="blue").pack(
            side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Update Selected", command=self.update_selected_application, bg="white",
                  fg="blue").pack(side=tk.LEFT, padx=5)

    def display_dashboard(self):
        """Display the dashboard with summary charts in the dashboard frame."""
        tk.Label(self.dashboard_frame, text="Dashboard", font=("Arial", 16)).pack(pady=5)

        # Frame for status distribution chart
        status_frame = tk.Frame(self.dashboard_frame)
        status_frame.pack(pady=10)
        create_status_pie_chart(status_frame)

        # Frame for applications over time chart
        timeline_frame = tk.Frame(self.dashboard_frame)
        timeline_frame.pack(pady=10)
        create_applications_over_time_chart(timeline_frame)

    def display_applications(self, event=None):
        """Display applications in the treeview with optional filtering."""
        # Clear the treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Get search term
        search_term = self.search_var.get().lower()

        # Retrieve applications from the database
        applications = get_all_applications()
        for app in applications:
            if search_term in (app[1].lower() + app[2].lower() + app[6].lower()):
                self.tree.insert("", "end", values=app)


    def add_application(self):
        """Add a new application to the database and display it in the treeview."""
        # Retrieve data from the form
        job_title = self.form_vars["Job Title"].get()
        company = self.form_vars["Company"].get()
        location = self.form_vars["Location"].get()
        salary = self.form_vars["Salary"].get()
        application_date = self.form_vars["Application Date"].get()
        status = self.form_vars["Status"].get()
        follow_up_date = self.form_vars["Follow-Up Date"].get()
        notes = self.form_vars["Notes"].get()

        # Add the application to the database
        add_application(job_title, company, location, salary, application_date, status, follow_up_date, notes)

        # Clear form fields after adding
        self.clear_form()

        # Update the display
        self.display_applications()

        # Show confirmation message
        messagebox.showinfo("Success", "Application added successfully!")

    def clear_form(self):
        """Clear all form fields after adding or updating an application."""
        for var in self.form_vars.values():
            var.set("")

    def delete_selected_application(self):
        """Delete the selected application from the database and the treeview."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an application to delete.")
            return

        # Get the application ID of the selected item
        app_id = self.tree.item(selected_item[0])["values"][0]

        # Delete the application from the database
        delete_application(app_id)

        # Remove the item from the treeview
        self.tree.delete(selected_item)

        messagebox.showinfo("Deleted", "Application deleted successfully.")

    def update_selected_application(self):
        """Update the selected application in the database and the treeview."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an application to update.")
            return

        # Get the application ID of the selected item
        app_id = self.tree.item(selected_item[0])["values"][0]

        # Retrieve the updated data from the form fields
        job_title = self.form_vars["Job Title"].get()
        company = self.form_vars["Company"].get()
        location = self.form_vars["Location"].get()
        salary = self.form_vars["Salary"].get()
        application_date = self.form_vars["Application Date"].get()
        status = self.form_vars["Status"].get()
        follow_up_date = self.form_vars["Follow-Up Date"].get()
        notes = self.form_vars["Notes"].get()

        # Update the application in the database
        update_application(app_id, job_title, company, location, salary, application_date, status, follow_up_date,
                              notes)

        # Refresh the treeview display
        self.display_applications()

        # Show confirmation message
        messagebox.showinfo("Success", "Application updated successfully!")



if __name__ == "__main__":
    app = JobTrackerApp()
    start_reminder_thread()
    app.mainloop()
