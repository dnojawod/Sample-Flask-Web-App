from flask import Flask, request, render_template, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/data'
db = SQLAlchemy(application)

class Book(db.Model):
    __tablename__ = 'book'
    title = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))
    id = db.Column(db.Integer,primary_key=True)

    def __repr__(self):
        return "<Title: {0}, Description: {1}>".format(self.title,self.description)

    title_click = 0
    id_click = 0

@application.route('/', methods=["POST","GET"])
def index():
    return render_template("home.html")

@application.route('/add', methods=["POST","GET"])
def add():
    if request.form:
        book = Book(title=request.form.get("title"),description=request.form.get("description"))
        db.session.add(book)
        db.session.commit()
    return render_template("add.html")

@application.route('/display', methods=["GET"])
def display():
    sort = request.args.get('sort', default='', type=str)
    if sort == 'title':
        Book.id_click = 0
        Book.title_click = Book.title_click + 1
        if Book.title_click % 2 == 0:
            books = Book.query.order_by(desc(Book.title)).all()
        else:
            books = Book.query.order_by(asc(Book.title)).all()
    elif sort =='id':
        Book.title_click = 0
        Book.id_click = Book.id_click + 1
        if Book.id_click % 2 == 0:
            books = Book.query.order_by(desc(Book.id)).all()
        else:
            books = Book.query.order_by(asc(Book.id)).all()
    else:
        Book.title_click = 0
        Book.id_click = 0
        books = Book.query.all()
    return render_template("display.html", books=books)

@application.route('/delete', methods=["POST","GET"])
def delete():
    if request.form:
        title = request.form.get("delete_title")
        book = Book.query.filter_by(title=title).first()
        db.session.delete(book)
        db.session.commit()
    books = Book.query.all()
    return render_template("delete.html",books=books)

@application.route('/update', methods=["POST","GET"])
def update():
    if "newtitle" in request.form:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        book = Book.query.filter_by(title=oldtitle).first()
        book.title = newtitle
        db.session.commit()
    elif "newdescription" in request.form:
        title = request.form.get("title")
        newdescription = request.form.get("newdescription")
        book = Book.query.filter_by(title=title).first()
        book.description = newdescription
        db.session.commit()
    books = Book.query.all()
    return render_template("update.html", books=books)

@application.route('/file', methods=["POST","GET"])
def file():
    if "updatefile" in request.form:
        file = open("files/Books.txt", "w")
        books = Book.query.all()
        for book in books:
            file.write(str(book.title + "\n" + book.description + "\n\n"))
        file.close()

    elif "downloadfile" in request.form:
        return send_file("files/Books.txt", as_attachment=True, attachment_filename="Books.txt")
    return render_template("file.html")

if __name__ == "__main__":
    # db.create_all()
    application.run(host='0.0.0.0', debug=True)