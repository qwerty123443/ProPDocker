from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from festivalWebsite.db import get_db
from festivalWebsite.auth import admin_only, login_required

bp = Blueprint('moneyAPI', __name__, url_prefix='/API/balance')

@bp.route('/deposit/<int:userID>/<int:amount>/', methods=['GET'])
@admin_only
def depositMoney(userID, amount):
    """Deposit money to a user with a certain user ID

    :param userID: id of the user
    :param amount: amount of money to add"""
    db = get_db()
    db.execute(
        'UPDATE user SET balance = balance + ? WHERE id = ?', (amount, userID,)
    )
    db.commit()
    return jsonify({'success': True})

@bp.route('/check/<int:userID>/', methods=['GET'])
def checkBalance(userID):
    """Check balance of a user with a certain user ID

    :param userID: id of the user"""
    db = get_db()
    balance = db.execute(
        'SELECT * FROM user WHERE id = ?', (userID,)
    ).fetchone()
    return jsonify(None) if not balance else jsonify({'id':balance['id'], 'balance':balance['balance']})
