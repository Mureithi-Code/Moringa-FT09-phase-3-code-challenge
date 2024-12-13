from database.connection import get_db_connection



class Article:
    def __init__(self, id=None, title=None, content=None, author_id=None, magazine_id=None):
        if id is None and title is not None and content is not None and author_id is not None and magazine_id is not None:
            # Insert article into the database
            self._title = title
            self._content = content
            self._author_id = author_id
            self._magazine_id = magazine_id
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                           (title, content, author_id, magazine_id))
            conn.commit()
            self._id = cursor.lastrowid
            conn.close()
        elif id is not None:
            # Fetch the article's information from the database if id is provided
            self._id = id
            self._title, self._content, self._author_id, self._magazine_id = self._fetch_details(id)

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def content(self):
        return self._content

    def _fetch_details(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT title, content, author_id, magazine_id FROM articles WHERE id = ?', (id,))
        title, content, author_id, magazine_id = cursor.fetchone()
        conn.close()
        return title, content, author_id, magazine_id

    def author(self):
        from models.author import Author # Delayed import
        return Author(self._author_id)

    def magazine(self):
        from models.magazine import Magazine # Delayed import
        return Magazine(self._magazine_id)

    def __repr__(self):
        return f'<Article {self.title}>'
