from flask import Flask



def create_app():
    app = Flask(__name__)

    from.views import main_view,stream_view,char_info_view
    

    app.register_blueprint(main_view.bp)
    app.register_blueprint(stream_view.bp)
    app.register_blueprint(char_info_view.bp)

    return app
    
