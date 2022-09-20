from flask import Flask, request, render_template
from flask_mysqldb import MySQL

import flask
import MySQLdb.cursors
import json

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'dbcontainer'
app.config['MYSQL_USER'] = 'example_user'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'example'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

@app.route('/professors', methods=['GET'])
def professor_list_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM professor')
    data = cursor.fetchall()
    resp = flask.Response(json.dumps(data))
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/createProfessor', methods=['GET'])
def send_to_create_page():
    return render_template('registerProfessors.html')

@app.route('/professors', methods=['POST'])
def professor_post_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    city = request.form['city']
    address = request.form['address']
    salary = request.form['salary']
    cursor.execute("INSERT INTO professor (first_name, last_name, city, address, salary) VALUES ('%s', '%s', '%s', '%s', %i)" % 
                   (first_name, last_name, city, address, float(salary)))
    
    mysql.connection.commit()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM professor')
    data = cursor.fetchall()
    return render_template('professorList.html', professors=data)

@app.route('/editProfessor', methods=['POST'])
def send_to_edit_page():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    id = request.form['id']
    cursor.execute('SELECT * FROM professor WHERE id=%i'% 
                   (int(id)))
    data = cursor.fetchall()
    return render_template('editProfessors.html', professor=data)

@app.route('/modifyProfessor', methods=['POST'])
def professor_put_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    id = request.form['id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    city = request.form['city']
    address = request.form['address']
    salary = request.form['salary']
    cursor.execute("UPDATE professor SET first_name='%s', last_name='%s', city='%s', address='%s', salary=%i WHERE id=%i" % 
                   (first_name, last_name, city, address, float(salary), int(id)))
    
    mysql.connection.commit()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM professor')
    data = cursor.fetchall()
    return render_template('professorList.html', professors=data)

@app.route('/deleteProfessor', methods=['POST'])
def professor_del_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    id = request.form['id']
    cursor.execute("DELETE FROM professor WHERE id=%i" % 
                   (int(id)))
    
    mysql.connection.commit()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM professor')
    data = cursor.fetchall()
    return render_template('professorList.html', professors=data)

@app.route('/professorlist', methods=['GET'])
def professor_list():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM professor')
    data = cursor.fetchall()
    return render_template('professorList.html', professors=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
