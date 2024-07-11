from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import logging
from createDb import initialize_database
import uuid  # Import uuid module

# Function to generate UUID
def generate_uuid():
    return str(uuid.uuid4())

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

# Initialize the database when the app starts
initialize_database()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dummy data for demonstration
records = [
    {
        'declaration_id': '001', 'declarant_name': 'John Doe', 'position': 'Manager', 'agency': 'Agency A', 'office_address': '123 Office St.',
        'spouse_name': 'Jane Doe', 'spouse_position': 'Engineer', 'spouse_agency': 'Agency B', 'spouse_office_address': '456 Office St.',
        'child_no': 1, 'child_name': 'Child One', 'child_birthdate': '2005-05-15', 'child_age': 18, 'real_asset_no': 1,
        'real_asset_description': 'House', 'real_asset_kind': 'Residential', 'real_asset_location': 'Location A', 'real_asset_assessed_value': 300000,
        'real_asset_market_value': 350000, 'real_asset_year_acquired': 2010, 'real_asset_mode_of_acquisition': 'Purchased', 'real_asset_acquisition_cost': 250000,
        'personal_asset_no': 1, 'personal_asset_description': 'Car', 'personal_asset_year_acquired': 2015, 'personal_asset_acquisition_cost': 20000,
        'liability_no': 1, 'liability_description': 'Mortgage', 'liability_creditor': 'Bank A', 'liability_balance': 150000,
        'real_assets_subtotal': 300000, 'personal_assets_subtotal': 20000, 'total_assets': 320000, 'total_liabilities': 150000, 'net_worth': 170000
    }
]

# Routes
def get_db_connection():
    conn = sqlite3.connect('saln_database.db')
    conn.row_factory = sqlite3.Row
    return conn
@app.route('/')
def index():
    logger.info('Rendering index page')
    return render_template('index.html')

@app.route('/submit_declaration', methods=['POST'])
def submit_declaration():
    conn = None
    try:
        conn = sqlite3.connect('saln_database.db')
        cursor = conn.cursor()

        # Insert declarant information
        cursor.execute("""
            INSERT INTO DeclarantInformation (declarant_name, declarant_position, declarant_agency, declarant_office_address, 
                                              spouse_name, spouse_position, spouse_agency, spouse_address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            request.form['declarant_name'],
            request.form['declarant_position'],
            request.form['declarant_agency'],
            request.form['declarant_office_address'],
            request.form['spouse_name'],
            request.form['spouse_position'],
            request.form['spouse_agency'],
            request.form['spouse_address']
        ))
        declarant_id = cursor.lastrowid  # Get the last inserted row id

         # Insert children information
        child_names = request.form.getlist('child_name[]')
        child_birthdates = request.form.getlist('child_dob[]')
        child_ages = request.form.getlist('child_age[]')

        for i in range(len(child_names)):
            if child_names[i]:
                cursor.execute("""
                    INSERT INTO ChildrenInformation (declarant_id, child_name, child_dob, child_age)
                    VALUES (?, ?, ?, ?)
                """, (
                    declarant_id,
                    child_names[i],
                    child_birthdates[i],
                    child_ages[i]
                ))

        # Insert real assets
        real_asset_descs = request.form.getlist('real_asset_desc[]')
        real_asset_kinds = request.form.getlist('real_asset_kind[]')
        real_asset_locs = request.form.getlist('real_asset_loc[]')
        real_asset_areas = request.form.getlist('real_asset_area[]')
        real_asset_market_vals = request.form.getlist('real_asset_market_val[]')
        real_asset_years_acq = request.form.getlist('real_asset_year_acq[]')
        real_asset_modes_acq = request.form.getlist('real_asset_mode_acq[]')
        real_asset_acq_costs = request.form.getlist('real_asset_acq_cost[]')

        for i in range(len(real_asset_descs)):
            if real_asset_descs[i]:
                cursor.execute("""
                    INSERT INTO RealAssets (declarant_id, asset_description, asset_kind, asset_location, asset_assessed_value, 
                                            asset_market_value, asset_year_acquired, asset_mode_of_acquisition, asset_acquisition_cost)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    declarant_id,
                    real_asset_descs[i],
                    real_asset_kinds[i],
                    real_asset_locs[i],
                    real_asset_areas[i],
                    real_asset_market_vals[i],
                    real_asset_years_acq[i],
                    real_asset_modes_acq[i],
                    real_asset_acq_costs[i]
                ))

        # Insert personal assets
        personal_asset_descs = request.form.getlist('personal_asset_desc[]')
        personal_asset_years_acq = request.form.getlist('personal_asset_year_acq[]')
        personal_asset_acq_costs = request.form.getlist('personal_asset_acq_cost[]')

        for i in range(len(personal_asset_descs)):
            if personal_asset_descs[i]:
                cursor.execute("""
                    INSERT INTO PersonalAssets (declarant_id, personal_asset_description, personal_asset_year_acquired, personal_asset_acquisition_cost)
                    VALUES (?, ?, ?, ?)
                """, (
                    declarant_id,
                    personal_asset_descs[i],
                    personal_asset_years_acq[i],
                    personal_asset_acq_costs[i]
                ))


        # Insert liabilities
        liability_descs = request.form.getlist('liabilities_desc[]')
        liability_creditors = request.form.getlist('liabilities_creditor[]')
        liability_balances = request.form.getlist('liabilities_balance[]')

        for i in range(len(liability_descs)):
            if liability_descs[i]:
                cursor.execute("""
                    INSERT INTO Liabilities (declarant_id, liability_description, liability_creditor, liability_balance)
                    VALUES (?, ?, ?, ?)
                """, (
                    declarant_id,
                    liability_descs[i],
                    liability_creditors[i],
                    liability_balances[i]
                ))

        # Insert subtotals and totals
        cursor.execute("""
            INSERT INTO SubtotalsTotals (declarant_id, R_Asset_Subtotal, P_Asset_Subtotal, total_assets, total_liabilities, net_worth)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            declarant_id,
            request.form['R_Asset_Subtotal'],
            request.form['P_Asset_Subtotal'],
            request.form['total_assets'],
            request.form['total_liabilities'],
            request.form['net_worth']
        ))

        conn.commit()
        flash('Declaration submitted successfully', 'success')
        return redirect(url_for('index'))

    except Exception as e:
        if conn:
            conn.rollback()
        flash(f'Error submitting declaration: {str(e)}', 'error')
        return redirect(url_for('application_form'))

    finally:
        if conn:
            conn.close()

@app.route('/application-form', methods=['GET', 'POST'])
def application_form():
    conn = None
    try:
        conn = sqlite3.connect('saln_database.db')
        cursor = conn.cursor()

        # Fetch the latest declarant_id from the DeclarantInformation table
        cursor.execute("SELECT MAX(declarant_id) FROM DeclarantInformation")
        result = cursor.fetchone()
        next_declarant_id = result[0] + 1 if result and result[0] else 1

        return render_template('appForm.html', next_declarant_id=next_declarant_id)

    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('index'))

    finally:
        if conn:
            conn.close()


@app.route('/view-database')
def view_database():
    try:
        # Initialize the database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Base query for fetching data
        query = '''
        SELECT DeclarantInformation.*, ChildrenInformation.*, RealAssets.*, PersonalAssets.*, Liabilities.*
        FROM DeclarantInformation
        LEFT JOIN ChildrenInformation ON DeclarantInformation.declarant_id = ChildrenInformation.declarant_id
        LEFT JOIN RealAssets ON DeclarantInformation.declarant_id = RealAssets.declarant_id
        LEFT JOIN PersonalAssets ON DeclarantInformation.declarant_id = PersonalAssets.declarant_id
        LEFT JOIN Liabilities ON DeclarantInformation.declarant_id = Liabilities.declarant_id
        '''
        query_params = []
        conditions = []


        # Combine all conditions
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)


        # Execute query and fetch results
        cursor.execute(query, query_params)
        declarant_data = cursor.fetchall()

        # Queries for fetching additional details
        children_query = 'SELECT * FROM ChildrenInformation WHERE declarant_id = ?;'
        real_assets_query = 'SELECT * FROM RealAssets WHERE declarant_id = ?;'
        personal_assets_query = 'SELECT * FROM PersonalAssets WHERE declarant_id = ?;'
        liabilities_query = 'SELECT * FROM Liabilities WHERE declarant_id = ?;'

        # Fetch additional details for each declarant
        declarants = []
        for declarant in declarant_data:
            declarant_dict = dict(declarant)
            declarant_id = declarant['declarant_id']

            # Fetch children records
            children_records = cursor.execute(children_query, (declarant_id,)).fetchall()
            declarant_dict['children'] = [dict(child) for child in children_records]

            # Fetch real assets records
            real_assets_records = cursor.execute(real_assets_query, (declarant_id,)).fetchall()
            declarant_dict['real_assets'] = [dict(asset) for asset in real_assets_records]

            # Fetch personal assets records
            personal_assets_records = cursor.execute(personal_assets_query, (declarant_id,)).fetchall()
            declarant_dict['personal_assets'] = [dict(asset) for asset in personal_assets_records]

            # Fetch liabilities records
            liabilities_records = cursor.execute(liabilities_query, (declarant_id,)).fetchall()
            declarant_dict['liabilities'] = [dict(liability) for liability in liabilities_records]

            declarants.append(declarant_dict)

        # Calculate aggregate totals
        aggregate_query = '''
        SELECT 
            SUM(asset_market_value) AS total_real_assets, 
            SUM(personal_asset_acquisition_cost) AS total_personal_assets, 
            SUM(liability_balance) AS total_liabilities
        FROM RealAssets, PersonalAssets, Liabilities
        '''
        aggregate_totals = cursor.execute(aggregate_query).fetchone()
        total_real_assets = aggregate_totals['total_real_assets'] or 0
        total_personal_assets = aggregate_totals['total_personal_assets'] or 0
        total_liabilities = aggregate_totals['total_liabilities'] or 0

        net_worth = (total_real_assets + total_personal_assets) - total_liabilities

        conn.close()

        return render_template(
            'viewDb.html', 
            declarants=declarants,
            total_real_assets=total_real_assets,
            total_personal_assets=total_personal_assets,
            total_liabilities=total_liabilities,
            net_worth=net_worth
        )

    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        return "Error fetching data. Please check logs for more details."


@app.route('/update-record')
def update_record():
    return "Update record page (not implemented)"

@app.route('/delete-record')
def delete_record():
    return "Delete record page (not implemented)"


@app.route('/compute_values', methods=['POST'])
def compute_values():
    try:
        # Retrieve form data
        real_asset_acq_costs = request.form.getlist('real_asset_acq_cost[]')
        personal_asset_acq_costs = request.form.getlist('personal_asset_acq_cost[]')
        liabilities_balances = request.form.getlist('liabilities_balance[]')

        # Convert all values to integers for calculation
        real_asset_acq_costs = list(map(int, real_asset_acq_costs))
        personal_asset_acq_costs = list(map(int, personal_asset_acq_costs))
        liabilities_balances = list(map(int, liabilities_balances))

        # Calculate subtotal and totals
        real_assets_subtotal = sum(real_asset_acq_costs)
        personal_assets_subtotal = sum(personal_asset_acq_costs)
        total_assets = real_assets_subtotal + personal_assets_subtotal
        total_liabilities = sum(liabilities_balances)
        net_worth = total_assets - total_liabilities

        # Prepare JSON response
        response_data = {
            'real_assets_subtotal': real_assets_subtotal,
            'personal_assets_subtotal': personal_assets_subtotal,
            'total_assets': total_assets,
            'total_liabilities': total_liabilities,
            'net_worth': net_worth
        }

        return jsonify(response_data)

    except Exception as e:
        flash(f'Error computing values: {str(e)}', 'error')
        return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)
