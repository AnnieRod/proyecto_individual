from flask_app import app
from flask_app.controllers import doctors, patients, sessions

if __name__ == "__main__":
    app.run(debug=True)
