## TODO

* 增加查看上下文功能
* 迁移之前 pythonanywhere / openshift 的旧项目
* 迁移测试文件目录, 更新 tests
* 模板继承 优化
* app 名称改为 heroku 重构
* 增加 error handler 403 404 500

## Changelog

### 0.0.10
    * 迁移 ccp concordance

### 0.0.9
    * 增加 .flake8 配置文件
    * 根据 flake8 提示, 优化 imports
    * vscode 配置中 flake8 args 增加 --config=.flake8
    * 增加 logging 功能, 参考 cookiecutter (不对 configure_logger 进行设置， 使用默认 werkzeug 的 logger)

### 0.0.8
    * 分离3个 blueprints: api, web, mongoapp
    * 蓝图中放置独立 templates 分区式 divisional structure

### 0.0.7
    * 变更密码 jj

### 0.0.6
    * app.register_blueprint(public.views.blueprint) __init__.py 里面增加 from . import
    * /logout /login -> url_for("public.login")

### 0.0.5
    * 根据 cookiecutter 重构

### 0.0.4
    * 新增 Mongo 数据库

### 0.0.3
    * 新增 Login 功能

## Notes

### Logging
    * 如果不给 app 增加新的 logging handler, 那么默认使用 werkzeug 的 logging handler, 需要设置 debug 才能看见 level 之上的内容
