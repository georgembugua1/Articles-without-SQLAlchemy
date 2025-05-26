import sqlite3
from lib.db.connection import get_connection
from lib.models.article import Article

class Author:
    def __init__(self, name, id=None):
        if not name or not isinstance(name, str):
            raise ValueError("Author name must be a non-empty string.")
        self.id = id
        self.name = name

    def save(self):
        conn = get_connection()
        try:
            with conn:
                if self.id:
                    conn.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self.id))
                else:
                    cursor = conn.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
                    self.id = cursor.lastrowid
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        return cls(row['name'], row['id']) if row else None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.execute("SELECT * FROM authors WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        return cls(row['name'], row['id']) if row else None

    def articles(self):
        conn = get_connection()
        cursor = conn.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        articles = [Article.from_row(row) for row in cursor.fetchall()]
        conn.close()
        return articles

    def magazines(self):
        conn = get_connection()
        cursor = conn.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON a.magazine_id = m.id
            WHERE a.author_id = ?
        """, (self.id,))
        from lib.models.magazine import Magazine
        magazines = [Magazine.from_row(row) for row in cursor.fetchall()]
        conn.close()
        return magazines

    def add_article(self, magazine, title):
        from lib.models.article import Article
        article = Article(title=title, author=self, magazine=magazine)
        article.save()
        return article

    def topic_areas(self):
        conn = get_connection()
        cursor = conn.execute("""
            SELECT DISTINCT m.category FROM magazines m
            JOIN articles a ON a.magazine_id = m.id
            WHERE a.author_id = ?
        """, (self.id,))
        categories = [row['category'] for row in cursor.fetchall()]
        conn.close()
        return categories

    @staticmethod
    def from_row(row):
        return Author(row['name'], row['id'])
