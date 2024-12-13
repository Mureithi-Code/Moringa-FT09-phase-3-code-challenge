from database.connection import get_db_connection



class Author:
    def __init__(self, id=None, name=None):
        if id is None and name is not None:
            self._name = name
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO authors (name) VALUES (?)', (name,))
            conn.commit()
            self._id = cursor.lastrowid
            conn.close()
        elif id is not None:
            self._id = id
            self._name = self._fetch_name(id)  # Fetch name from DB if id is provided

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise AttributeError("Name cannot be modified once set.")

    def _fetch_name(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM authors WHERE id = ?', (id,))
        name = cursor.fetchone()[0]
        conn.close()
        return name

    def articles(self):
        from models.article import Article # Delayed import
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM articles WHERE author_id = ?''', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return [Article(article['id'], article['title'], article['content'], article['author_id'], article['magazine_id']) for article in articles]

    def magazines(self):
        from models.magazine import Magazine # Delayed import
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM magazines WHERE id IN (SELECT magazine_id FROM articles WHERE author_id = ?)''', (self.id,))
        magazines = cursor.fetchall()
        conn.close()
        return [Magazine(magazine['id'], magazine['name'], magazine['category']) for magazine in magazines]

    def __repr__(self):
        return f'<Author {self.name}>'
