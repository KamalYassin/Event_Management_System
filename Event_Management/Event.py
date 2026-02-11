from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

root = None
user_schedule = []

def validate_login():
    global root, curr_attendee_id
    attendee_name = login_entry.get().strip()
    if not attendee_name:
        messagebox.showerror("Error", "Please enter your name")
        return

    conn = sqlite3.connect('event_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT AttendeeID, Name FROM Attendee WHERE LOWER(Name) = LOWER(?)", (attendee_name,))
    result = cursor.fetchone()
    conn.close()

    if result:
        curr_attendee_id = result[0]
        messagebox.showinfo("Login Successful", f"Welcome {attendee_name}!")
        root.destroy()  
        open_main_application()
    else:
        messagebox.showerror("Login Failed", "Please register if you are a new user.")

def register_user():
    reg_window = Toplevel(root)
    reg_window.title("Register for Carleton CS Connect")
    reg_window.geometry("400x300")
    Label(reg_window, text="Register for Activities", font=("Arial", 16, "bold")).pack(pady=10)
    Label(reg_window, text="Name:").pack(pady=5)
    name_entry = Entry(reg_window, width=30)
    name_entry.pack(pady=5)
    Label(reg_window, text="Email:").pack(pady=5)
    email_entry= Entry(reg_window, width=30)
    email_entry.pack(pady=5)


    def save_registration():
        name= name_entry.get()
        email= email_entry.get().strip().lower()
        if not name or not email:
            messagebox.showerror("Error", "All fields are required!")
            return
        conn = sqlite3.connect('event_management.db')
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO Attendee (Name, Email) VALUES (?, ?)", (name, email))
            conn.commit()
            messagebox.showinfo("Registration Successful", f"Registration successful! You can now log in with your name {name}")
            reg_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "This email is already registered!")
        finally:
            conn.close()
    Button(reg_window, text="Submit", command=save_registration).pack(pady=20)


def show_advanced_activity_details(event, tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select an activity")
        return
    activity_details = tree.item(selected_item, "values")
    if not activity_details:
        messagebox.showerror("Error", "No details available for this activity")
        return
    activity_name, activity_date, activity_time = activity_details

    detail_window= Toplevel()
    detail_window.title(f"Details for {activity_name}")
    detail_window.geometry("400x300")
    Label(detail_window, text=f"Activity: {activity_name}", font=("Arial", 16, "bold")).pack(pady=10)
    Label(detail_window, text=f"Date: {activity_date}", font=("Arial", 14)).pack(pady=5)
    Label(detail_window, text=f"Time: {activity_time}", font=("Arial", 14)).pack(pady=5)


def open_advanced_search():
    advanced_window = Toplevel()
    advanced_window.title("Advanced Search by Speaker")
    advanced_window.geometry("800x400")
    input_frame = Frame(advanced_window)
    input_frame.pack(pady=10)

    Label(input_frame, text="Speaker Name:", font=("Times New Roman", 20)).pack(side=LEFT, padx=5)
    speaker_entry = Entry(input_frame, width=30)
    speaker_entry.pack(side=LEFT, padx=5)
    search_button = Button(input_frame, text="Search", command=lambda: search_by_speaker())
    search_button.pack(side=LEFT)

    advanced_tree = ttk.Treeview(advanced_window, columns=("Activity Name", "Date", "Time"), show="headings", height=10)
    advanced_tree.heading("Activity Name", text="Activity Name")
    advanced_tree.heading("Date", text="Date")
    advanced_tree.heading("Time", text="Time")
    advanced_tree.pack(fill=BOTH, expand=True)


    def search_by_speaker():
        keyword = speaker_entry.get().strip()  
        if not keyword:
            messagebox.showinfo("Error", "Please enter a valid speaker name")
            return

        conn = sqlite3.connect('event_management.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Activity.ActivityName, Activity.Date, Activity.Time
            FROM Activity
            INNER JOIN ActivitySpeaker ON Activity.ActivityID = ActivitySpeaker.ActivityID
            INNER JOIN Speaker ON ActivitySpeaker.SpeakerID = Speaker.SpeakerID
            WHERE LOWER(Speaker.Name)= LOWER (?);  
        """, (keyword,))
        results = cursor.fetchall()
        conn.close()

        if results:
            display_results(advanced_tree, results)
        else:
            display_results(advanced_tree, [])  
            messagebox.showinfo("No Results", f"No activities found for speaker '{keyword}'")


    def register_from_advanced():
        selected_item = advanced_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an activity to register")
            return

        activity_details = advanced_tree.item(selected_item, "values")
        if not activity_details:
            messagebox.showerror("Error", "No details available for the selected activity")
            return
        activity_name, activity_date, activity_time = activity_details

        conn = sqlite3.connect('event_management.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ActivityID FROM Activity WHERE ActivityName = ?", (activity_name,))
        activity_id = cursor.fetchone()

        if not activity_id:
            messagebox.showerror("Error", "Activity not found")
            conn.close()
            return
        cursor.execute("SELECT * FROM Registration WHERE AttendeeID = ? AND ActivityID = ?", (curr_attendee_id, activity_id[0]))
        existing_registration = cursor.fetchone()

        if existing_registration:
            messagebox.showerror("Error", "You are already registered for this activity")
        else:
            try:
                cursor.execute("INSERT INTO Registration (AttendeeID, ActivityID) VALUES (?, ?)", (curr_attendee_id, activity_id[0]))
                conn.commit()
                messagebox.showinfo("Success", f"Registered for {activity_name}")
                user_schedule.append((activity_name, activity_date, activity_time))
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Failed to register for the activity")
        conn.close()
    register_button = Button(advanced_window, text="Register for Activity", command=register_from_advanced)
    register_button.pack(pady=10)


    def add_to_schedule_advanced():
        selected_item = advanced_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an activity to add")
            return
        activity_details = advanced_tree.item(selected_item, "values")
        if not activity_details:
            messagebox.showerror("Error", "No details available for the selected activity")
            return
        activity_name, activity_date, activity_time = activity_details

        conn = sqlite3.connect('event_management.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ActivityID FROM Activity WHERE ActivityName = ?", (activity_name,))
        activity_id = cursor.fetchone()

        if not activity_id:
            messagebox.showerror("Error", "Activity not found in the database!")
            conn.close()
            return

        cursor.execute("SELECT * FROM Registration WHERE AttendeeID = ? AND ActivityID = ?", (curr_attendee_id, activity_id[0]))
        existing_registration = cursor.fetchone()

        if existing_registration:
            messagebox.showerror("Error", "You are already registered for this activity")
        else:
            try:
                cursor.execute("INSERT INTO Registration (AttendeeID, ActivityID) VALUES (?, ?)", (curr_attendee_id, activity_id[0]))
                conn.commit()
                messagebox.showinfo("Success", f"You have registered for {activity_name}!")
                user_schedule.append((activity_name, activity_date, activity_time))
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "An error occurred while registering")
        conn.close()

def open_main_application():
    main_app = Tk()
    main_app.title("Carleton CS Connect Search")
    main_app.geometry("1150x650")
    top_frame = Frame(main_app)
    top_frame.pack(side=TOP, fill=X, pady=10)

    info_button = Button(top_frame, text="Event Info", command= show_event_info_window, width=15)
    info_button.pack(side=LEFT, padx=10)
    upcoming_button = Button(top_frame, text="Upcoming Activities", command=show_upcoming_activities, width=20)
    upcoming_button.pack(side=LEFT, padx=10)
    logout_button = Button(top_frame, text="Logout", command=lambda: logout(main_app), width=15)
    logout_button.pack(side=LEFT, padx=10)

    headline_frame = Frame(main_app)
    headline_frame.pack(pady=10)

    headline_label = Label(headline_frame, text="Welcome to Carleton CS Connect", font=("Times New Roman", 30, "bold"))
    headline_label.pack()
    search_frame = Frame(main_app)
    search_frame.pack(pady=40)

    search_label = Label(search_frame, text="Keyword:", font=("Times New Roman", 20))
    search_label.grid(row=0, column=0, padx=5)

    global search_entry
    search_entry = Entry(search_frame, width=40)
    search_entry.grid(row=0, column=1, padx=10)
    search_button = Button(search_frame, text="Search Activity", command=search_activity, width=15)
    search_button.grid(row=0, column=2, padx=5)
    advanced_search_button = Button(search_frame, text="Advanced Search", command=open_advanced_search, width=15)
    advanced_search_button.grid(row=0, column=3, padx=5)
    main_app.bind("<Return>", lambda event: search_activity())

    global result_tree
    result_frame = Frame(main_app)
    result_frame.pack(pady=20)

    result_tree = ttk.Treeview(result_frame, columns=("Activity Name", "Date", "Time"), show="headings", height=10)
    result_tree.heading("Activity Name", text="Activity Name")
    result_tree.heading("Date", text="Date")
    result_tree.heading("Time", text="Time")
    result_tree.pack(fill=BOTH, expand=True)
    result_tree.bind("<Return>", show_activity_details)

def logout(main_app):
    main_app.destroy()
    create_login_window()

def show_upcoming_activities():
    upcoming_window = Toplevel()
    upcoming_window.title("Upcoming Activities")
    upcoming_window.geometry("600x400")

    upcoming_tree = ttk.Treeview(upcoming_window, columns=("Activity Name", "Date", "Time"), show="headings", height=10)
    upcoming_tree.heading("Activity Name", text="Activity Name")
    upcoming_tree.heading("Date", text="Date")
    upcoming_tree.heading("Time", text="Time")
    upcoming_tree.pack(fill=BOTH, expand=True)

    def fetch_upcoming_activities():
        conn = sqlite3.connect('event_management.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Activity.ActivityName, Activity.Date, Activity.Time
            FROM Registration
            INNER JOIN Activity ON Registration.ActivityID = Activity.ActivityID
            WHERE Registration.AttendeeID = ?;
        """, (curr_attendee_id,))
        activities = cursor.fetchall()
        conn.close()
        return activities

    for activity in fetch_upcoming_activities():
        upcoming_tree.insert("", "end", values=activity)

    def remove_selected_activity():
        selected_item = upcoming_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an activity to remove")
            return

        activity_details = upcoming_tree.item(selected_item, "values")
        if not activity_details:
            messagebox.showerror("Error", "No details available for the selected activity")
            return
        activity_name, activity_date, activity_time = activity_details
        conn = sqlite3.connect('event_management.db')
        cursor = conn.cursor()

        cursor.execute("SELECT ActivityID FROM Activity WHERE ActivityName = ?", (activity_name,))
        activity_id = cursor.fetchone()
        if not activity_id:
            messagebox.showerror("Error", "Activity not found!")
            conn.close()
            return

        cursor.execute("DELETE FROM Registration WHERE AttendeeID = ? AND ActivityID = ?", (curr_attendee_id, activity_id[0]))
        conn.commit()
        conn.close()
        upcoming_tree.delete(selected_item)
        messagebox.showinfo("Removed", f"{activity_name} has been removed from your upcoming activities!")
    Button(upcoming_window, text="Remove Selected", command=remove_selected_activity).pack(pady=10)


def show_event_info_window():
    info_window = Toplevel()
    info_window.title("Event Information")
    info_window.geometry("600x400")
    Label(info_window, text="Welcome to Carleton CS Connect", font=("Times New Roman", 24, "bold")).pack(pady=10)

    info_text = """Carleton CS Connect is a 3-day event aimed at bringing together computer science students, professionals, and enthusiasts to learn, connect, and innovate. 

The event includes keynotes, workshops, panels, and speeches led by industry leaders. You'll have opportunities to gain insights on trending topics like AI ethics, cybersecurity, cloud computing, and the future of technology.

Location: Carleton Fieldhouse & Alumni Hall

Search Guide:
- Use the "Search Activity" feature to look up activities by keywords.
- Use "Advanced Search" to find activities based on speaker names.
- Press Enter on a search result to view more details and register for the activity.
- All registered activities will appear under "Upcoming Activities" for easy access.

Schedule Highlights:
- Day 1: Keynotes and introductory workshops
- Day 2: Advanced workshops and panel discussions
- Day 3: Closing sessions and networking

Guidelines:
- Register for activities to secure your spot.
- Be punctual and participate actively.
- Visit the "Upcoming Activities" tab to manage your schedule.

We look forward to seeing you at Carleton CS Connect!"""
    
    text_widget = Text(info_window, wrap=WORD, font=("Times New Roman", 17))
    text_widget.insert(1.0, info_text)
    text_widget.config(state=DISABLED) 
    text_widget.pack(fill=BOTH, expand=True, padx=10, pady=10)


def search_activity():
    keyword = search_entry.get()
    conn = sqlite3.connect('event_management.db')
    cursor = conn.cursor()

    if keyword.strip():  
        cursor.execute("SELECT ActivityName, Date, Time FROM Activity WHERE ActivityName LIKE ?", ('%' + keyword + '%',))
    else:  
        cursor.execute("SELECT ActivityName, Date, Time FROM Activity")
    results = cursor.fetchall()
    conn.close()

    if results:
        display_results(result_tree, results)
    else:
        messagebox.showinfo("No Results", "No activities found")


def display_results(tree, results):
    for row in tree.get_children():
        tree.delete(row)
    for result in results:
        tree.insert("", "end", values=result)


def show_activity_details(event=None):
    selected_item = result_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select an activity")
        return
    activity_details = result_tree.item(selected_item, "values")
    if not activity_details:
        messagebox.showerror("Error", "No details available for this activity")
        return
    activity_name, activity_date, activity_time = activity_details

    detail_window = Toplevel()
    detail_window.title(f"Details for {activity_name}")
    detail_window.geometry("400x400")
    Label(detail_window, text=f"Activity: {activity_name}", font=("Arial", 16, "bold")).pack(pady=10)
    Label(detail_window, text=f"Date: {activity_date}", font=("Arial", 14)).pack(pady=5)
    Label(detail_window, text=f"Time: {activity_time}", font=("Arial", 14)).pack(pady=5)

    def register_activity():
        conn = sqlite3.connect('event_management.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ActivityID FROM Activity WHERE ActivityName = ?", (activity_name,))
        activity_id = cursor.fetchone()

        if not activity_id:
            messagebox.showerror("Error", "Activity not found")
            conn.close()
            return

        cursor.execute("SELECT * FROM Registration WHERE AttendeeID = ? AND ActivityID = ?", (curr_attendee_id, activity_id[0]))
        existing_registration = cursor.fetchone()
        if existing_registration:
            messagebox.showerror("Error", "You are already registered for this activity")
        else:
            try:
                cursor.execute("INSERT INTO Registration (AttendeeID, ActivityID) VALUES (?, ?)", (curr_attendee_id, activity_id[0]))
                conn.commit()
                messagebox.showinfo("Success", f"Registered for {activity_name}")
                user_schedule.append((activity_name, activity_date, activity_time))
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "An error occurred during registration")
        conn.close()
    Button(detail_window, text="Register for Activity", command=register_activity).pack(pady=20)


    def add_to_schedule(activity_name, attendee_id):
        conn = sqlite3.connect('event_management.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ActivityID FROM Activity WHERE ActivityName = ?", (activity_name,))
        activity_id = cursor.fetchone()

        if not activity_id:
            messagebox.showerror("Error", "Activity not found")
            conn.close()
            return
        cursor.execute("SELECT * FROM Registration WHERE AttendeeID = ? AND ActivityID = ?", (attendee_id, activity_id[0]))
        existing_registration = cursor.fetchone()

        if existing_registration:
            messagebox.showerror("Error", "You are already registered for this activity")
        else:
            try:
                cursor.execute("INSERT INTO Registration (AttendeeID, ActivityID) VALUES (?, ?)", (attendee_id, activity_id[0]))
                conn.commit()
                messagebox.showinfo("Success", f"You have registered for {activity_name}")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "An error occurred while registering")
        conn.close()

    def view_speaker_details():
        conn = sqlite3.connect('event_management.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Speaker.Name, Speaker.Bio, ActivitySpeaker.IsMainSpeaker
            FROM Speaker
            INNER JOIN ActivitySpeaker ON Speaker.SpeakerID = ActivitySpeaker.SpeakerID
            WHERE ActivitySpeaker.ActivityID = (SELECT ActivityID FROM Activity WHERE ActivityName = ?)
        """, (activity_name,))
        speakers = cursor.fetchall()
        conn.close()

        if not speakers:
            messagebox.showinfo("No Speakers", "No speakers found for this activity")
            return

        speaker_window = Toplevel()
        speaker_window.title(f"Speakers for {activity_name}")
        speaker_window.geometry("400x400")
        Label(speaker_window, text=f"Speakers for {activity_name}", font=("Arial", 16, "bold")).pack(pady=10)

        for speaker in speakers:
            name, bio, is_main_speaker = speaker
            role = "Main Speaker" if is_main_speaker else "Secondary Speaker"
            Label(speaker_window, text=f"Name: {name}", font=("Arial", 14)).pack(pady=5)
            Label(speaker_window, text=f"Role: {role}", font=("Arial", 12)).pack(pady=5)
            Label(speaker_window, text=f"Bio: {bio}", font=("Arial", 12)).pack(pady=5)
            Label(speaker_window, text="-" * 40).pack(pady=5)
    Button(detail_window, text="View Speaker Details", command=view_speaker_details).pack(pady=10)

def create_login_window():
    global root
    root = Tk()
    root.title("Carleton CS Connect Login")
    root.geometry("800x400")

    Label(root, text="Login to Carleton CS Connect", font=("Arial", 16, "bold")).pack(pady=10)
    Label(root, text="Name:").pack(pady=5)
    global login_entry
    login_entry = Entry(root, width=30)
    login_entry.pack(pady=5)
    Button(root, text="Login", command=validate_login).pack(pady=10)
    Button(root, text="Register", command=register_user).pack(pady=5)
    root.mainloop()
create_login_window()
