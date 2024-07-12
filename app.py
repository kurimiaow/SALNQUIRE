from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
import logging
from createDb import initialize_database
import uuid

# Function to generate UUID
def generate_uuid():
    return str(uuid.uuid4())

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()
# Initialize the database when the app starts
initialize_database()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        declarant_id = cursor.lastrowid

        # Insert children information
        child_names = request.form.getlist('child_name[]')
        child_birthdates = request.form.getlist('child_dob[]')
        child_ages = request.form.getlist('child_age[]')

        for i in range(len(child_names)):
            if child_names[i]:
                cursor.execute("""
                    INSERT INTO ChildrenInformation (declarant_id, child_name, child_dob, child_age)
                    VALUES (?, ?, ?, ?)
                """, (declarant_id, child_names[i], child_birthdates[i], child_ages[i]))

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
                    declarant_id, real_asset_descs[i], real_asset_kinds[i], real_asset_locs[i], real_asset_areas[i],
                    real_asset_market_vals[i], real_asset_years_acq[i], real_asset_modes_acq[i], real_asset_acq_costs[i]
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
                """, (declarant_id, personal_asset_descs[i], personal_asset_years_acq[i], personal_asset_acq_costs[i]))

        # Insert liabilities
        liability_descs = request.form.getlist('liabilities_desc[]')
        liability_creditors = request.form.getlist('liabilities_creditor[]')
        liability_balances = request.form.getlist('liabilities_balance[]')

        for i in range(len(liability_descs)):
            if liability_descs[i]:
                cursor.execute("""
                    INSERT INTO Liabilities (declarant_id, liability_description, liability_creditor, liability_balance)
                    VALUES (?, ?, ?, ?)
                """, (declarant_id, liability_descs[i], liability_creditors[i], liability_balances[i]))

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
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM DeclarantInformation')
        declarants = cursor.fetchall()

        cursor.execute('SELECT * FROM ChildrenInformation')
        children = cursor.fetchall()

        cursor.execute('SELECT * FROM RealAssets')
        real_assets = cursor.fetchall()

        cursor.execute('SELECT * FROM PersonalAssets')
        personal_assets = cursor.fetchall()

        cursor.execute('SELECT * FROM Liabilities')
        liabilities = cursor.fetchall()

        cursor.execute('SELECT * FROM SubtotalsTotals')
        subtotals_totals = cursor.fetchall()

        conn.close()

        return render_template('viewDb.html',
                               declarants=declarants,
                               children=children,
                               real_assets=real_assets,
                               personal_assets=personal_assets,
                               liabilities=liabilities,
                               subtotals_totals=subtotals_totals)

    except Exception as e:
        logger.error(f"Error fetching data: {str(e)}")
        return "Error fetching data. Please check logs for more details."

@app.route('/update-record', methods=['GET', 'POST'])
def update_record():
    if request.method == 'POST':
        declarant_id = request.form['declarant_id']
        declarant_name = request.form['declarant_name']
        
        all_data = get_all_declarant_data(declarant_id)
        
        if all_data:
            return render_template('edit_record.html', data=all_data)
        else:
            flash('No matching record found', 'error')
            return redirect(url_for('update_record'))

    return render_template('update_record.html')

@app.route('/submit-updated-declaration', methods=['POST'])
def submit_updated_declaration():
    conn = None
    try:
        conn = sqlite3.connect('saln_database.db')
        cursor = conn.cursor()

        declarant_id = request.form['declarant_id']

        # Update DeclarantInformation
        cursor.execute("""
            UPDATE DeclarantInformation SET
            declarant_name = ?, declarant_position = ?, declarant_agency = ?, declarant_office_address = ?,
            spouse_name = ?, spouse_position = ?, spouse_agency = ?, spouse_address = ?
            WHERE declarant_id = ?
        """, (
            request.form['declarant_name'], request.form['declarant_position'],
            request.form['declarant_agency'], request.form['declarant_office_address'],
            request.form['spouse_name'], request.form['spouse_position'],
            request.form['spouse_agency'], request.form['spouse_address'],
            declarant_id
        ))

        # Delete existing children and insert updated ones
        cursor.execute("DELETE FROM ChildrenInformation WHERE declarant_id = ?", (declarant_id,))
        child_names = request.form.getlist('child_name[]')
        child_dobs = request.form.getlist('child_dob[]')
        child_ages = request.form.getlist('child_age[]')
        for name, dob, age in zip(child_names, child_dobs, child_ages):
            if name:
                cursor.execute("""
                    INSERT INTO ChildrenInformation (declarant_id, child_name, child_dob, child_age)
                    VALUES (?, ?, ?, ?)
                """, (declarant_id, name, dob, age))

        # Update RealAssets
        cursor.execute("DELETE FROM RealAssets WHERE declarant_id = ?", (declarant_id,))
        real_asset_descs = request.form.getlist('real_asset_desc[]')
        real_asset_kinds = request.form.getlist('real_asset_kind[]')
        real_asset_locs = request.form.getlist('real_asset_loc[]')
        real_asset_areas = request.form.getlist('real_asset_area[]')
        real_asset_market_vals = request.form.getlist('real_asset_market_val[]')
        real_asset_year_acqs = request.form.getlist('real_asset_year_acq[]')
        real_asset_mode_acqs = request.form.getlist('real_asset_mode_acq[]')
        real_asset_acq_costs = request.form.getlist('real_asset_acq_cost[]')
        for desc, kind, loc, area, market_val, year_acq, mode_acq, acq_cost in zip(
            real_asset_descs, real_asset_kinds, real_asset_locs, real_asset_areas,
            real_asset_market_vals, real_asset_year_acqs, real_asset_mode_acqs, real_asset_acq_costs
        ):
            if desc:
                cursor.execute("""
                    INSERT INTO RealAssets (declarant_id, asset_description, asset_kind, asset_location,
                    asset_assessed_value, asset_market_value, asset_year_acquired, asset_mode_of_acquisition,
                    asset_acquisition_cost)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (declarant_id, desc, kind, loc, area, market_val, year_acq, mode_acq, acq_cost))

        # Update PersonalAssets
        cursor.execute("DELETE FROM PersonalAssets WHERE declarant_id = ?", (declarant_id,))
        personal_asset_descs = request.form.getlist('personal_asset_desc[]')
        personal_asset_year_acqs = request.form.getlist('personal_asset_year_acq[]')
        personal_asset_acq_costs = request.form.getlist('personal_asset_acq_cost[]')
        for desc, year_acq, acq_cost in zip(personal_asset_descs, personal_asset_year_acqs, personal_asset_acq_costs):
            if desc:
                cursor.execute("""
                    INSERT INTO PersonalAssets (declarant_id, personal_asset_description,
                    personal_asset_year_acquired, personal_asset_acquisition_cost)
                    VALUES (?, ?, ?, ?)
                """, (declarant_id, desc, year_acq, acq_cost))

        # Update Liabilities
        cursor.execute("DELETE FROM Liabilities WHERE declarant_id = ?", (declarant_id,))
        liability_descs = request.form.getlist('liabilities_desc[]')
        liability_creditors = request.form.getlist('liabilities_creditor[]')
        liability_balances = request.form.getlist('liabilities_balance[]')
        for desc, creditor, balance in zip(liability_descs, liability_creditors, liability_balances):
            if desc:
                cursor.execute("""
                    INSERT INTO Liabilities (declarant_id, liability_description, liability_creditor, liability_balance)
                    VALUES (?, ?, ?, ?)
                """, (declarant_id, desc, creditor, balance))

        # Update SubtotalsTotals
        cursor.execute("""
            UPDATE SubtotalsTotals SET
            R_Asset_Subtotal = ?, P_Asset_Subtotal = ?, total_assets = ?, total_liabilities = ?, net_worth = ?
            WHERE declarant_id = ?
        """, (
            request.form['R_Asset_Subtotal'], request.form['P_Asset_Subtotal'],
            request.form['total_assets'], request.form['total_liabilities'],
            request.form['net_worth'], declarant_id
        ))

        conn.commit()
        flash('Declaration updated successfully', 'success')
        return redirect(url_for('index'))

    except Exception as e:
        if conn:
            conn.rollback()
        flash(f'Error updating declaration: {str(e)}', 'error')
        return redirect(url_for('update_record'))

    finally:
        if conn:
            conn.close()
@app.route('/delete-declaration/<int:declarant_id>', methods=['POST'])
def delete_declaration(declarant_id):
    conn = None
    try:
        conn = sqlite3.connect('saln_database.db')
        cursor = conn.cursor()

        # Delete from all related tables
        tables = ['DeclarantInformation', 'ChildrenInformation', 'RealAssets', 
                  'PersonalAssets', 'Liabilities', 'SubtotalsTotals']
        
        for table in tables:
            cursor.execute(f"DELETE FROM {table} WHERE declarant_id = ?", (declarant_id,))

        conn.commit()
        return jsonify({'success': True})

    except Exception as e:
        if conn:
            conn.rollback()
        print(f'Error deleting declaration: {str(e)}')
        return jsonify({'success': False})

    finally:
        if conn:
            conn.close()
@app.route('/delete-record')
def delete_record():
    return "Delete record page (not implemented)"

@app.route('/compute_values', methods=['POST'])
def compute_values():
    try:
        real_asset_acq_costs = request.form.getlist('real_asset_acq_cost[]')
        personal_asset_acq_costs = request.form.getlist('personal_asset_acq_cost[]')
        liabilities_balances = request.form.getlist('liabilities_balance[]')

        real_asset_acq_costs = list(map(int, real_asset_acq_costs))
        personal_asset_acq_costs = list(map(int, personal_asset_acq_costs))
        liabilities_balances = list(map(int, liabilities_balances))

        real_assets_subtotal = sum(real_asset_acq_costs)
        personal_assets_subtotal = sum(personal_asset_acq_costs)
        total_assets = real_assets_subtotal + personal_assets_subtotal
        total_liabilities = sum(liabilities_balances)
        net_worth = total_assets - total_liabilities

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

def get_declarant_by_id_and_name(declarant_id, declarant_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM DeclarantInformation WHERE declarant_id = ? AND declarant_name = ?', (declarant_id, declarant_name))
    declarant = cursor.fetchone()
    conn.close()
    return declarant

def get_all_declarant_data(declarant_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Fetch declarant information
    cursor.execute('SELECT * FROM DeclarantInformation WHERE declarant_id = ?', (declarant_id,))
    declarant_info = cursor.fetchone()
    
    if not declarant_info:
        return None

    # Fetch children information
    cursor.execute('SELECT * FROM ChildrenInformation WHERE declarant_id = ?', (declarant_id,))
    children = cursor.fetchall()

    # Fetch real assets
    cursor.execute('SELECT * FROM RealAssets WHERE declarant_id = ?', (declarant_id,))
    real_assets = cursor.fetchall()

    # Fetch personal assets
    cursor.execute('SELECT * FROM PersonalAssets WHERE declarant_id = ?', (declarant_id,))
    personal_assets = cursor.fetchall()

    # Fetch liabilities
    cursor.execute('SELECT * FROM Liabilities WHERE declarant_id = ?', (declarant_id,))
    liabilities = cursor.fetchall()

    # Fetch subtotals and totals
    cursor.execute('SELECT * FROM SubtotalsTotals WHERE declarant_id = ?', (declarant_id,))
    subtotals_totals = cursor.fetchone()

    conn.close()

    return {
        'declarant_info': declarant_info,
        'children': children,
        'real_assets': real_assets,
        'personal_assets': personal_assets,
        'liabilities': liabilities,
        'subtotals_totals': subtotals_totals
    }

def update_declarant_data(updated_data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Update DeclarantInformation table
        cursor.execute('''
            UPDATE DeclarantInformation
            SET declarant_name = ?, declarant_position = ?, declarant_agency = ?, declarant_office_address = ?,
                spouse_name = ?, spouse_position = ?, spouse_agency = ?, spouse_address = ?
            WHERE declarant_id = ?
        ''', (
            updated_data['declarant_name'],
            updated_data['declarant_position'],
            updated_data['declarant_agency'],
            updated_data['declarant_office_address'],
            updated_data['spouse_name'],
            updated_data['spouse_position'],
            updated_data['spouse_agency'],
            updated_data['spouse_address'],
            updated_data['declarant_id']
        ))

        # Update other tables (ChildrenInformation, RealAssets, PersonalAssets, Liabilities)
        # ... (implement similar update operations for other tables)

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error updating data: {str(e)}")
        return False

if __name__ == '__main__':
    app.run(debug=True)
