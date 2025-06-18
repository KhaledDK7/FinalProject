import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

DATA_FILE = "library_books.csv"

class LibraryManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Book Manager")
        self.root.geometry("1000x600")
        self.books = self.load_books()
        
        """Main layout"""
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="📚 Library Book Manager", font=('Arial', 16, 'bold')).pack(pady=(0, 20))
        
        """Buttons"""
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        buttons = [("📖 View All", self.view_all_books), ("🔍 Search", self.search_books), 
                  ("📝 Check Out", self.check_out_book), ("↩️ Return", self.return_book), 
                  ("➕ Add Book", self.add_new_book), ("⚠️ Overdue", self.view_overdue_books), 
                  ("❌ Delete", self.delete_book)]
        
        for text, command in buttons:
            ttk.Button(button_frame, text=text, command=command).pack(side=tk.LEFT, padx=5)
        
        """Treeview"""
        self.tree = ttk.Treeview(main_frame, columns=('Title', 'Author', 'ISBN', 'Status', 'Due Date', 'Borrower'), show='headings')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        """Status bar"""
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN).pack(fill=tk.X, pady=(10, 0))
        
        self.refresh_display()
    
    def load_books(self):
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'w', newline='') as file:
                csv.writer(file).writerow(["title", "author", "isbn", "status", "due_date", "borrower"])
            return []
        
        with open(DATA_FILE, 'r') as file:
            return list(csv.DictReader(file))
    
    def save_books(self):
        with open(DATA_FILE, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["title", "author", "isbn", "status", "due_date", "borrower"])
            writer.writeheader()
            writer.writerows(self.books)
    
    def refresh_display(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        today = datetime.now().date()
        for book in self.books:
            status, title = book['status'], book['title']
            if status == 'checked out' and book['due_date']:
                try:
                    if datetime.strptime(book['due_date'], '%Y-%m-%d').date() < today:
                        status, title = "⚠️ OVERDUE", f"⚠️ {title}"
                except ValueError:
                    pass
            
            self.tree.insert('', 'end', values=(title, book['author'], book['isbn'], status, book['due_date'] or 'N/A', book['borrower'] or 'N/A'))
        
        self.status_var.set(f"Displaying {len(self.books)} books")
    
    def view_all_books(self):
        self.books = self.load_books()
        self.refresh_display()
    
    def search_books(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Books")
        search_window.geometry("400x200")
        
        ttk.Label(search_window, text="Search Books", font=('Arial', 12, 'bold')).pack(pady=10)
        
        search_type = tk.StringVar(value="title")
        frame = ttk.Frame(search_window)
        frame.pack(pady=5)
        for text, value in [("Title", "title"), ("Author", "author"), ("ISBN", "isbn")]:
            ttk.Radiobutton(frame, text=text, variable=search_type, value=value).pack(side=tk.LEFT)
        
        ttk.Label(search_window, text="Search term:").pack(pady=(10, 0))
        search_entry = ttk.Entry(search_window, width=30)
        search_entry.pack(pady=5)
        search_entry.focus()
        
        def perform_search():
            term = search_entry.get().lower().strip()
            if not term:
                return messagebox.showwarning("Warning", "Please enter a search term")
            
            results = [book for book in self.books if term in book[search_type.get()].lower()]
            
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            if results:
                today = datetime.now().date()
                for book in results:
                    status, title = book['status'], book['title']
                    if status == 'checked out' and book['due_date']:
                        try:
                            if datetime.strptime(book['due_date'], '%Y-%m-%d').date() < today:
                                status, title = "⚠️ OVERDUE", f"⚠️ {title}"
                        except ValueError:
                            pass
                    self.tree.insert('', 'end', values=(title, book['author'], book['isbn'], status, book['due_date'] or 'N/A', book['borrower'] or 'N/A'))
                
                self.status_var.set(f"Found {len(results)} matching books")
                search_window.destroy()
            else:
                messagebox.showinfo("No Results", "No matching books found")
        
        ttk.Button(search_window, text="Search", command=perform_search).pack(pady=10)
        search_entry.bind('<Return>', lambda e: perform_search())
    
    def get_input_dialog(self, title, fields):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x" + str(150 + len(fields) * 40))
        
        ttk.Label(dialog, text=title, font=('Arial', 12, 'bold')).pack(pady=10)
        
        entries = {}
        for field in fields:
            ttk.Label(dialog, text=f"{field}:").pack()
            entry = ttk.Entry(dialog, width=30)
            entry.pack(pady=5)
            entries[field] = entry
            if field == fields[0]:
                entry.focus()
        
        result = {}
        def submit():
            for field, entry in entries.items():
                result[field] = entry.get().strip()
            dialog.destroy()
        
        ttk.Button(dialog, text="Submit", command=submit).pack(pady=10)
        dialog.wait_window()
        return result
    
    def check_out_book(self):
        if not self.books:
            return messagebox.showinfo("Info", "No books available")
        
        data = self.get_input_dialog("Check Out Book", ["Book ISBN", "Borrower Name"])
        if not data.get("Book ISBN") or not data.get("Borrower Name"):
            return
        
        for book in self.books:
            if book['isbn'] == data["Book ISBN"]:
                if book['status'] == 'available':
                    book['status'] = 'checked out'
                    book['due_date'] = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
                    book['borrower'] = data["Borrower Name"]
                    self.save_books()
                    self.refresh_display()
                    return messagebox.showinfo("Success", f"Successfully checked out '{book['title']}' to {data['Borrower Name']}")
                else:
                    return messagebox.showwarning("Warning", "Book is already checked out")
        
        messagebox.showerror("Error", "Book not found")
    
    def return_book(self):
        checked_out = [b for b in self.books if b['status'] == 'checked out']
        if not checked_out:
            return messagebox.showinfo("Info", "No books are currently checked out")
        
        data = self.get_input_dialog("Return Book", ["Book ISBN"])
        if not data.get("Book ISBN"):
            return
        
        for book in self.books:
            if book['isbn'] == data["Book ISBN"] and book['status'] == 'checked out':
                book['status'] = 'available'
                book['due_date'] = ''
                book['borrower'] = ''
                self.save_books()
                self.refresh_display()
                return messagebox.showinfo("Success", f"Successfully returned '{book['title']}'")
        
        messagebox.showerror("Error", "Book not found or already available")
    
    def add_new_book(self):
        data = self.get_input_dialog("Add New Book", ["Title", "Author", "ISBN (13 digits)"])
        
        if not data.get("Title") or not data.get("Author"):
            return messagebox.showwarning("Warning", "Title and author cannot be empty")
        
        isbn = data.get("ISBN (13 digits)", "")
        if len(isbn) != 13 or not isbn.isdigit():
            return messagebox.showwarning("Warning", "ISBN must be 13 digits")
        
        if any(book['isbn'] == isbn for book in self.books):
            return messagebox.showwarning("Warning", "A book with this ISBN already exists")
        
        self.books.append({'title': data["Title"], 'author': data["Author"], 'isbn': isbn, 'status': 'available', 'due_date': '', 'borrower': ''})
        self.save_books()
        self.refresh_display()
        messagebox.showinfo("Success", f"Successfully added '{data['Title']}' to the library")
    
    def view_overdue_books(self):
        today = datetime.now().date()
        overdue_books = []
        
        for book in self.books:
            if book['status'] == 'checked out' and book['due_date']:
                try:
                    if datetime.strptime(book['due_date'], '%Y-%m-%d').date() < today:
                        days_overdue = (today - datetime.strptime(book['due_date'], '%Y-%m-%d').date()).days
                        overdue_books.append({**book, 'fine': f"${days_overdue * 0.50:.2f}", 'days_overdue': days_overdue})
                except ValueError:
                    pass
        
        if not overdue_books:
            return messagebox.showinfo("Info", "No overdue books found")
        
        overdue_window = tk.Toplevel(self.root)
        overdue_window.title("Overdue Books")
        overdue_window.geometry("800x400")
        
        ttk.Label(overdue_window, text="⚠️ Overdue Books", font=('Arial', 14, 'bold')).pack(pady=10)
        
        overdue_tree = ttk.Treeview(overdue_window, columns=('Title', 'Author', 'Borrower', 'Due Date', 'Days Overdue', 'Fine'), show='headings')
        for col in overdue_tree['columns']:
            overdue_tree.heading(col, text=col)
            overdue_tree.column(col, width=120)
        
        total_fines = 0
        for book in overdue_books:
            overdue_tree.insert('', 'end', values=(book['title'], book['author'], book['borrower'], book['due_date'], book['days_overdue'], book['fine']))
            total_fines += book['days_overdue'] * 0.50
        
        overdue_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        ttk.Label(overdue_window, text=f"Total Fines Due: ${total_fines:.2f}", font=('Arial', 12, 'bold')).pack(pady=10)
    
    def delete_book(self):
        if not self.books:
            return messagebox.showinfo("Info", "No books available")
        
        data = self.get_input_dialog("Delete Book", ["Book ISBN"])
        if not data.get("Book ISBN"):
            return
        
        for i, book in enumerate(self.books):
            if book['isbn'] == data["Book ISBN"]:
                if book['status'] == 'checked out':
                    return messagebox.showwarning("Warning", "Cannot delete: Book is currently checked out")
                
                if messagebox.askyesno("Confirm Delete", f"Delete '{book['title']}'?"):
                    del self.books[i]
                    self.save_books()
                    self.refresh_display()
                    messagebox.showinfo("Success", "Book deleted successfully")
                return
        
        messagebox.showerror("Error", "Book not found")

def main():
    root = tk.Tk()
    app = LibraryManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()