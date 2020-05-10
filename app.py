
import csv
import os

from flask import Flask, session,send_file,render_template,redirect,flash, request, url_for,jsonify, Response
from flask_session import Session
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
# Database
# from config import Config
from sqlalchemy import event, create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker

from flask_migrate import Migrate

# from sqlalchemy.exc import IntegrityError
from sqlalchemy.event import listen
from werkzeug import secure_filename
import time
import json
import barcode, random
from barcode.writer import ImageWriter

from models import Users,Students, Levels, Majors, Subjects

# from flask_wtf import FlaskForm
# from wtforms import StringField
# from wtforms.validators import DataRequired

# Import Python Docx to Generate Word File
from docx import Document
from docx.shared import Inches

document = Document()

from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter, get_page_args
#
mod = Blueprint('student', __name__)

app = Flask(__name__)

# UPLOAD_FOLDER = '/files/'
# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
# configure session to use filesystem (instead of signed cookies)
# app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
#
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
Session(app)

# DB Connection Postgress

# app.config.from_object(os.environ['APP_SETTINGS'])
# app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456789@localhost:5432/student_barcode"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# POSTGRES = {
#     'user': 'postgres',
#     'pw': 'password',
#     'db': 'student_barcode',
#     'host': 'localhost',
#     'port': '5432',
# }
# app.config['DEBUG'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
# db.init_app(app)

# engine = create_engine('postgresql://scott:tiger@localhost/mydatabase')
# migrate = Migrate(app, db)


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



# second solution
@event.listens_for(Users.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db.session.add(Users(name='Ahmed Eid',username='admin',email='ahmedmohamedeid97@gmail.com',password=generate_password_hash("admin"),is_super_user=True, is_admin=True))
    # db.session.add(Users(name='medium'))
    # db.session.add(Users(name='high'))
    db.session.commit()

# event.listen(Users.__table__, 'after_create', insert_initial_values)



   # User Register Page #
@app.route("/signup", methods=['GET','POST'])
def signup():
    # session.clear()

    if request.method == 'POST':
        # name = request.form.get("full_name")
        username = request.form.get("name")
        email = request.form.get("email")
        password = generate_password_hash(request.form.get("password"))
        print (password)
        # check_email = Users.query(db.exists().where(Users.email==email)).scalar()
        check_email = db.session.query(db.exists().where(Users.email == email)).scalar()
        print(check_email)
        if not check_email:
            user = Users(name=username,username=username,email=email,password=password)
            print(user)
            db.session.add(user)
            db.session.commit()

            # Get Username to store Session
            session['userid'] = user.id
            session['username'] = user.username
            # redirect to Home
            return redirect("/")
        else:
            msg = "Theis User is already Exist!"
            print(msg)
            return render_template("signup.html", message=msg)
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
    # session.clear()
    if request.method == "POST":
        email = request.form.get("username")
        password = request.form.get("password")
        hash_password = generate_password_hash(password)
        result = Users.query.filter_by(email=email).first()
        print(result.status)
        #
        if result:
            if check_password_hash(result.password, password) and result.status == True:
                session["user_id"] = result.id
                session["user_name"] = result.name
                session["is_super_user"] = result.is_super_user
                session["is_admin"] = result.is_admin
                result.last_login = time.strftime('%A %B, %d %Y %H:%M:%S')
                print(result.last_login)
                db.session.commit()
                return redirect('/')
            else:
                # flash('Invalid email or password')
                message = "error in Password or username"
                print("Error")
                return redirect("/login")
        else:
            message = "Incorrect Email"
            return render_template("login.html",message="message")

    return render_template('login.html')

# if not current_user.is_authenticated:
#     return current_app.login_manager.unauthorized()
#
# @bull.route("/login", methods=["GET", "POST"])
# def login():
#     """For GET requests, display the login form.
#     For POSTS, login the current user by processing the form.
#
#     """
#     print (db)
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.get(form.email.data)
#         if user:
#             if bcrypt.check_password_hash(user.password, form.password.data):
#                 user.authenticated = True
#                 db.session.add(user)
#                 db.session.commit()
#                 login_user(user, remember=True)
#                 return redirect(url_for("bull.reports"))
#     return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    # logout_user()
    session.clear()
    return redirect('/login')


# @mod.route('/')
# def index():
#     # search = False
#     # q = request.args.get('q')
#     # if q:
#     #     search = True
#     #
#     # page = request.args.get(get_page_parameter(), type=int, default=1)
#     #
#     # users = User.find(...)
#     # pagination = Pagination(page=page, total=users.count(), search=search, record_name='users')
#     # # 'page' is the default name of the page parameter, it can be customized
#     # # e.g. Pagination(page_parameter='p', ...)
#     # # or set PAGE_PARAMETER in config file
#     # # also likes page_parameter, you can customize for per_page_parameter
#     # # you can set PER_PAGE_PARAMETER in config file
#     # e.g. Pagination(per_page_parameter='pp')
#
#     return render_template('/index.html',users=users,)
#
# def get_data():
#     majors =  Majors.query.all(),
#     levels =  Levels.query.all(),




@app.route('/setting')
@login_required
def setting():
    majors =  Majors.query.all(),
    levels =  Levels.query.all(),
    if session["is_super_user"]:
        users  =  Users.query.filter(Users.id != session["user_id"]).all()
    else:
        users  =  Users.query.filter(Users.id != session["user_id"], Users.is_super_user == None).all()
        print(users)

    # rows = {
    #     levels: levels[0],
    # }
    return render_template('setting.html', users=users, levels=levels[0], majors=majors[0])

@app.route('/adduser', methods=["POST"])
@login_required
def users():
    if request.method == 'POST':
        username = request.form.get("name")
        email = request.form.get("email")
        password = generate_password_hash(request.form.get("password"))
        is_admin = request.form.get("is_admin")
        is_user = request.form.get("is_user")
        status = request.form.get("status")
        if is_admin == "1":
            is_admin = True
        else:
            is_admin = False

        if is_user == "1":
            is_user = True
        else:
            is_user = False

        if status == "1":
            status = True
        else:
            status = False

        print(is_user)
        check_email = db.session.query(db.exists().where(Users.email == email)).scalar()
        if not check_email:
            user = Users(name=username,username=username,email=email,password=password, is_admin=is_admin, is_user=is_user, status=status)
            db.session.add(user)
            db.session.commit()
        flash("تم أضافة المستخدم بنجاح!")
        return redirect("/setting")
    else:
        flash("Error!")
        return redirect("/setting")


@app.route('/major', methods=["POST"])
def major():
    name = request.form.get("name")
    levels = request.form.getlist("levels")

    print(levels)
    major = Majors(name=name )
    db.session.add(major)
    db.session.commit()
    current_major = Majors.query.filter_by(name=name).first()
    print(current_major.id)
    # for level in levels:
    #     # level_id = Levels.query.filter_by(name=level)
    #     add = Majors.levels(level_id=level, major_id=current_major.id)
    #     print(add)
    # db.session.commit()
    # print("list :",level_list)
    #
    # # major.levels.append(levels)
    # # level = Levels(name=name,notes=notes)
    # print(major)
    # # db.session.add(major)
    # db.session.commit()
    return redirect("/setting")

def get_users(offset=0, per_page=10):
    return users[offset: offset + per_page]

@app.route('/')
@app.route('/index')
@login_required
def index():

    majors =  Majors.query.all()
    levels =  Levels.query.all()
    print(majors)
    # page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
    # Print(page)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    print(page)

    # users = student.find(...)
    # rows = db.execute("SELECT * FROM student").fetchall()
    rows = Students.query.all()
    # print(rows)
    pagination = Pagination(page=page, css_framework="bootstrap4",total=len(rows), record_name='rows')
    print(pagination)
    return render_template("index.html", pagination=pagination ,students=rows,majors=majors, levels=levels)

#
#
#
@app.route("/upload", methods=["GET","POST"])
@login_required
def student_upload_data():
    """Upload Student Data."""

    if request.method == "POST":
        major = request.form.get("major")
        level = request.form.get("level")
        file = request.files['student_file']
        file.save(secure_filename(file.filename))

        file = open(file.filename)
        students = csv.reader(file)

        for ui_code,name in students:
            students = Students(name=name,un_id=ui_code,major_id=major,level_id=level)
            db.session.add(students)
        db.session.commit()
        print(file)
    return redirect(url_for("index"))

    # else:
    #     return render_template("register.html")
#

@app.route('/students')
@login_required
def all_student():
    majors =  Majors.query.all()
    levels =  Levels.query.all()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    # print(page)
    rows = Students.query.all()
    rowss = {
        "students":rows,
    }
    major_level_dec = []
    for row in rows:
        # print(row.major_id.)
        major =  Majors.query.get(row.major_id)
        level =  Levels.query.get(row.level_id)
        major_level_dec.append({
        "student_id": row.id,
        "major":major.name,
        "level": level.name
        })
    rowss["data"] = major_level_dec
    # print("================",rowss)
        # print(major_level_dec)
    pagination = Pagination(page=page, css_framework="bootstrap4",total=len(rows), record_name='rows')
    # print(pagination)

    return render_template("student.html", pagination=pagination ,rows=rowss,major_level=major_level_dec,majors=majors,levels=levels )

# @app.route('/user/<username>')
# def profile(username):
#     ...
#
# @app.route('/<int:year>/<int:month>/<title>')
# def article(year, month, title):

@app.route('/student/<int:id>')
@login_required
def student(id):
    row = Students.query.get(id)
    major_id =  Majors.query.get(row.major_id)
    level_id =  Levels.query.get(row.level_id)

    return render_template("student_data.html",student=row,major=major_id,level=level_id )


#
# from sqlalchemy.ext.declarative import DeclarativeMeta
#
# class AlchemyEncoder(json.JSONEncoder):
#
#     def default(self, obj):
#         if isinstance(obj.__class__, DeclarativeMeta):
#             # an SQLAlchemy class
#             fields = {}
#             for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
#                 data = obj.__getattribute__(field)
#                 try:
#                     json.dumps(data) # this will fail on non-encodable values, like other classes
#                     fields[field] = data
#                 except TypeError:
#                     fields[field] = None
#             # a json-encodable dict
#             return fields
#
#         return json.JSONEncoder.default(self, obj)
#
# # c = YourAlchemyClass()
# # print (json.dumps(c, cls=AlchemyEncoder))
#
# @app.route('/search', methods=["GET","POST"])
# def search():
#     if request.method == 'GET':
#         text = request.args['searchText']
#         # search_data = request.form.get('search_data')
#         # print(search_data)
#         search = "%{}%".format(text)
#         result = Students.query.filter(Students.name.like(search)).all()
#
#         print(json.dumps(result, cls=AlchemyEncoder))
#         return json.dumps({"success": True, 'data':json.dumps(result, cls=AlchemyEncoder)})
#         # return render_template("student.html", pagination=pagination ,rows=rowss,major_level=major_level_dec,majors=majors,levels=levels )
#
from sqlalchemy import and_, or_, not_
@app.route('/search', methods=["GET","POST"])
def search():
    if request.method == 'POST':
        text = request.form.get('search_data')
        major_search = request.form.get('major_filter')
        level_search = request.form.get('level_filter')

        if isinstance(text, int):
            result = Students.query.filter(Students.un_id == text ).all()
        elif isinstance(text, str):
            search = "%{}%".format(text)
            result = Students.query.filter(Students.name.like(search) ).all()

        if major_search and level_search:
            result = Students.query.filter(Students.major_id == major_search,Students.level_id == level_search).all()
        majors =  Majors.query.all()
        levels =  Levels.query.all()
        page = request.args.get(get_page_parameter(), type=int, default=1)
        # print(page)

        rowss = {
            "students":result,
        }
        major_level_dec = []
        for row in result:
            # print(row.major_id.)
            major =  Majors.query.get(row.major_id)
            level =  Levels.query.get(row.level_id)
            major_level_dec.append({
            "student_id": row.id,
            "major":major.name,
            "level": level.name
            })
        rowss["data"] = major_level_dec
        # print("================",rowss)
            # print(major_level_dec)
        pagination = Pagination(page=page, css_framework="bootstrap4",total=len(result), record_name='rows')
        # print(pagination)

        return render_template("student.html", pagination=pagination ,rows=rowss,major_level=major_level_dec,majors=majors,levels=levels )




# Generate Word File
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_DIRECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH


@login_required
@app.route("/generate_word_file/<int:id>")
def generate_word_file(id):
    # style.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
    row = Students.query.get(id)
    major_id =  Majors.query.get(row.major_id)
    level_id =  Levels.query.get(row.level_id)

    head_title = document.add_heading(row.name, 0)
    head_title.alignment = WD_ALIGN_PARAGRAPH.CENTER


    # document.add_heading('Heading, level 1', level=1)
    nu_id = document.add_paragraph('الكود الجامعي : {}'.format(row.un_id))
    nu_id.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    major = document.add_paragraph('الشعبة : {}'.format(major_id.name))
    major.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    level = document.add_paragraph('الفرقة : {}'.format(level_id.name))
    level.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    subjects = document.add_paragraph('المواد الدراسية : ')
    subjects.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    document.add_picture('icon.png', width=Inches(1.25))
    #
    # table = document.add_table(row =3, cols= 3)
    # table.direction = WD_TABLE_DIRECTION.RTL

    document.add_page_break()
    path = document.save('demo-{}.docx'.format(row.un_id))
    print(path)
    return redirect(url_for('all_student'))
    # return send_file(path, as_attachment=True, attachment_filename="demo.docx")

#
# @app.route("/generate_png", methods=["GET", "POST"])
# def generate_png():
#
#     if request.method == "POST":
#         # num = random.randrange(1,00)
#         rows = db.execute("SELECT * FROM student").fetchall()
#         if rows:
#             for row in rows:
#                 num = "00{}".format(row[2])
#                 name = row[1]
#                 print (num)
#                 EAN = barcode.get_barcode_class('ean8')
#                 ean = EAN(u"{}".format(num),  writer=ImageWriter())
#                 fullname = ean.save(u'{}-{}'.format(num,name), text=name)
#     return redirect(url_for("index"))
#
@app.route("/generate_svg", methods=["GET", "POST"])
def generate_svg():
    if request.method == "POST":
        # num = random.randrange(1,00)
        path = ""
        rows = Students.query.filter(Students.barcode_path == None).all()
        # rows = db.execute("SELECT * FROM student WHERE barcode_path IS NULL;").fetchall()
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

                num = "00{}".format(row.un_id)
                name = row.name
                print (num)
                EAN = barcode.get_barcode_class('ean8')
                ean = EAN(u"{}".format(num))


                filenum = random.randrange(1,1000)
                fullname = ean.save(u'{}-{}'.format(num,filenum), text=name)
                path = "barcode_path/{}-{}.svg".format(num,filenum)
                st_img_path = Students.query.get(row.id)
                st_img_path.barcode_path = path
                print(st_img_path.barcode_path)
                print(time.strftime('%A %B, %d %Y %H:%M:%S'))
                st_img_path.update_at = time.strftime('%A %B, %d %Y %H:%M:%S')
                print(fullname)
                # db.execute("UPDATE student SET barcode_path=:barcode_path WHERE id=:id",{"barcode_path":path, "id":row[0]})
                db.session.commit()
    return redirect(url_for("all_student"))
#
#
@app.route("/delete_all", methods=["POST", "GET"])
def delete_all():
    if request.method == "POST":
        # db.execute("DELETE FROM student")
        Students.query.delete()
        db.session.commit()
    return redirect(url_for("index"))


# import os
# @app.route("/print_image", methods=['GET'])
# def print_image():
#     return os.startfile("icon.png", "print")


if __name__ == '__main__':
    # app.config.update(SECRET_KEY=os.urandom(24))
    # app.secret_key = 'super secret key'
    # app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)




    app.debug = True
    app.run()
