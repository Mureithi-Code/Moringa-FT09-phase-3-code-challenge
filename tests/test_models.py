import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine
from database.connection import get_db_connection

class TestModels(unittest.TestCase):

    def setUp(self):
        """Setup test database and insert sample data"""
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS authors (id INTEGER PRIMARY KEY, name TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS magazines (id INTEGER PRIMARY KEY, name TEXT, category TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY, title TEXT, content TEXT, author_id INTEGER, magazine_id INTEGER, FOREIGN KEY(author_id) REFERENCES authors(id), FOREIGN KEY(magazine_id) REFERENCES magazines(id))")
        self.conn.commit()

        # Insert sample data for testing
        self.author = Author(name="John Doe")
        self.magazine = Magazine(name="Tech Weekly", category="Technology")
        self.article = Article(title="Test Title", content="Test Content", author_id=self.author.id, magazine_id=self.magazine.id)

    def tearDown(self):
        """Clean up database after each test"""
        self.cursor.execute("DROP TABLE IF EXISTS authors")
        self.cursor.execute("DROP TABLE IF EXISTS magazines")
        self.cursor.execute("DROP TABLE IF EXISTS articles")
        self.conn.commit()
        self.conn.close()

    def test_author_creation(self):
        author = Author(name="Jane Doe")
        self.assertEqual(author.name, "Jane Doe")
        self.assertIsInstance(author.id, int)

    def test_article_creation(self):
        article = Article(title="New Article", content="New Content", author_id=self.author.id, magazine_id=self.magazine.id)
        self.assertEqual(article.title, "New Article")
        self.assertEqual(article.content, "New Content")
        self.assertEqual(article.author().name, self.author.name)
        self.assertEqual(article.magazine().name, self.magazine.name)

    def test_magazine_creation(self):
        magazine = Magazine(name="Health Weekly", category="Health")
        self.assertEqual(magazine.name, "Health Weekly")
        self.assertEqual(magazine.category, "Health")

    def test_article_author(self):
        article = self.article
        author = article.author()
        self.assertEqual(author.name, self.author.name)
        self.assertEqual(author.id, self.author.id)

    def test_article_magazine(self):
        article = self.article
        magazine = article.magazine()
        self.assertEqual(magazine.name, self.magazine.name)
        self.assertEqual(magazine.category, self.magazine.category)

    def test_author_articles(self):
        author = self.author
        articles = author.articles()
        self.assertGreater(len(articles), 0)
        self.assertEqual(articles[0].author().name, author.name)

    def test_author_magazines(self):
        author = self.author
        magazines = author.magazines()
        self.assertGreater(len(magazines), 0)
        self.assertEqual(magazines[0].name, self.magazine.name)

    def test_magazine_article_titles(self):
        magazine = self.magazine
        titles = magazine.article_titles()
        self.assertGreater(len(titles), 0)
        self.assertIn("Test Title", titles)

    def test_magazine_articles(self):
        magazine = self.magazine
        articles = magazine.articles()
        self.assertGreater(len(articles), 0)
        self.assertEqual(articles[0].magazine().name, magazine.name)

    def test_magazine_contributing_authors(self):
        # Ensure the author has more than 2 articles
        # Create multiple articles for the same author
        for _ in range(3):
            article = Article(title="Test Article", content="Test Content", author_id=self.author.id, magazine_id=self.magazine.id)

        magazine = self.magazine
        authors = magazine.contributing_authors()
        
        # Make sure the list is not empty and the author has contributed more than 2 articles
        self.assertGreater(len(authors), 0)
        self.assertEqual(authors[0].name, self.author.name)
        self.assertGreater(len(authors[0].articles()), 2)


    def test_magazine_contributors(self):
        magazine = self.magazine
        contributors = magazine.contributors()
        self.assertGreater(len(contributors), 0)
        self.assertEqual(contributors[0].name, self.author.name)

if __name__ == "__main__":
    unittest.main()
