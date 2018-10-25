from flask import Flask, request, redirect, render_template, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Nujabes_4@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "y337Ness@u"

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    post = db.Column(db.String(600))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, post, owner):
        self.title = title
        self.post = post
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password        

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/newpost', methods=['POST', 'GET'])
def post():
    user = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        title = request.form['title']
        post = request.form['new_post']
        if not title or not post:
            flash("Please fill in all fields")
            return redirect('/newpost')
        else:    
            blog = Blog(title, post, user)
            db.session.add(blog)
            db.session.commit()
            return render_template('post.html', blog=blog, user=user)

    return render_template('newpost.html')

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def main_blog():
    
    user = User.query.filter_by(username=session['username']).first()
    blogs = Blog.query.filter_by(owner=user).all()
    
    

    return render_template('blog.html', blogs=blogs, user=user)

@app.route('/blog/<int:blog_id>/')
def blog(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    user = User.query.filter_by(id=blog.owner_id).first()

    return render_template('post.html', blog=blog, user=user)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        elif user and user.password != password:
            flash("Incorrect password")
        else:
            flash("User does not exist") 

    return render_template('login.html')               

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        if verify != password:
            flash("Passwords do not match")

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            
            flash("Username is already in use.")
    return render_template('register.html')   

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/login')
   
@app.route('/user', methods=['POST', 'GET'])
def users():

    users = User.query.all()

    return render_template('users.html', users=users)

@app.route('/user/<int:user_id>', methods=['POST', 'GET'])
def user(user_id):

    user = User.query.filter_by(id=user_id).first()
    blogs = Blog.query.filter_by(owner=user).all()
   

    return render_template('blog.html', blogs=blogs, user=user)



if __name__=='__main__':
    app.run()    