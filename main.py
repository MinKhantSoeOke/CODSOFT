from flask import Flask
from models import db, User
from flask_login import AnonymousUserMixin, LoginManager

app = Flask(__name__, instance_relative_config=False)

app.config.from_pyfile('config.py')
app.debug = True

db.init_app(app)

with app.app_context():
    db.create_all()


class MyAnonymousUser(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Guest'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'views.bp_auth.login'
login_manager.anonymous_user = MyAnonymousUser


@login_manager.user_loader
def load_user(user_id):
    user = db.session.query(User).get(user_id)
    return user


from views import bp_views

app.register_blueprint(bp_views)

if __name__ == '__main__':
    app.run(debug=True)