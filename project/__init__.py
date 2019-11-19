from flask import Flask, render_template, request, redirect, url_for, flash
import os
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager, logout_user, login_user, current_user, login_required

import enum
from flask_moment import Moment

app = Flask(__name__)
db = SQLAlchemy(app)

POSTGRES = {
    'port': 5432,
    'pw': 'millions',
    'db': 'flask-fb',
    'host': 'localhost',    
    'user': 'primetimetran',
}


# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:\
%(port)s/%(db)s' % POSTGRES

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = 'My super secret secret'
moment = Moment()
moment.init_app(app)

#set up flask migration
migrate = Migrate(app,db)

login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

from project.models import Post, User, Comment

from project.users.views import users_blueprint

app.register_blueprint(users_blueprint)

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

@app.route('/posts', methods=['POST'])
def create_post():
    if request.method == 'POST':
        import code; code.interact(local=dict(globals(), **locals()))
        post = Post(image_url = request.form['image_url'], body = request.form['body'], user_id = current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Thank you for your Post!', 'success')
        return redirect(url_for('home'))

@app.route('/posts/<id>')
def view_post(id):
    post = Post.query.get(id)
    post.view_count +=1
    db.session.commit()
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


@app.route('/likes', methods=['POST'])
@login_required
def create_like():
    like = Like(type=1)
    current_user.likes.append(like)
    post.likes
