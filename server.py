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
    query = "SELECT * FROM mydb.user"
    db.cursor.execute(query)
    myresult = db.cursor.fetchall()
    return render_template("index.html",data=myresult)




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
                    return redirect(url_for("home.html"))
                else:    
                    return render_template("login.html",message = 'ŞİFRE YANLIŞ, TEKRAR DENEYİNİZ.')
            else:
                return render_template("login.html", message = 'BU KULLANICI ADIYLA BİR KAYIT BULUNAMADI, KAYIT OLMAK İSTER MİSİNİZ?')
        else:
            return render_template("login.html", message = 'EKSİK DOLDURDUNUZ')


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
            if mail != '':
                query = "INSERT INTO mydb.user (nickname, fullname, password, mail, age) VALUES (%s,%s,%s,%s,%s)"
                val = (nickname, fullname, password, mail, age)
                db.cursor.execute(query, val)
                db.con.commit()
            else:
                query = "INSERT INTO mydb.user (nickname, fullname, password, age) VALUES (%s,%s,%s,%s)"
                val = (nickname, fullname, password, age)
                db.cursor.execute(query, val)
                db.con.commit()
        else:
            if mail != '':
                query = "INSERT INTO mydb.user (nickname, fullname, password, mail) VALUES (%s,%s,%s,%s)"
                val = (nickname, fullname, password, mail)
                db.cursor.execute(query, val)
                db.con.commit()
            else:
                query = "INSERT INTO mydb.user (nickname, fullname, password) VALUES (%s,%s,%s)"
                vals = (nickname, fullname, password)
                db.cursor.execute(query, vals)
                db.con.commit()
        return render_template("register.html", message = "BAŞARIYLA KAYIT OLDUNUZ")




if __name__ == '__main__':
    app.run(debug=True)

