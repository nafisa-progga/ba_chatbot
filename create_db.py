import oracledb
import os
from dotenv import load_dotenv

# Load environment variables from the .env file.
# This ensures that your Oracle credentials are read from your .env file.
load_dotenv()

# --- Oracle Database Connection Configuration ---
# The script retrieves all credentials from environment variables.
# These variables should be set in your .env file.
DB_USER = os.environ.get("ORACLE_DB_USER")
DB_PASSWORD = os.environ.get("ORACLE_DB_PASSWORD")
DB_DSN = os.environ.get("ORACLE_DB_DSN")

# Check if the DSN variable is set.
# This is a critical step to ensure the script doesn't try to connect with a missing DSN.
if not DB_DSN:
    raise ValueError("ORACLE_DB_DSN environment variable is not set. Please add it to your .env file.")

def create_and_populate_tables():
    """
    Connects to the Oracle database, drops existing tables (if they exist),
    creates new dummy tables, and inserts sample data for testing.
    """
    connection = None
    try:
        # Create a connection to the Oracle database
        connection = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
        cursor = connection.cursor()

        print("Successfully connected to the Oracle database.")

        # --- Drop Tables (if they already exist) ---
        try:
            cursor.execute("DROP TABLE employees")
            print("Dropped 'employees' table.")
        except oracledb.DatabaseError as e:
            if "table or view does not exist" not in str(e):
                print(f"Error dropping 'employees' table: {e}")

        try:
            cursor.execute("DROP TABLE products")
            print("Dropped 'products' table.")
        except oracledb.DatabaseError as e:
            if "table or view does not exist" not in str(e):
                print(f"Error dropping 'products' table: {e}")

        # --- Create 'employees' table ---
        cursor.execute("""
            CREATE TABLE employees (
                id NUMBER(10) PRIMARY KEY,
                name VARCHAR2(255) NOT NULL,
                department VARCHAR2(255),
                salary NUMBER(10)
            )
        """)
        print("Created 'employees' table successfully.")

        # --- Insert dummy data into 'employees' ---
        employees_data = [
            (1, 'Alice Johnson', 'HR', 60000),
            (2, 'Bob Williams', 'IT', 85000),
            (3, 'Charlie Brown', 'IT', 92000),
            (4, 'Diana Miller', 'Marketing', 75000),
            (5, 'Eva Davis', 'HR', 62000)
        ]
        cursor.executemany("INSERT INTO employees VALUES (:1, :2, :3, :4)", employees_data)
        connection.commit()
        print("Inserted dummy data into 'employees' table.")

        # --- Create 'products' table ---
        cursor.execute("""
            CREATE TABLE products (
                product_id NUMBER(10) PRIMARY KEY,
                product_name VARCHAR2(255) NOT NULL,
                price NUMBER(10, 2),
                stock_quantity NUMBER(10)
            )
        """)
        print("Created 'products' table successfully.")

        # --- Insert dummy data into 'products' ---
        products_data = [
            (101, 'Laptop', 1200.50, 50),
            (102, 'Mouse', 25.00, 200),
            (103, 'Keyboard', 75.99, 150),
            (104, 'Monitor', 300.00, 75)
        ]
        cursor.executemany("INSERT INTO products VALUES (:1, :2, :3, :4)", products_data)
        connection.commit()
        print("Inserted dummy data into 'products' table.")

        print("Database setup complete.")

    except oracledb.Error as e:
        print(f"Error occurred: {e}")
    finally:
        if connection:
            connection.close()
            print("Connection closed.")

if __name__ == "__main__":
    create_and_populate_tables()
