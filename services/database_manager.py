import sqlite3
from typing import Any, Iterable

class DatabaseManager:
    """Handles SQLite database connections and queries."""

    def __init__(self, db_path: str):
        # Store the path to the database file
        self._db_path = db_path
        self._connection: sqlite3.Connection | None = None

    def connect(self) -> None:
        #Open a connection to the database if not already connected.
        if self._connection is None:
            self._connection = sqlite3.connect(self._db_path)

    def close(self) -> None:
        #Close the database connection.
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def execute_query(self, sql: str, params: Iterable[Any] = ()):
        #Execute a query that changes the database (INSERT, UPDATE, DELETE).
        #Returns the cursor.
        if self._connection is None:
            self.connect()
        cur = self._connection.cursor()
        cur.execute(sql, tuple(params))
        self._connection.commit()
        return cur

    def fetch_one(self, sql: str, params: Iterable[Any] = ()):
        """Fetch a single row from the database."""
        if self._connection is None:
            self.connect()
        cur = self._connection.cursor()
        cur.execute(sql, tuple(params))
        return cur.fetchone()

    def fetch_all(self, sql: str, params: Iterable[Any] = ()):
        """Fetch multiple rows from the database."""
        if self._connection is None:
            self.connect()
        cur = self._connection.cursor()
        cur.execute(sql, tuple(params))
        return cur.fetchall()
    
    def cursor(self):
        #Get a cursor object for custom queries
        if self._connection is None:
            self.connect()
        return self._connection.cursor()
