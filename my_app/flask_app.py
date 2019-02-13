from flask import Flask,render_template,g
import sqlite3


app = Flask(__name__)
app.database = "sample.db"

@app.route('/hello')
def hello_world():
    return 'Hello World'

@app.route('/')
def index():
    return render_template('index.html',
    						page = 'home',
    						title="Flask App")
@app.route('/about')
def about():
    return render_template('about.html',
    						page = 'about',
    						title="Flask App - About")
@app.route('/blog')
def blog():
    g.db = connect_db()
    cur = g.db.execute('select * from posts')
    posts = [dict(title =row[0],description=row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template('blog.html',
    						page = 'blog',
    						title="Flask App - Blog",
                            posts = posts)

@app.route('/photography')
def photography():
    return render_template('photography.html',
    						page = 'photography',
    						title="Flask App - Photography")
@app.route('/contact')
def contact():
    return render_template('contact.html',
    						page = 'contact',
    						title="Flask App - Contact")

def connect_db():
    return sqlite3.connect(app.database)



if __name__ == "__main__":
    app.debug = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run()
