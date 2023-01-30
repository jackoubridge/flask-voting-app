from flask import Flask, render_template, request, redirect, abort
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'votingsystem'
 
mysql = MySQL(app)

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login')
def login():
    return render_template('login.html', title='Login')

@app.route('/register')
def register():
    return render_template('register.html', title='Register')

@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/votes')
def home():
    return render_template('votes.html', title='Votes')

@app.route('/registerrequest', methods = ['POST', 'GET'])
def registerrequest():
    if request.method == 'GET':
        abort(404)

    elif request.method == 'POST':
        dbInsert(''' INSERT INTO users (firstname, surname, email, password) VALUES(%s,%s,%s,%s)''',
        (request.form['firstname'], request.form['surname'], request.form['email'], request.form['password']))

@app.route('/loginrequest', methods = ['POST', 'GET'])
def loginrequest():
    if request.method == 'GET':
        abort(404)

    elif request.method == 'POST':
        client_email = request.form['email']
        client_password = request.form['password']
        try:        
            db_password = dbSelect(''' SELECT password FROM users WHERE email = '%s' ''' % client_email)
            if client_password == db_password:
                return redirect('/home')
            else:
                return "Wrong Password"
        except Exception as e:
            return "Email not registered"

def dbSelect(request: str) -> str:
    cursor = mysql.connection.cursor()
    cursor.execute(request)
    data = cursor.fetchone()
    cursor.close()
    return data[0]

def dbInsert(request: str) -> str:
    cursor = mysql.connection.cursor()
    cursor.execute(request)
    mysql.connection.commit()
    cursor.close()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()