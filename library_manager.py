import csv
import os
from datetime import datetime

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

    #Display books in a formatted table.
    print("\nCurrent Library Inventory:")
    print(f"{'Title':<30} {'Author':<20} {'ISBN':<15} {'Status':<12} {'Due Date':<12} {'Borrower':<10}")
    print("-" * 100)

    for book in books:
        due_date = book['due_date'] if book['due_date'] else 'N/A'
        borrower = book['borrower'] if book['borrower'] else 'N/A'
        print(f"{book['title'][:28]:<30} {book['author'][:18]:<20} {book['isbn']:<15} "
              f"{book['status']:<12} {due_date:<12} {borrower:<10}") 
def main():
    #Main Program Loop
    books = load_books()
    print("Welcome to the Library Book Manager")
    
    while True:
        print("\nOptions:")
        print("1. View all books")
        print("2. Search books")
        print("3. Check out a book")
        print("4. Return a book")
        print("5. Add new book")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
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
            print("Goodbye!")
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