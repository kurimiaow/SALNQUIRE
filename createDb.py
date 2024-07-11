import sqlite3

def create_database():
    try:
        connection = sqlite3.connect('declarant_info.db')
        cursor = connection.cursor()

        # Create Declarant Information Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS DeclarantInformation (
                declarant_id INTEGER PRIMARY KEY AUTOINCREMENT,
                declarant_name TEXT NOT NULL,
                declarant_position TEXT NOT NULL,
                declarant_agency TEXT NOT NULL,
                declarant_office_address TEXT NOT NULL,
                spouse_name TEXT,
                spouse_position TEXT,
                spouse_agency TEXT,
                spouse_office_address TEXT
            );
        ''')

        # Create Children Information Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ChildrenInformation (
                child_id INTEGER PRIMARY KEY AUTOINCREMENT,
                declarant_id INTEGER NOT NULL,
                child_name TEXT,
                child_dob DATE,
                child_age INTEGER,
                FOREIGN KEY (declarant_id) REFERENCES DeclarantInformation (declarant_id)
            );
        ''')

        # Create Real Assets Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS RealAssets (
                asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
                declarant_id INTEGER NOT NULL,
                real_asset_desc TEXT,
                real_asset_kind TEXT,
                real_asset_loc TEXT,
                real_asset_area REAL,
                real_asset_market_val REAL,
                real_asset_year_acq DATE,
                real_asset_mode_acq TEXT,
                real_asset_acq_cost REAL,
                FOREIGN KEY (declarant_id) REFERENCES DeclarantInformation (declarant_id)
            );
        ''')

        # Create Personal Assets Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS PersonalAssets (
                personal_asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
                declarant_id INTEGER NOT NULL,
                personal_asset_desc TEXT,
                personal_asset_year_acq DATE,
                personal_asset_acq_cost REAL,
                FOREIGN KEY (declarant_id) REFERENCES DeclarantInformation (declarant_id)
            );
        ''')

        # Create Liabilities Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Liabilities (
                liability_id INTEGER PRIMARY KEY AUTOINCREMENT,
                declarant_id INTEGER NOT NULL,
                liabilities_desc TEXT,
                liabilities_amount REAL,
                liabilities_date DATE,
                FOREIGN KEY (declarant_id) REFERENCES DeclarantInformation (declarant_id)
            );
        ''')

         # Create Subtotals and Totals Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS SubtotalsAndTotals (
                subtotal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                declarant_id INTEGER NOT NULL,
                real_assets_subtotal REAL NOT NULL,
                personal_assets_subtotal REAL NOT NULL,
                total_assets REAL NOT NULL,
                total_liabilities REAL NOT NULL,
                net_worth REAL NOT NULL,
                FOREIGN KEY (declarant_id) REFERENCES DeclarantInformation (declarant_id)
            );
        ''')

        connection.commit()
        print("Database initialized successfully!")

    except sqlite3.Error as error:
        print("Error while connecting to SQLite:", error)
    finally:
        if connection:
            connection.close()

# Call the function to create the database
create_database()
