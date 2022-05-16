from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # @app.route('/') # 애너테이션
    # def hello_flsk(): # 라우팅 함수
    #     return 'Hello, Flask!'
    
    from .views import main_views 
    app.register_blueprint(main_views.bp) # 블루 프린트 등록
    
    return app

