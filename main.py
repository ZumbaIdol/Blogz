from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz2:happy@localhost:8889/blogz2'
db = SQLAlchemy(app)

class Blog(db.Model):
      
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(120))
    body = db.Column(db.String(2000))
  
    def __init__(self, owner, title, body):
        self.owner = owner
        self.title = title
        self.body = body 


class User(db.Model):
      
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.Column(db.String(2000))
  
    def __init__(self, username, password, blogs):
        self.username = username
        self.password = password
        self.blogs = blogs  

         
@app.route('/')
def index():
    encoded_error = request.args.get('error')
    author_username = request.args.get('owner_id')
    if author_username == None:
        blogs = Blog.query.all()
        return render_template("blog.html", blogs=blogs)
    else:
        individual_blog = Blog.query.get(id)
        return render_template('individual_blog.html', title="Build a Blog", individual_blog=individual_blog)

    endpoints_without_login = ['login', 'signup']


@app.route('/blog', methods=['GET'])
def new_blog():
    id = request.args.get('id')
    if id == None:
        blogs = Blog.query.all()
        return render_template("blog.html", blogs=blogs)
    else:
        individual_blog = Blog.query.get(id)
        return render_template('individual_blog.html', title="Build a Blog", individual_blog=individual_blog)
    
    
@app.route('/blog', methods=['POST', 'GET'])
def display_blog_form():
    
    blog_title = request.form['title']
    blog_body = request.form['body']  
    blog_title_error = ''
    blog_body_error = ''
    if blog_title == '':
        blog_title_error = flash('Cannot leave fields empty', category='message')
    if blog_body == '':
        blog_body_error = flash('Cannot leave fields empty', category='message')
    if blog_title_error == "" and blog_body_error == "": 
        blog = Blog(blog_title, blog_body)
        db.session.add(blog)
        db.session.commit()   
        return redirect('/blog?id=' + str(blog.id))
    else:
        return render_template('new_post.html', blog_title_error=blog_title_error, blog_body_error=blog_body_error)
      

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
        return redirect('/blog?id=' + blog.id)
    else:
        return render_template('new_post.html')

                       
@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index', 'blog']
    if request.endpoint not in allowed_routes and 'user' not in session:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username)
    if user.count() == 1:
        user = users.first()
        if password == user.password:
            session['user'] = user.username
            flash('Welcome back, ' + user.username)
            return redirect('/')
    else:    
        flash('Incorrect username or password')
        return redirect('/login')


@app.route('/signup', methods=['GET', 'POST']) 
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  
        confirm = request.form['confirm']
        username_error = ''
        password_error = ''
        confirm_password_error = ''
        if username == "" or len(username) < 3 or len(username) > 20:
           username_error = 'Value out of range (3-20)' 
        if password == "" or len(password) < 3 or len(password) > 20:
            password_error = 'Value out of range (3-20)'
            password = ''
        if confirm_password == "" or len(confirm_password) < 3 or len(confirm_password) > 20:
            confirm_password_error = 'Passwords must match'
            confirm_password = ''
            username_db_count = User.query.filter_by(username=username).count()
        if username_db_count > 0:
            flash('Shazpatz! ' + username +  ' is already a registered user')
            return redirect('/signup')
        if password != confirm:
            flash('Passwords must match')
            return redirect('/signup')
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            session['user'] = user.username
            return redirect('/new_post')
    else:
        return render_template('signup.html')
               

@app.route('/singleUser', methods=['GET'])
def singleUser():
    owner_id = request.form['owner_id']
    add_entry = Blog(new_blog)
    db.session.add(add_entry)
    db.session.commit()
    return redirect('/user?Id=' + user.id)
    

@app.route('/logout', methods=['GET'])
def logout():
    del session['username']
    return redirect('/')
   

# @app.route('/index', methods=['POST'])
# def index():
#     return render_template('index.html')
    


        
    
if __name__ == '__main__':
    app.secret_key = "secret"
    app.run()