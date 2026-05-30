from flask import Flask, render_template, request, redirect
import sqlite3
app = Flask(__name__)



# Connect to the SQLite database
DB_NAME = 'students.db'
STUDENTS_ROUTE = '/students'
def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute('''
                create table if not exists students(
                    id integer primary key autoincrement,
                    name text not null,
                    age integer,
                    course text
                )
                ''')
    conn.close()
@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    
    cursor = conn.execute("select count(*) from students")
    total_students = cursor.fetchone()[0]
    
    conn.close()
    
    return render_template('index.html', total_students=total_students)

@app.route('/add', methods=['GET','POST'])
def add_student():
    if request.method == 'POST':
        
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']
        
        conn = sqlite3.connect(DB_NAME)
        conn.execute(
            "insert into students (name, age, course) values (? , ? , ? )", (name, age, course)
        )
        conn.commit()
        print("student added successfully")
        conn.close()
        return redirect('/students')
    return render_template('add.html')

@app.route('/students')
def students():
    search = request.args.get('search')
    
    conn = sqlite3.connect(DB_NAME)
    
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
    conn = sqlite3.connect(DB_NAME)
    conn.execute("delete from students where id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(STUDENTS_ROUTE)

@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit_student(id):
    conn = sqlite3.connect(DB_NAME)
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']
        conn.execute(
            "UPDATE students SET name=?, age=?, course=? WHERE id=?",(name,age,course,id)
        )
        conn.commit()
        conn.close()
        return redirect(STUDENTS_ROUTE)
    
    cursor = conn.execute("select * from students WHERE id =?",(id,))
    student = cursor.fetchone()
    conn.close()
    return render_template('edit.html', student=student)
if __name__ == '__main__':
    init_db()
    app.run(debug=True)