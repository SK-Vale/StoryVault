import tkinter as tk
import json

from locations import locations


with open("characters.json", "r") as file:
    characters = json.load(file)


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


window = tk.Tk()

window.title("StoryVault")
window.geometry("500x600")

title = tk.Label(
    window,
    text="StoryVault",
    font=("Arial", 24)
)

title.pack(pady=20)

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
    width=20
)

timeline_button.grid(row=1, column=0, padx=10, pady=10)

creatures_button = tk.Button(
    button_frame,
    text="Creatures",
    width=20
)

creatures_button.grid(row=1, column=1, padx=10, pady=10)

projects_button = tk.Button(
    button_frame,
    text="Projects",
    width=20
)

projects_button.grid(row=2, column=0, padx=10, pady=10)

exit_button = tk.Button(
    button_frame,
    text="Exit",
    width=20,
    command=window.destroy
)

exit_button.grid(row=2, column=1, padx=10, pady=10)

window.mainloop()