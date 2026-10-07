import os
import sys
import tkinter as tk
from tkinter import messagebox
import json
from creatures import creatures
from locations import locations
from timeline import timeline 
from projects import projects

# =========================
# STORYVAULT THEME
# =========================

BG = "#120F18"
PANEL = "#211A24"
GOLD = "#D6A84B"
TEXT = "#F3E8D0"
MUTED = "#B7A78F"

BUTTON_BG = "#3A2A20"
BUTTON_TEXT = "#F3E8D0"
BUTTON_ACTIVE = "#5A402B"

BUTTON_STYLE = {
    "bg": BUTTON_BG,
    "fg": BUTTON_TEXT,
    "activebackground": BUTTON_ACTIVE,
    "activeforeground": TEXT,
    "relief": "flat",
    "borderwidth": 0
}

def get_data_path(filename):
    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, filename)

with open(get_data_path("characters.json"), "r") as file:
    characters = json.load(file)

try:
    with open(get_data_path("sessions.json"), "r") as file:
        sessions = json.load(file)
except FileNotFoundError:
    sessions = []

def show_item(item):

    details = tk.Toplevel(window)
    details.title(item["Name"])
    details.geometry("400x350")
    details.configure(bg=BG)

    title = tk.Label(
        details,
        text=item["Name"],
        font=("Arial", 20, "bold"),
        bg=BG,
        fg=GOLD
    )

    title.pack(pady=15)

    for field, value in item.items():

        if field == "Name":
            continue

        label = tk.Label(
            details,
            text=f"{field}: {value}",
            font=("Arial", 12),
            anchor="w",
            bg=BG,
            fg=TEXT
        )

        label.pack(anchor="w", padx=20)


def open_database_window(title_text, data, subtitle_field=None):

    database_window = tk.Toplevel(window)
    database_window.title(title_text)
    database_window.geometry("500x600")
    database_window.configure(bg=BG)

    title = tk.Label(
    database_window,
    text=title_text,
    font=("Arial", 20, "bold"),
    bg=BG,
    fg=GOLD
)

    title.pack(pady=20)



    for key, item in data.items():

        button_text = item["Name"]

        if subtitle_field is not None and subtitle_field in item:
            button_text = item["Name"] + " - " + item[subtitle_field]

        button = tk.Button(
            database_window,
            text=button_text,
            width=30,
            command=lambda i=item: show_item(i),
            **BUTTON_STYLE
        )

        button.pack(pady=5)

    back_button = tk.Button(
        database_window,
        text="Back",
        width=20,
        command=database_window.destroy,
        **BUTTON_STYLE
    )

    back_button.pack(pady=20)

total_words = 0

for session in sessions:
    total_words += int(session["Words"])


def refresh_dashboard():
    total_words = 0

    for session in sessions:
        total_words += int(session["Words"])

    summary.config(
        text=(
            f"{len(projects)} Projects  |  "
            f"{len(characters)} Characters  |  "
            f"{len(locations)} Locations\n"
            f"{len(creatures)} Creatures  |  "
            f"{len(timeline)} Timeline Events\n\n"
            f"Writing Sessions: {len(sessions)}  |  "
            f"Total Words: {total_words:,}"
        )
    )
def open_writing_statistics():
    stats_window = tk.Toplevel(window)
    stats_window.title("Writing Statistics")
    stats_window.geometry("500x500")
    stats_window.configure(bg=BG)

    title = tk.Label(
        stats_window,
        text="Writing Statistics",
        font=("Arial", 20),
        bg=BG,
        fg=GOLD
    )
    title.pack(pady=20)

    # ----- Calculate statistics -----

    total_sessions = len(sessions)

    total_words = 0
    goals_hit = 0
    goals_missed = 0
    best_session = None
    words_by_project = {}

    for session in sessions:
        words = int(session["Words"])
        goal = int(session["Goal"])

        total_words += words

        project = session["Project"]

        if project in words_by_project:
            words_by_project[project] += words
        else:
            words_by_project[project] = words

        if best_session is None or words > int(best_session["Words"]):
            best_session = session

        if words >= goal:
            goals_hit += 1
        else:
            goals_missed += 1

    if total_sessions > 0:
        average_words = total_words // total_sessions
    else:
        average_words = 0

    if best_session:
        best_session_text = (
            f"{best_session['Project']} "
            f"({int(best_session['Words']):,} words)"
        )
    else:
        best_session_text = "No sessions yet"

    project_stats_text = ""

    for project, words in words_by_project.items():
        project_stats_text += (
            f"{project}: {words:,} words\n"
        )

    stats_text = (
        f"Total Sessions: {total_sessions}\n\n"
        f"Total Words: {total_words:,}\n\n"
        f"Average Words Per Session: {average_words:,}\n\n"
        f"Best Session: {best_session_text}\n\n"
        f"Goals Hit: {goals_hit}\n\n"
        f"Goals Missed: {goals_missed}\n\n"
        f"Words By Project:\n"
        f"{project_stats_text}"
    )

    # ----- Scrollable statistics area -----

    content_frame = tk.Frame(
        stats_window,
        bg=BG
    )
    content_frame.pack(
        fill="both",
        expand=True,
        padx=20
    )

    canvas = tk.Canvas(
        content_frame,
        bg=BG
    )

    scrollbar = tk.Scrollbar(
        content_frame,
        orient="vertical",
        command=canvas.yview,
        bg=BUTTON_BG,
        activebackground=BUTTON_ACTIVE,
        troughcolor=BG,
        highlightthickness=0,
        borderwidth=0
    )

    stats_frame = tk.Frame(
        canvas,
        bg=BG
    )

    stats_frame.bind(
        "<Configure>",
        lambda event: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window(
        (0, 0),
        window=stats_frame,
        anchor="nw"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    def scroll_with_mouse(event):
        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    stats_window.bind(
        "<MouseWheel>",
        scroll_with_mouse
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    stats_label = tk.Label(
        stats_frame,
        text=stats_text,
        font=("Arial", 12),
        justify="left",
        bg=BG,
        fg=TEXT
    )

    stats_label.pack(
        anchor="w",
        pady=10
    )

    # ----- Permanent Back button -----

    back_button = tk.Button(
        stats_window,
        text="Back",
        width=20,
        command=stats_window.destroy,
        **BUTTON_STYLE
    )

    back_button.pack(
        pady=10
    )

def open_session_history():
    history_window = tk.Toplevel(window)
    history_window.title("Writing Session History")
    history_window.geometry("500x500")
    history_window.configure(bg=BG)

    title = tk.Label(
        history_window,
        text="Writing Session History",
        font=("Arial", 20),
        bg=BG,
        fg=GOLD
    )
    title.pack(pady=20)

    content_frame = tk.Frame(
        history_window,
        bg=BG,
        highlightthickness=0,
        borderwidth=0,
        relief="flat"
    )

    content_frame.pack(
        fill="both",
        expand=True,
        padx=20
    )

    canvas = tk.Canvas(
        content_frame,
        bg=BG,
        highlightthickness=0
    )
    
    scrollbar = tk.Scrollbar(
        content_frame,
        orient="vertical",
        command=canvas.yview
    )

    session_frame = tk.Frame(
        canvas,
        bg=BG,
        borderwidth=0,
        highlightthickness=0
    )

    session_frame.bind(
        "<Configure>",
        lambda event: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window(
        (0, 0),
        window=session_frame,
        anchor="nw"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    def scroll_with_mouse(event):
        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    history_window.bind(
        "<MouseWheel>",
        scroll_with_mouse
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    for session in sessions:
        session_text = (
            f"{session['Project']} | "
            f"Goal: {session['Goal']} | "
            f"Words: {session['Words']}"
        )

        session_label = tk.Label(
            session_frame,
            text=session_text,
            font=("Arial", 11),
            bg=BG,
            fg=TEXT,
            borderwidth=0,
            highlightthickness=0,
        )

        session_label.pack(
            anchor="w",
            pady=5
        )

    back_button = tk.Button(
        history_window,
        text="Back",
        width=20,
        command=history_window.destroy,
        **BUTTON_STYLE
    )

    back_button.pack(
        pady=10
    )
    

    canvas.bind_all(
        "<MouseWheel>",
        scroll_with_mouse
)
    canvas.pack(
        side="left",
        fill="both",
        expand=True,
        padx=20
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )
   
def open_about():
    about_window = tk.Toplevel(window)
    about_window.title("About StoryVault")
    about_window.geometry("400x350")
    about_window.configure(bg=BG)

    title = tk.Label(
        about_window,
        text="StoryVault",
        font=("Arial", 20),
        bg=BG,
        fg=GOLD
    )
    title.pack(pady=20)

    about_text = (
        "Version 0.2\n\n"
        "Created by S.K. Vale\n\n"
        "A desktop writing companion for authors.\n\n"
        "Built with Python\n"
        "Available on Windows and macOS"
    )

    info = tk.Label(
        about_window,
        text=about_text,
        font=("Arial", 11),
        justify="center",
        bg=BG,
        fg=TEXT
    )
    info.pack(pady=20)

    back_button = tk.Button(
        about_window,
        text="Back",
        width=20,
        command=about_window.destroy,
        **BUTTON_STYLE
    )
    back_button.pack(pady=20)

def open_writing_session():
    session_window = tk.Toplevel(window)
    session_window.title("Writing Session")
    session_window.geometry("400x400")
    session_window.configure(bg=BG)

    title = tk.Label(
        session_window,
        text="Writing Session",
        font=("Arial", 20),
        bg=BG,
        fg=GOLD
    )
    title.pack(pady=20)

    project_label = tk.Label(
           session_window,
           text="Project",
           bg=BG,
           fg=TEXT
)
    project_label.pack()

    project_entry = tk.Entry(
           session_window,
           width=30,
           bg=PANEL,
           fg=TEXT, 
           insertbackground=GOLD,
           relief="flat"
)
    project_entry.pack(pady=5)


    goal_label = tk.Label(
        session_window,
        text="Word Goal",
        bg=BG,
        fg=TEXT
)
    goal_label.pack()

    goal_entry = tk.Entry(
        session_window,
        width=30,
        bg=PANEL,
        fg=TEXT,
        insertbackground=GOLD,
        relief="flat"
)
    goal_entry.pack(pady=5)


    words_label = tk.Label(
         session_window,
         text="Words Written",
         bg=BG,
         fg=TEXT
)
    words_label.pack()

    words_entry = tk.Entry(
         session_window,
        width=30,
        bg=PANEL,
        fg=TEXT,
        insertbackground=GOLD,
        relief="flat"
)
    words_entry.pack(pady=5)



    def save_session():
        project = project_entry.get()
        goal = goal_entry.get()
        words = words_entry.get()
        if project == "" or goal == "" or words == "":
            messagebox.showerror(
                "Missing Information",
                "Please fill in all fields.",
                parent=session_window
            )
            return

        try:
            goal = int(goal)
            words = int(words)
        except ValueError:
            messagebox.showerror(
                "Invalid Numbers",
                "Word Goal and Words Written must be numbers.",
                parent=session_window
            )
            return

        if goal < 0 or words < 0:
            messagebox.showerror(
                "Invalid Numbers",
                "Word Goal and Words Written cannot be negative.",
                parent=session_window
            )
            return

        session = {
            "Project": project,
            "Goal": goal,
            "Words": words
        }

        sessions.append(session)

        with open(get_data_path("sessions.json"), "w") as file:
            json.dump(sessions, file, indent=4)

        refresh_dashboard()

        project_entry.delete(0, tk.END)
        goal_entry.delete(0, tk.END)
        words_entry.delete(0, tk.END)

        messagebox.showinfo(
            "Session Saved",
            "Writing session saved successfully!",
            parent=session_window
        )

        window.lift()
        session_window.focus_force()

    save_button = tk.Button(
        session_window,
        text="Save Session",
        width=20,
        command=save_session,
        **BUTTON_STYLE
    )
    save_button.pack(pady=10)

    back_button = tk.Button(
        session_window,
        text="Back",
        width=20,
        command=session_window.destroy,
        **BUTTON_STYLE
    )
    back_button.pack(pady=20)


window = tk.Tk()

window.title("StoryVault")
window.geometry("500x600")

window.configure(bg=BG)

title = tk.Label(
    window,
    text="StoryVault",
    font=("Arial", 24, "bold"),
    bg=BG,
    fg=GOLD
)

title.pack(pady=(20, 5))

version_label = tk.Label(
    window,
    text="Version 0.2",
    font=("Arial", 10),
    bg=BG,
    fg=MUTED
)

version_label.pack()

summary = tk.Label(
    window,
    text=(
       f"{len(projects)} Projects  |  "
       f"{len(characters)} Characters  |  "
       f"{len(locations)} Locations\n"
       f"{len(creatures)} Creatures  |  "
       f"{len(timeline)} Timeline Events\n\n"
       f"Writing Sessions: {len(sessions)}  |  "
       f"Total Words: {total_words:,}"
  ),
  font=("Arial", 11),
  bg=BG,
  fg=TEXT
  
)

summary.pack(pady=10)

button_frame = tk.Frame(
    window,
    bg=BG
)
button_frame.pack(pady=20)

characters_button = tk.Button(
    button_frame,
    text="Characters",
    width=20,
    command=lambda: open_database_window("Characters", characters, "Race"),
    **BUTTON_STYLE
)

characters_button.grid(row=0, column=0, padx=10, pady=10)

locations_button = tk.Button(
    button_frame,
    text="Locations",
    width=20,
    command=lambda: open_database_window("Locations", locations),
    **BUTTON_STYLE
)

locations_button.grid(row=0, column=1, padx=10, pady=10)

timeline_button = tk.Button(
    button_frame,
    text="Timeline",
    width=20,
    command=lambda: open_database_window("Timeline", timeline),
    **BUTTON_STYLE
)

timeline_button.grid(row=1, column=0, padx=10, pady=10)

creatures_button = tk.Button(
    button_frame,
    text="Creatures",
    width=20,
    command=lambda: open_database_window("Creatures", creatures),
    **BUTTON_STYLE
)

creatures_button.grid(row=1, column=1, padx=10, pady=10)

projects_button = tk.Button(
    button_frame,
    text="Projects",
    width=20,
    command=lambda: open_database_window("Projects", projects),
    **BUTTON_STYLE
)

projects_button.grid(row=2, column=0, padx=10, pady=10)

exit_button = tk.Button(
    button_frame,
    text="Exit",
    width=20,
    command=window.destroy,
    **BUTTON_STYLE
)

exit_button.grid(row=2, column=1, padx=10, pady=10)

about_button = tk.Button(
    button_frame,
    text="About",
    width=20,
    command=open_about,
    **BUTTON_STYLE
)

about_button.grid(
    row=6,
    column=0,
    columnspan=2,
    pady=10
)

writing_session_button = tk.Button(
    button_frame,
    text="Writing Session",
    width=20,
    command=open_writing_session,
    **BUTTON_STYLE
)

writing_session_button.grid(
    row=3,
    column=0,
    columnspan=2,
    pady=10

)
stats_button = tk.Button(
    button_frame,
    text="Writing Statistics",
    width=20,
    command=open_writing_statistics,
    **BUTTON_STYLE
)

history_button = tk.Button(
    button_frame,
    text="Session History",
    width=20,
    command=open_session_history,
    **BUTTON_STYLE
)

history_button.grid(
    row=4,
    column=0,
    columnspan=2,
    pady=10
)
stats_button.grid(
    row=5,
    column=0,
    columnspan=2,
    pady=10
)
window.mainloop()