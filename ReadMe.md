# Magazine Management System

This is a simple **Magazine Management System** built using Python, SQLite, and an object-oriented approach. The system allows users to create, read, and manage authors, magazines, and articles while maintaining relationships between them.

## Features

- **Authors**: Manage authors, including creating and retrieving authors.
- **Magazines**: Create magazines and associate them with articles and authors.
- **Articles**: Create articles and associate them with both authors and magazines.
- **Database**: Uses SQLite for storing data, with all entities (authors, magazines, and articles) linked through relational database tables.

## Technologies Used

- **Python 3.x**: The main programming language used for backend logic.
- **SQLite**: A lightweight, serverless, self-contained SQL database engine used for data storage.
- **SQLAlchemy** (optional for ORM): If using SQLAlchemy, this would allow ORM-based interaction with the database.
- **Command-Line Interface (CLI)**: Manual testing and interaction with the system through Python scripts and SQL queries.

## Prerequisites

Ensure you have the following tools installed:

- Python 3.x
- SQLite (or other databases supported in your project)
- pip (Python package installer)

You can install the required dependencies using:

```bash
pip install -r requirements.txt
```

## Setup Instructions

### 1. Clone the Repository

First, clone this repository to your local machine

### 2. Running the Application

There are Python scripts available for creating and managing authors, magazines, and articles through the CLI.

#### Create an Author

To create a new author, use the following command:

```bash
python create_author.py --name "John Doe"
```

#### Create a Magazine

To create a new magazine, use the following command:

```bash
python create_magazine.py --name "Tech Weekly" --category "Technology"
```

#### Create an Article

To create an article and associate it with an author and a magazine:

```bash
python create_article.py --title "Tech Innovations 2024" --content "Some content" --author_id 1 --magazine_id 1
```

### 3. Manual Testing

You can manually test the application by running the commands for creating authors, magazines, and articles and checking the database entries using SQL queries.

#### Example:

To check if an author has been created, use:

```bash
sqlite3 database/magazine.db "SELECT * FROM authors WHERE name = 'John Doe';"
```

To check the articles associated with a specific magazine:

```bash
sqlite3 database/magazine.db "SELECT * FROM articles WHERE magazine_id = 1;"
```

### 4. Running Tests

You can use the `pytest` framework to run automated tests for your application.

Make sure all test cases pass successfully, and the database operations are correctly executed.

### 5. Cleaning Up the Database

To delete data from the database, run the following commands:

#### Delete an Author

```bash
python delete_author.py --author_id 1
```

#### Delete a Magazine

```bash
python delete_magazine.py --magazine_id 1
```

#### Delete an Article

```bash
python delete_article.py --article_id 1
```

## End-to-End Testing

For end-to-end (E2E) testing, follow the full flow:

1. **Create an Author**:
   ```bash
   python create_author.py --name "John Doe"
   ```

2. **Create a Magazine**:
   ```bash
   python create_magazine.py --name "Tech Weekly" --category "Technology"
   ```

3. **Create an Article**:
   ```bash
   python create_article.py --title "Tech Innovations 2024" --content "Content of the article" --author_id 1 --magazine_id 1
   ```

4. **Check the Data**:
   Verify the data using SQL queries.

## Contributing

If you'd like to contribute to this project, feel free to open a pull request. Ensure that your changes pass the tests and maintain code quality.

