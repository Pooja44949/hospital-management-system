from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="8287290108pooja",
    database="hospital_db"
)

cur = db.cursor()

# HOME PAGE
@app.route('/')
def index():
    cur.execute("""
    SELECT Patients.patient_id, Patients.name, Patients.age, Patients.gender,
           Doctors.name AS doctor_name,
           Appointments.appointment_date,
           Treatments.diagnosis
    FROM Patients
    LEFT JOIN Appointments ON Patients.patient_id = Appointments.patient_id
    LEFT JOIN Doctors ON Doctors.doctor_id = Appointments.doctor_id
    LEFT JOIN Treatments ON Treatments.patient_id = Patients.patient_id
    """)
    
    data = cur.fetchall()
    return render_template('index.html', data=data)

# ADD PATIENT
@app.route('/add', methods=['GET','POST'])
def add():
    cur.execute("SELECT * FROM Doctors")
    doctors = cur.fetchall()

    if request.method == 'POST':
        pid = request.form['id']
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        phone = request.form['phone']
        doctor_id = request.form['doctor']
        date = request.form['date']
        diagnosis = request.form['diagnosis']

        cur.execute("INSERT INTO Patients VALUES (%s,%s,%s,%s,%s)",
                    (pid,name,age,gender,phone))

        cur.execute("INSERT INTO Appointments (patient_id, doctor_id, appointment_date) VALUES (%s,%s,%s)",
                    (pid,doctor_id,date))

        cur.execute("INSERT INTO Treatments (patient_id, diagnosis, treatment_details) VALUES (%s,%s,%s)",
                    (pid,diagnosis,"Treatment ongoing"))

        db.commit()
        return redirect('/')

    return render_template('add.html', doctors=doctors)

# DELETE
@app.route('/delete/<int:id>')
def delete(id):
    cur.execute("DELETE FROM Patients WHERE patient_id=%s",(id,))
    cur.execute("DELETE FROM Appointments WHERE patient_id=%s",(id,))
    cur.execute("DELETE FROM Treatments WHERE patient_id=%s",(id,))
    db.commit()
    return redirect('/')

# EDIT
@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    if request.method == 'POST':
        cur.execute("""
        UPDATE Patients SET name=%s, age=%s, gender=%s, phone=%s
        WHERE patient_id=%s
        """,
        (request.form['name'],
         request.form['age'],
         request.form['gender'],
         request.form['phone'],
         id))

        db.commit()
        return redirect('/')

    cur.execute("SELECT * FROM Patients WHERE patient_id=%s",(id,))
    data = cur.fetchone()
    return render_template('edit.html', data=data)

app.run(debug=True)