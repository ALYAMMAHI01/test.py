import sqlite3
from datetime import datetime

# Database file name
DB_NAME = 'saeed_module4_1.db'

def create_tasks_table():
    """Create the tasks table in the SQLite database."""

    # SQL schema for the tasks table
    schema = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'pending',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """

    try:
        # Connect to SQLite database (creates file if it doesn't exist)
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Execute the CREATE TABLE statement
        cursor.execute(schema)

        # Commit the changes
        conn.commit()

        print(f"Successfully created tasks table in {DB_NAME}")
        print("Table schema:")
        print("- id: INTEGER PRIMARY KEY AUTOINCREMENT")
        print("- title: TEXT NOT NULL")
        print("- description: TEXT")
        print("- status: TEXT DEFAULT 'pending'")
        print("- created_at: DATETIME DEFAULT CURRENT_TIMESTAMP")

    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

    finally:
        if conn:
            conn.close()

def insert_sample_data():
    """Insert some sample tasks for testing."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        sample_tasks = [
            ("Complete project proposal", "Write and submit the Q1 project proposal", "pending"),
            ("Review code changes", "Review pull requests from team members", "in_progress"),
            ("Update documentation", "Update API documentation with new endpoints", "completed"),
            ("Fix bug in login", "Resolve authentication issue reported by users", "pending"),
            ("Plan team meeting", "Schedule and prepare agenda for weekly team meeting", "pending")
        ]

        cursor.executemany("""
            INSERT INTO tasks (title, description, status)
            VALUES (?, ?, ?)
        """, sample_tasks)

        conn.commit()
        print(f"Inserted {len(sample_tasks)} sample tasks")

    except sqlite3.Error as e:
        print(f"Error inserting sample data: {e}")

    finally:
        if conn:
            conn.close()


