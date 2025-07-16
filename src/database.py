import sqlite3

def setup_database(db_name="employee.db"):
    """
    Sets up the SQLite database, creates tables, and populates them with initial data.
    """
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Define table creation queries
    tables = {
        "employees": """
            CREATE TABLE IF NOT EXISTS employees (
                emp_id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL, hire_date TEXT NOT NULL, salary REAL NOT NULL
            );
        """,
        "customers": """
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT NOT NULL, last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL, phone TEXT
            );
        """,
        "orders": """
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id INTEGER NOT NULL,
                order_date TEXT NOT NULL, amount REAL NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
            );
        """
    }

    # Execute table creation
    for table_name, query in tables.items():
        cursor.execute(query)

    # Insert data only if the employees table is empty to prevent duplicates
    cursor.execute("SELECT COUNT(*) FROM employees")
    if cursor.fetchone()[0] == 0:
        print("Database appears empty. Populating with initial data...")
        employee_data = [
            (1, "Sunny", "Savita", "sunny.sv@abc.com", "2023-06-01", 50000.00),
            (2, "Arhun", "Meheta", "arhun.m@gmail.com", "2022-04-15", 60000.00),
            (3, "Alice", "Johnson", "alice.johnson@jpg.com", "2021-09-30", 55000.00),
            (4, "Bob", "Brown", "bob.brown@uio.com", "2020-01-20", 45000.00),
        ]
        customers_data = [
            (1, "John", "Doe", "john.doe@example.com", "1234567890"),
            (2, "Jane", "Smith", "jane.smith@example.com", "9876543210"),
        ]
        orders_data = [
            (1, 1, "2023-12-01", 250.75),
            (2, 2, "2023-11-20", 150.50),
        ]
        cursor.executemany("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?)", employee_data)
        cursor.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?)", customers_data)
        cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", orders_data)
        connection.commit()
        print("Data insertion complete.")
    else:
        print("Database already populated. Skipping data insertion.")

    connection.close()