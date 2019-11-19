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

def create():
    if request.method == 'POST':
        import code; code.interact(local=dict(globals(), **locals()))
        post = Post(image_url = request.form['image_url'], body = request.form['body'], user_id = current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Thank you for your Post!', 'success')
        return redirect(url_for('home'))