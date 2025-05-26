import pytest
from lib.models.magazine import Magazine
from lib.models.author import Author
from lib.models.article import Article
from lib.db.connection import get_connection

@pytest.fixture(autouse=True)
def setup_db():
    conn = get_connection()
    with open('lib/db/schema.sql') as f:
        conn.executescript(f.read())
    conn.close()

def test_magazine_save_and_find():
    mag = Magazine("Nature", "Science")
    mag.save()
    found = Magazine.find_by_id(mag.id)
    assert found.name == "Nature"
    assert found.category == "Science"

def test_magazine_articles_and_contributors():
    mag = Magazine("Tech Life", "Tech"); mag.save()
    author = Author("Dana"); author.save()
    art = author.add_article(mag, "5G Networks")
    assert mag.articles()[0].title == "5G Networks"
    assert mag.contributors()[0].name == "Dana"

def test_article_titles_and_contributing_authors():
    mag = Magazine("World News", "News"); mag.save()
    a1 = Author("Eve"); a1.save()
    a2 = Author("Frank"); a2.save()
    for i in range(3):
        a1.add_article(mag, f"Article {i}")
    a2.add_article(mag, "Another Article")
    titles = mag.article_titles()
    assert "Article 0" in titles
    assert len(mag.contributing_authors()) == 1  # Only Eve has >2 articles

def test_top_publisher():
    mag1 = Magazine("A", "Cat1"); mag1.save()
    mag2 = Magazine("B", "Cat2"); mag2.save()
    author = Author("Greg"); author.save()
    for _ in range(5):
        author.add_article(mag2, "X")
    for _ in range(2):
        author.add_article(mag1, "Y")
    top = Magazine.top_publisher()
    assert top.name == "B"
