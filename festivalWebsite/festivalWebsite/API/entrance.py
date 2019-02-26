from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from festivalWebsite.db import get_db
from festivalWebsite.auth import admin_only, login_required

bp = Blueprint('entranceAPI', __name__, url_prefix='/API/enter')

@bp.route('/festival/<int:userID>', methods=['GET'])
@admin_only
def canEnterFestival(userID):
    """Check if user can enter the festival

    :param userID: id of the user"""
    db = get_db()
    user = db.execute(
        'SELECT * FROM user WHERE id = ?', (userID,)
    ).fetchone()

    if user is not None and user['canEnterFestival'] == 'True':
        return jsonify({'canEnter': True})
    return jsonify({'canEnter': False})

@bp.route('/camping/<int:userID>', methods=['GET'])
@admin_only
def canEnterCamping(userID):
    """Check if user can enter the camping

    :param userID: id of the user"""
    db = get_db()
    user = db.execute(
        'SELECT * FROM user WHERE id = ?', (userID,)
    ).fetchone()

    if user is not None and user['canEnterCamping'] == 'True':
        return jsonify({'canEnter': True})
    return jsonify({'canEnter': False})

@bp.route('/festival/<int:userID>', methods=['POST'])
@admin_only
def checkInFestival(userID):
    """Check in user to the festival

    :param userID: id of the user"""
    db = get_db()
    if db.execute('SELECT hasFestivalTicket FROM user WHERE id = ?', (userID,)).fetchone()['hasFestivalTicket'] == 'False':
        return jsonify({'success': False, 'reason': 'User has no festival ticket'})
    db.execute(
        'UPDATE user festivalCheckintime = CURRENT_TIMESTAMP WHERE id = ? ', (userID,)
    )
    db.commit()
    return jsonify({'success': True})


@bp.route('/camping/<int:userID>', methods=['POST'])
@admin_only
def checkInCamping(userID):
    """Check in user to camping

    :param userID: id of the user"""
    db = get_db()
    if db.execute('SELECT hasCampingTicket FROM user WHERE id = ?', (userID,)).fetchone()['hasCampingTicket'] == 'False':
        return jsonify({'success': False, 'reason': 'User has no camping ticket'})
    db.execute(
        'UPDATE user campingCheckintime = CURRENT_TIMESTAMP WHERE id = ? ', (userID,)
    )
    db.commit()
    return jsonify({'success': True})
