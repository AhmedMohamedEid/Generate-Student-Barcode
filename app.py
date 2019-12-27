
import csv
import os

from flask import Flask, session,render_template,redirect, request, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug import secure_filename
import sqlite3

import barcode, random
from barcode.writer import ImageWriter

UPLOAD_FOLDER = '/files/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = sqlite3.connect('student.db', check_same_thread=False)


@app.route('/')
def index():
    rows = db.execute("SELECT * FROM student").fetchall()
    print(rows)

    return render_template("index.html", students=rows)




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

        rows = db.execute("SELECT * FROM student").fetchall()
        barcode_path = "student_barcode/"
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
    app.run()
