"""
    Public section, including homepage and signup.
"""

from flask import Blueprint, jsonify, redirect, request, url_for
# from flask_login import login_required
# from myflask.db import query
# from unpc.extensions import login_manager
from myflask.models import UrlParams

blueprint = Blueprint("api", __name__, template_folder="templates", url_prefix="/api")


# login 插件部分
# @login_manager.user_loader
# def load_user(user_id):
#     return User(1)


# @login_manager.unauthorized_handler
# def unauthorized_callback():
#     return redirect(url_for("web.login"))


#################################################################


# @login_required
@blueprint.route("/")
def api():
    """API接口."""
    # 验证url参数
    params = UrlParams(**request.args)
    return jsonify(query(params).dict())
