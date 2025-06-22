from flask import Blueprint, render_template, request, redirect, url_for
import pymysql, os  
from dotenv import load_dotenv
load_dotenv()

# os : 파이썬에서 운영체제와 상호 작용할 수 있게 해주는 모듈
bp = Blueprint('bp', __name__, url_prefix='/')

# db와 연결하기 위한 함수
def get_db_connection():
    return pymysql.connect(
        # os.environ.get 함수 : .env에 설정된 값을 불러옴
        host=os.environ.get('DB_HOST','localhost'),
        user=os.environ.get('DB_USER','root'),
        password=os.environ.get('DB_PASSWORD'),
        db=os.environ.get('DB_NAME','myboard_db'),
        charset='utf8mb4',
        # pymysql.cursors.DictCursor : {{ post.created_at }},{{ post.title }}에 해당하는 항목들을 불러오기 위함
        #         
        cursorclass=pymysql.cursors.DictCursor
    )

# '/'URL로 라우팅
@bp.route('/')
def index():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, title, created_at FROM posts ORDER BY id DESC")
        posts = cursor.fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

# '/create'URL로 라우팅
# GET : 작성 폼 보여주기
# POST : 작성 폼 제출 
@bp.route('/create', methods=('GET', 'POST'))
def create():
    # 'POST' 방식이 요청된거면 생성하겠다는 것이므로 db에 연결해 저장
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
            conn.commit()
        conn.close()
        return redirect(url_for('bp.index'))
    # 작성 폼을 보여줘야 전송할 수 있으므로 'GET'방식으로 출력
    return render_template('create.html')

# '<int:post_id>는 정수형으로 받고, 해당 post_id를 view함수에 파라미터로 전달한다.
@bp.route('/view/<int:post_id>')
def view(post_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
        post = cursor.fetchone()
    conn.close()
    return render_template('view.html', post=post)