import sqlite3
import random
import string

def view_sql_database_tables(db_file):
    """
    Function to view all tables and their contents in a SQLite database.
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Get all table names from sqlite_master
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if not tables:
            print(f"No tables found in database: {db_file}")
            return

        print(f"Database: {db_file}")
        print("=" * 60)

        # Loop through each table
        for table in tables:
            table_name = table[0]
            print(f"\nTable: {table_name}")
            print("-" * 40)

            # Get table schema (column information)
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()

            print("Columns:")
            for col in columns:
                col_id, col_name, col_type, not_null, default_val, pk = col
                pk_str = " (PRIMARY KEY)" if pk else ""
                print(f"  {col_name}: {col_type}{pk_str}")

            # Get all data from the table
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()

            print(f"\nData ({len(rows)} rows):")
            if rows:
                # Print column headers
                col_names = [col[1] for col in columns]
                header = " | ".join(col_names)
                print(header)
                print("-" * len(header))

                # Print each row
                for row in rows:
                    row_str = " | ".join(str(cell) if cell is not None else "NULL" for cell in row)
                    print(row_str)
            else:
                print("  (No data in this table)")

            print()

    except sqlite3.Error as e:
        print(f"Error accessing database: {e}")

    finally:
        if conn:
            conn.close()

def add_missing_field_column(db_file, table_name):
    """Add the missing_field column to the specified table."""
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Add the new column
        alter_query = f"ALTER TABLE {table_name} ADD COLUMN missing_field TEXT;"
        cursor.execute(alter_query)
        conn.commit()

        print(f"Successfully added 'missing_field' column to table '{table_name}'")

    except sqlite3.Error as e:
        print(f"Error adding column: {e}")

    finally:
        if conn:
            conn.close()

def populate_missing_field_with_random_chars(db_file, table_name):
    """Populate the missing_field column with random single characters."""
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Get all row IDs
        cursor.execute(f"SELECT id FROM {table_name};")
        rows = cursor.fetchall()

        if not rows:
            print(f"No rows found in table '{table_name}' to populate.")
            return

        # Update each row with a random character
        for row in rows:
            row_id = row[0]
            # Generate a random single character (letters, digits, punctuation)
            random_char = random.choice(string.ascii_letters + string.digits + string.punctuation)

            cursor.execute(f"""
                UPDATE {table_name}
                SET missing_field = ?
                WHERE id = ?
            """, (random_char, row_id))

        conn.commit()
        print(f"Successfully populated 'missing_field' with random characters for {len(rows)} rows")

    except sqlite3.Error as e:
        print(f"Error populating column: {e}")

    finally:
        if conn:
            conn.close()

def ensure_sample_data(db_file, table_name):
    """Ensure there's at least one row in the table for demonstration."""
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Check if there's any data
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cursor.fetchone()[0]

        if count == 0:
            # Insert a few sample tasks
            sample_tasks = [
                ("Task 1", "First sample task", "pending"),
                ("Task 2", "Second sample task", "in_progress"),
                ("Task 3", "Third sample task", "completed")
            ]

            cursor.executemany(f"""
                INSERT INTO {table_name} (title, description, status)
                VALUES (?, ?, ?)
            """, sample_tasks)
            conn.commit()
            print(f"Inserted {len(sample_tasks)} sample tasks for demonstration.")

    except sqlite3.Error as e:
        print(f"Error ensuring sample data: {e}")

    finally:
        if conn:
            conn.close()


