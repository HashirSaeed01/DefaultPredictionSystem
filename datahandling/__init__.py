from flask import Blueprint

blueprint = Blueprint(
    'datahandling_blueprint',
    __name__,
    url_prefix='/data'
)
# No more 'from apps.datahandling import routes'