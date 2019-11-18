# Setup

A Facebook clone written with Flask.

1. `git clone git@github.com:PrimeTimeTran/cs-Facebook.git`
2. `cd cs-Facebook`
3. `pip install -r requirements.txt`
4. `python app.py`

## Todo

- [ ] Reactions.
- [ ] Commenting.
- [ ] File upload.

## One to many relationship

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    posts = db.Relationship('Post', backref='user', lazy=True)

    liked_posts = db.relationship('Post', secondary='likes', backref='likers', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

## Many to many relationship

likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
    db.Column('post_id', db.integer, db.ForeignKey('post.id'), primary_key=True)
)
