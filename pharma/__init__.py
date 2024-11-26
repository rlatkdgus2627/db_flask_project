from flask import Blueprint

pharma_bp = Blueprint('pharma', __name__, template_folder='templates')

from . import routes