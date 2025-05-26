import sqlite3
from lib.db.connection import get_connection

class Article:
    def __init__(self, title, author, magazine, id=None):
        if not title or not isinstance(title, str):
            raise ValueError("Article title must be a non-empty string.")
        if not author or not hasattr(author, 'id'):
            raise ValueError("Author must be a valid Author instance.")
        if not magazine or not hasattr(magazine, 'id'):
            raise ValueError("Magazine must be a valid Magazine instance.")
        self.id = id
        self.title = title
        self.author = author
        self.magazine = magazine

    def save(self):
        conn = get_connection()
        try:
            with conn:
                if self.id:
                    conn.execute("UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?", (self.title, self.author.id, self.magazine.id, self.id))
                else:
                    cursor = conn.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", (self.title, self.author.id, self.magazine.id))
                    self.id = cursor.lastrowid
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.execute("SELECT * FROM articles WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            from lib.models.author import Author
            from lib.models.magazine import Magazine
            author = Author.find_by_id(row['author_id'])
            magazine = Magazine.find_by_id(row['magazine_id'])
            return cls(row['title'], author, magazine, row['id'])
        return None

    @staticmethod
    def from_row(row):
        from lib.models.author import Author
        from lib.models.magazine import Magazine
        author = Author.find_by_id(row['author_id'])
        magazine = Magazine.find_by_id(row['magazine_id'])
        return Article(row['title'], author, magazine, row['id'])
