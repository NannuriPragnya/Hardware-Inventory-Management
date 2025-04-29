import sqlite3
import os

def create_connection():
    db_path = os.path.join("db", "inventory.db")
    return sqlite3.connect(db_path)

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS Weapons (
        weapon_id INTEGER PRIMARY KEY AUTOINCREMENT,
        weapon_name TEXT,
        type TEXT,
        range TEXT,
        functionality TEXT
    );

    CREATE TABLE IF NOT EXISTS Inventory (
        inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
        weapon_id INTEGER,
        quantity INTEGER,
        FOREIGN KEY (weapon_id) REFERENCES Weapons(weapon_id)
    );

    CREATE TABLE IF NOT EXISTS PoliceOfficers (
        officer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        rank TEXT,
        department TEXT
    );

    CREATE TABLE IF NOT EXISTS Assigned (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        weapon_id INTEGER,
        assigned_date TEXT,
        officer_id INTEGER,
        FOREIGN KEY (weapon_id) REFERENCES Weapons(weapon_id),
        FOREIGN KEY (officer_id) REFERENCES PoliceOfficers(officer_id)
    );
    """)

    conn.commit()
    conn.close()
    print("Tables created successfully!")

if __name__ == "__main__":
    create_tables()
