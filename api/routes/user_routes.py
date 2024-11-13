from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, current_user, logout_user
from api.models.user import User, Photo
from api import db

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect(url_for('user.register'))
        
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('user.profile'))
    return render_template('register.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('user.profile'))
        
        flash('Invalid username or password')
        return redirect(url_for('user.login'))
    return render_template('login.html')

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))

@user_bp.route('/profile')
@login_required
def profile():
    current_user.reset_daily_hearts()
    return render_template('profile.html', user=current_user)

@user_bp.route('/upload', methods=['POST'])
@login_required
def upload():
    if current_user.daily_hearts > 0:
        current_user.daily_hearts -= 1
        new_photo = Photo(user_id=current_user.id)
        db.session.add(new_photo)
        db.session.commit()
        flash('Photo uploaded successfully!')
    else:
        flash('No daily hearts left today.')
    return redirect(url_for('user.profile'))
