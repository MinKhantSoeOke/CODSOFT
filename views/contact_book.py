from flask import Blueprint, render_template, request, flash, redirect
from flask_login import login_required, current_user
from controllers import ContactBookController
from models import db

bp_cb = Blueprint('bp_cb', __name__)


@bp_cb.route('/contact_book', methods=['GET'])
@login_required
def contact_book():
    contacts = ContactBookController.get_all_contacts(current_user.id)
    return render_template('/contact_book/index.html', contacts=contacts, current_user=current_user, logged_in=True)


@bp_cb.route('/add_new_contact', methods=['GET', 'POST'])
@login_required
def add_new_contact():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()

            missing_fields = [key for key, value in data.items() if not value]
            if missing_fields:
                flash("All fields are required", 'danger')
                return redirect('/add_new_contact')

            result = ContactBookController.add_new_contact(data['name'], data['phone'], data['email'], data['address'])

            if result is True:
                return redirect('/contact_book')
            else:
                flash(f'{result}', 'danger')

        except Exception as e:
            flash(f'{e}', 'danger')

    return render_template('/contact_book/add_new_contact.html', current_user=current_user, logged_in=True)


@bp_cb.route('update_contact/<int:contact_id>', methods=['GET', 'POST'])
@login_required
def edit_task(contact_id):
    contact = ContactBookController.get_contact_by_contact_id(contact_id)
    if request.method == 'POST':
        try:
            data = request.form.to_dict()

            if 'name' in data:
                contact.name = data['name']
            if 'phone' in data:
                contact.phone = data['phone']
            if 'email' in data:
                contact.email = data['email']
            if 'address' in data:
                contact.address = data['address']

            db.session.commit()
            return redirect('/contact_book')

        except Exception as e:
            flash(f'{e}', 'danger')
    return render_template('/contact_book/update_contact.html', contact=contact, current_user=current_user, logged_in=True)


@bp_cb.route('/delete_contact/<int:contact_id>', methods=['GET'])
@login_required
def delete_task(contact_id):
    contact = ContactBookController.get_contact_by_contact_id(contact_id)

    if contact:
        if contact.user_id == current_user.id:
            result = ContactBookController.delete_contact(contact)
            if result is not True:
                flash(f'{result}', 'danger')
        else:
            flash('User is not authenticated to delete!', 'danger')
    else:
        flash('There is no contact!', 'danger')
    return redirect('/contact_book')


@bp_cb.route('/search', methods=['GET'])
@login_required
def search_contact():
    if request.method == 'GET':
        search_query = request.args.get('search')
        search_type = request.args.get('search_type')

        if search_type == 'name':
            contact = ContactBookController.get_contact_by_name(search_query)
            if contact is not None:
                return redirect(f'/update_contact/{contact.id}')
            else:
                flash("There is no user with provided name!", "danger")
        elif search_type == 'phone':
            contact = ContactBookController.get_contact_by_phone(search_query)
            if contact is not None:
                return redirect(f'/update_contact/{contact.id}')
            else:
                flash("There is no user with provided phone!", "danger")

    return redirect('/contact_book')