class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.borrowed_books = []

    def borrow_book(self, book):
        if book not in self.borrowed_books:
            self.borrowed_books.append(book)
            return True
        return False

    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            return True
        return False

    def get_borrowed_books(self):
        return self.borrowed_books

    def __str__(self):
        return f"User: {self.username}, Borrowed Books: {len(self.borrowed_books)}"

    def __repr__(self):
        return f"User(username='{self.username}', password='{self.password}')"

# Predefined user
ellie = User("ellie", "123456")