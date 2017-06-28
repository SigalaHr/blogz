from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:abc123@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'NJfpoqwenDFSljqnlkjqLK'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(2500))

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def __repr__(self):
        return '<Blog %r>' % self.title

def get_blogs():
    return Blog.query.filter_by().all()

@app.route('/newblog', methods=['POST', 'GET'])
def new_blog():
    body_error = ""
    title_error = ""
    blog_title = ""
    blog_body = ""
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        if blog_body is not "" and blog_title is not "":
            new_blog_post = Blog(blog_title, blog_body)
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
    blog_id = request.args.get('id')
    if blog_id is None:
        return redirect('/blog?id=None')
    blog = Blog.query.get(blog_id)
    return render_template('blog.html', title="Blog Page", blog=blog, blogs=get_blogs())

if __name__ == "__main__":
    app.run()