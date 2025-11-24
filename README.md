# Event Management & Activity Registration System

A desktop-based **event management and activity registration system** for the 3-day conference **Carleton CS Connect**.  

<p>
  <img 
    src="https://github.com/user-attachments/assets/4f78d5a8-2841-4b44-b8f2-891260459696" 
    alt="Event Management Dashboard UI" 
    width="750"
  />
</p>


## 🧠 Project Overview

This application simulates how a real event registration portal might work for a multi-day Computer Science conference:

- Attendees log in using their **name**, or **register as new users**.
- Activities (keynotes, workshops, panels, etc.) are stored in a **SQLite database**.
- Users can **search activities** by keyword or perform an **advanced search by speaker name**.
- From search results, users can open details, **view speakers**, and **register** for activities.
- A dedicated **“Upcoming Activities”** view shows all activities the attendee is registered for, with the option to remove them.
- An **“Event Info”** page explains the event, highlights, and how to use the interface.

The goal of the project is to model a realistic academic event system with relational data, user-facing UI, and basic integrity checks around registration.

---

## ✨ Features

- **Name-based Login & Registration**
  - Log in using your name (case-insensitive).
  - Register as a new attendee with **name + unique email**.
- **Keyword Activity Search**
  - Search activities by keywords in the activity name.
  - View results in a table with **Activity Name, Date, and Time**.
- **Advanced Search by Speaker**
  - Find activities that feature a specific speaker.
  - View results in a dedicated table and register directly from there.
- **Activity Details & Speaker Info**
  - View full details of a selected activity.
  - See all speakers attached to that activity, including whether they are **main** or **secondary** speakers.
- **Registration & Schedule Management**
  - Register for selected activities (with duplicate registration checks).
  - View all your registered activities in **Upcoming Activities**.
  - Remove activities from your upcoming schedule.
- **Event Info Window**
  - Describes Carleton CS Connect (3 days, structure, topics, location).
  - Includes a **usage guide** for the application.

---

## 🗂 Repository Contents

This submission contains the following main files:

- `FinalProject.py`  
  The main Python script implementing the **Tkinter GUI** and all application logic (login, search, registration, schedule, event info).

- `event_management.db`  
  The SQLite database file containing:
  - `Attendee`, `Activity`, `Speaker`, `ActivitySpeaker`, `Registration`, etc.
  - All sample data used by the interface.

- `FP.pdf`  
  A short report including:
  - The **ER model** of the database.
  - An **English description** of the project design and schema.

> In the original course submission, these files were provided as a zip, but here they are organized for easier viewing and execution.

---

## 🛠 Tech Stack

- **Language:** Python 3  
- **GUI Framework:** Tkinter (`tkinter`, `ttk`, `messagebox`)  
- **Database:** SQLite (`sqlite3`)  
- **Architecture:** Event-driven GUI + relational database backend

🎥 Demo Video

A full walkthrough of the interface and features is available on YouTube:

👉 YouTube Demo:
https://youtu.be/P1qhYono4ag
