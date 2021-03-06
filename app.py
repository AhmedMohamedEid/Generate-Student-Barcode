
import csv
import os

from flask import Flask, session,render_template,redirect, request, url_for
from flask_session import Session
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
# Database
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug import secure_filename
import sqlite3

import barcode, random
from barcode.writer import ImageWriter

# from flask_wtf import FlaskForm
# from wtforms import StringField
# from wtforms.validators import DataRequired


from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter, get_page_args

mod = Blueprint('student', __name__)


UPLOAD_FOLDER = '/files/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# configure session to use filesystem (instead of signed cookies)
# app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
Session(app)

db = sqlite3.connect('student.db', check_same_thread=False)

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function



   # User Register Page #
@app.route("/signup", methods=['GET','POST'])
def signup():
    # session.clear()
    if request.method == 'POST':
        username = request.form.get("name")
        email = request.form.get("email")
        password = generate_password_hash(request.form.get("password"))
        print (password)
        check_email = db.execute("SELECT email FROM users WHERE email = :email", {"email": email}).rowcount
        print(check_email)
        if check_email+1 == 0:
            db.execute("INSERT INTO users (username, email, password) VALUES(:username, :email, :password)", {"username":username, "email": email,"password":password})
            db.commit()

            # Get Username to store Session
            user = db.execute("SELECT id,username FROM users WHERE email = :email",{"email":email}).fetchone()
            print(user)
            # print(session['secret_key'])
            session['userid'] = user[0]
            session['username'] = user[1]
            # redirect to Home
            return redirect("/")
        else:
            return render_template("signup.html")
    else:
        message = "Invalid Register"
        print(message)
        return render_template("signup.html", message=message)


# class MyForm(FlaskForm):
#     name = StringField('name', validators=[DataRequired()])
#     print(name)

@app.route('/login', methods=('GET', 'POST'))
def login():

    # Forget All Session_id
    session.clear()
    if request.method == "POST":
        email = request.form.get("username")
        password = request.form.get("password")
        hash_password = generate_password_hash(password)
        result = db.execute("SELECT * FROM users WHERE email = :email",{"email":email}).fetchone()

        if result:
            if check_password_hash(result[3], password):
                session["user_id"] = result[0]
                session["user_name"] = result[1]

                return redirect('/')
            else:
                # flask.flash('Invalid email or password')

                return redirect("/login")
        else:
            message = "Incorrect Email"
            return render_template("login.html",message="message")

    return render_template('login.html')

# if not current_user.is_authenticated:
#     return current_app.login_manager.unauthorized()


@app.route("/logout")
@login_required
def logout():
    # logout_user()
    session.clear()
    return redirect('/login')


# @mod.route('/')
# def index():
#     search = False
#     q = request.args.get('q')
#     if q:
#         search = True
#
#     page = request.args.get(get_page_parameter(), type=int, default=1)
#
#     users = User.find(...)
#     pagination = Pagination(page=page, total=users.count(), search=search, record_name='users')
#     # 'page' is the default name of the page parameter, it can be customized
#     # e.g. Pagination(page_parameter='p', ...)
#     # or set PAGE_PARAMETER in config file
#     # also likes page_parameter, you can customize for per_page_parameter
#     # you can set PER_PAGE_PARAMETER in config file
#     # e.g. Pagination(per_page_parameter='pp')
#
#     return render_template('users/index.html',
#                            users=users,
#                            pagination=pagination,
#                            )




def get_users(offset=0, per_page=10):
    return users[offset: offset + per_page]

@app.route('/')
@app.route('/index')
@login_required
def index():

    # page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
    # Print(page)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    print(page)

    # users = student.find(...)
    rows = db.execute("SELECT * FROM student").fetchall()
    # print(rows)
    pagination = Pagination(page=page, css_framework="bootstrap4",total=len(rows), record_name='rows')
    print(pagination)
    return render_template("index.html", pagination=pagination ,students=rows)




@app.route("/upload", methods=["GET","POST"])
def student_data():
    """Register user."""
    # file = open("books.csv")
    # books = csv.reader(file)
    if request.method == "POST":
        file = request.files['student_file']
        file.save(secure_filename(file.filename))

        file = open(file.filename)
        students = csv.reader(file)
        for name,ui_code,level in students:
            db.execute("INSERT INTO student (name, ui_code, level) VALUES (:name, :ui_code, :level)", {"name":name, "ui_code":ui_code, "level":level})
        db.commit()

        # print(file.filename)
        print(file)
    #     # insert the new user into users, storing the hash of the user's password
    #     result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",dict(username=request.form.get("username"), hash=pwd_context.encrypt(request.form.get("password"))))
    #
    #     if not result:
    #         return apology("Username already exist")
    #
    #     # remember which user has logged in
    #     session["user_id"] = result
    #
    #     # redirect user to home page
    return redirect(url_for("index"))

    # else:
    #     return render_template("register.html")



@app.route("/generate_png", methods=["GET", "POST"])
def generate_png():

    if request.method == "POST":
        # num = random.randrange(1,00)
        rows = db.execute("SELECT * FROM student").fetchall()
        if rows:
            for row in rows:
                num = "00{}".format(row[2])
                name = row[1]
                print (num)
                EAN = barcode.get_barcode_class('ean8')
                ean = EAN(u"{}".format(num),  writer=ImageWriter())
                fullname = ean.save(u'{}-{}'.format(num,name), text=name)
    return redirect(url_for("index"))

@app.route("/generate_svg", methods=["GET", "POST"])
def generate_svg():
    if request.method == "POST":
        # num = random.randrange(1,00)
        path = ""
        rows = db.execute("SELECT * FROM student WHERE barcode_path IS NULL;").fetchall()
        print(rows)
        barcode_path = "static/barcode_path"
        try:
            os.makedirs(barcode_path)

        except OSError:
            print ("Creation of the directory %s failed" % barcode_path)
        else:
            print ("Successfully created the directory %s " % barcode_path)
        os.chdir(barcode_path)
        if rows:
            for row in rows:

                num = "00{}".format(row[2])
                name = row[1]
                print (num)
                EAN = barcode.get_barcode_class('ean8')
                ean = EAN(u"{}".format(num))


                filenum = random.randrange(1,1000)
                fullname = ean.save(u'{}-{}-{}'.format(num,name,filenum), text=name)
                print(fullname)
                path = "barcode_path/{}-{}-{}.svg".format(num,name,filenum)
                db.execute("UPDATE student SET barcode_path=:barcode_path WHERE id=:id",{"barcode_path":path, "id":row[0]})
            db.commit()
    return redirect(url_for("index"))


@app.route("/delete_all", methods=["POST", "GET"])
def delete_all():
    if request.method == "POST":
        db.execute("DELETE FROM student")
    return redirect(url_for("index"))

if __name__ == '__main__':
    # app.config.update(SECRET_KEY=os.urandom(24))
    app.secret_key = 'super secret key'
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)




    app.debug = True
    app.run()
