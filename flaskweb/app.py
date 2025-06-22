from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # views 디렉토리에서 index_view 모듈 가져오기
    from views import index_view    
    app.register_blueprint(index_view.bp)

    # flask 서버 실행
    return app