from flask import (
    Blueprint, render_template, request
)

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Display main page"""
    return render_template('info/index.html.j2')
