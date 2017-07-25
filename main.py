#!/usr/bin/env python

__author__ = "student"
__version__ = "1.0"
# July 2017
# Flask Blog App Continued re: LaunchCode lc-101
# Rubric: http://education.launchcode.org/web-fundamentals/assignments/blogz/


from flask import request, redirect, render_template, session, flash
from app import app, db
from models import User, Blog
from hashutils import check_password_hash


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

        if (len(password) < 3) or (len(username) < 3):
            flash("Username and password must be more than 3 characters long", "error")
            return redirect('/signup')
        elif username_db_count > 0:
            flash('yikes! "' + username + '" is already taken and password reminders are not implemented', "error")
            return redirect('/signup')
        elif password != verify:
            flash('passwords did not match', "error")
            return redirect('/signup')

        user = User(username, password)
        db.session.add(user)
        db.session.commit()

        flash('account created', 'error')
        session['user'] = user.username
        return redirect("/newblog")

    return render_template('signup.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if not user:
            flash('username does not exist', 'error')
        elif user and check_password_hash(password, user.pw_hash):
            session['user'] = user.username
            flash('welcome back, ' + user.username, 'error')
            return redirect("/newblog")
        else:
            flash('bad password', 'error')
            return redirect("/login")

    return render_template('login.html')


@app.route('/')
def homepage():
    return render_template('index.html', title='blog users', users=get_users())


@app.route("/logout")
def logout():
    del session['user']
    flash('logging out', 'error')
    return redirect("/blog")


@app.route('/newblog', methods=['POST', 'GET'])
def new_blog():
    body_error = ""
    title_error = ""
    blog_title = ""
    blog_body = ""
    user = User.query.filter_by(username=session['user']).first()

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']

        if blog_body and blog_title:
            new_blog_post = Blog(blog_title, blog_body, user.id)
            db.session.add(new_blog_post)
            db.session.commit()

            blog_id = new_blog_post.id
            return redirect('/blog?id=' + str(blog_id))
        elif not blog_body:
            body_error = 'Please enter a body'
            blog_body = ""
        elif not blog_title:
            title_error = 'Please enter a title'
            blog_title = ""

    return render_template('new_blog.html', title="Create a New Blog", body_error=body_error, title_error=title_error,
                           blog_title=blog_title, blog_body=blog_body)


@app.route('/blog', methods=['GET'])
def index():
    user = request.args.get('user')
    if user:
        user = User.query.filter_by(username=user).first()
        blogs = Blog.query.filter_by(owner_id=user.id).all()
        return render_template('single_user.html', title="blog posts", user=user, blogs=blogs)

    blog_id = request.args.get('id')
    if not blog_id:
        return redirect('/blog?id=None')

    blog = Blog.query.get(blog_id)
    return render_template('blog.html', title="blog posts", blog=blog, blogs=get_blogs())


@app.before_request
def require_login():
    no_login = ['login', 'signup', 'index', 'homepage']
    if not ('user' in session or request.endpoint in no_login):
        return redirect("/login")


if __name__ == "__main__":
    app.run()
