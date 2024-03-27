from flask import Flask, Blueprint, request, jsonify, render_template
from datetime import datetime
from models import db, Transaction, Books, Members

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/issue_book', methods=['GET', 'POST'])
def issue_book():
    if request.method == 'POST': 

        book_id = request.form.get('book_id')
        member_id = request.form.get('member_id')

        book = Books.query.get(book_id)
        member = Members.query.get(member_id)

        if not book:
            return jsonify({'message': 'Book not found!'}), 404

        if not member:
            return jsonify({'message': 'Member  not found!'}), 404
        
        if book.is_issued:
            return jsonify({'message': 'Book already issued!'}), 400

        if member.debt > 500:
            return jsonify({'message': 'Member has outstanding debt!'}), 400
        
        transaction = Transaction(book_id=book_id, member_id=member_id, issue_date=datetime.now())
        book.is_issued = True
        db.session.add(transaction)
        db.session.commit()

        return jsonify({'message': 'Book issued successfully!'})

    elif request.method == 'GET': 
        return render_template('transactionHTML/issue_book.html')
    

@transaction_bp.route('/return_book', methods=['GET','POST'])
def return_book():
    if request.method == 'POST':
        data = request.json
        book_id = data['book_id']
        member_id = data['member_id']
        
        book = Books.query.get(book_id)
        member = Members.query.get(member_id)
        
        if not book or not member:
            return jsonify({'message': 'Book or Member not found!'}), 404
        
        transaction = Transaction.query.filter_by(book_id=book_id, member_id=member_id, return_date=None).first()
        if not transaction:
            return jsonify({'message': 'No active transaction found!'}), 400
        
        # charging fees
        days_diff = (datetime.now().date() - transaction.issue_date).days
        if days_diff > 3:
            transaction.fee = (days_diff - 3) * 10  # Assuming rs 10 per day late fee
            member.debt += transaction.fee
        
        transaction.return_date = datetime.now()
        book.is_issued = False
        db.session.commit()
        
        return jsonify({'message': 'Book returned successfully!'})
    elif request.method == 'GET':
        return render_template('transactionHTML/return_book.html')

