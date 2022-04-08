from unittest import TestCase

from app import app
from models import db, User, Post, Tag, PostTag, default_image_url

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class BloglyUserViewsTestCase(TestCase):
    """Tests for views for Blogly users"""

    def setUp(self):
        """Add sample user and post."""

        PostTag.query.delete()
        Post.query.delete()
        Tag.query.delete()
        User.query.delete()

        user = User(first_name="Test", last_name="User")

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

        post = Post(title="Test Post", content="content", author=f"{self.user_id}")

        db.session.add(post)
        db.session.commit()

        self.post_id = post.id
        self.post = post

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            """Test users list view"""

            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User', html)

    def test_user_details(self):
        with app.test_client() as client:
            """Test user details view"""

            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test User</h1>', html)
            self.assertIn('Test Post', html)
            self.assertIn('Edit', html)

    def test_add_user(self):
        with app.test_client() as client:
            """Test adding new user view"""

            d = {"first_name": "Test2", "last_name": "User2", "image_url": default_image_url}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test2 User2", html)

    def test_edit_user(self):
        """Test edit user view"""

        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit a User', html)
            self.assertIn('<form', html)

class BloglyPostViewsTestCase(TestCase):
    """Test for views for Blogly posts"""

    def setUp(self):
        """Add sample post and user"""

        PostTag.query.delete()
        Post.query.delete()
        Tag.query.delete()
        User.query.delete()

        user = User(first_name="Test", last_name="User")

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

        post = Post(title="Test Post", content="content", author=f"{self.user_id}")

        db.session.add(post)
        db.session.commit()

        self.post_id = post.id
        self.created_at = post.write_date
        self.post = post

    def tearDown(self):
        """Clean up any fouled transactions"""

        db.session.rollback()

    def test_user_posts(self):
        """Test user views for posts"""

        with app.test_client() as client:
            resp = client.get(f'/users/{self.user.id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Post', html)
            self.assertIn('Add post', html)
    
    def test_post_details(self):
        """Test Post properties on post details view"""

        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('By Test User', html)
            self.assertIn(f'Posted {self.created_at}', html)
            self.assertIn('Edit', html)

    def test_add_post(self):
        """Test adding new post"""

        with app.test_client() as client:

            d = {"title": "Post 2", "content": "more content", "author": f"{self.user_id}"}

            resp = client.post(f"/users/{self.user_id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Post 2", html)
            self.assertIn('Test User', html)

    def test_edit_post(self):
        """Test edit post form view"""

        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit Post', html)
            self.assertIn('Test Post', html)

class BloglyTagViewsTestCase(TestCase):
    """Test for views for Blogly posts"""

    def setUp(self):
        """Add sample post and user"""

        PostTag.query.delete()
        Post.query.delete()
        Tag.query.delete()
        User.query.delete()

        db.session.commit()

        user = User(first_name="Test", last_name="User")

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

        tag = Tag(name="cool")

        db.session.add(tag)
        db.session.commit()

        self.tag_id = tag.id
        self.tags = tag

        post = Post(title="Test Post", content="content", author=f"{self.user_id}")

        db.session.add(post)
        db.session.commit()

        self.post_id = post.id
        self.created_at = post.write_date
        self.post = post

        post_tag = PostTag(post_id=self.post_id, tag_id=self.tag_id)

        db.session.add(post_tag)
        db.session.commit()

        self.post_tag = post_tag

    def tearDown(self):
        """Clean up any fouled transactions"""

        db.session.rollback()

    def test_show_tags(self):
        """Test tag appears on tags list"""

        with app.test_client() as client:
            resp = client.get('/tags')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('cool', html)

    def test_add_tag_form(self):
        """Test view form to add tag"""

        with app.test_client() as client:
            resp = client.get('/tags/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Create a Tag', html)
            self.assertIn('Add', html)

    def test_add_tag(self):
        """Test adding new tag to db"""

        with app.test_client() as client:

            d = {"name": "test tag"}
            resp = client.post("/tags/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test tag', html)

    