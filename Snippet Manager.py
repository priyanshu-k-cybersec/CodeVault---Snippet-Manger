#Snippet Manager
import json
import os
from datetime import datetime

#file or program save or export location
Project_folder = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(Project_folder, "snippets.json")
lod_file = os.path.join(Project_folder, "activity_log.txt")
export_dir = os.path.join(Project_folder, "exports")

languages = ("Python", "Java", "C", "C++", "JavaScript", "SQL", "Other")
extensions = {
    "Python": ".py", "Java": ".java", "C": ".c", "C++": ".cpp",
    "JavaScript": ".js", "SQL": ".sql", "Other": ".txt"
}

#custom exception
class ValidationError(Exception):
    pass

#for delete yes no
def ask_yes_no(question):
    while True:
        answer = input(question + " (Y/N): ").strip().upper() #strip to remove space
        if answer == "Y":
            return True
        elif answer == "N":
            return False
        print("Please enter Y or N.")

#for input
def read_code():
    print("Enter code (type :done on a new line to finish, or :cancel to cancel):")
    lines = [] #normal input takes only one line 
    while True:
        line = input()
        if line.strip().lower() == ":done":
            return "\n".join(lines).rstrip()
        if line.strip().lower() == ":cancel":
            return None
        lines.append(line)
#run until user type :done or :cancel

#store data in object
class Snippet: #individual snippet
    def __init__(self, snippet_id, title, language, category, description, code):
        self.snippet_id = snippet_id
        self.title = title
        self.language = language
        self.category = category
        self.description = description
        self.code = code

    def show_row(self): #short info
        print(f"{self.snippet_id:<6}{self.title[:25]:<28}{self.language:<12}{self.category[:15]:<18}")

    def show_details(self): #full info 
        print("\n" + "=" * 55)
        print("ID          :", self.snippet_id)
        print("Title       :", self.title)
        print("Language    :", self.language)
        print("Category    :", self.category)
        print("Description :", self.description or "-")
        print("-" * 55)
        print(self.code)
        print("=" * 55)

#to update the existing snippet
    def update(self, title, language, category, description, code):
        if title.strip():
            self.title = title.strip()# replace the old
        if language.strip():
            self.language = language.strip()
        if category.strip():
            self.category = category.strip()
        if description.strip():
            self.description = description.strip()
        if code.strip():
            self.code = code.strip()

# convert obj to dic to save easily json 
    def to_dict(self):
        return {
            "id": self.snippet_id,
            "title": self.title,
            "language": self.language,
            "category": self.category,
            "description": self.description,
            "code": self.code
        }


class SnippetManager: # complete snippet manager
    def __init__(self):
        self.snippets = [] #list of all snippets
        self.locked = False
        self.unsaved = False
        self.log("Application started")
        self.load_snippets() # log create, existing snippet load

#log manager
    def log(self, message):
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #readable format convert
        try:
            with open(lod_file, "a", encoding="utf-8") as f:
                f.write(f"{time_str} | {message}\n")
        except OSError:
            print("Warning: could not write to the log file.")

#load snippet form json
    def load_snippets(self):
        try:
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            for r in data:
                self.snippets.append(Snippet(
                    int(r["id"]), r["title"], r["language"],
                    r["category"], r["description"], r["code"]
                ))
            self.log(f"Loaded {len(self.snippets)} snippet(s)")
        except FileNotFoundError:
            print("Storage file not found. Creating a new one...")
            self.log("Storage file missing, new file created")
            self.save_snippets()
        except json.JSONDecodeError:
            self.lock("The storage file has invalid JSON")
        except KeyError as e:
            self.lock(f"A record is missing the field {e}")
        except (ValueError, TypeError):
            self.lock("The storage file has wrongly formatted data")
        except PermissionError:
            self.lock("No permission to read the storage file")
        except OSError:
            self.lock("The storage file could not be read")

# agar storage me serious problem aaye to program ke modifying operation disable karta h
    def lock(self, reason):
        self.locked = True
        self.snippets = []
        print(f"\nWARNING: {reason}.")
        print("Original file is untouched. Add/Edit/Delete are disabled.")
        print("Fix or rename snippets.json and restart.\n")
        self.log("Storage error: " + reason)

#save current snippet to json
    def save_snippets(self):
        records = [s.to_dict() for s in self.snippets] #obj to dic 
        try:
            with open(data_file, "w", encoding="utf-8") as f:
                json.dump(records, f, indent=4) #dic to json
            self.unsaved = False
            return True
        except PermissionError:
            print("Error: no permission to save the file.")
            self.log("Storage error: permission denied while saving")
        except OSError:
            print("Error: could not save the file.")
            self.log("Storage error: could not save")
        self.unsaved = True
        return False

#find snippet with id
    def find(self, snippet_id):
        for s in self.snippets:
            if s.snippet_id == snippet_id:
                return s
        return None

    def ask_snippet(self, prompt):
        try:
            snippet_id = int(input(prompt))
        except ValueError:
            print("Error: ID must be a number.")
            self.log("Invalid input: non-numeric ID")
            return None
        snippet = self.find(snippet_id)
        if snippet is None:
            print("No snippet found with ID", snippet_id)
        return snippet

    def ask_language(self, can_skip=False, can_cancel=False):
        print("\nlanguages:")
        for i, name in enumerate(languages, start=1):
            print(f"  {i}. {name}")
        while True:
            choice = input("Choose language number: ").strip()
            if choice.lower() == ":cancel" and can_cancel:
                return None
            if choice == "" and can_skip:
                return ""
            try:
                number = int(choice)
                if number < 1 or number > len(languages):
                    raise ValidationError("Choose a number from the list.")
                return languages[number - 1]
            except ValueError:
                print("Error: enter a number.")
                self.log("Invalid input: non-numeric language choice")
            except ValidationError as e:
                print("Error:", e)

#show snippets in table format
    def show_table(self, items):
        print(f"\n{'ID':<6}{'Title':<28}{'Language':<12}{'Category':<18}")
        print("-" * 64)
        for s in items:
            s.show_row()
        print("Total:", len(items))
        choice = input("Enter an ID to see full details (Enter to go back): ").strip()
        if choice != "": #show full details of snippet
            if choice.isdigit() and self.find(int(choice)):
                self.find(int(choice)).show_details()
            else:
                print("Invalid ID.")

#add snippet 
    def add_snippet(self):
        if self.locked:
            print("Storage has a problem, changes are disabled.")
            return
        print("\n--- Add New Snippet ---")
        print("Type ':cancel' at any step to return to the main menu.")

        while True:
            try:
                id_input = input("Snippet ID: ").strip()
                if id_input.lower() == ":cancel":
                    print("Adding snippet cancelled.")
                    return

                snippet_id = int(id_input)
                if snippet_id <= 0:
                    raise ValidationError("ID must be positive.")
                if self.find(snippet_id) is not None:
                    raise ValidationError("This ID already exists.")
                break
            except ValueError:
                print("Error: ID must be a number.")
                self.log("Invalid input: non-numeric ID")
            except ValidationError as e:
                print("Error:", e)
                self.log("Invalid input: " + str(e))

        while True:
            title = input("Title: ").strip()
            if title.lower() == ":cancel":
                print("Adding snippet cancelled.")
                return
            try:
                if title == "":
                    raise ValidationError("Title cannot be empty.")
                break
            except ValidationError as e:
                print("Error:", e)
                self.log("Invalid input: " + str(e))

        language = self.ask_language(can_cancel=True)
        if language is None:
            print("Adding snippet cancelled.")
            return

        category = input("Category: ").strip()
        if category.lower() == ":cancel":
            print("Adding snippet cancelled.")
            return
        category = category or "General"

        description = input("Description: ").strip()
        if description.lower() == ":cancel":
            print("Adding snippet cancelled.")
            return

#enter code to save
        while True:
            code = read_code()
            if code is None:
                print("Adding snippet cancelled.")
                return
            try:
                if code.strip() == "":
                    raise ValidationError("Code cannot be empty.")
                break
            except ValidationError as e:
                print("Error:", e)
                self.log("Invalid input: " + str(e))

        self.snippets.append(Snippet(snippet_id, title, language, category, description, code)) #after code obj append to list  
        self.log(f"Snippet added: ID {snippet_id}")
        if self.save_snippets():
            print("Snippet added and saved!")
        else:
            print("Snippet added but not saved. It will be retried on exit.")

    def view_all(self):
        if len(self.snippets) == 0:
            print("\nNo snippets saved yet.")
        else:
            self.show_table(self.snippets)

    def search_snippet(self):
        keyword = input("\nSearch (ID, title, language or category): ").strip().lower()
        if keyword == "":
            print("Search text cannot be empty.")
            return
        results = [
            s for s in self.snippets
            if (keyword == str(s.snippet_id) or keyword in s.title.lower()
                or keyword in s.language.lower() or keyword in s.category.lower())
        ]
        if len(results) == 0:
            print("No snippets matched your search.")
        else:
            self.show_table(results)

    def filter_by_language(self):
        language = self.ask_language(can_skip=True)
        if language == "":
            print("Filter cancelled.")
            return
        matches = [s for s in self.snippets if s.language == language]
        if len(matches) == 0:
            print(f"No {language} snippets found.")
        else:
            self.show_table(matches)

    def edit_snippet(self):
        if self.locked:
            print("Storage has a problem, changes are disabled.")
            return
        snippet = self.ask_snippet("\nEnter ID of snippet to edit: ")
        if snippet is None:
            return
        snippet.show_details()
        print("Press Enter to keep the old value.")
        title = input("New title: ").strip()
        language = self.ask_language(can_skip=True)
        category = input("New category: ").strip()
        description = input("New description: ").strip()
        print("New code - type :done directly to keep old code.")
        code = read_code()

        snippet.update(title, language, category, description, code)
        self.log(f"Snippet edited: ID {snippet.snippet_id}")
        if self.save_snippets():
            print("Snippet updated and saved!")
        else:
            print("Snippet updated but not saved. It will be retried on exit.")

    def delete_snippet(self):
        if self.locked:
            print("Storage has a problem, changes are disabled.")
            return
        snippet = self.ask_snippet("\nEnter ID of snippet to delete: ")
        if snippet is None:
            return
        snippet.show_details()
        if ask_yes_no("Do you really want to delete this snippet?"):
            self.snippets.remove(snippet)
            self.log(f"Snippet deleted: ID {snippet.snippet_id}")
            if self.save_snippets():
                print("Snippet deleted.")
            else:
                print("Deleted but not saved. It will be retried on exit.")
        else:
            print("Deletion cancelled.")

    def export_snippet(self):
        snippet = self.ask_snippet("\nEnter ID of snippet to export: ")
        if snippet is None:
            return
        folder = input("Export folder (Enter for default 'exports'): ").strip()
        if folder == "":
            folder = export_dir

        name = "".join(ch if ch.isalnum() else "_" for ch in snippet.title)
        ext = extensions.get(snippet.language, ".txt")
        file_name = f"{name}_{snippet.snippet_id}{ext}"
        path = os.path.join(folder, file_name)

        if os.path.exists(path):
            if not ask_yes_no("File already exists. Overwrite?"):
                print("Export cancelled.")
                return
        try:
            os.makedirs(folder, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(snippet.code + "\n")
            print("Exported to:", path)
            self.log(f"Snippet exported: ID {snippet.snippet_id}")
        except PermissionError:
            print("Export failed: no permission for that location.")
            self.log("Storage error: export permission denied")
        except OSError:
            print("Export failed: invalid path or file cannot be written.")
            self.log("Storage error: export failed (invalid path)")

    def view_log(self):
        try:
            with open(lod_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print("\nNo activity log yet.")
            return
        except OSError:
            print("\nCould not read the activity log.")
            return
        print("\n--- Activity Log (last 30 entries) ---")
        for line in lines[-30:]:
            print(line.rstrip())

    def run(self):
        while True:
            print("\n" + "=" * 38)
            print("   CODEVAULT — PERSONAL CODE LIBRARY")
            print("=" * 38)
            print("1. Add New Snippet")
            print("2. View All Snippets")
            print("3. Search Snippet")
            print("4. Filter by Programming Language")
            print("5. Edit Snippet")
            print("6. Delete Snippet")
            print("7. Export Snippet")
            print("8. View Activity Log")
            print("9. Exit")

            try:
                choice = int(input("Enter your choice (1-9): "))
            except ValueError:
                print("Invalid input! Enter a number from 1 to 9.")
                self.log("Invalid input: non-numeric menu choice")
                continue

            if choice == 1:
                self.add_snippet()
            elif choice == 2:
                self.view_all()
            elif choice == 3:
                self.search_snippet()
            elif choice == 4:
                self.filter_by_language()
            elif choice == 5:
                self.edit_snippet()
            elif choice == 6:
                self.delete_snippet()
            elif choice == 7:
                self.export_snippet()
            elif choice == 8:
                self.view_log()
            elif choice == 9:
                break
            else:
                print("Invalid choice! Please select between 1 and 9.")
                self.log("Invalid input: menu choice out of range")


def main():
    manager = SnippetManager()
    try:
        manager.run()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram interrupted.")
    finally:
        if manager.unsaved and not manager.locked:
            manager.save_snippets()
        manager.log("Application exited")
        print("\nThank you for using CodeVault. Goodbye!")


if __name__ == "__main__":
    main()