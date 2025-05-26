import sqlite3
from lib.db.connection import get_connection

class Magazine:
    def __init__(self, name, category, id=None):
        if not name or not isinstance(name, str):
            raise ValueError("Magazine name must be a non-empty string.")
        if not category or not isinstance(category, str):
            raise ValueError("Magazine category must be a non-empty string.")
        self.id = id
        self.name = name
        self.category = category

    def save(self):
        conn = get_connection()
        try:
            with conn:
                if self.id:
                    conn.execute("UPDATE magazines SET name = ?, category = ? WHERE id = ?", (self.name, self.category, self.id))
                else:
                    cursor = conn.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self.name, self.category))
                    self.id = cursor.lastrowid
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        return cls(row['name'], row['category'], row['id']) if row else None

    def articles(self):
        from lib.models.article import Article
        conn = get_connection()
        cursor = conn.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        articles = [Article.from_row(row) for row in cursor.fetchall()]
        conn.close()
        return articles

    def contributors(self):
        from lib.models.author import Author
        conn = get_connection()
        cursor = conn.execute("""
            SELECT DISTINCT au.* FROM authors au
            JOIN articles ar ON ar.author_id = au.id
            WHERE ar.magazine_id = ?
        """, (self.id,))
        authors = [Author.from_row(row) for row in cursor.fetchall()]
        conn.close()
        return authors

    def article_titles(self):
        conn = get_connection()
        cursor = conn.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
        titles = [row['title'] for row in cursor.fetchall()]
        conn.close()
        return titles

    def contributing_authors(self):
        from lib.models.author import Author
        conn = get_connection()
        cursor = conn.execute("""
            SELECT au.*, COUNT(ar.id) as article_count FROM authors au
            JOIN articles ar ON ar.author_id = au.id
            WHERE ar.magazine_id = ?
            GROUP BY au.id
            HAVING article_count > 2
        """, (self.id,))
        authors = [Author.from_row(row) for row in cursor.fetchall()]
        conn.close()
        return authors

    @classmethod
    def top_publisher(cls):
        conn = get_connection()
        cursor = conn.execute("""
            SELECT m.*, COUNT(a.id) as article_count FROM magazines m
            JOIN articles a ON a.magazine_id = m.id
            GROUP BY m.id
            ORDER BY article_count DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        conn.close()
        return cls(row['name'], row['category'], row['id']) if row else None

    @staticmethod
    def from_row(row):
        return Magazine(row['name'], row['category'], row['id'])
