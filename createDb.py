import sqlite3
import os

def initialize_database():
    # Check if the database file already exists
    db_file = 'saln_database.db'
    db_exists = os.path.exists(db_file)

    # Connect to the database (this will create it if it doesn't exist)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS DeclarantInformation (
            declarant_id INTEGER PRIMARY KEY AUTOINCREMENT,
            declarant_name TEXT NOT NULL,
            declarant_position TEXT NOT NULL,
            declarant_agency TEXT NOT NULL,
            declarant_office_address TEXT NOT NULL,
            spouse_name TEXT,
            spouse_position TEXT,
            spouse_agency TEXT,
            spouse_address TEXT
        );

        CREATE TABLE IF NOT EXISTS ChildrenInformation (
            child_id INTEGER PRIMARY KEY AUTOINCREMENT,
            declarant_id INTEGER,
            child_name TEXT,
            child_dob DATE,
            child_age INTEGER,
            FOREIGN KEY (declarant_id) REFERENCES DeclarantInformation (declarant_id)
        );

        CREATE TABLE IF NOT EXISTS RealAssets (
            asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
            declarant_id INTEGER,
            asset_description TEXT,
            asset_kind TEXT,
            asset_location TEXT,
            asset_assessed_value REAL,
            asset_market_value REAL,
            asset_year_acquired DATE,
            asset_mode_of_acquisition TEXT,
            asset_acquisition_cost REAL,
            FOREIGN KEY (declarant_id) REFERENCES DeclarantInformation (declarant_id)
        );

        CREATE TABLE IF NOT EXISTS PersonalAssets (
            personal_asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
            declarant_id INTEGER,
            personal_asset_description TEXT,
            personal_asset_year_acquired DATE,
            personal_asset_acquisition_cost REAL,
            FOREIGN KEY (declarant_id) REFERENCES DeclarantInformation (declarant_id)
        );

        CREATE TABLE IF NOT EXISTS Liabilities (
            liability_id INTEGER PRIMARY KEY AUTOINCREMENT,
            declarant_id INTEGER,
            liability_description TEXT,
            liability_creditor TEXT,
            liability_balance REAL,
            FOREIGN KEY (declarant_id) REFERENCES DeclarantInformation (declarant_id)
        );

        CREATE TABLE IF NOT EXISTS SubtotalsTotals (
            declarant_id INTEGER PRIMARY KEY,
            R_Asset_Subtotal REAL,
            P_Asset_Subtotal REAL,
            total_assets REAL,
            total_liabilities REAL,
            net_worth REAL,
            FOREIGN KEY (declarant_id) REFERENCES DeclarantInformation (declarant_id)
        );
    ''')

    conn.commit()
    conn.close()

    if db_exists:
        print("Database already existed. Tables checked/updated.")
    else:
        print("Database created and tables initialized successfully.")

if __name__ == '__main__':
    initialize_database()

