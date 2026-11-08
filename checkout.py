from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import get_db
from cart import cart_details

checkout_bp = Blueprint('checkout', __name__)

@checkout_bp.route('/checkout', methods=['GET', 'POST'])
def checkout_page():
    if not session.get('user_id'):
        flash('Please log in before checking out.', 'error')
        return redirect(url_for('auth.login'))
    rows, total = cart_details()
    if not rows:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('menu.menu_page'))
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        payment_method = request.form.get('payment_method', 'Cash on delivery')
        if not customer_name or not phone or not address:
            flash('Please complete your delivery details.', 'error')
            return render_template('checkout.html', rows=rows, total=total)
        if payment_method not in ['Cash on delivery', 'Demo payment']:
            flash('Please choose an available payment method.', 'error')
            return render_template('checkout.html', rows=rows, total=total)
        db = get_db()
        cursor = db.execute('''INSERT INTO orders
            (user_id, customer_name, phone, delivery_address, total, payment_method)
            VALUES (?, ?, ?, ?, ?, ?)''',
            (session['user_id'], customer_name, phone, address, total, payment_method))
        order_id = cursor.lastrowid
        for row in rows:
            item = row['item']
            db.execute('INSERT INTO order_items (order_id, item_name, quantity, unit_price) VALUES (?, ?, ?, ?)',
                       (order_id, item['name'], row['quantity'], item['price']))
        db.commit()
        db.close()
        session['cart'] = {}
        return render_template('order_success.html', order_id=order_id)
    return render_template('checkout.html', rows=rows, total=total)
