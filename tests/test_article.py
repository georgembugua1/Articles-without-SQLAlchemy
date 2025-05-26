import pytest
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.db.connection import get_connection

@pytest.fixture(autouse=True)
def setup_db():
    conn = get_connection()
    with open('lib/db/schema.sql') as f:
        conn.executescript(f.read())
    conn.close()

def test_article_save_and_find():
    author = Author("Helen"); author.save()
    mag = Magazine("Daily", "News"); mag.save()
    art = Article("Big News", author, mag)
    art.save()
    found = Article.find_by_id(art.id)
    assert found.title == "Big News"
    assert found.author.id == author.id
    assert found.magazine.id == mag.id

def test_article_validation():
    author = Author("Ivan"); author.save()
    mag = Magazine("Tech", "Tech"); mag.save()
    with pytest.raises(ValueError):
        Article("", author, mag)
    with pytest.raises(ValueError):
        Article("Valid", None, mag)
    with pytest.raises(ValueError):
        Article("Valid", author, None)
