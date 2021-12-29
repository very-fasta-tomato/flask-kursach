from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///libra.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Author(db.Model):
    __tablename__ = 'author'
    idAuthor = db.Column(db.Integer, primary_key=True)
    authorName = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    books = db.relationship('Book', backref='Author', lazy='dynamic')

    def __repr__(self):
        return '<Author %r>' % self.idAuthor


class Book(db.Model):
    __tablename__ = 'book'
    idBook = db.Column(db.Integer, primary_key=True)
    idAuthor = db.Column(db.Integer, db.ForeignKey('author.idAuthor'), nullable=False)
    title = db.Column(db.String(100), nullable=True)
    publisher = db.Column(db.String(100), nullable=True)
    readers = db.relationship('Reader', backref='Book', lazy='dynamic')

    def __repr__(self):
        return '<Book %r>' % self.idBook


class Reader(db.Model):
    __tablename__ = 'reader'
    idReader = db.Column(db.Integer, primary_key=True)
    idBook = db.Column(db.Integer, db.ForeignKey('book.idBook'), nullable=False)
    readerName = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return '<Reader %r>' % self.idReader


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/authors-base')
def authors_base():
    authors = Author.query.order_by(Author.authorName).all()
    return render_template("authors-base.html", authors=authors)


@app.route('/books-base')
def books_base():
    books = Book.query.order_by(Book.title).all()
    return render_template("books-base.html", books=books)


@app.route('/add-author', methods=['POST', 'GET'])
def add_author():
    if request.method == 'POST':
        authorName = request.form['authorName']
        country = request.form['country']

        author = Author(authorName=authorName, country=country)

        try:
            db.session.add(author)
            db.session.commit()
            return redirect('/')
        except:
            return "При добавлении автора произошла ошибка"
    else:
        return render_template("add-author.html")


@app.route('/add-book', methods=['POST', 'GET'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        publisher = request.form['publisher']
        idAuthor = request.form['idAuthor']

        book = Book(title=title, publisher=publisher, idAuthor=idAuthor)

        try:
            db.session.add(book)
            db.session.commit()
            return redirect('/')
        except:
            return "При добавлении книги произошла ошибка"
    else:
        return render_template("add-book.html")


@app.route('/add-reader', methods=['POST', 'GET'])
def add_reader():
    if request.method == 'POST':
        readerName = request.form['readerName']
        address = request.form['address']
        idBook = request.form['idBook']

        book = Book(readerName=readerName, address=address, idBook=idBook)

        try:
            db.session.add(book)
            db.session.commit()
            return redirect('/')
        except:
            return "При добавлении книги произошла ошибка"
    else:
        return render_template("add-reader.html")


if __name__ == "__main__":
    app.run(debug=True)
