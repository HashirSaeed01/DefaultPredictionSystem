import io
from flask import json, render_template, request, jsonify
from flask_login import login_required
from werkzeug.utils import secure_filename
from apps.datahandling import blueprint
from sqlalchemy.exc import NoSuchTableError
import pandas as pd
from sqlalchemy import inspect, text
from apps import db  


import pandas as pd

from apps.datahandling.models import FinancialMetrics
from apps.datahandling.ModelService import ModelService







# @blueprint.route('/index')

# @login_required
# def index():
#     print("=== DEBUG: Index Route Started ===")
#     print(f"URL Parameters: {request.args}")
    
#     # If no URL parameters, try to get the latest record
#     if not request.args:
#         print("No URL parameters, attempting to fetch latest record")
#         try:
#             query = text('SELECT * FROM "FinancialMetrics" ORDER BY id DESC LIMIT 1')
#             print(f"Executing query: {query}")
            
#             result = db.session.execute(query)
#             latest_record = result.fetchone()
            
#             print(f"Query result: {latest_record}")
            
#             if latest_record:
#                 columns = result.keys()
#                 record_dict = dict(zip(columns, latest_record))
#                 print(f"Converted to dict: {record_dict}")
                
#                 return render_template('home/index.html', 
#                     segment='index',
#                     data=record_dict
#                 )
#             else:
#                 print("No records found in database")
                
#         except Exception as e:
#             print(f"ERROR in database query: {str(e)}")
#             print(f"Error type: {type(e)}")
#             import traceback
#             print(f"Traceback: {traceback.format_exc()}")
    
#     print("Rendering template with default values")
#     return render_template('home/index.html', segment='index')

















@blueprint.route('/history', methods=['GET'])
# @login_required
def history():
    print("history")
    try:
        # Check if 'FinancialMetrics' table exists
        inspector = inspect(db.engine)
        if not inspector.has_table('FinancialMetrics'):  # Lowercase for Postgres
            return render_template('home/tables.html', 
                                   records=[], 
                                   columns=[], 
                                   error="No data available yet.")
        
        # Execute query
        query = text('SELECT * FROM "FinancialMetrics"')  # Use double quotes
        result = db.session.execute(query)
        records = result.fetchall()

        # Get column names
        columns = result.keys()

        # Convert records to a list of dictionaries
        records = [dict(zip(columns, row)) for row in records]

        return render_template('home/tables.html', 
                               records=records,
                               columns=columns,
                               error=None)

    except Exception as e:
        print(f"Error fetching history: {str(e)}")
        return render_template('home/tables.html', 
                               records=[], 
                               columns=[], 
                               error=f"Error fetching data: {str(e)}")



























        
@blueprint.route('/check-columns', methods=['POST'])
# @login_required
def check_columns():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file uploaded'})

    file = request.files['file']
    
    if not file.filename:
        return jsonify({'success': False, 'message': 'No file selected'})

    try:
        # Read CSV or Excel file based on file type
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith('.xlsx'):
            try:
                df = pd.read_excel(file, engine='openpyxl')
            except Exception as excel_error:
                print(f"Excel reading error: {str(excel_error)}")
                return jsonify({
                    'success': False, 
                    'message': 'Error reading Excel file. Please make sure it is not corrupted and try again.'
                })
        else:
            return jsonify({'success': False, 'message': 'Unsupported file type. Please upload a CSV or XLSX file.'})

        # Debug: Print column information (but not file content)
        print("File type:", file.filename)
        print("Columns found:", list(df.columns))
        print("Data types:", df.dtypes)
        
        # Standardize columns (lowercase and replace spaces with underscores)
        df.columns = [col.lower().replace(" ", "_") for col in df.columns]
        
        # Check if columns exist in the database
        inspector = inspect(db.engine)
        existing_columns = [c['name'] for c in inspector.get_columns('rawdata')] if inspector.has_table('rawdata') else []
        missing_columns = [col for col in df.columns if col not in existing_columns]

        # Debug: Print database information
        print("Existing DB columns:", existing_columns)
        print("Missing columns:", missing_columns)

        if missing_columns:
            return jsonify({
                'success': True,
                'missing_columns': missing_columns,
                'message': 'New columns detected. Do you want to create them?'
            })

        return jsonify({'success': True, 'message': 'All columns exist in the database.'})

    except Exception as e:
        print(f"Error details: {str(e)}")
        return jsonify({'success': False, 'message': f'Error reading file: {str(e)}'})
        










@blueprint.route('/upload-data', methods=['POST'])
def upload_data():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file uploaded'})

    file = request.files['file']
    try:
        # Initialize ModelService
        model_service = ModelService()

        # Load file into DataFrame
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith('.xlsx'):
            try:
                df = pd.read_excel(file, engine='openpyxl')
            except Exception as e:
                print(f"Excel reading error: {str(e)}")
                return jsonify({'success': False, 'message': 'Error reading Excel file.'})
        else:
            return jsonify({'success': False, 'message': 'Unsupported file type. Upload CSV/XLSX.'})

        # Debug print
        print("Original columns:", df.columns.tolist())

        # Custom column mapping to match model attributes
        column_mapping = {
            'rowid': 'rowID',
            'material': 'material',
            'quantity': 'quantity',
            'musharaka': 'musharaka',
            'profit_rate': 'profit_rate',
            'kibor_rate': 'kibor_rate',
            'kibor_tenure_name': 'kibor_tenure_name',
            'financing_amount': 'financing_amount',
            'tenure': 'tenure',
            'actual_tenure': 'actual_tenure',
            'program': 'program',
            'cos_qty': 'cos_qty',
            'repayment_status': 'repayment_status',
            'remaining_principal_amount': 'remaining_principal_amount',
            'charity_amount': 'charity_amount',
            'district': 'district',
            'business_years': 'business_years',
            'entity_type': 'entity_type',
            'collection_period_days': 'collection_period_days',
            'season': 'season',
            'repayment_days': 'repayment_days',
            'repayment_days_ratio': 'repayment_days_ratio',
            'assissted_tv': 'assisted_tv',
            'previous_transactions': 'previous_transactions',
            'previous_data': 'previous_data',
            'ethic': 'ethic',
            'temperature': 'temperature',
            'gdp': 'gdp',
            'kse100_index': 'kse100_index',
            'exchange_rate': 'exchange_rate',
            'target_variable': 'target_variable'
        }

        # Standardize column names and apply mapping
        df.columns = [col.lower().replace(" ", "_") for col in df.columns]
        
        # Print columns before mapping for debugging
        print("Columns after standardization:", df.columns.tolist())
        
        # Apply mapping
        df = df.rename(columns=column_mapping)
        
        # Print columns after mapping for debugging
        print("Columns after mapping:", df.columns.tolist())

        # Get predictions
        csv_string = df.to_csv(index=False)
        try:
            predictions = model_service.predict(csv_string)
            print(f"Predictions received: {predictions}")
        except Exception as e:
            print(f"Prediction error: {str(e)}")
            return jsonify({'success': False, 'message': f'Error in prediction: {str(e)}'})

        # Prepare records with predictions
        records = df.to_dict('records')
        for record, prediction in zip(records, predictions):
            record['target_variable'] = 'Success' if prediction > 50 else 'Failure'
            record['prediction_percentage'] = float(prediction)
            
            # Convert column types to match model
            for col in record:
                if col in ['quantity', 'actual_tenure', 'cos_qty', 'business_years', 
                          'collection_period_days', 'repayment_days', 'assisted_tv', 
                          'previous_transactions']:
                    record[col] = int(float(record[col])) if record[col] else 0
                elif col in ['musharaka', 'profit_rate', 'kibor_rate', 'financing_amount',
                           'remaining_principal_amount', 'charity_amount', 'repayment_days_ratio',
                           'previous_data', 'ethic', 'temperature', 'gdp', 'kse100_index', 
                           'exchange_rate', 'prediction_percentage']:
                    record[col] = float(record[col]) if record[col] else 0.0

        # Print sample record for debugging
        print("Sample record:", records[0] if records else "No records")

        # Create FinancialMetrics objects
        try:
            objects = [FinancialMetrics(**record) for record in records]
            db.session.bulk_save_objects(objects)
            db.session.commit()
            print(f"Successfully saved {len(objects)} records")
        except Exception as e:
            print(f"Database error: {str(e)}")
            db.session.rollback()
            return jsonify({'success': False, 'message': f'Database error: {str(e)}'})

        return jsonify({
            'success': True,
            'message': f'Successfully processed {len(objects)} records',
            'predictions': predictions
        })

    except Exception as e:
        print(f"General error: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})















def create_or_update_table(columns):
    inspector = inspect(db.engine)

    # Standardize column names
    standardized_columns = [col.lower().replace(" ", "_") for col in columns]

    # Check if the table exists
    if not inspector.has_table('rawdata'):
        # Make all columns nullable by default
        columns_def = [f'"{col}" TEXT NULL' for col in standardized_columns]
        query = text(f"""
            CREATE TABLE rawdata (
                id SERIAL PRIMARY KEY,
                {', '.join(columns_def)}
            )
        """)
        db.session.execute(query)
        db.session.commit()
    else:
        existing_columns = [c['name'] for c in inspector.get_columns('rawdata')]
        for col in standardized_columns:
            if col not in existing_columns:
                # Add new columns as nullable
                query = text(f'ALTER TABLE rawdata ADD COLUMN "{col}" TEXT NULL')
                db.session.execute(query)
        db.session.commit()

    return standardized_columns









@blueprint.route('/tables', methods=['GET'])
@login_required
def tables():
    try:
        # Debug: Print database info
        inspector = inspect(db.engine)
        print("Database URL:", db.engine.url)
        print("Available tables:", inspector.get_table_names())
        
        # Check if table exists
        if not inspector.has_table('FinancialMetrics'):
            print("Table 'FinancialMetrics' not found!")
            return render_template('home/tables.html', 
                                records=[], 
                                columns=[], 
                                error="No predictions available yet",
                                segment='tables')
        
        # Get the query result
        query = text('SELECT * FROM "FinancialMetrics"')
        result = db.session.execute(query)
        
        # Debug: Print first row
        first_row = result.fetchone()
        print("First row:", first_row)
        result = db.session.execute(query)  # Re-execute query after fetchone
        
        # Get column names
        columns = result.keys()
        print("Columns:", columns)
        
        # Convert result to list of dictionaries
        records = [dict(zip(columns, row)) for row in result]
        print(f"Found {len(records)} records")
        
        return render_template('home/tables.html', 
                             records=records,
                             columns=columns,
                             error=None,
                             segment='tables')

    except Exception as e:
        print(f"Error fetching predictions: {str(e)}")
        return render_template('home/tables.html', 
                             records=[],
                             columns=[],
                             error=f"Error fetching data: {str(e)}",
                             segment='tables')