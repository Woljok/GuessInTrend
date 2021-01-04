from flask import Flask, abort, current_app, render_template, request, session, url_for, redirect, flash
from flask_mysqldb import MySQL
from MySQLdb import IntegrityError
import bcrypt
from database import Database


app = Flask(__name__)
app.secret_key = 'woljokerino'
db = Database("127.0.0.1",3306, "root", "furkan1907", "mydb")
mysql = MySQL(app)


@app.route("/")
def index():
    session["logged"] = False
    session["admin"] = False
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
        password = request.form.get("password").encode('utf-8')
        password2 = request.form.get("passwordNew").encode('utf-8')
        password3 = request.form.get("passwordNew2").encode('utf-8')
        fullname = request.form.get("fullname")
        mail = request.form.get("mail")
        age = request.form.get("age")
        if(bcrypt.hashpw(password,profileHolder[3].encode('utf-8')) != profileHolder[3].encode('utf-8')):
            return render_template("edit_profile.html", profile= profileHolder, message = 'ŞİFRE YANLIŞ, TEKRAR DENEYİNİZ.')
        if password2 != '':
            if password2 != password3:
                return render_template("edit_profile.html", profile= profileHolder, message = 'ŞİFRELER EŞLEŞMİYOR.')
               
        if age != '':
            if fullname != '':
                if password2 != '':
                    hashedPass = bcrypt.hashpw(password2,bcrypt.gensalt()) 
                    query = "UPDATE mydb.user SET nickname = %s, fullname = %s, password = %s, mail = %s, age = %s WHERE idUser = %s"
                    vals = (nickname, fullname, hashedPass, mail, age,str(session["idUser"]))
                    db.cursor.execute(query, vals)
                    db.con.commit()
                else:
                    query = "UPDATE mydb.user SET nickname = %s, fullname = %s, mail = %s, age = %s WHERE idUser = %s"
                    vals = (nickname, fullname, mail, age, str(session["idUser"]) )
                    db.cursor.execute(query, vals)
                    db.con.commit()
            else:
                if password2 != '':
                    hashedPass = bcrypt.hashpw(password2,bcrypt.gensalt()) 
                    query = "UPDATE mydb.user SET nickname = %s, password = %s, mail = %s, age = %s WHERE idUser = %s"
                    vals = (nickname, hashedPass, mail, age,str(session["idUser"]))
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
                    hashedPass = bcrypt.hashpw(password2,bcrypt.gensalt()) 
                    query = "UPDATE mydb.user SET nickname = %s, fullname = %s, password = %s, mail = %s WHERE idUser = %s"
                    val = (nickname, fullname, hashedPass, mail,str(session["idUser"]))
                    db.cursor.execute(query, val)
                    db.con.commit()
            else:
                if password2 == '':
                    
                    query = "UPDATE mydb.user SET nickname = %s,mail = %s WHERE idUser = %s"
                    val = (nickname, mail,str(session["idUser"]))
                    db.cursor.execute(query, val)
                    db.con.commit()
                else:
                    hashedPass = bcrypt.hashpw(password2,bcrypt.gensalt()) 
                    query = "UPDATE mydb.user SET nickname = %s,password = %s, mail = %s WHERE idUser = %s"
                    val = (nickname,hashedPass, mail,str(session["idUser"]))
                    db.cursor.execute(query, val)
                    db.con.commit()
        return redirect(url_for("profile", userNickname = nickname))

@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    query = "SELECT * FROM mydb.user ORDER BY coin DESC, fullname"
    db.cursor.execute(query)
    users = db.cursor.fetchall()
    counter = 0
    for user in users:
        userHolder = users[counter]
        userId = userHolder[0] 
        counter += 1 
        query = "UPDATE mydb.rank SET idRank = ("+ str(counter) +") WHERE userId = (" + str(userId) +")"
        db.cursor.execute(query)
        db.con.commit()
    query = "SELECT * FROM mydb.rank ORDER BY idRank"
    db.cursor.execute(query)
    leaderboard = db.cursor.fetchall()
    lenTable = len(leaderboard)
    query = "SELECT  rank.idRank, rank.userId, user.nickname, user.coin FROM mydb.rank LEFT JOIN mydb.user ON rank.userId = user.idUser ORDER BY rank.idRank"
    db.cursor.execute(query)
    mergedTables = db.cursor.fetchall()
    lenTable = len(mergedTables)
    return render_template("leaderboard.html", merged = mergedTables, lenTable = lenTable)
        
@app.route("/login", methods=["GET", "POST"])
def login():
    message = ''
    if request.method == "GET":
        return render_template("login.html")
    else:
        nickname = request.form.get("nickname")
        password = request.form.get("password").encode('utf-8')
        if nickname is not None:
            print(nickname)
            query = "SELECT * FROM mydb.user WHERE nickname = \"" + nickname + "\""
            db.cursor.execute(query)
            userChecker = db.cursor.fetchone()
            if userChecker:
                if bcrypt.hashpw(password,userChecker[3].encode('utf-8')) == userChecker[3].encode('utf-8'):
                    session["logged"] = True
                    session["idUser"] = userChecker[0]
                    session["nickname"] = userChecker[1]
                    session.permanent = True
                    if(nickname == "admin"):
                        session["admin"] = True 
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
        password = request.form.get("password").encode('utf-8')
        password2 = request.form.get("password2").encode('utf-8')
        fullname = request.form.get("fullname")
        mail = request.form.get("mail")
        age = request.form.get("age")
        if password2 != password:
            return render_template("register.html", message='ŞİFRELER EŞLEŞMİYOR. TEKRAR DENEYİNİZ..')
        hashedPass = bcrypt.hashpw(password,bcrypt.gensalt())
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
                vals = (nickname, fullname, hashedPass, mail, age)
                db.cursor.execute(query, vals)
                db.con.commit()
            else:
                query = "INSERT INTO mydb.user (nickname, password, mail, age) VALUES (%s,%s,%s,%s)"
                vals = (nickname, hashedPass, mail , age)
                db.cursor.execute(query, vals)
                db.con.commit()
        else:
            if fullname != '':
                query = "INSERT INTO mydb.user (nickname, fullname, password, mail) VALUES (%s,%s,%s,%s)"
                vals = (nickname, fullname, hashedPass, mail)
                db.cursor.execute(query, vals)
                db.con.commit()
            else:
                query = "INSERT INTO mydb.user (nickname, password, mail) VALUES (%s,%s,%s)"
                vals = (nickname, hashedPass, mail)
                db.cursor.execute(query, vals)
                db.con.commit()
        query = "SELECT idUser FROM mydb.user WHERE nickname = \"" + nickname+ "\""
        db.cursor.execute(query)
        checkUser = db.cursor.fetchone()
        idHolder = checkUser[0]
        query = "INSERT INTO mydb.rank (userId) VALUES ("+ str(idHolder) +")"
        db.cursor.execute(query)
        db.con.commit()
        return render_template("register.html", message = "BAŞARIYLA KAYIT OLDUNUZ")


@app.route("/logout")
def logout():
    session["logged"] = False
    session["nickname"] = False
    session["IdUser"] = False
    session["admin"] = False
    return redirect(url_for("index"))

@app.route("/error")
def error():
    return render_template("error.html")


if __name__ == '__main__':
    app.run(debug=True)

