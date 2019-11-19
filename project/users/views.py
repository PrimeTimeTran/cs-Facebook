from flask import render_template, flash, request, url_for, Blueprint, redirect
from flask_login import logout_user, login_user, current_user

from project.models import User

users_blueprint = Blueprint(
    'users',
    __name__,
    template_folder='templates'
)

@users_blueprint.route('/', methods=['POST'])
def create():
    print('Creating a user KHOA')
    user = User.query.filter_by(email = request.form['email']).first()
    if user:
        if user.check_password(request.form['password']):
            login_user(user)
            flash('Welcome back {0}~!'.format(current_user.email), 'info')
            return redirect(url_for('home'))
        else: 
            flash('Incorrect password', 'info')
            return redirect(url_for('home'))
    else:
        if request.method == 'POST':
            user = User(email = request.form['email'], avatar_url = request.form['avatar_url'])
            user.set_password(request.form['password'])
            flash('Successfully signed up!', 'success')
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('home'))

@users_blueprint.route('/logout')
def logout():
    # flash('Logged out {0}!'.format(current_user.email), 'info')
    logout_user()
    return render_template('/views/root.html')