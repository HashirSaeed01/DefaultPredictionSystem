from flask_migrate import Migrate
from apps.home import blueprint
from flask import render_template, request, redirect, url_for
from flask_login import login_required
from jinja2 import TemplateNotFound
from sqlalchemy import text
from apps import db

from flask import jsonify, current_app
from apps.home import blueprint

@blueprint.route('/db-info')
def db_info():
    return jsonify({
        'database_type': current_app.config['DATABASE_TYPE'],
        'database_url': current_app.config['SQLALCHEMY_DATABASE_URI'],
        'connected': True
    })





# @blueprint.route('/index')
@blueprint.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    print("=== DEBUG: Index Route Started ===")
    print(f"URL Parameters: {request.args}")
    
    # If no URL parameters, try to get the latest record
    if not request.args:
        print("No URL parameters, attempting to fetch latest record")
        try:
            query = text('SELECT * FROM "FinancialMetrics" ORDER BY id DESC LIMIT 1')
            print(f"Executing query: {query}")
            
            result = db.session.execute(query)
            latest_record = result.fetchone()
            
            print(f"Query result: {latest_record}")
            
            if latest_record:
                columns = result.keys()
                record_dict = dict(zip(columns, latest_record))
                print(f"Converted to dict: {record_dict}")
                
                return render_template('home/index.html', 
                    segment='index',
                    data=record_dict
                )
            else:
                print("No records found in database")
                
        except Exception as e:
            print(f"ERROR in database query: {str(e)}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
    
    print("Rendering template with default values")
    return render_template('home/index.html', segment='index')








@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
