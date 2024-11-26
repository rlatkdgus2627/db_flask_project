from flask import Blueprint

patient_bp = Blueprint('doctor', __name__, template_folder='templates')

from . import routes