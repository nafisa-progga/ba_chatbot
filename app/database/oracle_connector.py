# app/database/oracle_connector.py

import oracledb
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_db_connection():
    """
    Establishes a connection to the Oracle Database.

    This function uses credentials from environment variables for security.
    It returns a connection object if successful, otherwise it raises an
    exception with a descriptive error message.
    """
    try:
        # Get database credentials from environment variables
        db_user = os.getenv("ORACLE_DB_USER", "system")
        db_password = os.getenv("ORACLE_DB_PASSWORD")
        
        # Connection string for Oracle Database. 
        # The service name must match what is configured in your database.
        # Based on your lsnrctl status output, this should be 'freepdb1'.
        dsn = "localhost:1521/freepdb1"
        
        # Attempt to create a connection to the database
        connection = oracledb.connect(user=db_user, password=db_password, dsn=dsn)
        print("Successfully connected to the Oracle Database!")
        return connection
    except oracledb.Error as e:
        # If an error occurs, print a detailed message and re-raise the exception
        error, = e.args
        print(f"Error connecting to Oracle Database: {error.message}")
        raise

