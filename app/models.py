from app import app, db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

class User(db.Model, UserMixin):
    id =db.Column(db.Integer, primary_key=True)
    bio =db.Column(db.String(150))
    url =db.Column(db.String(150), default="http://placehold.it/250x250")
    username =db.Column(db.String(30), unique=True, index=True)
    email =db.Column(db.String(120), unique=True)
    password_hash =db.Column(db.String(256))
    posts =db.relationship('Post', backref=db.backref('user', lazy='joined'))
    # public = db.Column(db.Boolean)

    # setup methods to set and check password_hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    url =db.Column(db.String(150))
    desc = db.Column(db.String(140))
    date_posted = db.Column(db.DateTime, default=datetime.now().date())


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
