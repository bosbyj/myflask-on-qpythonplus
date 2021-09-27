"""
    Public section, including homepage and signup.
"""

from flask import Blueprint, redirect,  url_for
from unpc.extensions import login_manager, mongo
from unpc.models import User

blueprint = Blueprint("mongoapp", __name__, template_folder="templates", url_prefix="/mongoapp")


# login 插件部分
@login_manager.user_loader
def load_user(user_id):
    return User(1)


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for("web.login"))


#################################################################


@blueprint.route("/")
def index():
    from bson.json_util import dumps

    results = mongo.db.runoob.find()
    return dumps(results)
