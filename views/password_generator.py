from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import string
import random

bp_pw = Blueprint('bp_pw', __name__)


@bp_pw.route('/password_generator', methods=['GET'])
@login_required
def password_generator():
    return render_template('/password_generator/index.html', current_user=current_user, logged_in=True)


@bp_pw.route('/generate', methods=['POST'])
@login_required
def generate_password():
    if request.method == 'POST':
        length = int(request.form['length'])

        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digit = string.digits
        special = string.punctuation

        all_characters = lowercase + uppercase + digit + special

        password = []

        password += [random.choice(all_characters) for _ in range(length)]

        random.shuffle(password)

        password = ''.join(password)

        return render_template('/password_generator/index.html', password=password, current_user=current_user, logged_in=True)