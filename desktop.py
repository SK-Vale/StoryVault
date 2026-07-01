import tkinter as tk
import json

with open("characters.json", "r") as file:
    characters = json.load(file)

def show_character(character):

    details = tk.Toplevel(window)
    details.title(character["Name"])
    details.geometry("400x350")

    title = tk.Label(
        details,
        text=character["Name"],
        font=("Arial", 20)
    )

    title.pack(pady=15)

    for field, value in character.items():

        if field == "Name":
            continue

        label = tk.Label(
            details,
            text=f"{field}: {value}",
            font=("Arial", 12),
            anchor="w"
        )

        label.pack(anchor="w", padx=20)

def open_characters_window():

    characters_window = tk.Toplevel(window)
    characters_window.title("Characters")
    characters_window.geometry("500x600")

    title = tk.Label(
        characters_window,
        text="Characters",
        font=("Arial", 20)
    )

    title.pack(pady=20)

    for key, character in characters.items():

        character_text = character["Name"] + " - " + character["Race"]

        button = tk.Button(
            characters_window,
            text=character_text,
            width=30,
            command=lambda c=character: show_character(c)
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

characters_button = tk.Button(
    window,
    text="Characters",
    width=20,
    command=open_characters_window
)

characters_button.pack(pady=10)

window.mainloop()