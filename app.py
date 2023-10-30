from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

DB_URL = "postgresql://postgres:postgreSQL@localhost:5432/amsdb"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.app_context().push()

@app.route('/')
def hello_world():
   return "hello"

if __name__ == '__main__':
   app.run(debug=True)