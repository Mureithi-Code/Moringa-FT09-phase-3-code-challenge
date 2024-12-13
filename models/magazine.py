from database.connection import get_db_connection
from models.article import Article
from models.author import Author

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        if id is None and name is not None and category is not None:
            self._name = name
            self._category = category
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (name, category))
            conn.commit()
            self._id = cursor.lastrowid
            conn.close()
        elif id is not None:
            self._id = id
            self._name, self._category = self._fetch_details(id)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if 2 <= len(value) <= 16:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE magazines SET name = ? WHERE id = ?', (value, self.id))
            conn.commit()
            conn.close()
            self._name = value
        else:
            raise ValueError("Name must be between 2 and 16 characters.")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if len(value) > 0:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE magazines SET category = ? WHERE id = ?', (value, self.id))
            conn.commit()
            conn.close()
            self._category = value
        else:
            raise ValueError("Category must be longer than 0 characters.")

    def _fetch_details(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT name, category FROM magazines WHERE id = ?', (id,))
        name, category = cursor.fetchone()
        conn.close()
        return name, category

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM articles WHERE magazine_id = ?''', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return [Article(article['id'], article['title'], article['content'], article['author_id'], article['magazine_id']) for article in articles]

    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM authors WHERE id IN (SELECT author_id FROM articles WHERE magazine_id = ?)''', (self.id,))
        authors = cursor.fetchall()
        conn.close()
        return [Author(author['id'], author['name']) for author in authors]

    def article_titles(self):
        articles = self.articles()
        if articles:
            return [article.title for article in articles]
        return None

    def contributing_authors(self):
        authors = self.contributors()
        return [author for author in authors if len(author.articles()) > 2]

    def __repr__(self):
        return f'<Magazine {self.name}>'
