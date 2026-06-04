import os
import sqlite3
from flask import Flask, render_template, request, redirect, session, flash
from datetime import datetime

SECRET_KEY = "student_management_secret"
app = Flask(__name__)
app.secret_key = SECRET_KEY




# Connect to the SQLite database
DB_NAME = 'students.db'
STUDENTS_ROUTE = '/students'
LOGIN_ROUTE = '/login'
SECRET_KEY = "student_management_secret"

app.secret_key = SECRET_KEY
def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute('''
                create table if not exists students(
                    id integer primary key autoincrement,
                    name text not null,
                    age integer,
                    course text,
                    email TEXT,
                    phone TEXT,
                    address TEXT,
                    created_at TEXT
                )
                ''')
    print(os.path.abspath(DB_NAME))
    conn.commit()
    conn.close()
    print("column added")
    
@app.route('/')
def index():
    print("index is opened")
    conn = sqlite3.connect(DB_NAME)
    
    cursor = conn.execute("select count(*) from students")
    total_students = cursor.fetchone()[0]
    
    conn.close()
    
    if 'user' not in session:
        return redirect(LOGIN_ROUTE)
    
    return render_template('index.html', total_students=total_students)

@app.route(LOGIN_ROUTE, methods=['GET','POST'])
def login():
    
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'admin@132':
            
            session['user'] = username
            
            return redirect('/')
        return "invalid username or password"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(LOGIN_ROUTE)

@app.route('/add', methods=['GET','POST'])
def add_student():
    if 'user' not in session:
        return redirect(LOGIN_ROUTE)
    if request.method == 'POST':
        
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form.get('address')
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn = sqlite3.connect(DB_NAME)
        conn.execute(
            "insert into students (name, age, course, email, phone, address, created_at) values (? , ? , ?, ?, ?, ?, ?)", (name, age, course, email, phone, address, created_at)
        )
        conn.commit()
        flash("student added successfully")
        print("student added successfully")
        conn.close()
        return redirect(STUDENTS_ROUTE)
    return render_template('add.html')

@app.route('/students')
def students():
    
    conn = sqlite3.connect(DB_NAME)
    
    if 'user' not in session:
        return redirect(LOGIN_ROUTE)
    
    search = request.args.get('search')
    
    if search:
        cursor = conn.execute("select * from students where name like ?", ('%' + search + '%',))
    else:
        cursor = conn.execute("select * from students")
    student_data = cursor.fetchall()
    print(student_data)
    conn.close()
    return render_template('students.html', students=student_data)

@app.route('/delete/<int:id>')
def delete_student(id):
    if 'user' not in session:
        return redirect(LOGIN_ROUTE)
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DELETE FROM students WHERE id = ?", (id,))
    conn.commit()
    flash("student deleted successfully")
    conn.close()
    return redirect(STUDENTS_ROUTE)

@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit_student(id):
    if 'user' not in session:
        return redirect(LOGIN_ROUTE)
    conn = sqlite3.connect(DB_NAME)
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        conn.execute(
            "UPDATE students SET name=?, age=?, course=?, email=?, phone=?, address=? WHERE id=?",(name,age,course,email,phone,address,id)
        )
        conn.commit()
        flash("student updated successfully")
        conn.close()
        return redirect(STUDENTS_ROUTE)
    
    cursor = conn.execute("select * from students WHERE id =?",(id,))
    student = cursor.fetchone()
    conn.close()
    return render_template('edit.html', student=student)
if __name__ == '__main__':
    init_db()
    app.run(debug=True)