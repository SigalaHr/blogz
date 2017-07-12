#Worked with Joe Ylagan

from flask import request, redirect, render_template, session, flash
import cgi
from app import app, db
from models import User, Blog
from hashutils import check_pw_hash

def get_blogs():
    return Blog.query.filter_by().all()

def get_users():
    return User.query.filter_by().all()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        username_db_count = User.query.filter_by(username=username).count()
        if len(password) < 3 or len(username) < 3:
            flash("Username and password must be more than 3 characters long")
            return redirect('/signup')
        if username_db_count > 0:
            flash('yikes! "' + username + '" is already taken and password reminders are not implemented')
            return redirect('/signup')
        if password != verify:
            flash('passwords did not match')
            return redirect('/signup')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        session['user'] = user.username
        return redirect("/newblog")
    else:
        return render_template('signup.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = User.query.filter_by(username=username)
        if users.count() == 0:
            flash('username does not exist')
        else:
            user = users.first()
            if user and check_pw_hash(password, user.pw_hash):
                session['user'] = user.username
                flash('welcome back, '+user.username)
                return redirect("/newblog")
        flash('bad password')
        return redirect("/login")

@app.route('/')
def homepage():
    return render_template('index.html', title='blog users', users=get_users())

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    del session['user']
    return redirect("/blog")

@app.route('/newblog', methods=['POST', 'GET'])
def new_blog():
    body_error = ""
    title_error = ""
    blog_title = ""
    blog_body = ""
    owner = User.query.filter_by(username=session['user']).first()
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        if blog_body is not "" and blog_title is not "":
            new_blog_post = Blog(blog_title, blog_body, owner)
            db.session.add(new_blog_post)
            db.session.commit()
            blog_id = new_blog_post.id
            return redirect('/blog?id=' + str(blog_id))
        if blog_body is "":
            body_error = 'Please enter a body'
        else:
            blog_body = blog_body
        if blog_title is "":
            title_error = 'Please enter a title'
        else:
            blog_title = blog_title
    return render_template('newblog.html', title="Create a New Blog",
        body_error=body_error,
        title_error=title_error,
        blog_title=blog_title,
        blog_body=blog_body)

@app.route('/blog', methods=['GET'])
def index():
    user = request.args.get('user')
    if user:
        user = User.query.filter_by(username=user).first()
        blogs = Blog.query.filter_by(owner_id=user.id).all()
        return render_template('singleUser.html', title="blog posts", user=user, blogs=blogs)
    blog_id = request.args.get('id')
    if blog_id is None:
        return redirect('/blog?id=None')
    blog = Blog.query.get(blog_id)
    return render_template('blog.html', title="blog posts", blog=blog, blogs=get_blogs())

nologin = ['login', 'signup', 'index', 'homepage']

@app.before_request
def require_login():
    if not ('user' in session or request.endpoint in nologin):
        return redirect("/login")

if __name__ == "__main__":
    app.run()