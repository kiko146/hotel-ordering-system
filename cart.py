from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import get_db

cart_bp = Blueprint('cart', __name__)

def cart_details():
    cart = session.get('cart', {})
    if not cart:
        return [], 0
    ids = [int(item_id) for item_id in cart]
    placeholders = ','.join('?' for _ in ids)
    db = get_db()
    items = db.execute(f'SELECT * FROM menu_items WHERE id IN ({placeholders})', ids).fetchall()
    db.close()
    rows, total = [], 0
    for item in items:
        quantity = int(cart.get(str(item['id']), 0))
        subtotal = item['price'] * quantity
        rows.append({'item': item, 'quantity': quantity, 'subtotal': subtotal})
        total += subtotal
    return rows, total

@cart_bp.route('/cart')
def view_cart():
    rows, total = cart_details()
    return render_template('cart.html', rows=rows, total=total)

@cart_bp.route('/cart/add/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    db = get_db()
    item = db.execute('SELECT id FROM menu_items WHERE id = ?', (item_id,)).fetchone()
    db.close()
    if not item:
        flash('That menu item could not be found.', 'error')
        return redirect(url_for('menu.menu_page'))
    cart = session.get('cart', {})
    key = str(item_id)
    cart[key] = min(int(cart.get(key, 0)) + 1, 20)
    session['cart'] = cart
    flash('Added to your cart.', 'success')
    return redirect(request.referrer or url_for('menu.menu_page'))

@cart_bp.route('/cart/update/<int:item_id>', methods=['POST'])
def update_cart(item_id):
    quantity = request.form.get('quantity', '1', type=int)
    cart = session.get('cart', {})
    key = str(item_id)
    if quantity <= 0:
        cart.pop(key, None)
    elif key in cart:
        cart[key] = min(quantity, 20)
    session['cart'] = cart
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/cart/remove/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    cart = session.get('cart', {})
    cart.pop(str(item_id), None)
    session['cart'] = cart
    return redirect(url_for('cart.view_cart'))
