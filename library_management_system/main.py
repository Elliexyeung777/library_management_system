import sys
import os

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from library import Library
    from book import Book
    from user_interface import UserInterface
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

class LibraryManagementSystem:
    def __init__(self):
        self.library = Library()
        self.user_interface = UserInterface(self.library)

    def display_main_menu(self):
        print("\nLibrary Management System")
        print("1. Enter as Librarian")
        print("2. Enter as User")
        print("3. Register New User")
        print("4. Exit")

    def display_librarian_menu(self):
        print("\nLibrarian Interface")
        print("1. Add a book")
        print("2. Update a book")
        print("3. Remove a book")
        print("4. Search for a book")
        print("5. Display all books")
        print("6. Return to main menu")

    def add_book(self):
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        isbn = input("Enter book ISBN: ")
        quantity = input("Enter book quantity: ")

        try:
            quantity = int(quantity)
        except ValueError:
            print("Error: Quantity must be a number")
            return

        book = Book(title, author, isbn, quantity)
        if self.library.add_book(book):
            print("Book added successfully")
        else:
            print("Failed to add book. It may already exist.")

    def update_book(self):
        isbn = input("Enter the ISBN of the book to update: ")
        book = self.library.get_book(isbn)
        if not book:
            print("Book not found")
            return

        title = input(f"Enter new title (current: {book.title}) or press Enter to keep current: ")
        author = input(f"Enter new author (current: {book.author}) or press Enter to keep current: ")
        quantity = input(f"Enter new quantity (current: {book.quantity}) or press Enter to keep current: ")

        if title:
            book.title = title
        if author:
            book.author = author
        if quantity:
            try:
                book.quantity = int(quantity)
            except ValueError:
                print("Error: Quantity must be a number")
                return

        if self.library.update_book(book):
            print("Book updated successfully")
        else:
            print("Failed to update book")

    def remove_book(self):
        isbn = input("Enter the ISBN of the book to remove: ")
        if self.library.remove_book(isbn):
            print("Book removed successfully")
        else:
            print("Failed to remove book. It may not exist.")

    def search_book(self):
        keyword = input("Enter search keyword: ")
        books = self.library.search_book(keyword)
        if books:
            print("\nSearch Results:")
            for book in books:
                print(book)
        else:
            print("No books found matching the search criteria")

    def display_all_books(self):
        books = self.library.get_all_books()
        if books:
            print("\nAll Books:")
            for book in books:
                print(book)
        else:
            print("No books in the library")

    def librarian_menu(self):
        while True:
            self.display_librarian_menu()
            choice = input("Enter your choice (1-6): ")

            if choice == '1':
                self.add_book()
            elif choice == '2':
                self.update_book()
            elif choice == '3':
                self.remove_book()
            elif choice == '4':
                self.search_book()
            elif choice == '5':
                self.display_all_books()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    def run(self):
        while True:
            self.display_main_menu()
            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                self.librarian_menu()
            elif choice == '2':
                self.user_interface.run()
            elif choice == '3':
                self.user_interface.register_user()
            elif choice == '4':
                print("Thank you for using the Library Management System. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

def main():
    try:
        lms = LibraryManagementSystem()
        lms.run()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
   