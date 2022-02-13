
from flask import Flask

from flask_pymongo import PyMongo
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)


from routes import buildings, devices, main, users
if __name__ == '__main__':
    app.run(debug=True)
