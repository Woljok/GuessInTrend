from flask import Flask, abort, current_app, render_template, request, session, url_for, redirect, flash
from flask_mysqldb import MySQL
from MySQLdb import IntegrityError
from database import Database


app = Flask(__name__)
app.secret_key = 'woljokerino'
db = Database("127.0.0.1",3306, "root", "furkan1907", "mydb")
mysql = MySQL(app)


@app.route("/")
def index():
    session["logged"] = False
    return render_template("index.html")

@app.route("/home")
def home_page():
    boolUser = False
    if session["logged"] == True:
        boolUser = True
        return render_template("home.html", boolUser= boolUser, nickname = session["nickname"])
    else:
        return render_template("home.html", boolUser= boolUser)
   


@app.route("/profile/<string:userNickname>")
def profile(userNickname):
    print("geldi")
    if session["logged"] == True:
        query = "SELECT * FROM mydb.user WHERE idUser = \"" + str(session["idUser"]) + "\""
        db.cursor.execute(query)
        profileHolder = db.cursor.fetchone()
        return render_template("profile.html", profile = profileHolder)
    else:
        return redirect(url_for("error"))

@app.route("/profile/<string:userNickname>/edit", methods=["GET", "POST"])
def editProfile(userNickname):
    if request.method == "GET":
        if session["logged"] == True:
            query = "SELECT * FROM mydb.user WHERE idUser = \"" + str(session["idUser"]) + "\""
            db.cursor.execute(query)
            profileHolder = db.cursor.fetchone()
            return render_template("edit_profile.html", profile = profileHolder)
        else:
            return redirect(url_for("error"))
    else:
        query = "SELECT * FROM mydb.user WHERE idUser = \"" + str(session["idUser"]) + "\""
        db.cursor.execute(query)
        profileHolder = db.cursor.fetchone()
        nickname = request.form.get("nickname")
        password = request.form.get("password")
        password2 = request.form.get("passwordNew")
        password3 = request.form.get("passwordNew2")
        fullname = request.form.get("fullname")
        mail = request.form.get("mail")
        age = request.form.get("age")
        if(profileHolder[3] != password):
            return render_template("edit_profile.html", profile= profileHolder, message = 'ŞİFRE YANLIŞ, TEKRAR DENEYİNİZ.')
        if password2 != '':
            if password2 != password3:
                return render_template("edit_profile.html", profile= profileHolder, message = 'ŞİFRELER EŞLEŞMİYOR.')
        if age != '':
            if fullname != '':
                if password2 != '':
                    query = "UPDATE mydb.user SET nickname = %s, fullname = %s, password = %s, mail = %s, age = %s WHERE idUser = %s"
                    vals = (nickname, fullname, password2, mail, age,str(session["idUser"]))
                    db.cursor.execute(query, vals)
                    db.con.commit()
                else:
                    query = "UPDATE mydb.user SET nickname = %s, fullname = %s, mail = %s, age = %s WHERE idUser = %s"
                    vals = (nickname, fullname, mail, age, str(session["idUser"]) )
                    db.cursor.execute(query, vals)
                    db.con.commit()
            else:
                if password2 != '':
                    query = "UPDATE mydb.user SET nickname = %s, password = %s, mail = %s, age = %s WHERE idUser = %s"
                    vals = (nickname, password2, mail, age,str(session["idUser"]))
                    db.cursor.execute(query, vals)
                    db.con.commit()
                else:
                    query = "UPDATE mydb.user SET nickname = %s, mail = %s, age = %s WHERE idUser = %s"
                    vals = (nickname, mail, age,str(session["idUser"]))
                    db.cursor.execute(query, vals)
                    db.con.commit()
        else:
            if fullname != '':
                if password2 == '':
                    query = "UPDATE mydb.user SET nickname = %s, fullname = %s, mail = %s WHERE idUser = %s"
                    val = (nickname, fullname, mail,str(session["idUser"]))
                    db.cursor.execute(query, val)
                    db.con.commit()
                else:
                    query = "UPDATE mydb.user SET nickname = %s, fullname = %s, password = %s, mail = %s WHERE idUser = %s"
                    val = (nickname, fullname, password2, mail,str(session["idUser"]))
                    db.cursor.execute(query, val)
                    db.con.commit()
            else:
                if password2 == '':
                    query = "UPDATE mydb.user SET nickname = %s,mail = %s WHERE idUser = %s"
                    val = (nickname, mail,str(session["idUser"]))
                    db.cursor.execute(query, val)
                    db.con.commit()
                else:
                    query = "UPDATE mydb.user SET nickname = %s,password = %s, mail = %s WHERE idUser = %s"
                    val = (nickname,password2, mail,str(session["idUser"]))
                    db.cursor.execute(query, val)
                    db.con.commit()
        return redirect(url_for("profile", userNickname = nickname))

        


@app.route("/login", methods=["GET", "POST"])
def login():
    message = ''
    if request.method == "GET":
        return render_template("login.html")
    else:
        nickname = request.form.get("nickname")
        password = request.form.get("password")
        if nickname is not None:
            print(nickname)
            query = "SELECT * FROM mydb.user WHERE nickname = \"" + nickname + "\""
            db.cursor.execute(query)
            userChecker = db.cursor.fetchone()
            if userChecker:
                if userChecker[3] == password:
                    session["logged"] = True
                    session["idUser"] = userChecker[0]
                    session["nickname"] = userChecker[1]
                    session.permanent = True 
                    return redirect(url_for("home_page"))
                else:    
                    return render_template("login.html",message = 1)
            else:
                return render_template("login.html", message = 2)
        else:
            return render_template("login.html", message = 3)


@app.route("/register", methods=["POST","GET"])
def register():
    message =''
    if request.method == "GET":
        return render_template("register.html")
    else:
        nickname = request.form.get("nickname")
        password = request.form.get("password")
        password2 = request.form.get("password2")
        fullname = request.form.get("fullname")
        mail = request.form.get("mail")
        age = request.form.get("age")
        if password2 != password:
            return render_template("register.html", message='ŞİFRELER EŞLEŞMİYOR. TEKRAR DENEYİNİZ..')
        query = "SELECT * FROM mydb.user WHERE mail = \"" + mail + "\""
        db.cursor.execute(query)
        checkMail = db.cursor.fetchone()
        if checkMail is not None:
            return render_template("register.html", message='BU MAİLLE BİR KAYIT ZATEN VAR.')
        query = "SELECT * FROM mydb.user WHERE nickname = \"" + nickname+ "\""
        db.cursor.execute(query)
        checkUser = db.cursor.fetchone()
        if checkUser is not None:
            return render_template("register.html", message="BU KULLANICI ADI KULLANIMDA")
        if age != '':
            if fullname != '':
                query = "INSERT INTO mydb.user (nickname, fullname, password, mail, age) VALUES (%s,%s,%s,%s,%s)"
                vals = (nickname, fullname, password, mail, age)
                db.cursor.execute(query, vals)
                db.con.commit()
            else:
                query = "INSERT INTO mydb.user (nickname, password, mail, age) VALUES (%s,%s,%s,%s)"
                vals = (nickname, password, mail , age)
                db.cursor.execute(query, vals)
                db.con.commit()
        else:
            if fullname != '':
                query = "INSERT INTO mydb.user (nickname, fullname, password, mail) VALUES (%s,%s,%s,%s)"
                vals = (nickname, fullname, password, mail)
                db.cursor.execute(query, vals)
                db.con.commit()
            else:
                query = "INSERT INTO mydb.user (nickname, password, mail) VALUES (%s,%s,%s)"
                vals = (nickname, password, mail)
                db.cursor.execute(query, vals)
                db.con.commit()
        return render_template("register.html", message = "BAŞARIYLA KAYIT OLDUNUZ")


@app.route("/logout")
def logout():
    session["logged"] = False
    session["nickname"] = False
    session["IdUser"] = False
    return redirect(url_for("home"))

@app.route("/error")
def error():
    return render_template("error.html")


if __name__ == '__main__':
    app.run(debug=True)

