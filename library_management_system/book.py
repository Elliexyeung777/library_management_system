# book.py
class Book:
    def __init__(self, title: str, author: str, isbn: str, quantity: int):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.quantity = quantity

    def __str__(self) -> str:
        return f"{self.title} by {self.author} (ISBN: {self.isbn}, Quantity: {self.quantity})"

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "quantity": self.quantity
        }