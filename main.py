from characters import characters
from locations import locations
from relationships import relationships
from world import world


def show_header(title):
    print("=" * 40)
    print(title)
    print("=" * 40)
    print()


def display_item(item):
    for title, value in item.items():
        if isinstance(value, list):
            if len(value) == 0:
                continue

            print(title + ":")

            for entry in value:
                print("  •", entry)

        else:
            print(title + ":")
            print("  ", value)

        print()


def character_menu(character):
    while True:
        print("=" * 30)
        print(character["Name"])
        print("=" * 30)
        print("1. General Information")
        print("2. Relationships")
        print("3. Timeline")
        print("4. Notes")
        print("5. Quotes")
        print("6. Back")

        choice = input("Choice: ")
        print()

        if choice == "1":
            display_item(character)
            input("Press Enter...")

        elif choice == "2":
            character_name = character["Name"]

            if character_name in relationships:
                print("=" * 30)
                print(character_name + " Relationships")
                print("=" * 30)
                display_item(relationships[character_name])
            else:
                print("No relationships found for", character_name + ".")

            input("Press Enter...")

        elif choice == "3":
            print("Timeline coming soon!")
            input("Press Enter...")

        elif choice == "4":
            print("Notes coming soon!")
            input("Press Enter...")

        elif choice == "5":
            print("Quotes coming soon!")
            input("Press Enter...")

        elif choice == "6":
            break

        else:
            print("Invalid choice.")
            input("Press Enter...")


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

    input("Press Enter to return to the main menu...")


show_header("        StoryVault v1.0.0")

player_name = input("What's your name? ")
print()
print("Welcome,", player_name + "!")
print()

while True:
    print()
    print("Main Menu")
    print("-" * 20)
    print("1. Characters")
    print("2. Locations")
    print("3. World")
    print("4. Creatures")
    print("5. Timeline")
    print("6. Relationships")
    print("7. Exit")

    menu_choice = input("Enter your choice: ")
    print()

    if menu_choice == "1":
        run_search(characters, "Character")

    elif menu_choice == "2":
        run_search(locations, "Location")

    elif menu_choice == "3":
        run_search(world, "World")

    elif menu_choice == "4":
        print("Creatures module coming soon!")
        input("Press Enter to return to the main menu...")

    elif menu_choice == "5":
        print("Timeline module coming soon!")
        input("Press Enter to return to the main menu...")

    elif menu_choice == "6":
        run_search(relationships, "Relationship")

    elif menu_choice == "7":
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")
        input("Press Enter to return to the main menu...")