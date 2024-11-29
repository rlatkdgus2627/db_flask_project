from flask import Blueprint

pharma_bp = Blueprint('pharma', __name__, url_prefix='/pharma')

from . import routes