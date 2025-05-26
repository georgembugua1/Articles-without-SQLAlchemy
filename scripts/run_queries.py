import sys
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

MENU = """
Choose an option:
1. List all authors
2. List all magazines
3. List all articles
4. Add author
5. Add magazine
6. Add article
7. Find articles by author
8. Find magazines by author
9. Find authors for magazine
10. Top publisher
0. Exit
"""

def list_authors():
    # Simple list all authors
    import sqlite3
    from lib.db.connection import get_connection
    conn = get_connection()
    cursor = conn.execute("SELECT * FROM authors")
    for row in cursor.fetchall():
        print(f"{row['id']}: {row['name']}")
    conn.close()

def list_magazines():
    from lib.db.connection import get_connection
    conn = get_connection()
    cursor = conn.execute("SELECT * FROM magazines")
    for row in cursor.fetchall():
        print(f"{row['id']}: {row['name']} ({row['category']})")
    conn.close()

def list_articles():
    from lib.db.connection import get_connection
    conn = get_connection()
    cursor = conn.execute("SELECT * FROM articles")
    for row in cursor.fetchall():
        print(f"{row['id']}: {row['title']} (Author ID: {row['author_id']}, Magazine ID: {row['magazine_id']})")
    conn.close()

def add_author():
    name = input("Author name: ")
    author = Author(name)
    author.save()
    print(f"Added author {author.name} (ID: {author.id})")

def add_magazine():
    name = input("Magazine name: ")
    category = input("Category: ")
    magazine = Magazine(name, category)
    magazine.save()
    print(f"Added magazine {magazine.name} (ID: {magazine.id})")

def add_article():
    title = input("Article title: ")
    author_id = int(input("Author ID: "))
    magazine_id = int(input("Magazine ID: "))
    author = Author.find_by_id(author_id)
    magazine = Magazine.find_by_id(magazine_id)
    if not author or not magazine:
        print("Invalid author or magazine ID.")
        return
    article = Article(title, author, magazine)
    article.save()
    print(f"Added article {article.title} (ID: {article.id})")

def find_articles_by_author():
    author_id = int(input("Author ID: "))
    author = Author.find_by_id(author_id)
    if not author:
        print("Author not found.")
        return
    for article in author.articles():
        print(f"{article.id}: {article.title}")

def find_magazines_by_author():
    author_id = int(input("Author ID: "))
    author = Author.find_by_id(author_id)
    if not author:
        print("Author not found.")
        return
    for mag in author.magazines():
        print(f"{mag.id}: {mag.name} ({mag.category})")

def find_authors_for_magazine():
    magazine_id = int(input("Magazine ID: "))
    magazine = Magazine.find_by_id(magazine_id)
    if not magazine:
        print("Magazine not found.")
        return
    for author in magazine.contributors():
        print(f"{author.id}: {author.name}")

def top_publisher():
    mag = Magazine.top_publisher()
    if mag:
        print(f"Top publisher: {mag.name} ({mag.category})")
    else:
        print("No magazines found.")

def main():
    while True:
        print(MENU)
        choice = input("Enter choice: ")
        if choice == "1":
            list_authors()
        elif choice == "2":
            list_magazines()
        elif choice == "3":
            list_articles()
        elif choice == "4":
            add_author()
        elif choice == "5":
            add_magazine()
        elif choice == "6":
            add_article()
        elif choice == "7":
            find_articles_by_author()
        elif choice == "8":
            find_magazines_by_author()
        elif choice == "9":
            find_authors_for_magazine()
        elif choice == "10":
            top_publisher()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
