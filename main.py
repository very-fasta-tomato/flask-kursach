from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///libra.db'
db = SQLAlchemy(app)


class Autor(db.Model):
    __tablename__ = 'autor'
    idAutor = db.Column(db.Integer, primary_key=True)
    autorName = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return '<Autor %r>' % self.idAutor


class Book(db.Model):
    __tablename__ = 'book'
    idBook = db.Column(db.Integer, primary_key=True)
    idAutor = db.Column(db.Integer, db.ForeignKey('autor.idAutor'), nullable=False)
    title = db.Column(db.String(100), nullable=True)
    publisher = db.Column(db.String(100), nullable=True)

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


@app.route('/about')
def about():
    return "About page"


if __name__ == "__main__":
    app.run(debug=True)
