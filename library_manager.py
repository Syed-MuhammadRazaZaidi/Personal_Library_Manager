import json
import os
import shutil

LIBRARY_FILE = "library.txt"
BACKUP_FILE = "backup_library.txt"

def load_library():
    """Load the library from library.txt using JSON format."""
    if os.path.exists(LIBRARY_FILE) and os.path.getsize(LIBRARY_FILE) > 0:
        with open(LIBRARY_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("Warning: Could not decode JSON. Starting with an empty library.")
                return []
    return []

def save_library(library):
    """Save the library list to library.txt as JSON."""
    with open(LIBRARY_FILE, 'w') as f:
        json.dump(library, f, indent=4)

def backup_library():
    """Create a backup of the library file."""
    if os.path.exists(LIBRARY_FILE):
        shutil.copy(LIBRARY_FILE, BACKUP_FILE)
        print(f"Backup created successfully in {BACKUP_FILE}.")
    else:
        print("No library file found to backup.")

def print_book_details(book, prefix=""):
    """Print details of a book."""
    isbn_str = f" (ISBN: {book['isbn']})" if book.get("isbn") else ""
    status = "Read" if book["read"] else "Unread"
    print(f"{prefix}Title: {book['title']}, Author: {book['author']}, Year: {book['year']}, Genre: {book['genre']}{isbn_str}, Status: {status}")

def add_book(library):
    title = input("Enter the book title: ").strip()
    author = input("Enter the author: ").strip()
    while True:
        try:
            pub_year = int(input("Enter the publication year: ").strip())
            break
        except ValueError:
            print("Please enter a valid integer for the publication year.")
    genre = input("Enter the genre: ").strip()
    isbn = input("Enter the ISBN (optional): ").strip()
    read_input = input("Have you read this book? (yes/no): ").strip().lower()
    read_status = True if read_input in ['yes', 'y'] else False

    book = {
        "title": title,
        "author": author,
        "year": pub_year,
        "genre": genre,
        "read": read_status,
        "isbn": isbn if isbn else None
    }
    library.append(book)
    print("\nBook added successfully!")
    print_book_details(book, prefix=">> ")

def remove_book(library):
    title = input("Enter the title of the book to remove: ").strip()
    found = False
    for book in library:
        if book["title"].lower() == title.lower():
            print("\nRemoving the following book:")
            print_book_details(book, prefix=">> ")
            library.remove(book)
            print("Book removed successfully!")
            found = True
            break
    if not found:
        print("Book not found.")

def search_book(library):
    print("Search by:")
    print("1. Title")
    print("2. Author")
    choice = input("Enter your choice (1 or 2): ").strip()
    if choice == '1':
        query = input("Enter the title to search: ").strip().lower()
        matches = [b for b in library if query in b["title"].lower()]
    elif choice == '2':
        query = input("Enter the author to search: ").strip().lower()
        matches = [b for b in library if query in b["author"].lower()]
    else:
        print("Invalid choice.")
        return

    if matches:
        print("\nMatching Books:")
        for idx, b in enumerate(matches, 1):
            print(f"{idx}. ", end="")
            print_book_details(b)
    else:
        print("No matching books found.")

def display_all_books(library):
    if not library:
        print("Your library is empty.")
        return

    sort_option = input("Sort books? (y/n): ").strip().lower()
    if sort_option == 'y':
        print("Sort by: 1. Title  2. Author  3. Publication Year  4. Genre")
        choice = input("Enter choice number: ").strip()
        key_map = {'1': "title", '2': "author", '3': "year", '4': "genre"}
        key = key_map.get(choice)
        if key:
            if key == "year":
                library = sorted(library, key=lambda b: b[key])
            else:
                library = sorted(library, key=lambda b: b[key].lower())
        else:
            print("Invalid sort option. Displaying unsorted list.")
    
    print("\nYour Library:")
    for idx, b in enumerate(library, 1):
        print(f"{idx}. ", end="")
        print_book_details(b)

def update_book(library):
    if not library:
        print("Library is empty. Nothing to update.")
        return
    print("\nCurrent Books:")
    for idx, b in enumerate(library, 1):
        print(f"{idx}. ", end="")
        print_book_details(b)
    try:
        index = int(input("Enter the index number of the book to update: ").strip())
        if index < 1 or index > len(library):
            print("Invalid index.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    book = library[index - 1]
    print("\nCurrent details of the selected book:")
    print_book_details(book)
    print("Leave a field blank to keep the current value.")

    new_title = input(f"Enter new title (current: {book['title']}): ").strip()
    new_author = input(f"Enter new author (current: {book['author']}): ").strip()
    new_year = input(f"Enter new publication year (current: {book['year']}): ").strip()
    new_genre = input(f"Enter new genre (current: {book['genre']}): ").strip()
    new_isbn = input(f"Enter new ISBN (current: {book.get('isbn', 'None')}): ").strip()
    new_read = input(f"Have you read this book? (yes/no, current: {'yes' if book['read'] else 'no'}): ").strip().lower()

    if new_title:
        book['title'] = new_title
    if new_author:
        book['author'] = new_author
    if new_year:
        try:
            book['year'] = int(new_year)
        except ValueError:
            print("Invalid year entered; keeping the current value.")
    if new_genre:
        book['genre'] = new_genre
    if new_isbn:
        book['isbn'] = new_isbn
    if new_read in ['yes', 'y']:
        book['read'] = True
    elif new_read in ['no', 'n']:
        book['read'] = False

    print("\nBook updated successfully!")
    print("New details:")
    print_book_details(book, prefix=">> ")

def display_statistics(library):
    total = len(library)
    if total == 0:
        print("No books in library to display statistics.")
        return
    read_count = sum(1 for b in library if b["read"])
    percent_read = (read_count / total) * 100
    print(f"Total books: {total}")
    print(f"Percentage read: {percent_read:.1f}%")

def menu():
    library = load_library()
    while True:
        print("\nWelcome to your Personal Library Manager!")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Search for a book")
        print("4. Display all books")
        print("5. Update a book")
        print("6. Display statistics")
        print("7. Backup library")
        print("8. Exit")
        choice = input("Enter your choice (1-8): ").strip()

        if choice == '1':
            add_book(library)
        elif choice == '2':
            remove_book(library)
        elif choice == '3':
            search_book(library)
        elif choice == '4':
            display_all_books(library)
        elif choice == '5':
            update_book(library)
        elif choice == '6':
            display_statistics(library)
        elif choice == '7':
            backup_library()
        elif choice == '8':
            save_library(library)
            print("Library saved to file. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
