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
    #Main program loop
    books = load_books()
    print("Welcome to the Library Book Manager")
    
    while True:
        print("\nOptions:")
        print("1. View all books")
        print("2. Search books")
        print("3. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            display_books(books)
        elif choice == "2":
            search_books(books)
        elif choice == "3":
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

#Implemented search_books() to filter by title, author, or ISBN
#Added menu option for searching
#Displays formatted results using existing display_books()
#Handles no-results case gracefully
#next step i will add check-out/return system (update status, due_date, borrower)
