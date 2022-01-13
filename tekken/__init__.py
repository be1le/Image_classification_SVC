from flask import Flask

from .views import char_result_view



def create_app():
    app = Flask(__name__)

    from.views import main_view,stream_view,all_char_table_view,char_result_view,char_detail_view
    

    app.register_blueprint(main_view.bp)
    app.register_blueprint(stream_view.bp)
    app.register_blueprint(char_result_view.bp)
    app.register_blueprint(all_char_table_view.bp)
    app.register_blueprint(char_detail_view.bp)

    return app
    
