from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
db = SQLAlchemy()

class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), nullable=True)
    title = db.Column(db.String(200), nullable=True)
    authors = db.Column(db.String(200), nullable=True)
    publisher = db.Column(db.String(200), nullable=True)
    pages = db.Column(db.Integer, nullable=True)
    is_issued = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f"{self.title},{self.id}"
    # if self nhi toh Books use kr skte h 

class Members(db.Model):
    __tablename__ = 'member'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable = False)
    email_id = db.Column(db.String(30), unique=True, nullable = True)
    mobile_no = db.Column(db.Integer, nullable = False)
    isMember = db.Column(db.Boolean, default = False)
    memberShip_id = db.Column(db.Integer, unique=True, nullable = False)
    debt = db.Column(db.Float, default=0) 

    def __repr__(self) -> str:
        return f"{self.name}, {self.mobile_no}"
    
class Transaction(db.Model):
    __tablename__ = 'transaction' 
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id')) 
    member_id = db.Column(db.Integer, db.ForeignKey('member.id')) 
    issue_date = db.Column(db.Date)
    return_date = db.Column(db.Date)
    fee = db.Column(db.Float)