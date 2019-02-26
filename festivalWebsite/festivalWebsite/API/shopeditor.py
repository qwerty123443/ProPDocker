import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from festivalWebsite.db import get_db
from festivalWebsite.auth import login_required, admin_only

bp = Blueprint('shopeditor', __name__, url_prefix='/admin/shopeditor')

@bp.route('/', methods=['GET'])
@admin_only
def shopeditor():
    """Display shop editor page"""
    db = get_db()
    shops  = db.execute(
        'SELECT * FROM shop'
    ).fetchall()
    return render_template('admin/shopeditor.html.j2', shops=shops)

@bp.route('/', methods=['POST'])
@admin_only
def addShop():
    """Add a shop to the database. No input validation is done"""
    db = get_db()
    db.execute(
        'INSERT INTO shop (shopName, ownerID) VALUES (?, ?)', (request.form['ShopName'], g.user['id'])
    )
    db.commit()
    return redirect(url_for('shopeditor.shopeditor'))

@bp.route('/<int:shopID>/')
@admin_only
def getShopByID(shopID):
    """Get a shop and the products that shop offers by shop ID

    :param shopID: id of the shop to display
    """
    db = get_db()
    shop  = db.execute(
        'SELECT * FROM shop WHERE shopID = ?', (shopID,)
    ).fetchone()
    items = db.execute(
        'SELECT * FROM product WHERE shopID = ?', (shopID,)
    ).fetchall()
    return render_template('admin/shopDetails.html.j2', shop=shop, items=items)

@bp.route('/<string:shopName>/')
@admin_only
def getShopsByName(shopName):
    """Get a shop (or shops) by its name.
    Automatically goes to the details page if only one shop is found.

    :param shopName: name of the shop(s) to search for
    """
    db = get_db()
    shops  = db.execute(
        'SELECT * FROM shop WHERE shopName LIKE ?', ('%'+shopName+'%',)
    ).fetchall()

    if len(shops) == 1:
         return render_template('admin/shopDetails.html.j2', shop=shops[0])
    else:
        return render_template('admin/shopeditor.html.j2', shops=shops)

@bp.route('/<int:shopID>/remove')
@admin_only
def removeShop(shopID):
    """Remove a shop by its shop ID

    :param shopID: id of the shop to remove
    """
    db = get_db()
    db.execute(
        'DELETE FROM shop WHERE shopID = ?', (shopID,)
    )
    db.execute(
        'DELETE FROM product WHERE shopID = ?', (shopID,)
    )
    db.commit()
    return redirect(url_for('shopeditor.shopeditor'))

@bp.route('/<int:shopID>/<int:productID>/edit', methods=['POST'])
@admin_only
def editProduct(shopID, productID):
    """Edit a product for a specific shop ID and product ID

    :param shopID: id of the shop to edit the item from
    :param productID: id of the item to edit"""
    db = get_db()
    accounts  = db.execute(
        #TODO: update product table with correct info
        #TODO: WHERE clause
        'UPDATE product SET shopID = ?, name = ?, description = ?, price = ?', (shopID, request.form['ItemName'], request.form['ItemDescription'], request.form['ItemPrice'],)
    )
    db.commit()
    return redirect(url_for('shopeditor.getShopByID', shopID=shopID))

@bp.route('/<int:shopID>/add', methods=['POST'])
@admin_only
def addProduct(shopID):
    """Add a product to a shop by shopID

    :param shopID: id of the shop to add
    """
    db = get_db()
    db.execute(
        'INSERT INTO product (shopID, name, description, price) VALUES (?, ?, ?, ?)', (shopID, request.form['ItemName'], request.form['ItemDescription'], request.form['ItemPrice'],)
    )
    db.commit()
    return redirect(url_for('shopeditor.getShopByID', shopID=shopID))

@bp.route('/<int:shopID>/<int:productID>/delete', methods=['POST'])
@admin_only
def removeProduct(shopID, productID):
    """Remove a product from the shop

    :param shopID: id of the shop to remove the item from
    :param productID: id of the item to remove"""
    db = get_db()
    accounts  = db.execute(
        'DROP FROM product where shopID = ? and productID = ?', (shopID, productID,)
    )
    return redirect(url_for('shopeditor.getShopByID', shopID=shopID))
