from flask import Blueprint, render_template, request, redirect, url_for
import pymysql, os
from dotenv import load_dotenv
load_dotenv()

bp = Blueprint('bp', __name__, url_prefix='/')

def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('DB_HOST','localhost'),
        user=os.environ.get('DB_USER','root'),
        password=os.environ.get('DB_PASSWORD'),
        db=os.environ.get('DB_NAME','myboard_db'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

@bp.route('/')
def index():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, title, created_at FROM posts ORDER BY id DESC")
        posts = cursor.fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
            conn.commit()
        conn.close()
        return redirect(url_for('bp.index'))
    return render_template('create.html')

@bp.route('/view/<int:post_id>')
def view(post_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
        post = cursor.fetchone()
    conn.close()
    return render_template('view.html', post=post)