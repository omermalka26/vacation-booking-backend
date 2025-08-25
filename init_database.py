#!/usr/bin/env python3
"""
Database initialization script for Vacation Booking System
This script will create the initial data including admin user, countries, and sample vacations.
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize the database with initial data"""
    
    # Connect to database
    db_path = "projectdb.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Initializing database...")
    
    # Create tables if they don't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            role_id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT UNIQUE NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role_id INTEGER DEFAULT 2,
            FOREIGN KEY (role_id) REFERENCES roles(role_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS countries (
            country_id INTEGER PRIMARY KEY AUTOINCREMENT,
            country_name TEXT UNIQUE NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vacations (
            vacation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            vacation_description TEXT NOT NULL,
            country_id INTEGER NOT NULL,
            vacation_start DATE NOT NULL,
            vacation_end DATE NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            picture_file_name TEXT,
            FOREIGN KEY (country_id) REFERENCES countries(country_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS likes (
            like_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            vacation_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (vacation_id) REFERENCES vacations(vacation_id),
            UNIQUE(user_id, vacation_id)
        )
    ''')
    
    # Insert roles
    print("Inserting roles...")
    cursor.execute("INSERT OR IGNORE INTO roles (role_id, role_name) VALUES (1, 'admin')")
    cursor.execute("INSERT OR IGNORE INTO roles (role_id, role_name) VALUES (2, 'user')")
    
    # Insert admin user
    print("Inserting admin user...")
    admin_password_hash = generate_password_hash('admin123')
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, first_name, last_name, email, password_hash, role_id)
        VALUES (1, 'Admin', 'User', 'admin@admin.com', ?, 1)
    ''', (admin_password_hash,))
    
    # Insert countries
    print("Inserting countries...")
    countries = [
        'USA', 'Canada', 'UK', 'France', 'Germany', 'Italy', 'Spain', 
        'Japan', 'China', 'India', 'Australia', 'Brazil', 'Mexico', 
        'South Africa', 'Egypt', 'Israel', 'Turkey', 'Greece', 'Netherlands', 'Sweden'
    ]
    
    for country in countries:
        cursor.execute("INSERT OR IGNORE INTO countries (country_name) VALUES (?)", (country,))
    
    # Insert sample vacations
    print("Inserting sample vacations...")
    sample_vacations = [
        ('Amazing vacation in Italy', 6, '2024-06-01', '2024-06-07', 1500.00, 'italy.jpg'),
        ('Beautiful beaches in Spain', 7, '2024-07-15', '2024-07-22', 1200.00, 'spain.jpg'),
        ('Adventure in Japan', 8, '2024-08-10', '2024-08-17', 2000.00, 'japan.jpg'),
        ('Relaxing in France', 4, '2024-09-01', '2024-09-05', 1800.00, 'france.jpg'),
        ('Explore USA', 1, '2024-10-15', '2024-10-22', 1600.00, 'usa.jpg'),
        ('Canadian wilderness', 2, '2024-11-01', '2024-11-08', 1400.00, 'canada.jpg'),
        ('UK cultural tour', 3, '2024-12-01', '2024-12-08', 1700.00, 'uk.jpg'),
        ('German Christmas markets', 5, '2024-12-15', '2024-12-22', 1900.00, 'germany.jpg'),
        ('Chinese New Year', 9, '2025-01-15', '2025-01-22', 2200.00, 'china.jpg'),
        ('Indian heritage tour', 10, '2025-02-01', '2025-02-08', 1300.00, 'india.jpg'),
        ('Australian outback', 11, '2025-03-01', '2025-03-08', 2500.00, 'australia.jpg'),
        ('Brazilian carnival', 12, '2025-04-01', '2025-04-08', 2100.00, 'brazil.jpg'),
        ('Mexican fiesta', 13, '2025-05-01', '2025-05-08', 1400.00, 'mexico.jpg'),
        ('South African safari', 14, '2025-06-01', '2025-06-08', 2800.00, 'safari.jpg'),
        ('Egyptian pyramids', 15, '2025-07-01', '2025-07-08', 1800.00, 'egypt.jpg'),
        ('Israel holy sites', 16, '2025-08-01', '2025-08-08', 1600.00, 'israel.jpg'),
        ('Turkish bazaars', 17, '2025-09-01', '2025-09-08', 1500.00, 'turkey.jpg'),
        ('Greek islands', 18, '2025-10-01', '2025-10-08', 1700.00, 'greece.jpg'),
        ('Dutch windmills', 19, '2025-11-01', '2025-11-08', 1600.00, 'netherlands.jpg'),
        ('Swedish aurora', 20, '2025-12-01', '2025-12-08', 2400.00, 'sweden.jpg')
    ]
    
    for vacation in sample_vacations:
        cursor.execute('''
            INSERT OR IGNORE INTO vacations 
            (vacation_description, country_id, vacation_start, vacation_end, price, picture_file_name)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', vacation)
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print("Database initialization completed successfully!")
    print(f"Database file: {os.path.abspath(db_path)}")

if __name__ == "__main__":
    init_database()
