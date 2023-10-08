"""
    Public section, including homepage and signup.
"""

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
# from flask_login import login_required, login_user, logout_user
# from myflask.db import query
# from unpc.extensions import login_manager
from myflask.models import UrlParams

blueprint = Blueprint("unpc", __name__, template_folder="templates", url_prefix="/unpc")


# login 插件部分
# @login_manager.user_loader
# def load_user(user_id):
#     return User(1)


# @login_manager.unauthorized_handler
# def unauthorized_callback():
#     return redirect(url_for("web.login"))


#################################################################


# @blueprint.route("/login/", methods=["GET", "POST"])
# def login():
#     # 这里我们使用一个类，来表示和验证客户端表单数据
#     # 例如，WTForms 库可以用来为我们处理这些工作，
#     # 我们使用自定义的 LoginForm 来验证表单数据。
#     current_app.logger.info("来自login的问候!")

#     # user = User(1)

#     if request.method == "POST" and request.form["password"] == "jj":
#         # 登录并且验证用户
#         # user 应该是你 `User` 类的一个实例
#         login_user(user)

#         flash("Logged in successfully.")
#         print("Logged in successfully.")
#         current_app.logger.info("Logging功能, 你好呀!")
#         return redirect(url_for("web.index"))

#     return render_template("login.html")


# @blueprint.route("/logout/")
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for("web.login"))


@blueprint.route("/", methods=["GET", "POST"])
# @login_required
def index():
    """unpc Web界面."""
    current_app.logger.info("来自web的问候!")
    # 验证url参数
    # params = UrlParams(**request.args) or None
    if request.method == "POST":
        print(request.form)
        if request.form["es"]:
            k = request.form["es"]
            return redirect(f"/unpc/es/{k}/1")
        elif request.form["zh"]:
            k = request.form["zh"]
            return redirect(f"/unpc/zh/{k}/1")
    else:
        return render_template("web.html")


@blueprint.route(
    "/<string:language>/<string:keywords>/<int:page>", methods=["GET", "POST"]
)
def web_results(language: str, keywords: str, page: int):
    """Web查询结果."""
    # 验证url参数
    # params = UrlParams(**request.args) or None
    if request.method == "POST":
        # print(request.form)
        if request.form["es"]:
            k = request.form["es"]
            return redirect(f"/unpc/es/{k}/1")
        elif request.form["zh"]:
            k = request.form["zh"]
            return redirect(f"/unpc/zh/{k}/1")

        # return redirect(f'/you_were_redirected')

    else:
        params = UrlParams(language=language, keywords=keywords, page=page)

        resp_obj = query(params).dict()

        return render_template("web_results.html", resp_obj=resp_obj, **params.dict())
