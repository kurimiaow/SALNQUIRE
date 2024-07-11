from flask import Flask, render_template, request, jsonify
import sqlite3
import traceback
from createDb import create_database

app = Flask(__name__)
app.secret_key = 'your_secret_key'

create_database()

@app.route('/')
def index():
    app.logger.info('Rendering index page')
    return render_template('index.html')

@app.route('/application-form', methods=['GET', 'POST'])
def application_form():
    if request.method == 'POST':
        conn = None
        try:
            conn = sqlite3.connect('declarant_info.db')
            cursor = conn.cursor()

            print("Form Data:")
            for key, value in request.form.items():
                print(f"{key}: {value}")

            # Insert Declarant Information
            cursor.execute('''
                INSERT INTO DeclarantInformation 
                (declarant_name, declarant_position, declarant_agency, declarant_office_address, 
                spouse_name, spouse_position, spouse_agency, spouse_office_address)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                request.form['declarant_name'], request.form['declarant_position'],
                request.form['declarant_agency'], request.form['declarant_office_address'],
                request.form['spouse_name'], request.form['spouse_position'],
                request.form['spouse_agency'], request.form['spouse_address']
            ))
            
            declarant_id = cursor.lastrowid
            print(f"Inserted declarant with ID: {declarant_id}")

            # Insert Children Information
            child_names = request.form.getlist('child_name[]')
            child_dobs = request.form.getlist('child_dob[]')
            child_ages = request.form.getlist('child_age[]')
            
            for name, dob, age in zip(child_names, child_dobs, child_ages):
                if name and dob and age:
                    cursor.execute('''
                        INSERT INTO ChildrenInformation 
                        (declarant_id, child_name, child_dob, child_age)
                        VALUES (?, ?, ?, ?)
                    ''', (declarant_id, name, dob, age))
                    print(f"Inserted child: {name}")

            # Insert Real Assets
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
                if all([desc, kind, loc, area, market_val, year_acq, mode_acq, acq_cost]):
                    cursor.execute('''
                        INSERT INTO RealAssets 
                        (declarant_id, real_asset_desc, real_asset_kind, real_asset_loc, real_asset_area,
                        real_asset_market_val, real_asset_year_acq, real_asset_mode_acq, real_asset_acq_cost)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (declarant_id, desc, kind, loc, area, market_val, year_acq, mode_acq, acq_cost))
                    print(f"Inserted real asset: {desc}")

            # Insert Personal Assets
            personal_asset_descs = request.form.getlist('personal_asset_desc[]')
            personal_asset_year_acqs = request.form.getlist('personal_asset_year_acq[]')
            personal_asset_acq_costs = request.form.getlist('personal_asset_acq_cost[]')

            for desc, year_acq, acq_cost in zip(personal_asset_descs, personal_asset_year_acqs, personal_asset_acq_costs):
                if all([desc, year_acq, acq_cost]):
                    cursor.execute('''
                        INSERT INTO PersonalAssets 
                        (declarant_id, personal_asset_desc, personal_asset_year_acq, personal_asset_acq_cost)
                        VALUES (?, ?, ?, ?)
                    ''', (declarant_id, desc, year_acq, acq_cost))
                    print(f"Inserted personal asset: {desc}")

            # Insert Liabilities
            liabilities_descs = request.form.getlist('liabilities_desc[]')
            liabilities_amounts = request.form.getlist('liabilities_amount[]')
            liabilities_dates = request.form.getlist('liabilities_date[]')

            for desc, amount, date in zip(liabilities_descs, liabilities_amounts, liabilities_dates):
                if all([desc, amount, date]):
                    cursor.execute('''
                        INSERT INTO Liabilities 
                        (declarant_id, liabilities_desc, liabilities_amount, liabilities_date)
                        VALUES (?, ?, ?, ?)
                    ''', (declarant_id, desc, amount, date))
                    print(f"Inserted liability: {desc}")

            # Insert Subtotals and Totals
            cursor.execute('''
                INSERT INTO SubtotalsAndTotals
                (declarant_id, real_assets_subtotal, personal_assets_subtotal, total_assets, total_liabilities, net_worth)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                declarant_id,
                request.form['R_Asset_Subtotal'],
                request.form['P_Asset_Subtotal'],
                request.form['total_assets'],
                request.form['total_liabilities'],
                request.form['net_worth']
            ))
            print("Inserted subtotals and totals")

            conn.commit()
            print("All data committed to database")
            return jsonify({"message": "Form submitted successfully"}), 200
        except Exception as e:
            print(f"Error submitting form: {str(e)}")
            print(traceback.format_exc())
            if conn:
                conn.rollback()
            return jsonify({"error": str(e)}), 400
        finally:
            if conn:
                conn.close()

    return render_template('appForm.html')


@app.route('/view-database')
def view_database():
    conn = sqlite3.connect('declarant_info.db')
    cursor = conn.cursor()

    # Fetch all data from all tables
    cursor.execute('''
        SELECT d.*, c.*, r.*, p.*, l.*, s.*
        FROM DeclarantInformation d
        LEFT JOIN ChildrenInformation c ON d.declarant_id = c.declarant_id
        LEFT JOIN RealAssets r ON d.declarant_id = r.declarant_id
        LEFT JOIN PersonalAssets p ON d.declarant_id = p.declarant_id
        LEFT JOIN Liabilities l ON d.declarant_id = l.declarant_id
        LEFT JOIN SubtotalsAndTotals s ON d.declarant_id = s.declarant_id
    ''')

    data = cursor.fetchall()
    conn.close()

    return render_template('viewDb.html', data=data)

@app.route('/update-record')
def update_record():
    return "Update record page (not implemented)"

@app.route('/delete-record')
def delete_record():
    return "Delete record page (not implemented)"

@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        r_asset_subtotal = request.form['R_Asset_Subtotal']
        # Process the form data here
        return 'Form submitted successfully!'
    except KeyError as e:
        # Handle the case where 'R_Asset_Subtotal' key is missing
        return f'Error: Missing required field {e.args[0]}', 400
    except Exception as e:
        # Handle other unexpected exceptions
        return f'Error: {str(e)}', 500

if __name__ == '__main__':
    app.run(debug=True)
