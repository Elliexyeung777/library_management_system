from typing import List, Optional, Dict, Any, Tuple
from book import Book
from database import Database

class Library:
    def __init__(self):
        self.db = Database()

    def add_book(self, book: Book) -> bool:
        query = "INSERT INTO books (title, author, isbn, quantity) VALUES (%s, %s, %s, %s)"
        params: Tuple[str, str, str, int] = (book.title, book.author, book.isbn, book.quantity)
        return bool(self.db.execute_query(query, params))

    def remove_book(self, isbn: str) -> bool:
        query = "DELETE FROM books WHERE isbn = %s"
        return bool(self.db.execute_query(query, (isbn,)))

    def update_book(self, book: Book) -> bool:
        query = """
        UPDATE books 
        SET title = %s, author = %s, quantity = %s 
        WHERE isbn = %s
        """
        params: Tuple[str, str, int, str] = (book.title, book.author, book.quantity, book.isbn)
        return bool(self.db.execute_query(query, params))

    def get_book(self, isbn: str) -> Optional[Book]:
        query = "SELECT * FROM books WHERE isbn = %s"
        result = self.db.execute_query(query, (isbn,))
        if result and isinstance(result, list) and len(result) > 0:
            book_data = result[0]
            return Book(
                title=str(book_data.get('title', '')),
                author=str(book_data.get('author', '')),
                isbn=str(book_data.get('isbn', '')),
                quantity=int(book_data.get('quantity', 0))
            )
        return None

    def search_book(self, keyword: str) -> List[Book]:
        query = """
        SELECT * FROM books 
        WHERE title LIKE %s OR author LIKE %s OR isbn LIKE %s
        """
        params: Tuple[str, str, str] = (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
        results = self.db.execute_query(query, params)
        return [
            Book(
                title=str(book.get('title', '')),
                author=str(book.get('author', '')),
                isbn=str(book.get('isbn', '')),
                quantity=int(book.get('quantity', 0))
            )
            for book in (results or [])
        ]

    def get_all_books(self) -> List[Book]:
        query = "SELECT * FROM books"
        results = self.db.execute_query(query)
        return [
            Book(
                title=str(book.get('title', '')),
                author=str(book.get('author', '')),
                isbn=str(book.get('isbn', '')),
                quantity=int(book.get('quantity', 0))
            )
            for book in (results or [])
        ]

    def get_borrowed_books(self) -> List[Dict[str, Any]]:
        query = """
        SELECT b.title, b.author, b.isbn, u.name, l.borrow_date
        FROM loans l
        JOIN books b ON l.book_id = b.id
        JOIN users u ON l.user_id = u.id
        WHERE l.return_date IS NULL
        """
        return self.db.execute_query(query) or []

    def get_overdue_books(self) -> List[Dict[str, Any]]:
        query = """
        SELECT b.title, b.isbn, u.name, u.email, l.borrow_date,
               DATEDIFF(CURDATE(), l.borrow_date) - 14 AS days_overdue
        FROM loans l
        JOIN books b ON l.book_id = b.id
        JOIN users u ON l.user_id = u.id
        WHERE l.return_date IS NULL
          AND DATEDIFF(CURDATE(), l.borrow_date) > 14
        """
        return self.db.execute_query(query) or []

    def borrow_book(self, user_id: int, isbn: str) -> bool:
        book = self.get_book(isbn)
        if book and book.quantity > 0:
            query = """
            INSERT INTO loans (user_id, book_id, borrow_date)
            SELECT %s, id, CURDATE()
            FROM books
            WHERE isbn = %s
            """
            if self.db.execute_query(query, (user_id, isbn)):
                update_query = "UPDATE books SET quantity = quantity - 1 WHERE isbn = %s"
                return bool(self.db.execute_query(update_query, (isbn,)))
        return False

    def return_book(self, user_id: int, isbn: str) -> bool:
        query = """
        UPDATE loans
        SET return_date = CURDATE()
        WHERE user_id = %s
          AND book_id = (SELECT id FROM books WHERE isbn = %s)
          AND return_date IS NULL
        """
        if self.db.execute_query(query, (user_id, isbn)):
            update_query = "UPDATE books SET quantity = quantity + 1 WHERE isbn = %s"
            return bool(self.db.execute_query(update_query, (isbn,)))
        return False

