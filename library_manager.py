import csv
import os
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

DATA_FILE = "library_books.csv"

def load_books():
    """Load all books from the CSV data file.
    
    Returns:
        list: A list of dictionaries where each dictionary represents a book
        with keys: title, author, isbn, status, due_date, borrower.
        Returns empty list if file doesn't exist (creates file in this case).
    """
    books = []
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["title", "author", "isbn", "status", "due_date", "borrower"])
        return books

    with open(DATA_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            books.append(row)
    return books

def save_books(books):
    """Save the list of books to the CSV data file.
    
    Args:
        books (list): List of book dictionaries to be saved.
    """
    with open(DATA_FILE, 'w', newline='') as file:
        fieldnames = ["title", "author", "isbn", "status", "due_date", "borrower"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books)

def fill_tree(tree, books):
    """Populate a Treeview widget with book data.
    
    Args:
        tree (ttk.Treeview): The Treeview widget to populate.
        books (list): List of book dictionaries to display in the tree.
    """
    for row in tree.get_children():
        tree.delete(row)
    today = datetime.now().date()
    for book in books:
        due_date_str = book['due_date'] if book['due_date'] else 'N/A'
        status = book['status']
        borrower = book['borrower'] if book['borrower'] else 'N/A'

        is_overdue = False
        if status == 'checked out' and book['due_date']:
            due_date = datetime.strptime(book['due_date'], '%Y-%m-%d').date()
            if due_date < today:
                is_overdue = True
                status = "OVERDUE"
                display_title = "⚠️ " + book['title'][:28]
            else:
                display_title = book['title'][:30]
        else:
            display_title = book['title'][:30]

        tree.insert('', 'end', values=(
            display_title,
            book['author'][:20],
            book['isbn'],
            status,
            due_date_str,
            borrower
        ))

def view_all_books():
    """Display a window showing all books in the library with their current status."""
    books = load_books()
    win = tk.Toplevel(root)
    win.title("View All Books")
    win.geometry("850x400")

    cols = ("Title", "Author", "ISBN", "Status", "Due Date", "Borrower")
    tree = ttk.Treeview(win, columns=cols, show='headings')
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(expand=True, fill='both')

    fill_tree(tree, books)

def add_new_book():
    """Display a form to add a new book to the library collection."""
    def submit():
        """Validate and submit new book data to be added to the library."""
        title = ent_title.get().strip()
        author = ent_author.get().strip()
        isbn = ent_isbn.get().strip()

        if not title or not author:
            messagebox.showerror("Input Error", "Title and author cannot be empty.")
            return
        if len(isbn) != 13 or not isbn.isdigit():
            messagebox.showerror("Input Error", "ISBN must be exactly 13 digits.")
            return

        books = load_books()
        if any(book['isbn'] == isbn for book in books):
            messagebox.showerror("Input Error", "A book with this ISBN already exists.")
            return

        new_book = {
            'title': title,
            'author': author,
            'isbn': isbn,
            'status': 'available',
            'due_date': '',
            'borrower': ''
        }
        books.append(new_book)
        save_books(books)
        messagebox.showinfo("Success", f"'{title}' added to the library.")
        win.destroy()

    win = tk.Toplevel(root)
    win.title("Add New Book")
    win.geometry("350x200")

    tk.Label(win, text="Title:").pack(pady=5)
    ent_title = tk.Entry(win, width=40)
    ent_title.pack()

    tk.Label(win, text="Author:").pack(pady=5)
    ent_author = tk.Entry(win, width=40)
    ent_author.pack()

    tk.Label(win, text="ISBN (13 digits):").pack(pady=5)
    ent_isbn = tk.Entry(win, width=40)
    ent_isbn.pack()

    tk.Button(win, text="Add Book", command=submit).pack(pady=10)

def check_out_book():
    """Display interface for checking out available books to borrowers."""
    books = load_books()
    available_books = [b for b in books if b['status'] == 'available']

    if not available_books:
        messagebox.showinfo("Info", "No available books to check out.")
        return

    def submit():
        """Process book checkout with validation of selected book and borrower name."""
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a book to check out.")
            return
        borrower = ent_borrower.get().strip()
        if not borrower:
            messagebox.showerror("Error", "Enter borrower name.")
            return

        isbn = tree.item(selected[0])['values'][2]
        for book in books:
            if book['isbn'] == isbn:
                book['status'] = 'checked out'
                book['due_date'] = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
                book['borrower'] = borrower
                save_books(books)
                messagebox.showinfo("Success", f"Checked out '{book['title']}' to {borrower}.")
                win.destroy()
                return

    win = tk.Toplevel(root)
    win.title("Check Out Book")
    win.geometry("800x400")

    cols = ("Title", "Author", "ISBN", "Status", "Due Date", "Borrower")
    tree = ttk.Treeview(win, columns=cols, show='headings')
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(expand=True, fill='both')

    fill_tree(tree, available_books)

    tk.Label(win, text="Borrower Name:").pack(pady=5)
    ent_borrower = tk.Entry(win, width=40)
    ent_borrower.pack()

    tk.Button(win, text="Check Out", command=submit).pack(pady=10)

def return_book():
    """Display interface for returning checked out books to the library."""
    books = load_books()
    checked_out = [b for b in books if b['status'] == 'checked out']

    if not checked_out:
        messagebox.showinfo("Info", "No books are currently checked out.")
        return

    def submit():
        """Process book return for the selected book."""
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a book to return.")
            return

        isbn = tree.item(selected[0])['values'][2]
        for book in books:
            if book['isbn'] == isbn and book['status'] == 'checked out':
                book['status'] = 'available'
                book['due_date'] = ''
                book['borrower'] = ''
                save_books(books)
                messagebox.showinfo("Success", f"Returned '{book['title']}'.")
                win.destroy()
                return

    win = tk.Toplevel(root)
    win.title("Return Book")
    win.geometry("800x400")

    cols = ("Title", "Author", "ISBN", "Status", "Due Date", "Borrower")
    tree = ttk.Treeview(win, columns=cols, show='headings')
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(expand=True, fill='both')

    fill_tree(tree, checked_out)

    tk.Button(win, text="Return Book", command=submit).pack(pady=10)

def search_books():
    """Display search interface to find books by title, author, or ISBN."""
    books = load_books()

    def do_search():
        """Execute search based on user's criteria and display results."""
        term = ent_search.get().lower()
        choice = var_search.get()
        if not term:
            messagebox.showerror("Error", "Enter a search term.")
            return

        results = []
        for book in books:
            if choice == "Title" and term in book['title'].lower():
                results.append(book)
            elif choice == "Author" and term in book['author'].lower():
                results.append(book)
            elif choice == "ISBN" and term in book['isbn'].lower():
                results.append(book)

        fill_tree(tree, results)
        lbl_result.config(text=f"{len(results)} result(s) found.")

    win = tk.Toplevel(root)
    win.title("Search Books")
    win.geometry("850x500")

    tk.Label(win, text="Search by:").pack(pady=5)
    var_search = tk.StringVar(value="Title")
    frame = tk.Frame(win)
    frame.pack()
    for opt in ["Title", "Author", "ISBN"]:
        tk.Radiobutton(frame, text=opt, variable=var_search, value=opt).pack(side='left')

    ent_search = tk.Entry(win, width=50)
    ent_search.pack(pady=5)

    tk.Button(win, text="Search", command=do_search).pack()

    cols = ("Title", "Author", "ISBN", "Status", "Due Date", "Borrower")
    tree = ttk.Treeview(win, columns=cols, show='headings')
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(expand=True, fill='both')

    lbl_result = tk.Label(win, text="")
    lbl_result.pack(pady=5)

def check_overdue_books():
    """Display all overdue books with calculated fines."""
    books = load_books()
    today = datetime.now().date()
    overdue_books = []
    total_fines = 0.0

    for book in books:
        if book['status'] == 'checked out' and book['due_date']:
            due_date = datetime.strptime(book['due_date'], '%Y-%m-%d').date()
            if due_date < today:
                days_overdue = (today - due_date).days
                fine = days_overdue * 0.50
                total_fines += fine
                overdue_books.append(book)

    if not overdue_books:
        messagebox.showinfo("No Overdue Books", "No overdue books found.")
        return

    win = tk.Toplevel(root)
    win.title("Overdue Books and Fines")
    win.geometry("850x400")

    cols = ("Title", "Author", "ISBN", "Status", "Due Date", "Borrower", "Fine")
    tree = ttk.Treeview(win, columns=cols, show='headings')
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=110)
    tree.pack(expand=True, fill='both')

    for book in overdue_books:
        due_date = datetime.strptime(book['due_date'], '%Y-%m-%d').date()
        days_overdue = (today - due_date).days
        fine = days_overdue * 0.50
        display_title = "⚠️ " + book['title'][:28]

        tree.insert('', 'end', values=(
            display_title,
            book['author'][:20],
            book['isbn'],
            "OVERDUE",
            book['due_date'],
            book['borrower'],
            f"${fine:.2f}"
        ))

    lbl = tk.Label(win, text=f"Total Fines Due: ${total_fines:.2f}", font=("Arial", 12, "bold"))
    lbl.pack(pady=10)

def edit_book():
    """Display interface for editing book details (title, author, ISBN)."""
    books = load_books()

    def load_book_details(event):
        """Load selected book's details into the edit form."""
        selected = tree.selection()
        if not selected:
            return
        isbn = tree.item(selected[0])['values'][2]
        for book in books:
            if book['isbn'] == isbn:
                ent_title.delete(0, tk.END)
                ent_title.insert(0, book['title'])
                ent_author.delete(0, tk.END)
                ent_author.insert(0, book['author'])
                ent_isbn.delete(0, tk.END)
                ent_isbn.insert(0, book['isbn'])
                current_isbn.set(isbn)
                break

    def submit():
        """Validate and save edited book details."""
        original_isbn = current_isbn.get()
        new_title = ent_title.get().strip()
        new_author = ent_author.get().strip()
        new_isbn_val = ent_isbn.get().strip()

        if not new_title or not new_author:
            messagebox.showerror("Error", "Title and Author cannot be empty.")
            return
        if len(new_isbn_val) != 13 or not new_isbn_val.isdigit():
            messagebox.showerror("Error", "ISBN must be exactly 13 digits.")
            return
        if any(b['isbn'] == new_isbn_val and b['isbn'] != original_isbn for b in books):
            messagebox.showerror("Error", "Another book with this ISBN exists.")
            return

        for book in books:
            if book['isbn'] == original_isbn:
                book['title'] = new_title
                book['author'] = new_author
                book['isbn'] = new_isbn_val
                save_books(books)
                messagebox.showinfo("Success", "Book updated successfully.")
                win.destroy()
                return

    win = tk.Toplevel(root)
    win.title("Edit Book")
    win.geometry("400x250")

    cols = ("Title", "Author", "ISBN", "Status", "Due Date", "Borrower")
    tree = ttk.Treeview(win, columns=cols, show='headings', height=6)
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack()

    fill_tree(tree, books)
    tree.bind('<<TreeviewSelect>>', load_book_details)

    current_isbn = tk.StringVar()

    frm = tk.Frame(win)
    frm.pack(pady=10)

    tk.Label(frm, text="Title:").grid(row=0, column=0, sticky='e')
    ent_title = tk.Entry(frm, width=30)
    ent_title.grid(row=0, column=1)

    tk.Label(frm, text="Author:").grid(row=1, column=0, sticky='e')
    ent_author = tk.Entry(frm, width=30)
    ent_author.grid(row=1, column=1)

    tk.Label(frm, text="ISBN:").grid(row=2, column=0, sticky='e')
    ent_isbn = tk.Entry(frm, width=30)
    ent_isbn.grid(row=2, column=1)

    tk.Button(win, text="Update Book", command=submit).pack(pady=10)

def delete_book():
    """Display interface for deleting books from the library collection."""
    books = load_books()

    def submit():
        """Delete selected book after confirmation, with validation for checked out books."""
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a book to delete.")
            return
        isbn = tree.item(selected[0])['values'][2]
        for i, book in enumerate(books):
            if book['isbn'] == isbn:
                if book['status'] == 'checked out':
                    messagebox.showerror("Error", "Cannot delete a checked out book.")
                    return
                confirm = messagebox.askyesno("Confirm Delete", f"Delete '{book['title']}'?")
                if confirm:
                    del books[i]
                    save_books(books)
                    messagebox.showinfo("Success", "Book deleted.")
                    win.destroy()
                return

    win = tk.Toplevel(root)
    win.title("Delete Book")
    win.geometry("800x400")

    cols = ("Title", "Author", "ISBN", "Status", "Due Date", "Borrower")
    tree = ttk.Treeview(win, columns=cols, show='headings')
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(expand=True, fill='both')

    fill_tree(tree, books)

    tk.Button(win, text="Delete Selected Book", command=submit).pack(pady=10)

root = tk.Tk()
root.title("Library Book Manager")
root.geometry("400x500")

title_lbl = tk.Label(root, text="📚 Library Book Manager", font=("Arial", 18, "bold"))
title_lbl.pack(pady=20)

btn_specs = [
    ("📖 View All Books", view_all_books),
    ("🔍 Search Books", search_books),
    ("📝 Check Out Book", check_out_book),
    ("↩️ Return Book", return_book),
    ("➕ Add New Book", add_new_book),
    ("⚠️ View Overdue Books & Fines", check_overdue_books),
    ("✏️ Edit Book Details", edit_book),
    ("❌ Delete Book", delete_book),
    ("❎ Exit", root.quit),
]

for (text, func) in btn_specs:
    tk.Button(root, text=text, font=("Arial", 12), width=30, command=func).pack(pady=5)

root.mainloop()