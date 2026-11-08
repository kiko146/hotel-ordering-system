from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        if not name or not email or len(password) < 8:
            flash('Enter all details. Your password must be at least 8 characters.', 'error')
            return render_template('register.html')
        db = get_db()
        try:
            cursor = db.execute('INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
                                (name, email, generate_password_hash(password)))
            db.commit()
            session['user_id'] = cursor.lastrowid
            session['user_name'] = name
            flash('Your account has been created. Welcome!', 'success')
            return redirect(url_for('home'))
        except Exception:
            flash('That email may already be registered. Try logging in.', 'error')
        finally:
            db.close()
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        db.close()
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            flash('Welcome back!', 'success')
            return redirect(url_for('home'))
        flash('Incorrect email or password.', 'error')
    return render_template('login.html')
