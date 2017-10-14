from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'
db = SQLAlchemy(app)

class Blog(db.Model):
      
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(2000))
  
    def __init__(self, title, body):
        self.title = title
        self.body = body      


@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect('/blog') 


@app.route('/blog', methods=['GET'])
def new_blog():
    blog_ids = request.args.get('ids')
    if blog_ids == None: 
        blogs = Blog.query.all()
        return render_template("blog.html", blogs=blogs)
    else:
        individual_blog = Blog.query.get(blog_ids)
        render_template('individual_blog.html', + blog_ids)
    
    
@app.route('/blog', methods=['POST'])
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
        return redirect('/blog?id=' + blog.id)  
    else:
        return render_template('new_post.html', blog_title_error=blog_title_error, blog_body_error=blog_body_error)
      

@app.route('/new_post', methods=['GET'])
def start_post():
     return render_template("new_post.html")

@app.route('/individual_blog', methods=['POST', 'GET'])
def individual_blog():
    if request.method == 'POST':
        new_blog = request.form['new_blog']
        add_entry = Blog(new_blog)
        db.session.add(add_entry)
        db.session.commit()
        return redirect('/individual_blog?id=' + new_blog.id)
    else:
         return render_template('new_post.html') 
          
    
if __name__ == '__main__':
    app.secret_key = "secret"
    app.run()