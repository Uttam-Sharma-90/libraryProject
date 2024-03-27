from flask import Flask, request,Blueprint, json, jsonify, render_template
import requests
from sqlalchemy import text
from models import db, Books

FRAPPE_API_URL = "https://frappe.io/api/method/frappe-library?page=2&title=and"

importBooks_bp = Blueprint('import_book', __name__)

@importBooks_bp.route('/drop_table/<Books>')
def drop_table(Books):
    try:
        statement = text(f"DROP TABLE IF EXISTS {Books};")
        db.session.execute(statement)
        db.session.commit()
        return f'Table {Books} dropped successfully'
    except Exception as e:
        return f'Error dropping table: {str(e)}'

@importBooks_bp.route('/delete_all_books')
def delete_all_books():
    try:
        # Use delete() method with no filters to delete all rows
        db.session.query(Books).delete()
        db.session.commit()
        return 'All data deleted from the Books table'
    except Exception as e:
        db.session.rollback()
        return f'Error deleting data from the Books table: {str(e)}'

@importBooks_bp.route('/importBooks', methods=['GET','POST'])
def importBook():
    if request.method == 'POST':
        title = request.form.get('title')
        num_books = request.form.get('num_books')

        response = requests.get(FRAPPE_API_URL, params={'title': title})

        if response.status_code == 200:
            books_data = response.json()['message']

            for book_data in books_data[:int(num_books)]:

                book = Books(
                    title = book_data.get('title'),
                    authors = book_data.get('authors'),
                    isbn = book_data.get('isbn'),
                    publisher = book_data.get('publisher'),
                    pages = book_data.get('  num_pages')
                )
                db.session.add(book)
            db.session.commit()

            return jsonify({'message': f'{num_books} books imported successfully!{book_data}'})
        else:
            return jsonify({'message':'Failed to import books. Error:'})
    else:
        return render_template('importBookHTML/importBook.html')