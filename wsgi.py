from unpc import app

heroku_app = app.create_app()

if __name__ == "__main__":
    heroku_app.run(debug=True)
