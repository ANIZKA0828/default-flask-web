from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from views import index_view
    app.register_blueprint(index_view.bp)

    return app