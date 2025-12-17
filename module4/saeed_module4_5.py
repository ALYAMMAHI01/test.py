import sqlite3
import time

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

def ensure_sample_data(db_file):
    """Ensure there's at least one row in the tasks table for demonstration."""
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Check if there's any data
        cursor.execute("SELECT COUNT(*) FROM tasks;")
        count = cursor.fetchone()[0]

        if count == 0:
            # Insert a sample task
            cursor.execute("""
                INSERT INTO tasks (title, description, status)
                VALUES (?, ?, ?)
            """, ("Sample Task", "This is a sample task for demonstration", "pending"))
            conn.commit()
            print("Inserted sample data for demonstration.")

    except sqlite3.Error as e:
        print(f"Error ensuring sample data: {e}")

    finally:
        if conn:
            conn.close()

def update_and_revert_task(db_file):
    """Update a task, show the change, wait 15 seconds, then revert."""
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Get the first task to update
        cursor.execute("SELECT id, title, description, status FROM tasks LIMIT 1;")
        task = cursor.fetchone()

        if not task:
            print("No tasks found to update.")
            return

        task_id, original_title, original_desc, original_status = task

        # Store original values for reversion
        original_values = (original_title, original_desc, original_status)

        # Update values
        new_title = "Updated Task Title"
        new_desc = "This task has been temporarily updated"
        new_status = "in_progress"

        cursor.execute("""
            UPDATE tasks
            SET title = ?, description = ?, status = ?
            WHERE id = ?
        """, (new_title, new_desc, new_status, task_id))

        conn.commit()

        print(f"\n=== AFTER UPDATE (Task ID: {task_id}) ===")
        view_sql_database_tables(db_file)

        print(f"\nWaiting 15 seconds before reverting changes...")
        time.sleep(15)

        # Revert changes
        cursor.execute("""
            UPDATE tasks
            SET title = ?, description = ?, status = ?
            WHERE id = ?
        """, (original_values[0], original_values[1], original_values[2], task_id))

        conn.commit()

        print(f"\n=== AFTER REVERT (Task ID: {task_id}) ===")
        view_sql_database_tables(db_file)

    except sqlite3.Error as e:
        print(f"Error updating/reverting task: {e}")

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # Database file name
    database_file = 'saeed_module4_1.db'

    print("=== INITIAL DATABASE STATE ===")
    view_sql_database_tables(database_file)

    # Ensure we have data to work with
    ensure_sample_data(database_file)

    print("\n=== STARTING UPDATE DEMONSTRATION ===")
    update_and_revert_task(database_file)
