from flask import Blueprint

bp_views = Blueprint("views", __name__)

from . import auth

bp_views.register_blueprint(auth.bp_auth, url_prefix="/")

from . import todolist

bp_views.register_blueprint(todolist.bp_todolist, url_prefix='/')

from . import calculator

bp_views.register_blueprint(calculator.bp_calculator, url_prefix='/')

from . import password_generator

bp_views.register_blueprint(password_generator.bp_pw, url_prefix='/')

from . import game

bp_views.register_blueprint(game.bp_game, url_prefix='/')

from . import contact_book

bp_views.register_blueprint(contact_book.bp_cb, url_prefix='/')
