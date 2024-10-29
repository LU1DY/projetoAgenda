from app import app
from app.appAdmin import init_app

init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
