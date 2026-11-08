from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import get_db

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['GET', 'POST'])
def feedback_page():
    if not session.get('user_id'):
        flash('Please log in to leave feedback.', 'error')
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        rating = request.form.get('rating', type=int)
        comment = request.form.get('comment', '').strip()
        if rating not in range(1, 6) or not comment:
            flash('Choose a rating and enter your feedback.', 'error')
        else:
            db = get_db()
            db.execute('INSERT INTO feedback (user_id, rating, comment) VALUES (?, ?, ?)',
                       (session['user_id'], rating, comment))
            db.commit()
            db.close()
            flash('Thank you for sharing your feedback!', 'success')
            return redirect(url_for('feedback.feedback_page'))
    return render_template('feedback.html')
