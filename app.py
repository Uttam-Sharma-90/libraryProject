from flask import Flask, render_template
from flask_migrate import Migrate
from models import db
from view.books import books_bp
from view.members import members_bp
from view.transcation import transaction_bp
from view.importBooks import importBooks_bp

app = Flask(__name__)

# sqlite setup
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lms_python.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

# initalize the sql instance 
db.init_app(app)

migrate = Migrate(app, db)

@app.route('/')
def hello_world():
    return render_template('home.html')

# operation with help of blueprints
app.register_blueprint(books_bp)
app.register_blueprint(members_bp)
app.register_blueprint(transaction_bp)
app.register_blueprint(importBooks_bp)

if __name__ == '__main__':
        with app.app_context():
            db.create_all()    
        app.run(debug=True, port=8000)