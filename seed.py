"""Seed file to make sample db"""

from models import User, Post, db
from app import app

# Create all tables

db.drop_all()
db.create_all()

CONTENT = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Est velit egestas dui id ornare. Eu facilisis sed odio morbi."

users = [
    User(first_name="Billy", last_name="Bob"),
    User(first_name="Jamie", last_name="Joe"),
    User(first_name="Peggy", last_name="Sue")
]

posts = [
    Post(title="Post 1", content=CONTENT, author=1),
    Post(title="Post 2", content=CONTENT, author=2),
    Post(title="Post 3", content=CONTENT, author=3),
    Post(title="Post 4", content=CONTENT, author=2),
    Post(title="Post 5", content=CONTENT, author=2),
    Post(title="Post 6", content=CONTENT, author=1),
    Post(title="Post 7", content=CONTENT, author=3)
]

db.session.add_all(users)
db.session.commit()

db.session.add_all(posts)
db.session.commit()