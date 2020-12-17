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
        username = request.form("username")
        password = request.form("password")
        if username and password:
            query = "SELECT * FROM mydb.user WHERE username = \"" + username + "\""
            db.cursor.execute(query)
            passChecker = db.cursor.fetchone()
            if passChecker:
                if passChecker[3] == password:
                else:    
            
            else:
                message = 'BU KULLANICI ADIYLA BİR KAYIT BULUNAMADI.'
                return render_template("login.html", message)
        else:
            flash("EKSİK DOLDURDUNUZ","danger")
            return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")

if __name__ == '__main__':
    app.run(debug=True)

