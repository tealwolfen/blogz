from flask import Flask, request, redirect, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Nujabes_4@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "y337Ness@u"

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    post = db.Column(db.String(600))

    def __init__(self, title, post):
        self.title = title
        self.post = post
        



@app.route('/newpost', methods=['POST', 'GET'])
def post():

    if request.method == 'POST':
        title = request.form['title']
        post = request.form['new_post']
        if not title or not post:
            flash("Please fill in all fields")
            return redirect('/newpost')
        else:    
            blog = Blog(title, post)
            db.session.add(blog)
            db.session.commit()
            return render_template('post.html', blog=blog)

    return render_template('newpost.html')

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def main_blog():

    blogs = Blog.query.all()


    return render_template('blog.html', blogs=blogs)

@app.route('/blog/<int:blog_id>')
def blog(blog_id):
    blog = Blog.query.filter_by(id=blog_id).one()

    return render_template('post.html', blog=blog)


if __name__=='__main__':
    app.run()    