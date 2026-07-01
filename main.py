import json
from timeline import timeline
from creatures import creatures
with open("characters.json", "r") as file:
    characters = json.load(file)
from locations import locations
from relationships import relationships
from world import world
from notes import notes
from projects import projects
from goals import goals
import random
from tips import tips
try:
    with open("sessions.json", "r") as file:
        sessions = json.load(file)
except FileNotFoundError:
    sessions = []
with open("settings.json", "r") as file:
    settings = json.load(file)
from utils import print_header, pause 


def show_header(title):
    print("=" * 40)
    print(title)
    print("=" * 40)
    print()


def display_item(item):
    for title, value in item.items():
        if isinstance(value, dict):
            print(title + ":")

            for sub_title, sub_value in value.items():
                print("  " + sub_title + ":", sub_value)

        elif isinstance(value, list):
            if len(value) == 0:
                continue

            print(title + ":")

            for entry in value:
                print("  •", entry)

        else:
            print(title + ":")
            print("  ", value)

        print()


def project_overview():
    total_entries = (
        len(characters)
        + len(locations)
        + len(relationships)
        + len(world)
        + len(notes)
        + len(projects)
        + len(goals)
        + len(sessions)
        + len(creatures)
        + len(timeline)
    )

    total_words = 0

    for session in sessions:
        total_words = total_words + int(session["Words"])

    print("=" * 30)
    print("Project Overview")
    print("=" * 30)
    print()

    print("Database Statistics")
    print("-" * 20)
    print("Characters     :", len(characters))
    print("Locations      :", len(locations))
    print("Relationships  :", len(relationships))
    print("World Entries  :", len(world))
    print("Notes          :", len(notes))
    print("Projects       :", len(projects))
    print("Goals          :", len(goals))
    print("Writing Logs   :", len(sessions))
    print("Creatures      :", len(creatures))
    print("Timeline Events:", len(timeline))
    print()

    print("Writer Dashboard")
    print("-" * 20)
    print("Current Writer :", settings["Username"])
    print("Total Words    :", total_words)
    print()

    print("StoryVault Status")
    print("-" * 20)
    print("Total Entries  :", total_entries)
    print("Version        :", settings["Version"])
    print("Status         : Prototype")
    print()

    input("Press Enter...")

def timeline_database():

    print("=" * 30)
    print("Timeline")
    print("=" * 30)
    print()

    for key, event in timeline.items():

        print("=" * 30)
        print(event["Name"])
        print("=" * 30)

        display_item(event)

    input("Press Enter...")

def creature_database():

    print("=" * 30)
    print("Creatures")
    print("=" * 30)
    print()

    for key, creature in creatures.items():

        print("=" * 30)
        print(creature["Name"])
        print("=" * 30)

        display_item(creature)

    input("Press Enter...")

def about():
    print("=" * 30)
    print("About StoryVault")
    print("=" * 30)
    print()

    print("StoryVault")
    print("Version : 1.2.0")
    print("Language: Python")
    print()

    print("StoryVault is a worldbuilding and")
    print("project organization tool for")
    print("writers.")
    print()

    print("Created by:")
    print("Manson")
    print()

    print("Current Modules")
    print("----------------")
    print("Characters")
    print("Locations")
    print("World")
    print("Relationships")
    print("Notes")
    print("Projects")
    print("Goals")

    input("Press Enter...")

def pinned_projects():

    print("=" * 30)
    print("Pinned Projects")
    print("=" * 30)
    print()

    found = False

    for project in projects.values():

        if project.get("Pinned") == "Yes":
            print("⭐", project["Name"])
            found = True

    if not found:
        print("No pinned projects.")

    print()
    input("Press Enter...")

def save_sessions():

    with open("sessions.json", "w") as file:
        json.dump(sessions, file, indent=4)

def writing_session():

    print("=" * 30)
    print("Writing Session")
    print("=" * 30)
    print()

    project = input("Project: ")
    goal = input("Goal (words): ")

    print()
    input("Press Enter when you've finished writing...")

    print()

    words = input("Words written: ")

    session = {
        "Project": project,
        "Goal": goal,
        "Words": words
    }

    sessions.append(session)
    save_sessions()

    print()
    print("Session Saved!")
    print()

    print("Project :", project)
    print("Goal    :", goal)
    print("Written :", words)
    print()

    input("Press Enter...")

def writing_statistics():

    print("=" * 30)
    print("Writing Statistics")
    print("=" * 30)
    print()

    if len(sessions) == 0:
        print("No writing sessions yet.")

    else:
        total_words = 0
        best_session = 0
        project_totals = {}
        goals_hit = 0

        for session in sessions:
            project_name = session["Project"]
            words = int(session["Words"])
            goal = int(session["Goal"])

            total_words = total_words + words

            if words > best_session:
                best_session = words

            if project_name not in project_totals:
                project_totals[project_name] = 0

            project_totals[project_name] = project_totals[project_name] + words

            if words >= goal:
                goals_hit = goals_hit + 1

        average_words = total_words / len(sessions)

        print("Sessions        :", len(sessions))
        print("Total Words     :", total_words)
        print("Average Session :", round(average_words))
        print("Best Session    :", best_session)

        print()
        print("Words By Project")
        print("-" * 20)

        for project_name, words in project_totals.items():
            print(project_name + ":", words)

        print()
        print("Goals Summary")
        print("-" * 20)
        print("Goals Hit    :", goals_hit)
        print("Goals Missed :", len(sessions) - goals_hit)

    print()
    input("Press Enter...")

def session_history():

    print("=" * 30)
    print("Writing History")
    print("=" * 30)
    print()

    if len(sessions) == 0:
        print("No writing sessions yet.")

    else:
        total_words = 0

        for number, session in enumerate(sessions, start=1):
            total_words = total_words + int(session["Words"])
            
            

            print("Session", number)
            print("-" * 15)

            display_item(session)
            goal = int(session["Goal"])
            words = int(session["Words"])

            difference = words - goal

            if difference >= 0:
                print("Result:")
                print("   Goal Achieved! (+" + str(difference) + " words)")
            else:
                print("Result:")
                print("   Goal Missed (" + str(difference) + " words)")

            print()

    print("=" * 30)
    print("Total Words Written:", total_words)
    print("=" * 30)
    print()

    input("Press Enter...")

def favorite_characters():
    print("=" * 30)
    print("Favorite Characters")
    print("=" * 30)
    print()

    found = False

    for character in characters.values():
        if character.get("Favorite") == "Yes":
            print("•", character["Name"])
            found = True

    if not found:
        print("No favorite characters.")

    print()
    input("Press Enter...")


def search_all():
    print("=" * 30)
    print("Search All")
    print("=" * 30)

    search = input("Enter search: ").lower()
    print()

    databases = {
        "Character": characters,
        "Location": locations,
        "World": world,
        "Relationship": relationships,
        "Note": notes,
        "Project": projects,
        "Goal": goals,
        "Timeline": timeline,
        "creature": creatures
    }

    found = False
    match_count = 0

    for label, database in databases.items():
        for key, item in database.items():

            if label == "Relationship":
                if search in key.lower() or search in str(item).lower():
                    print("=" * 30)
                    print(label + ":", key)
                    print("=" * 30)
                    display_item(item)
                    print()

                    found = True
                    match_count = match_count + 1

            else:
                if search in str(item).lower():
                    print("=" * 30)
                    print(label + ":", item["Name"])
                    print("=" * 30)
                    display_item(item)
                    print()

                    found = True
                    match_count = match_count + 1

    if not found:
        print("No results found.")
    else:
        print("=" * 30)
        print("Matches Found:", match_count)
        print("=" * 30)

    print()
    input("Press Enter...")

def view_characters():

    print("=" * 30)
    print("Characters")
    print("=" * 30)
    print()

    for key, character in characters.items():

        print("=" * 30)
        print(character["Name"])
        print("=" * 30)

        display_item(character)

    input("Press Enter...")

def save_characters():

    with open("characters.json", "w") as file:
        json.dump(characters, file, indent=4)

def edit_character():

    print("=" * 30)
    print("Edit Character")
    print("=" * 30)
    print()

    name = input("Character to edit: ")

    if name not in characters:
        print("Character not found.")
        input("Press Enter...")
        return

    print()
    print("Leave blank to keep current value.")
    print()

    age = input(f'Age ({characters[name]["Age"]}): ')
    race = input(f'Race ({characters[name]["Race"]}): ')
    status = input(f'Status ({characters[name]["Status"]}): ')

    if age != "":
        characters[name]["Age"] = age

    if race != "":
        characters[name]["Race"] = race

    if status != "":
        characters[name]["Status"] = status

    save_characters()

    print()
    print("Character updated!")

    input("Press Enter...")

def delete_character():

    print("=" * 30)
    print("Delete Character")
    print("=" * 30)
    print()

    name = input("Character to delete: ")

    if name not in characters:
        print("Character not found.")
        input("Press Enter...")
        return

    print()
    confirm = input(f'Delete "{name}"? (y/n): ').lower()

    if confirm == "y":
        del characters[name]
        save_characters()

        print()
        print("Character deleted!")

    else:
        print()
        print("Deletion cancelled.")

    input("Press Enter...")

def character_menu():

    while True:

        print("=" * 30)
        print("Characters")
        print("=" * 30)
        print()

        print("1. View Characters")
        print("2. Add Character")
        print("3. Edit Character")
        print("4. Delete Character")
        print("5. Back")
        print()

        choice = input("Choice: ")

        if choice == "1":
            view_characters()

        elif choice == "2":
            add_character()

        elif choice == "3":
            edit_character()

        elif choice == "4":
            delete_character()

        elif choice == "5":
            break  

        else:
            print("Invalid choice.")

def add_character():

    print("=" * 30)
    print("Add Character")
    print("=" * 30)
    print()

    name = input("Name: ")
    age = input("Age: ")
    race = input("Race: ")
    status = input("Status: ")

    characters[name] = {
        "Name": name,
        "Age": age,
        "Race": race,
        "Status": status
        
    }
    save_characters()
    print()
    print(name, "added successfully!")

    input("Press Enter...")


def open_item(item, label, match):
    print("=" * 30)

    if label == "Relationship":
        print("Relationship:", match["name"])
    else:
        print(label + ":", item["Name"])

    print("Match found in", match["matched_title"])
    print()

    if label == "Character":
        character_menu(item)
    else:
        display_item(item)


def run_search(database, label):
    print("Choose a", label.lower())
    print("-" * 20)

    for key, item in sorted(database.items()):
        if label == "Relationship":
            print(key)
        else:
            print(key + ".", item["Name"])

    print()
    search = input("Enter number or " + label.lower() + " search: ")
    print()

    matches = []

    if label == "Relationship":
        for character_name, relationship_info in database.items():
            if search.lower() in character_name.lower():
                matches.append({
                    "name": character_name,
                    "item": relationship_info,
                    "matched_title": "Character",
                    "matched_value": character_name
                })
                continue

            for title, value in relationship_info.items():
                if search.lower() in str(value).lower():
                    matches.append({
                        "name": character_name,
                        "item": relationship_info,
                        "matched_title": title,
                        "matched_value": value
                    })
                    break

    else:
        if search.isdigit() and search in database:
            info = database[search]

            matches.append({
                "item": info,
                "matched_title": "Selection",
                "matched_value": search
            })

        else:
            for info in database.values():
                for title, value in info.items():
                    if search.lower() in str(value).lower():
                        matches.append({
                            "item": info,
                            "matched_title": title,
                            "matched_value": value
                        })
                        break

    if not matches:
        print("No", label.lower(), "found.")
    else:
        print("Matches Found!")
        print()

        for match in matches:
            item = match["item"]
            open_item(item, label, match)

    input("Press Enter to return to the main menu...")


show_header("        StoryVault v1.3.0")

if settings["Username"] == "Writer":
    player_name = input("What's your name? ")
    settings["Username"] = player_name

    with open("settings.json", "w") as file:
        json.dump(settings, file, indent=4)

else:
    player_name = settings["Username"]

print()
print("Welcome,", player_name + "!")
print()

print("=" * 40)
print("Today's Writing Tip")
print("-" * 40)
print(random.choice(tips))
print("=" * 40)
print()

print("Loaded Successfully!")
print()

while True:
    print()
    print("Main Menu")
    print("-" * 20)
    print("0. Project Overview")
    print("1. Characters")
    print("2. Locations")
    print("3. World")
    print("4. Creatures")
    print("5. Timeline")
    print("6. Relationships")
    print("7. Notes")
    print("8. Projects")
    print("9. About")
    print("A. Search All")
    print("F. Favorite Characters")
    print("P. Pinned Projects")
    print("G. Goals")
    print("W. Writing Session")
    print("H. Session History")
    print("S. Writing Statistics")
    print("10. Exit")

    menu_choice = input("Enter your choice: ")
    print()

    if menu_choice == "0":
        project_overview()

    elif menu_choice == "1":
        character_menu()

    elif menu_choice == "2":
        run_search(locations, "Location")

    elif menu_choice == "3":
        run_search(world, "World")

    elif menu_choice == "4":
        creature_database()

    elif menu_choice == "5":
        timeline_database()

    elif menu_choice == "6":
        run_search(relationships, "Relationship")

    elif menu_choice == "7":
        run_search(notes, "Note")

    elif menu_choice == "8":
        run_search(projects, "Project")

    elif menu_choice == "9":
        about()

    elif menu_choice.lower() == "a":
        search_all()

    elif menu_choice.lower() == "f":
        favorite_characters()

    elif menu_choice.lower() == "p":
        pinned_projects()

    elif menu_choice.lower() == "g":
        run_search(goals, "Goal")

    elif menu_choice.lower() == "w":
        writing_session()

    elif menu_choice.lower() == "h":
        session_history()

    elif menu_choice.lower() == "s":
        writing_statistics()

    elif menu_choice == "10":
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")
        input("Press Enter to return to the main menu...")