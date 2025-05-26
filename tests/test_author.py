import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

@pytest.fixture(autouse=True)
def setup_db():
    # Recreate schema for each test
    conn = get_connection()
    with open('lib/db/schema.sql') as f:
        conn.executescript(f.read())
    conn.close()

def test_author_save_and_find():
    author = Author("Alice")
    author.save()
    found = Author.find_by_id(author.id)
    assert found.name == "Alice"
    assert found.id == author.id

def test_author_articles_and_magazines():
    author = Author("Bob"); author.save()
    mag = Magazine("Tech Today", "Tech"); mag.save()
    art = author.add_article(mag, "AI Revolution")
    assert art.title == "AI Revolution"
    assert art.author.id == author.id
    assert art.magazine.id == mag.id
    assert author.articles()[0].title == "AI Revolution"
    assert author.magazines()[0].name == "Tech Today"

def test_topic_areas():
    author = Author("Carol"); author.save()
    mag1 = Magazine("Science Now", "Science"); mag1.save()
    mag2 = Magazine("Tech World", "Tech"); mag2.save()
    author.add_article(mag1, "Quantum Computing")
    author.add_article(mag2, "Cloud Trends")
    assert set(author.topic_areas()) == {"Science", "Tech"}
