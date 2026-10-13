I'll rewrite this README in a more natural voice while keeping every fact the same. I've left out the em-dashes and the banned words.

# CodeVault: Personal Code Library

CodeVault is a menu-driven snippet manager written in Python. You can store, organize, search, edit, and reuse code snippets from one place.

It runs as a simple command-line tool that handles snippets in several programming languages. Snippets are saved as JSON, and you can export them to files. The app also validates input and keeps an activity log.

## Features

- **Add Snippet:** Save a snippet with a unique ID, title, language, category, and description. You can cancel at any point and go back to the main menu.
- **View Snippets:** See saved snippets in a table and read their full descriptions.
- **Search Snippet:** Look up snippets by ID, title, language, or category.
- **Filter by Language:** Show only the snippets for one programming language.
- **Edit Snippet:** Update a snippet's description. The other fields stay the same.
- **Delete Snippet:** Remove a snippet, but only after you confirm.
- **Export Snippet:** Save code to language-specific files like `.py`, `.java`, `.cpp`, `.js`, and `.sql`.
- **JSON Storage:** Snippets go into `snippets.json`, so they're still there next time you open the app.
- **Activity Log:** Events are recorded, and you can view the latest 30 entries.
- **Input Validation:** Invalid menu choices, IDs, and other bad input get caught.
- **Exception Handling:** Storage, file access, and JSON format errors are handled gracefully.

## Technologies Used

- Python 3
- JSON for storage
- `os` for file and directory operations
- `datetime` for log timestamps

Everything the app uses comes from Python's standard library, so there's nothing extra to install.

## Getting Started

### Prerequisites

Install Python 3 if you don't have it yet. To check, run:

```bash
python --version
```

### Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/CodeVault.git
```

Move into the project folder:

```bash
cd CodeVault
```

Start the app:

```bash
python main.py
```

If your Python file has a different name, swap in its actual name for `main.py`.

## Main Menu

1. Add a new snippet
2. View all snippets
3. Search for snippets
4. Filter by programming language
5. Edit a snippet
6. Delete a snippet
7. Export a snippet
8. View the activity log
9. Exit

## Data Storage

CodeVault creates these files and folders in the project directory as it runs:

- `snippets.json` holds your saved snippet records.
- `activity_log.txt` holds timestamped application events.
- `exports/` is where exported code files go by default.

The storage files appear the first time you use the app that needs them.

**Note:** If `snippets.json` holds snippets you care about, back it up regularly.

## Input Controls

- Type `:cancel` to back out of snippet creation.
- Type `:done` on a new line to finish entering code.
- On an edit prompt, press Enter to keep the current value.

## Demonstrated Concepts

The project uses classes and objects, functions, lists, tuples, dictionaries, loops, conditionals, list parsing, file management, JSON serialization, and exception handling.

## Future Improvements

- Add sorting and more advanced search.
- Support importing snippets from external files.
- Add backup and restore options.
- Build a graphical user interface.

## License

No license has been chosen yet. If you want to set terms for how others can use, modify, or share the code, add a license file.
