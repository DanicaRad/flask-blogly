"""Blogly application."""

from pydoc import render_doc
from flask import Flask, request, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "nigel"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def show_home():
    """redirects to users list"""
    posts = Post.query.order_by(Post.id.desc()).limit(5)
    return render_template('all-posts.html', posts=posts)

################ USERS ROUTES ###############################

@app.route('/users')
def show_users():
    """Shows list of all users in db"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def show_form():
    """shows form to add new user"""
    return render_template('new-user.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    """Create new user and add to db"""

    new_user = User(first_name=request.form["first_name"], 
                last_name=request.form["last_name"], 
                image_url=request.form["image_url"] or None)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details for single user"""

    user = User.query.get_or_404(user_id)
    return render_template('user-details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    """Show form to edit user"""

    user = User.query.get_or_404(user_id)
    return render_template('edit-user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Handle form submission for updating user details"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Deletes a user from the db"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """Show form to add new post"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('/new-post.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """Handle form submission for creating a new post"""

    new_post = Post(title=request.form['title'],
                    content=request.form['content'], 
                    author=user_id
                    )
    tags = request.form.getlist('tag_id')

    db.session.add(new_post)
    db.session.commit()

    for tag in tags:
        db.session.add(PostTag(post_id=new_post.id, tag_id=tag))
    db.session.commit()

    return redirect(f'/users/{user_id}')

################ POSTS ROUTES ###############################

@app.route('/posts')
def show_all_posts():
    """Shows all posts"""

    posts = Post.query.order_by(Post.created_at).all()

    return render_template('posts.html', posts=posts)
    

@app.route('/posts/<int:post_id>')
def view_post(post_id):
    """Show post details"""

    post = Post.query.get_or_404(post_id)
    return render_template('post-details.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Shows form to edit post"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.order_by(Tag.name).all()

    return render_template('edit-post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """Handle form submission to edit post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    tag_ids = [int(id) for id in request.form.getlist('tag_id')]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Deletes post from db"""

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect('/users')

################ TAGS ROUTES ###############################

@app.route('/tags')
def show_all_tags():
    """Shows list of all tags"""

    tags = Tag.query.order_by(Tag.name).all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    """Show details about tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag-details.html', tag=tag)

@app.route('/tags/new')
def show_new_tag_form():
    """Shows form to add new tag"""

    return render_template('new-tag.html')

@app.route('/tags/new', methods=['POST'])
def add_new_tag():
    """Handle form submission to add new tag to db"""

    tag = Tag(name=request.form['name'])
    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    """Show form to edit tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit-tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def update_tag(tag_id):
    """Handle form submission to edit tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')