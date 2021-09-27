"""
    The app module, containing the app factory function.
"""


from flask import Flask, g

from unpc import api, mongoapp, web, ccp
from unpc.db import jieba
from unpc.extensions import login_manager, mongo


def create_app(config_object="unpc.settings") -> Flask:
    """工厂函数.
    Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.

    Returns:
        Flask 实例

    """
    app = Flask(__name__)
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)
    configure_logger(app)

    with app.app_context():
        # Flask实例运行之后, 手动初始化jieba
        jieba.initialize()

    @app.teardown_appcontext
    def close_connection(exception):
        """Flask结束后, 执行关闭数据库."""
        db = getattr(g, "_database", None)
        if db is not None:
            db.close()

    return app


def register_extensions(app):
    """Register Flask extensions."""
    # mongo.init_app(app)
    login_manager.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(api.views.blueprint)
    app.register_blueprint(web.views.blueprint)
    # app.register_blueprint(mongoapp.views.blueprint)
    app.register_blueprint(ccp.views.blueprint)
    return None


def configure_logger(app):
    """Configure loggers."""
    pass


if __name__ == "__main__":
    DATABASE = "tmdata.db"
    app: Flask = create_app()

    # app.run(host='0.0.0.0', ssl_context='adhoc')
    # app.run(host='0.0.0.0', port=8002, ssl_context='adhoc')
    app.run(host="0.0.0.0", debug=True)
