from flask import Flask,render_template,url_for,request
from flaskext.mysql import MySQL
#import mysql.connector
#from flask_mysql import MySQL

app=Flask(__name__,template_folder='template')

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="Vedang@9"
app.config["MYSQL_DB"]="travelapp"

#mydb=MySQL(app)  
mysql = MySQL()
mysql.init_app(app)
#cur=mysql.get_db().cursor()

#mycursor=mydb.connection.cursor()  

@app.route('/')
def travelapp():
    return render_template("Travel app.html")

@app.route('/signup',methods=["GET","POST"])
def signup():
    if request.method=="POST":
        details=request.form
        firstname=details["firstname"]
        lastname=details["lastname"]
        number=details["number"]
        username=details["username"]
        password=details["password"]
        cur=mysql.get_db().cursor()
        #cur=mysql.connection.cursor()   
        cur.execute("INSERT INTO user(firstname,lastname,number,username,password) VALUES (?,?,?,?,?)",(firstname,lastname,number,username,password))
        mysql.connection.commit
        cur.close()
        return "Success"
    return render_template("sign up.html")

if __name__=="__main__":
    app.run(debug=True)