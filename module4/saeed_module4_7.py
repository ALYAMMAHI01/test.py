import sqlite3

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

def order_by_sql_query(db_file, table_name, order_direction='ASC'):
    """
    Approach 1: Order table content using SQL ORDER BY clause.
    This is the most efficient approach as sorting is done at the database level.
    """
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Get column information for display
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        col_names = [col[1] for col in columns]

        # SQL query with ORDER BY
        query = f"SELECT * FROM {table_name} ORDER BY missing_field {order_direction};"
        cursor.execute(query)
        rows = cursor.fetchall()

        print(f"=== APPROACH 1: SQL ORDER BY ({order_direction}) ===")
        print(f"Query: {query}")
        print(f"Ordered {len(rows)} rows by missing_field column")
        print()

        # Display results
        if rows:
            header = " | ".join(col_names)
            print(header)
            print("-" * len(header))

            for row in rows:
                row_str = " | ".join(str(cell) if cell is not None else "NULL" for cell in row)
                print(row_str)
        else:
            print("No data found")

        print()

    except sqlite3.Error as e:
        print(f"Error in SQL ordering: {e}")

    finally:
        if conn:
            conn.close()

def order_by_python_sorting(db_file, table_name, reverse=False):
    """
    Approach 2: Fetch all data and sort using Python's sorting capabilities.
    This approach loads all data into memory before sorting.
    """
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Get column information
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        col_names = [col[1] for col in columns]

        # Find the index of missing_field column
        missing_field_index = None
        for i, col in enumerate(columns):
            if col[1] == 'missing_field':
                missing_field_index = i
                break

        if missing_field_index is None:
            print("Error: missing_field column not found")
            return

        # Fetch all data
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()

        # Sort rows by missing_field (index position)
        sorted_rows = sorted(rows, key=lambda row: row[missing_field_index] or '', reverse=reverse)

        order_type = "DESCENDING" if reverse else "ASCENDING"
        print(f"=== APPROACH 2: PYTHON SORTING ({order_type}) ===")
        print(f"Fetched {len(rows)} rows and sorted in Python by missing_field column")
        print()

        # Display results
        if sorted_rows:
            header = " | ".join(col_names)
            print(header)
            print("-" * len(header))

            for row in sorted_rows:
                row_str = " | ".join(str(cell) if cell is not None else "NULL" for cell in row)
                print(row_str)
        else:
            print("No data found")

        print()

    except sqlite3.Error as e:
        print(f"Error in Python sorting: {e}")

    finally:
        if conn:
            conn.close()


