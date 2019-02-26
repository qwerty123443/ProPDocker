from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from festivalWebsite.db import get_db
from festivalWebsite.API.money import checkBalance
bp = Blueprint('shop', __name__, url_prefix='/shop')

"""a"""


"""
functions to make:
buy items
    - check balance
    - authentication
separate on-site and off-line transactions?
    --> partly, maybe make an API and make use of that
    --> authentication?
"""
