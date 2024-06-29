from flask import Blueprint, render_template, request, redirect, flash
from flask_login import current_user, login_user, login_required, logout_user
from models import db, User

bp_auth = Blueprint("bp_auth", __name__)


@bp_auth.route("/")
@bp_auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if current_user and current_user.is_authenticated:
            return redirect("/dashboard")

        email = request.form.get('email')
        password = request.form.get('password')

        if email and password:
            user = db.session.query(User).filter_by(email=email).first()
            if user and User.check_password(email, password):
                login_user(user)
                return redirect('/dashboard')
            else:
                flash('Invalid email or password', 'danger')
        else:
            flash('Both email and password are required', 'danger')
    return render_template('/auth/login.html', logged_in=False)


@bp_auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not db.session.query(User).filter_by(email=email).first():
            user = User(username=username, email=email, password=User.create_password(password))
            db.session.add(user)
            db.session.commit()
            flash('User successfully registered!', 'success')
        else:
            flash('User already exists!', 'warning')

        return redirect('/login')
    return render_template('/auth/register.html', logged_in=False)


@bp_auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')