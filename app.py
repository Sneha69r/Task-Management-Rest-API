from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET")

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Import routes
from routes.auth import auth_bp
from routes.tasks import task_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(task_bp, url_prefix='/api/tasks')

if __name__ == "__main__":
    app.run(debug=True)