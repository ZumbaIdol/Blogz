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
            return render_template('new_post.html')
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
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            flash('Signed up')
            return render_template('new_post.html')
        else:
            flash('User already exists')
    return render_template('signup.html')


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

         
@app.route('/', methods=['POST', 'GET'])
def index(): 
    if request.method == 'POST': 
        blog_name = request.form['blog']
        new_blog = Blog(blog_name, owner)
        owner = User.query.filter_by(username=session['username']).first()
        users = User.query.all()
        db.session.add(new_blog)
        db.session.commit()
        blogs = Blog.query.filter_by(owner=owner).all()
        new_post = Blog.query.filter_by(new=True, owner=owner)
        if single_user != None:
            user = User.query.filter_by(username=username).first()
    return render_template("blog.html")
    
    


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    id = request.args.get('id')
    if request.method == 'GET':
        users = User.query.all()
    return render_template('index.html', title="Blogz", users=users)
    if id != None:
        #individual post
        individual_blog = Blog.query.get(id)
        return render_template('individual_blog.html', title="Blogs", individual_blog=individual_blog)
    if single_user != None:
        user = User.query.filter_by(username=username).first()
        #username = single_user
        return render_template('singleUser.html', singleUser=User)
    #singleUser and blog templates almost indentical
    blogs = Blog.query.all()
    return render_template("blog.html", blogs=blogs)
                       

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body'] 
        owner = User.query.filter_by(username=session['username']).first() 
        if blog_title == '' or blog_body == '':
            flash('Cannot leave fields empty')
            return render_template('new_post.html')
        blog = Blog(blog_title, blog_body, owner)
        db.session.add(blog)
        db.session.commit()   
        return redirect('/blog?id=' + blog.id)
    else:
        if request.method == 'GET':
            return render_template('new_post.html', title="Add Blog Entry")


@app.route('/individual_blog', methods=['POST', 'GET'])
def individual_blog():
    if request.method == 'POST':
        individual_blog = request.form['individual_blog']
        add_entry = Blog(individual_blog)
        db.session.add(add_entry)
        db.session.commit()
        flash('Welcome, ' + username)
        return redirect('/blog?id=' + blog.id)
    elif request.method == 'GET':
        return render_template('individual_blog.html')
               

@app.route('/singleUser', methods=['GET'])
def singleUser():
    username= request.form['username']
    #add_entry = Blog(new_blog)
    db.session.add(add_entry)
    db.session.commit()
    return render_template('singleUser.html')
        
    
if __name__ == '__main__':
    app.secret_key = "secret"
    app.run()