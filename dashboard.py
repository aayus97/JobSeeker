# dashboard.py

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db_manager import get_all_applications
import tkinter as tk
from collections import Counter
from datetime import datetime


def create_status_pie_chart(frame):
    """Create a pie chart showing the distribution of applications by status."""
    applications = get_all_applications()
    statuses = [app[6] for app in applications]  # Status is the 7th column
    status_counts = Counter(statuses)

    # Plot the pie chart
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(status_counts.values(), labels=status_counts.keys(), autopct='%1.1f%%', startangle=140)
    ax.set_title("Applications by Status")

    # Display the chart in the Tkinter frame
    canvas = FigureCanvasTkAgg(fig, frame)
    canvas.get_tk_widget().pack()
    canvas.draw()


def create_applications_over_time_chart(frame):
    """Create a bar chart showing the number of applications over time."""
    applications = get_all_applications()
    dates = [app[5] for app in applications if app[5]]  # Application date is the 6th column

    # Extract month and year from dates
    months = [datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m") for date in dates]
    month_counts = Counter(months)
    sorted_months = sorted(month_counts.keys())

    # Plot the bar chart
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(sorted_months, [month_counts[month] for month in sorted_months], color='skyblue')
    ax.set_title("Applications Over Time")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Applications")
    plt.xticks(rotation=45)

    # Display the chart in the Tkinter frame
    canvas = FigureCanvasTkAgg(fig, frame)
    canvas.get_tk_widget().pack()
    canvas.draw()
