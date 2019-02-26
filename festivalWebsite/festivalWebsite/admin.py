import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from festivalWebsite.db import get_db
from festivalWebsite.auth import login_required, admin_only
from festivalWebsite.API.money import depositMoney

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/')
@admin_only
def checkadmin():
    """Display main admin page"""
    return render_template('admin/index.html.j2')

@bp.route('/ATM/', methods=('GET', 'POST'))
@admin_only
def atmProcessor():
    """Show form for uploading ATM files and process them accordingly"""
    message = ""
    if request.method == 'POST':
        db = get_db()
        if 'fileToUpload' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        flash('File uploaded')
        # windows uses \r\n for line endings while linux uses \n for line endings
        # If you strip (remove all) \r and then split on \n you handle both systems at once
        transfers = (request.files['fileToUpload'].read().strip(b'\r').split(b'\n'))[4:]
        for transfer in transfers:
            transfer = transfer.decode("utf-8").split(' ')
            depositMoney(transfer[0], transfer[1])
    return render_template('admin/uploadATMFile.html.j2')

@bp.route('/accounts/')
@admin_only
def listAccounts():
    """List all accounts, sorted by account ID"""
    db = get_db()
    accounts  = db.execute(
        'SELECT * FROM user ORDER BY id'
    ).fetchall()
    return render_template('admin/accounts.html.j2', users=accounts)

@bp.route('/visitors/')
@admin_only
def getVisitors():
    """List all visitor accounts (exclude those which aren't visiting)"""
    db = get_db()
    visitors  = db.execute(
        'SELECT * FROM user WHERE hasFestivalTicket = \'True\' OR hasCampingTicket = \'True\' ORDER BY id'
    ).fetchall()
    return render_template('admin/visitors.html.j2', visitors=visitors)

@bp.route('/camping/')
@admin_only
def getCampingStats():
    """Display camping statistics"""
    db = get_db()
    totals  = db.execute(
        'SELECT COUNT(spotID) as spotsTaken, COUNT(userID) as userCount from camping'
    ).fetchone()
    perCamping  = db.execute(
        'SELECT spotID, COUNT(userID) as peopleOnSpot from camping GROUP BY spotID'
    ).fetchall()
    return render_template('admin/campingStats.html.j2', totals = totals, perCamping = perCamping)


@bp.route('/sales/')
@admin_only
def listSalesInfo():
    """List sales info from all shops"""
    db = get_db()
    sales  = db.execute(
        ''#TODO: get sales info
    ).fetchall()
    return render_template('admin/sales.html.j2', sales=sales)

@bp.route('/sql/', methods=['GET'])
@admin_only
def sqlPage():
    """Display page where SQL queries can be run"""
    return render_template('admin/sql.html.j2')

@bp.route('/sql/', methods=['POST'])
@admin_only
def runSQLQuery():
    """Run a SQL query"""
    db = get_db()
    sql = request.form['sql']
    if sql.upper().startswith("SELECT"):
        cursor = db.execute(sql)
        return jsonify([dict(zip([key[0] for key in cursor.description], row)) for row in cursor.fetchall()])
    elif sql.upper().startswith("UPDATE") or sql.upper().startswith("INSERT"):
        db.execute(sql)
        db.commit()
        flash("Database updated")
        return redirect(url_for("admin.runSQLQuery"))
    else:
        result = db.execute(sql).fetchall()
        db.commit()
        return jsonify([list(x) for x in result]) if result else redirect(url_for("admin.runSQLQuery"))
