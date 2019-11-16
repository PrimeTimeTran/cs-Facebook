from flask import Flask, render_template, request, redirect, url_for, flash
import os
from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin, LoginManager, logout_user, login_user, current_user, login_required

from werkzeug.security import generate_password_hash, check_password_hash
import enum
from flask_moment import Moment

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']      
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = 'Secret'

moment = Moment()
moment.init_app(app)
login_manager = LoginManager(app)
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    avatar_url = db.Column(db.Text)

    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    image_url = db.Column(db.Text)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)
    body = db.Column(db.Text)
    image_url = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

# class ReactionEnum(enum.Enum):
#     liked = 'liked'
#     laughed = 'laughed'
#     wowed = 'wowed'
#     frowned = 'frowned'
#     loved = 'loved'

# class Reaction(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer)
#     post_id = db.Column(db.Integer)
#     reaction_type = db.Column(
#         db.Enum(ReactionEnum), 
#         default=ReactionEnum.liked,
#         nullable=False
#     )

db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def home():
    if request.args.get('filter') == 'most-recent':
        posts = Post.query.order_by(Post.created_at.desc()).all()
    else: 
        posts = Post.query.all()
    for post in posts:
        user = User.query.get(post.user_id)
        post.avatar_url = user.avatar_url
        post.username = user.email
    return render_template('/views/root.html', posts = posts)

@app.route('/users', methods=['POST'])
def create_user():
    user = User.query.filter_by(email = request.form['email']).first()
    if user:
        print('found')
        if user.check_password(request.form['password']):
            return redirect(url_for('home'))
        else: 
            flash('Incorrect password', 'info')
            return redirect(url_for('home'))
    else:
        if request.method == 'POST':
            user = User(email = request.form['email'], avatar_url = request.form['avatar_url'])
            user.set_password(request.form['password'])
            flash('Successfully signed up!', 'success')
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('home'))

@app.route('/logout')
def logout():
    flash('Logged out {0}!'.format(current_user.email), 'info')
    logout_user()
    return render_template('/views/root.html')

@app.route('/posts', methods=['POST'])
def create_post():
    if request.method == 'POST':
        post = Post(image_url = request.form['image_url'], body = request.form['body'], user_id = current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Thank you for your Post!', 'success')
        return redirect(url_for('home'))

@app.route('/posts/<id>')
def view_post(id):
    post = Post.query.get(id)
    user = User.query.get(post.user_id)
    post.avatar_url = user.avatar_url
    post.username = user.email
    comments = Comment.query.filter_by(post_id = post.id).all()
    for comment in comments:
        user = User.query.get(comment.user_id)
        comment.username = user.email
        comment.avatar_url = user.avatar_url
    return render_template('/views/post.html', post = post, comments = comments)

@app.route('/posts/<id>/comments', methods=["POST"])
def create_comment(id):
    comment = Comment(user_id = current_user.id, post_id = id, image_url = request.form['image_url'], body = request.form['body'])
    db.session.add(comment)
    db.session.commit()
    flash('Thank you for your comment', 'success')
    return redirect(url_for('view_post', id=id))

@app.route('/posts/<id>', methods=["POST"])
def edit_post(id):
    post = Post.query.get(id)
    post.body = request.form['body']
    post.image_url = request.form['image_url']
    db.session.commit()
    return redirect(url_for('view_post', id=id))

if __name__ == "__main__":
    # app.run(debug = True)
    app.run()