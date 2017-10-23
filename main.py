from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz2:happy@localhost:8889/blogz2'
db = SQLAlchemy(app)

class Blog(db.Model):
      
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(2000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  
    def __init__(self, title, body, owner):
        self.title = title
        self.body = body 
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
    allowed_routes = ['login', 'signup', 'blog', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] 
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username 
            flash('Logged in') 
            return redirect('/')
        else:
            if user and user.password != password or len(username) < 3 or len(username) > 20 or len(password) < 3 or len(password) > 20 or username == "" or password == "":
                flash('Incorrect password or no such user exists')
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST']) 
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  
        confirm = request.form['confirm']
        username_error = ""
        password_error = ""
        confirm_error = ""
        if username == "" or len(username) < 3 or len(username) > 20:
            flash('Value out of range (3-20)')
            return redirect('signup')
        if password == "" or len(password) < 3 or len(password) > 20:
            flash('Value out of range (3-20)')
            return redirect('/signup')
        if confirm == "" or len(confirm) < 3 or len(confirm) > 20:
            flash('Value out of range (3-20)')
            return redirect('/signup')
        if confirm != password:
            flash('Passwords must match')
        if username_error == "" and password_error == "" and confirm_error == "":
            return render_template('new_post.html')
            existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            flash('Signed up')
            return redirect('/')
        else:
            flash('User already exists')

    return render_template('signup.html')


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

         
@app.route('/', methods=['POST', 'GET'])
def index(): 
    owner = User.query.filter_by(username=session['username']).all()
    if request.method == 'POST': 
        blog_name = request.form['blog']
        new_blog = Blog(blog_name, owner)
        db.session.add(new_blog)
        db.session.commit()
        blogs = Blog.query.filter_by(owner=owner).all()
        new_blogs = Blog.query.filter_by(new=True, owner=owner)

    return render_template("blog.html")
    


@app.route('/blog', methods=['GET'])
def new_blog():
    page_title = 'New Posts'
    id = request.args.get('id')
    if id == None:
        blogs = Blog.query.all()
        return render_template("blog.html", blogs=blogs)
    single_user = request.args.get('username')
    if single_user == 'username':
        return render_template('singleUser.html', title="Add a New Entry", singleUser=singleUser)
    else:
        individual_blog = Blog.query.get(id)
        return render_template('individual_blog.html', title="Build a Blog", individual_blog=individual_blog)
    
    
@app.route('/blog', methods=['POST', 'GET'])
def display_blog_form():
    page_title = 'Blogz'
    blog_title = request.form['title']
    blog_body = request.form['body']  
    blog_title_error = ''
    blog_body_error = ''
    if blog_title == '':
        flash('Cannot leave fields empty')
    if blog_body == '':
        flash('Cannot leave fields empty')
    owner = User.query.filter_by(username=session['username']).first()
    if blog_title_error == "" and blog_body_error == "": 
        blog = Blog(blog_title, blog_body, owner)
        db.session.add(blog)
        db.session.commit()   
        return redirect('/blog?id=' + str(blog.id))
    else:
        return render_template('new_post.html')
      

@app.route('/new_post', methods=['GET'])
def new_post():
     return render_template('new_post.html')

@app.route('/individual_blog', methods=['POST', 'GET'])
def individual_blog():
    if request.method == 'POST':
        new_blog = request.form['new_blog']
        add_entry = Blog(new_blog)
        db.session.add(add_entry)
        db.session.commit()
        flash('Welcome, ' + username)
        return redirect('/blog?id=' + blog.id)
    elif request.method == 'GET':
        return render_template('new_post.html')
               

@app.route('/singleUser', methods=['GET'])
def singleUser():
    owner_id = request.form['owner_id']
    add_entry = Blog(new_blog)
    db.session.add(add_entry)
    db.session.commit()
    return redirect('/user?Id=' + user.id)
        
    
if __name__ == '__main__':
    app.secret_key = "secret"
    app.run()