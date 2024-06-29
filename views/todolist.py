from flask import Blueprint, render_template, request, flash, redirect
from flask_login import login_required, current_user
from controllers import ToDoListController
from models import db

bp_todolist = Blueprint('bp_todolist', __name__)


@bp_todolist.route('/dashboard', methods=['GET'])
@bp_todolist.route('/todolist', methods=['GET', 'POST'])
@login_required
def todolist():
    tasks = ToDoListController.get_all_todolist()
    return render_template('/todolist/index.html', tasks=tasks, current_user=current_user, logged_in=True)


@bp_todolist.route('/add_new_task', methods=['GET', 'POST'])
@login_required
def add_new_task():
    if request.method == "POST":
        try:
            data = request.form.to_dict()
            status = request.form['status']

            missing_fields = [key for key, value in data.items() if not value]
            if missing_fields:
                flash("All fields are required", 'danger')
                return redirect('/add_new_task')

            result = ToDoListController.add_new_task(data['title'], data['description'], status, data['priority'])

            if result is True:
                return redirect('/todolist')
            else:
                flash(f'{result}', 'danger')
        except Exception as e:
            flash(f'{e}', 'danger')

    return render_template('/todolist/add_new_task.html', current_user=current_user, logged_in=True)


@bp_todolist.route('edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    status = ['not started', 'in process', 'done']
    task = ToDoListController.get_todolist(task_id)
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            status = request.form['status']

            if 'title' in data:
                task.title = data['title']
            if 'description' in data:
                task.description = data['description']
            if 'priority' in data:
                task.priority = data['priority']
            if status:
                task.status = status

            db.session.commit()
            return redirect('/todolist')

        except Exception as e:
            flash(f'{e}', 'danger')
    return render_template('/todolist/edit_task.html', task=task, status=status, current_user=current_user, logged_in=True)


@bp_todolist.route('/delete_task/<int:task_id>', methods=['GET'])
@login_required
def delete_task(task_id):
    task = ToDoListController.get_todolist(task_id)

    if task:
        if task.user_id == current_user.id:
            result = ToDoListController.delete_task(task)
            if result is not True:
                flash(f'{result}', 'danger')
        else:
            flash('User is not authenticated to delete!', 'danger')
    else:
        flash('There is no task!', 'danger')
    return redirect('/todolist')
