from flask import Blueprint, render_template, request, redirect, url_for, current_app
from models import Books, db

books_bp = Blueprint('books', __name__)

@books_bp.route('/createBooks',methods=['GET','POST'])
def create():
    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        authors = request.form['authors']
        publisher = request.form['publisher']
        pages = request.form['pages']

        with current_app.app_context():
            book = Books(title=title, authors=authors, publisher=publisher, pages=pages, isbn=isbn)
            db.session.add(book)
            db.session.commit()

        return redirect(url_for('books.show'))
    return render_template('bookHTML/index.html')

# @books_bp.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     book = Books.query.get_or_404(id)

#     if request.method == 'POST':
#         book.isbn = request.form['isbn']
#         book.title = request.form['title']
#         book.authors = request.form['authors']
#         book.publisher = request.form['publisher']
#         book.pages = request.form['pages']

#         try:
#             db.session.commit()
#             return redirect(url_for('books.show'))
#         except Exception as e:
#             return str(e)

#     return render_template('bookHTML/update.html', book=book)

@books_bp.route('/updateBook', methods=['GET', 'POST'])
def updateBook():

    if request.method == 'POST':
        if 'book_id' in request.form:  
            book_id = request.form['book_id']
        
            books = Books.query.get(book_id) 

            if books:
                if 'isbn' in request.form:  
                    books.isbn = request.form['isbn'] 
                if 'title' in request.form:
                    books.title = request.form['title']
                if 'authors' in request.form:  
                    books.authors = request.form['authors'] 
                if 'publisher' in request.form:  
                    books.publisher = request.form['publisher'] 
                if 'pages' in request.form:  
                    books.pages = request.form['pages'] 
                
                db.session.commit()
            return render_template('bookHTML/update.html', books=books, book_id=book_id)
    return render_template('bookHTML/updateRes.html')

# @books_bp.route('/delete/<int:id>')
# def delete(id):
#     del_book = Books.query.get_or_404(id)

#     db.session.delete(del_book) 
#     db.session.commit()
#     return redirect(url_for('books.show'))

@books_bp.route('/deleteBook', methods=['GET','POST'])
def deleteBook():
    if request.method == 'POST':
        book_id = request.form['book_id']
        del_book = Books.query.get_or_404(book_id)

        db.session.delete(del_book) 
        db.session.commit()
        return redirect(url_for('books.show'))
    return render_template('bookHTML/updateRes.html')
    

@books_bp.route('/viewBooks')
def show():
    all_book = Books.query.all()
    return render_template('bookHTML/books.html', all_book=all_book)

@books_bp.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search_term']

        books = Books.query.filter(
            (Books.title.like(f"%{search_term}%")) | 
            (Books.authors.like(f"%{search_term}%"))
        ).all() 
        # print(books)
        return render_template('bookHTML/searchResult.html', books=books, search_term=search_term)
    
    return render_template('bookHTML/search.html')