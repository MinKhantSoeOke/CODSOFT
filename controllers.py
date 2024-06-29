from models import db, ToDoList, ContactBook
from flask_login import current_user
from sqlalchemy import asc


class ToDoListController:
    @staticmethod
    def get_all_todolist():
        return db.session.query(ToDoList).filter_by(user_id=current_user.id).all()

    @staticmethod
    def get_todolist(task_id):
        return db.session.query(ToDoList).filter_by(id=task_id).first()

    @staticmethod
    def add_new_task(title, description, status, priority):
        try:
            new_task = ToDoList(user_id=current_user.id, title=title, description=description, status=status, priority=priority)
            db.session.add(new_task)
            db.session.commit()
            return True
        except Exception as e:
            return e

    @staticmethod
    def delete_task(task):
        try:
            db.session.delete(task)
            db.session.commit()
            return True
        except Exception as e:
            return e


class ContactBookController:
    @staticmethod
    def get_all_contacts(user_id):
        return db.session.query(ContactBook).filter_by(user_id=user_id).order_by(asc(ContactBook.name)).all()

    @staticmethod
    def get_contact_by_contact_id(contact_id):
        return db.session.query(ContactBook).filter_by(id=contact_id).first()

    @staticmethod
    def get_contact_by_name(name):
        return db.session.query(ContactBook).filter_by(name=name).first()

    @staticmethod
    def get_contact_by_phone(phone):
        return db.session.query(ContactBook).filter_by(phone=phone).first()

    @staticmethod
    def add_new_contact(name, phone, email, address):
        try:
            new_contact = ContactBook(user_id=current_user.id, name=name, phone=phone, email=email, address=address)
            db.session.add(new_contact)
            db.session.commit()
            return True
        except Exception as e:
            return e

    @staticmethod
    def delete_contact(contact):
        try:
            db.session.delete(contact)
            db.session.commit()
            return True
        except Exception as e:
            return e
