from flask import Flask, render_template, session, redirect, url_for, flash
from database import init_db
from auth import auth_bp
from menu import menu_bp
from cart import cart_bp
from checkout import checkout_bp
from feedback import feedback_bp
from header import inject_header_data
from footer import inject_footer_data

app = Flask(__name__)
import os
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['DATABASE'] = 'database/hotel.db'

init_db(app.config['DATABASE'])
app.register_blueprint(auth_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(checkout_bp)
app.register_blueprint(feedback_bp)
app.context_processor(inject_header_data)
app.context_processor(inject_footer_data)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/customer-service')
def customer_service():
    return render_template('customer_service.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
