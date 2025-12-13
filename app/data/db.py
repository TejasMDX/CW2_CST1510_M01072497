import sqlite3
from pathlib import Path

# Path to the SQLite database file
# The database is stored inside the DATA folder
DB_PATH = Path("DATA") / "intelligence_platform.db"

def connect_database(db_path=DB_PATH):
    """Connect to SQLite database."""
    # Convert the Path object to a string and connect to the database
    return sqlite3.connect(str(db_path))

