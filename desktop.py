import tkinter as tk
from tkinter import messagebox
import json
from creatures import creatures
from locations import locations
from timeline import timeline 
from projects import projects


with open("characters.json", "r") as file:
    characters = json.load(file)

try:
    with open("sessions.json", "r") as file:
        sessions = json.load(file)
except FileNotFoundError:
    sessions = []

def show_item(item):

    details = tk.Toplevel(window)
    details.title(item["Name"])
    details.geometry("400x350")

    title = tk.Label(
        details,
        text=item["Name"],
        font=("Arial", 20)
    )

    title.pack(pady=15)

    for field, value in item.items():

        if field == "Name":
            continue

        label = tk.Label(
            details,
            text=f"{field}: {value}",
            font=("Arial", 12),
            anchor="w"
        )

        label.pack(anchor="w", padx=20)


def open_database_window(title_text, data, subtitle_field=None):

    database_window = tk.Toplevel(window)
    database_window.title(title_text)
    database_window.geometry("500x600")

    title = tk.Label(
        database_window,
        text=title_text,
        font=("Arial", 20)
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
            command=lambda i=item: show_item(i)
        )

        button.pack(pady=5)

    back_button = tk.Button(
        database_window,
        text="Back",
        width=20,
        command=database_window.destroy
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

def open_session_history():
    history_window = tk.Toplevel(window)
    history_window.title("Writing Session History")
    history_window.geometry("500x500")

    title = tk.Label(
        history_window,
        text="Writing Session History",
        font=("Arial", 20)
    )
    title.pack(pady=20)

    canvas = tk.Canvas(history_window)
    scrollbar = tk.Scrollbar(
        history_window,
        orient="vertical",
        command=canvas.yview
    )

    session_frame = tk.Frame(canvas)

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

    for session in sessions:
        session_text = (
            f"{session['Project']} | "
            f"Goal: {session['Goal']} | "
            f"Words: {session['Words']}"
        )
    
        session_label = tk.Label(
            session_frame,
            text=session_text,
            font=("Arial", 11)
        )
        session_label.pack(
            anchor="w",
            pady=5
        )

    back_button = tk.Button(
        history_window,
        text="Back",
        width=20,
        command=history_window.destroy
    )
        
    back_button.pack(
        side="bottom",
        pady=10
    )

def open_writing_session():
    session_window = tk.Toplevel(window)
    session_window.title("Writing Session")
    session_window.geometry("400x400")

    title = tk.Label(
        session_window,
        text="Writing Session",
        font=("Arial", 20)
    )
    title.pack(pady=20)

    project_label = tk.Label(session_window, text="Project")
    project_label.pack()

    project_entry = tk.Entry(session_window, width=30)
    project_entry.pack(pady=5)

    goal_label = tk.Label(session_window, text="Word Goal")
    goal_label.pack()

    goal_entry = tk.Entry(session_window, width=30)
    goal_entry.pack(pady=5)

    words_label = tk.Label(session_window, text="Words Written")
    words_label.pack()

    words_entry = tk.Entry(session_window, width=30)
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

        with open("sessions.json", "w") as file:
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

        session=window.lift()
        session_window.focus_force()

    save_button = tk.Button(
        session_window,
        text="Save Session",
        width=20,
        command=save_session
    )
    save_button.pack(pady=10)

    back_button = tk.Button(
        session_window,
        text="Back",
        width=20,
        command=session_window.destroy
    )
    back_button.pack(pady=20)


window = tk.Tk()

window.title("StoryVault")
window.geometry("500x600")

title = tk.Label(
    window,
    text="StoryVault",
    font=("Arial", 24)
)

title.pack(pady=20)

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
  font=("Arial", 11)
  
)

summary.pack(pady=10)

button_frame = tk.Frame(window)
button_frame.pack(pady=20)

characters_button = tk.Button(
    button_frame,
    text="Characters",
    width=20,
    command=lambda: open_database_window("Characters", characters, "Race")
)

characters_button.grid(row=0, column=0, padx=10, pady=10)

locations_button = tk.Button(
    button_frame,
    text="Locations",
    width=20,
    command=lambda: open_database_window("Locations", locations)
)

locations_button.grid(row=0, column=1, padx=10, pady=10)

timeline_button = tk.Button(
    button_frame,
    text="Timeline",
    width=20,
    command=lambda: open_database_window("Timeline", timeline)
)

timeline_button.grid(row=1, column=0, padx=10, pady=10)

creatures_button = tk.Button(
    button_frame,
    text="Creatures",
    width=20,
    command=lambda: open_database_window("Creatures", creatures)
)

creatures_button.grid(row=1, column=1, padx=10, pady=10)

projects_button = tk.Button(
    button_frame,
    text="Projects",
    width=20,
    command=lambda: open_database_window("Projects", projects)
)

projects_button.grid(row=2, column=0, padx=10, pady=10)

exit_button = tk.Button(
    button_frame,
    text="Exit",
    width=20,
    command=window.destroy
)

exit_button.grid(row=2, column=1, padx=10, pady=10)



writing_session_button = tk.Button(
    button_frame,
    text="Writing Session",
    width=20,
    command=open_writing_session
)

writing_session_button.grid(
    row=3,
    column=0,
    columnspan=2,
    pady=10
)

history_button = tk.Button(
    button_frame,
    text="Session History",
    width=20,
    command=open_session_history
)

history_button.grid(
    row=4,
    column=0,
    columnspan=2,
    pady=10
)
 
window.mainloop()