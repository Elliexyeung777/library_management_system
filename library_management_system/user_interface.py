from user import User

class UserInterface:
    def __init__(self, library):
        self.library = library
        self.users = {"ellie": User("ellie", "123456")}  # Include the predefined user
        self.current_user = None

    def display_menu(self):
        print("\nUser Interface")
        print("1. Search for a book")
        print("2. Display all books")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. View borrowed books")
        print("6. Return to main menu")

    def register_user(self):
        username = input("Enter username: ")
        if username in self.users:
            print("Username already exists. Please choose a different username.")
            return
        password = input("Enter password: ")
        user = User(username, password)
        self.users[username] = user
        print("User registered successfully.")

    def login_user(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        user = self.users.get(username)
        if user and user.password == password:
            self.current_user = user
            print(f"Welcome, {username}!")
            return True
        else:
            print("Invalid username or password.")
            return False

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

    def borrow_book(self):
        if not self.current_user:
            print("Please login first.")
            return
        self.display_all_books()
        book_name = input("Enter the name of the book you want to borrow: ")
        books = self.library.search_book(book_name)
        if books:
            if len(books) > 1:
                print("Multiple books found with that name. Please be more specific:")
                for i, book in enumerate(books, 1):
                    print(f"{i}. {book.title} by {book.author}")
                choice = int(input("Enter the number of the book you want to borrow: ")) - 1
                book = books[choice]
            else:
                book = books[0]
            
            if book.quantity > 0:
                if self.current_user.borrow_book(book):
                    book.quantity -= 1
                    print(f"You have successfully borrowed '{book.title}'.")
                else:
                    print("You have already borrowed this book.")
            else:
                print("This book is currently not available for borrowing.")
        else:
            print("No book found with that name.")

    def return_book(self):
        if not self.current_user:
            print("Please login first.")
            return
        borrowed_books = self.current_user.get_borrowed_books()
        if borrowed_books:
            print("\nYour borrowed books:")
            for i, book in enumerate(borrowed_books, 1):
                print(f"{i}. {book.title}")
            choice = int(input("Enter the number of the book you want to return: ")) - 1
            book = borrowed_books[choice]
            if self.current_user.return_book(book):
                book.quantity += 1
                print(f"You have successfully returned '{book.title}'.")
            else:
                print("Error returning the book.")
        else:
            print("You haven't borrowed any books.")

    def view_borrowed_books(self):
        if not self.current_user:
            print("Please login first.")
            return
        borrowed_books = self.current_user.get_borrowed_books()
        if borrowed_books:
            print("\nYour borrowed books:")
            for book in borrowed_books:
                print(book)
        else:
            print("You haven't borrowed any books.")

    def run(self):
        if not self.login_user():
            return
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-6): ")

            if choice == '1':
                self.search_book()
            elif choice == '2':
                self.display_all_books()
            elif choice == '3':
                self.borrow_book()
            elif choice == '4':
                self.return_book()
            elif choice == '5':
                self.view_borrowed_books()
            elif choice == '6':
                self.current_user = None
                break
            else:
                print("Invalid choice. Please try again.")