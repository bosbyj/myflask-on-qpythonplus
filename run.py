from unpc import app

# gunicorn 调用
heroku_app = app.create_app()

if __name__ == "__main__":
    # 命令行直接启动 使用 debug 模式
    heroku_app.run(debug=True)
