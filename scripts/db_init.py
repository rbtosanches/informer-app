#!/usr/bin/env python3
"""
Database Initialization Script
Creates database, schema, and tables if they don't exist.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql

# Load environment variables
load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'informer')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')


def connect_to_postgres():
    """Connect to PostgreSQL default database to create informer DB."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database='postgres'
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        sys.exit(1)


def connect_to_informer():
    """Connect to the informer database."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to informer database: {e}")
        return None


def create_database():
    """Create the informer database if it doesn't exist."""
    conn = connect_to_postgres()
    conn.autocommit = True
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"CREATE DATABASE {DB_NAME}")
        print(f"✓ Database '{DB_NAME}' created successfully.")
    except psycopg2.Error as e:
        if 'already exists' in str(e):
            print(f"✓ Database '{DB_NAME}' already exists.")
        else:
            print(f"Error creating database: {e}")
            sys.exit(1)
    finally:
        cursor.close()
        conn.close()


def execute_sql_file(conn, filepath):
    """Execute SQL commands from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        cursor = conn.cursor()
        cursor.execute(sql_script)
        conn.commit()
        cursor.close()
        print(f"✓ Executed: {filepath}")
        return True
    except Exception as e:
        print(f"Error executing {filepath}: {e}")
        conn.rollback()
        return False


def main():
    """Main initialization function."""
    print("\n" + "="*60)
    print("INFORMER - DATABASE INITIALIZATION")
    print("="*60 + "\n")
    
    print(f"Database Configuration:")
    print(f"  Host: {DB_HOST}")
    print(f"  Port: {DB_PORT}")
    print(f"  User: {DB_USER}")
    print(f"  Database: {DB_NAME}\n")
    
    # Step 1: Create database
    print("Step 1: Creating database...")
    create_database()
    
    # Step 2: Connect to informer database
    print("\nStep 2: Connecting to informer database...")
    conn = connect_to_informer()
    if not conn:
        print("Failed to connect to informer database.")
        sys.exit(1)
    print("✓ Connected to informer database.")
    
    # Step 3: Create tables
    print("\nStep 3: Creating tables and schema...")
    scripts_dir = Path(__file__).parent
    create_tables_file = scripts_dir / 'create_tables.sql'
    
    if create_tables_file.exists():
        execute_sql_file(conn, create_tables_file)
    else:
        print(f"Warning: {create_tables_file} not found.")
    
    # Step 4: Insert default data
    print("\nStep 4: Inserting default data...")
    insert_data_file = scripts_dir / 'insert_default_data.sql'
    
    if insert_data_file.exists():
        execute_sql_file(conn, insert_data_file)
    else:
        print(f"Warning: {insert_data_file} not found.")
    
    # Close connection
    conn.close()
    
    print("\n" + "="*60)
    print("✓ DATABASE INITIALIZATION COMPLETED SUCCESSFULLY!")
    print("="*60 + "\n")
    print("Next steps:")
    print("  1. Run the application: python run.py")
    print("  2. Access the application: http://localhost:8000")
    print("  3. Login with:")
    print("     - Username: admin")
    print("     - Password: s4nch3s\n")


if __name__ == '__main__':
    main()
