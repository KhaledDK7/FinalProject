# Library Book Manager

A simple and intuitive desktop application for managing a library's book inventory, checkouts, returns, and overdue fines.

## Description

The Library Book Manager is a Python-based GUI application designed to help librarians or small libraries track books, borrowers, and overdue statuses. It provides functionality to add, view, search, delete, check out, and return books, with automatic due dates and fine calculations. Data is stored in a CSV file for persistence and easy backup.

Built with `Tkinter`, this application offers a clean, user-friendly interface and is entirely local—no internet or external databases required.

## Getting Started

### Dependencies

- Python 3.7 or later
- Tkinter (comes with Python standard library)
- OS: Windows, macOS, or Linux (with Python GUI support)

## Requirements

This app uses only Python's standard library. No additional packages are required.

### Executing program

1. Open a terminal or command prompt.
2. Run the program with:
```
python library_manager.py
```
3. The main window will launch. From there, you can:
   - Add books
   - Search by title, author, or ISBN
   - Check out and return books
   - View overdue books and associated fines
   - Delete books that are available

## Help

If the app window doesn't appear or you receive a `TclError`, make sure your Python installation includes `Tkinter`.
```
sudo apt-get install python3-tk   # For Ubuntu/Debian
```

If you get a file not found error, ensure that the CSV file (`library_books.csv`) is in the same folder, or let the app generate it on first run.

## Authors

Khaled Deek  
[@KhaledDK7](https://github.com/KhaledDK7)

## Version History

* 0.2
    * Added overdue fine calculation and display
    * Enhanced UI with emoji indicators
    * Bug fixes and UI improvements
* 0.1
    * Initial Release with book add/view/search/check out/return/delete functionality