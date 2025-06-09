import csv
import os
from datetime import datetime, timedelta
from collections import defaultdict

DATA_FILE = "library_books.csv"

def load_books():
    #Load books from CSV file into a list of dictionaries.
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
    #Save list of books to CSV file.
    with open(DATA_FILE, 'w', newline='') as file:
        fieldnames = ["title", "author", "isbn", "status", "due_date", "borrower"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books)
def display_books(books):
    #Display books with overdue highlighting.
    print("\nCurrent Library Inventory:")
    print(f"{'Title':<30} {'Author':<20} {'ISBN':<15} {'Status':<12} {'Due Date':<12} {'Borrower':<10}")
    print("-" * 100)
    
    today = datetime.now().date()
    
    for book in books:
        due_date_str = book['due_date']
        status = book['status']
        borrower = book['borrower'] or 'N/A'
        
        # Check if book is overdue
        is_overdue = False
        if status == 'checked out' and due_date_str:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            is_overdue = due_date < today
        
        # Format display with color/emphasis for overdue books
        title = book['title'][:28]
        if is_overdue:
            title = f"⚠️ {title}"  # Or use color if supported
            status = "OVERDUE"
        
        print(f"{title:<30} {book['author'][:18]:<20} {book['isbn']:<15} "
              f"{status:<12} {due_date_str or 'N/A':<12} {borrower:<10}")
def main():
    books = load_books()
    print("\n" + "="*50)
    print("LIBRARY BOOK MANAGER".center(50))
    print("="*50)
    
    while True:
        print("\nMAIN MENU:")
        print("1. 📖 View All Books")
        print("2. 🔍 Search Books")
        print("3. 📝 Check Out Book")
        print("4. ↩️ Return Book")
        print("5. ➕ Add New Book")
        print("6. ⚠️ View Overdue Books")
        print("7. ✏️ Edit Book")
        print("8. ❌ Delete Book")
        print("9. 📊 Generate Reports")
        print("0. 🚪 Exit")
        
        choice = input("\nEnter your choice (0-9): ").strip()
        
        if choice == "1":
            display_books(books)
        elif choice == "2":
            search_books(books)
        elif choice == "3":
            check_out_book(books)
        elif choice == "4":
            return_book(books)
        elif choice == "5":
            add_new_book(books)
        elif choice == "6":
            check_overdue_books(books)
        elif choice == "7":
            edit_book(books)
        elif choice == "8":
            delete_book(books)
        elif choice == "9":
            generate_report(books)
        elif choice == "0":
            print("\nThank you for using the Library Book Manager!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

def search_books(books):
    #Search books by title, author, or ISBN.
    print("\nSearch Options:")
    print("1. By Title")
    print("2. By Author")
    print("3. By ISBN")
    
    choice = input("Choose search type (1-3): ").strip()
    term = input("Enter search term: ").lower()
    
    results = []
    for book in books:
        if choice == "1" and term in book['title'].lower():
            results.append(book)
        elif choice == "2" and term in book['author'].lower():
            results.append(book)
        elif choice == "3" and term in book['isbn'].lower():
            results.append(book)
    
    if results:
        print(f"\nFound {len(results)} matching book(s):")
        display_books(results)
    else:
        print("No matching books found.")

from datetime import datetime, timedelta

def check_out_book(books):
    #Check out a book by ISBN and update its status.
    display_books(books)
    isbn = input("\nEnter ISBN of the book to check out: ").strip()
    borrower = input("Enter borrower name: ").strip()
    
    for book in books:
        if book['isbn'] == isbn:
            if book['status'] == 'available':
                book['status'] = 'checked out'
                book['due_date'] = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
                book['borrower'] = borrower
                save_books(books)
                print(f"Successfully checked out '{book['title']}' to {borrower}.")
            else:
                print("Book is already checked out.")
            return
    
    print("Book not found.")

def return_book(books):
    #Return a book by ISBN and update its status.
    display_books([b for b in books if b['status'] == 'checked out'])
    if not any(b['status'] == 'checked out' for b in books):
        print("No books are currently checked out.")
        return
    
    isbn = input("\nEnter ISBN of the book to return: ").strip()
    
    for book in books:
        if book['isbn'] == isbn and book['status'] == 'checked out':
            book['status'] = 'available'
            book['due_date'] = ''
            book['borrower'] = ''
            save_books(books)
            print(f"Successfully returned '{book['title']}'.")
            return
    
    print("Book not found or already available.")

def add_new_book(books):
    #Add a new book to the library inventory.
    print("\nAdd New Book")
    title = input("Enter book title: ").strip()
    author = input("Enter author name: ").strip()
    isbn = input("Enter ISBN (13 digits): ").strip()
    
    # Basic validation
    if not title or not author:
        print("Error: Title and author cannot be empty.")
        return
    
    if len(isbn) != 13 or not isbn.isdigit():
        print("Error: ISBN must be 13 digits.")
        return
    
    # Check for duplicate ISBN
    if any(book['isbn'] == isbn for book in books):
        print("Error: A book with this ISBN already exists.")
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
    print(f"Successfully added '{title}' to the library.")

def check_overdue_books(books):
    #Display overdue books with fine calculations.
    today = datetime.now().date()
    overdue_books = []
    total_fines = 0.0
    
    for book in books:
        if book['status'] == 'checked out' and book['due_date']:
            due_date = datetime.strptime(book['due_date'], '%Y-%m-%d').date()
            if due_date < today:
                days_overdue = (today - due_date).days
                fine = days_overdue * 0.50  # $0.50 per day
                total_fines += fine
                book['fine'] = f"${fine:.2f}"
                overdue_books.append(book)
    
    if overdue_books:
        print("\nOverdue Books (Fines Calculated at $0.50/day):")
        display_books(overdue_books)
        print(f"\nTotal Fines Due: ${total_fines:.2f}")
    else:
        print("No overdue books found.")

def edit_book(books):
    #Edit an existing book's details.
    display_books(books)
    isbn = input("\nEnter ISBN of the book to edit: ").strip()
    
    for book in books:
        if book['isbn'] == isbn:
            print(f"\nEditing: {book['title']}")
            print("Leave field blank to keep current value")
            
            new_title = input(f"Title [{book['title']}]: ").strip()
            new_author = input(f"Author [{book['author']}]: ").strip()
            new_isbn = input(f"ISBN [{book['isbn']}]: ").strip()
            
            if new_title:
                book['title'] = new_title
            if new_author:
                book['author'] = new_author
            if new_isbn:
                if len(new_isbn) != 13 or not new_isbn.isdigit():
                    print("Error: ISBN must be 13 digits. Not updated.")
                elif any(b['isbn'] == new_isbn for b in books if b != book):
                    print("Error: ISBN already exists. Not updated.")
                else:
                    book['isbn'] = new_isbn
            
            save_books(books)
            print("Book updated successfully.")
            return
    
    print("Book not found.")

def delete_book(books):
    #Remove a book from the library.
    display_books(books)
    isbn = input("\nEnter ISBN of the book to delete: ").strip()
    
    for i, book in enumerate(books):
        if book['isbn'] == isbn:
            if book['status'] == 'checked out':
                print("Cannot delete: Book is currently checked out.")
                return
            
            confirm = input(f"Delete '{book['title']}'? (y/n): ").lower()
            if confirm == 'y':
                del books[i]
                save_books(books)
                print("Book deleted successfully.")
            return
    
    print("Book not found.")

def generate_report(books):
    #Generate inventory and overdue reports.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    # Inventory Report
    with open(f"library_inventory_{timestamp}.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=books[0].keys())
        writer.writeheader()
        writer.writerows(books)
    
    # Overdue Report
    overdue_books = [
        book for book in books 
        if book['status'] == 'checked out' 
        and book['due_date']
        and datetime.strptime(book['due_date'], '%Y-%m-%d').date() < datetime.now().date()
    ]
    
    if overdue_books:
        with open(f"overdue_books_{timestamp}.csv", 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=overdue_books[0].keys())
            writer.writeheader()
            writer.writerows(overdue_books)
    
    print(f"Generated: inventory and {'overdue' if overdue_books else 'no overdue'} reports")