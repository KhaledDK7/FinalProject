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
        
        #Fixed the load_books() function
        #mplemented the save_books() function
        #Added display_books() for user-friendly output
        #Ensured proper CSV file creation with all necessary columns


        #Add Main program loop , Create a basic menu system in main()