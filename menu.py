from flask import Blueprint, render_template, request
from database import get_db

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/menu')
def menu_page():
    category = request.args.get('category', 'All')
    db = get_db()
    if category == 'All':
        items = db.execute('SELECT * FROM menu_items ORDER BY category, name').fetchall()
    else:
        items = db.execute('SELECT * FROM menu_items WHERE category = ? ORDER BY name', (category,)).fetchall()
    db.close()
    categories = ['All', 'Breakfast', 'Lunch', 'Dinner', 'Drinks', 'Dessert']
    return render_template('menu.html', items=items, categories=categories, selected_category=category)
