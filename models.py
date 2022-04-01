"""Models for Blogly."""
from crypt import methods
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

default_image_url = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"

class User(db.Model):
    __tablename__ = "users"

    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>"


    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    first_name = db.Column(db.Text, nullable=False)

    last_name = db.Column(db.Text, nullable=False)

    image_url = db.Column(db.Text,
                            nullable=False,
                            default=default_image_url)

    posts = db.relationship('Post', cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return full user name"""
        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    """Post model"""

    __tablename__ = 'posts'

    def __repr__(self):
        p = self
        return f"<title={p.title} content={p.content} created_at={p.created_at} author={p.author}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.Text, nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=f"{datetime.now()}")

    author = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User')

    @property
    def author_name(self):
        """Show author name"""
        user = User.query.get_or_404(self.author)
        return f"{user.first_name} {user.last_name}"

    @property 
    def write_date(self):
        """Returns string from date and time"""
        dt = self.created_at
        d = dt.strftime("%B %d, %Y")
        t = dt.strftime("%-I:%M%p")
        return f"{d} at {t}"