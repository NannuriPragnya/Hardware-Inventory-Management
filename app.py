from flask import Flask, render_template, request, redirect
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DB_PATH = os.path.join("db", "inventory.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_weapon', methods=['GET', 'POST'])
def add_weapon():
    if request.method == 'POST':
        name = request.form['name']
        type_ = request.form['type']
        range_ = request.form['range']
        functionality = request.form['functionality']
        quantity = int(request.form['quantity'])

        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO Weapons (weapon_name, type, range, functionality) VALUES (?, ?, ?, ?)",
                    (name, type_, range_, functionality))
        weapon_id = cur.lastrowid
        cur.execute("INSERT INTO Inventory (weapon_id, quantity) VALUES (?, ?)", (weapon_id, quantity))
        conn.commit()
        conn.close()
        return redirect('/view_weapons')
    return render_template('add_weapon.html')

@app.route('/view_weapons')
def view_weapons():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT w.*, i.quantity FROM Weapons w
        JOIN Inventory i ON w.weapon_id = i.weapon_id
    """)
    weapons = cur.fetchall()
    conn.close()
    return render_template('view_weapons.html', weapons=weapons)

@app.route('/assign_weapon', methods=['GET', 'POST'])
def assign_weapon():
    conn = get_db()
    cur = conn.cursor()
    if request.method == 'POST':
        weapon_id = request.form['weapon_id']
        officer_id = request.form['officer_id']
        assigned_date = datetime.now().strftime('%Y-%m-%d')
        cur.execute("INSERT INTO Assigned (weapon_id, officer_id, assigned_date) VALUES (?, ?, ?)",
                    (weapon_id, officer_id, assigned_date))
        conn.commit()
        return redirect('/assigned')
    
    cur.execute("SELECT * FROM Weapons")
    weapons = cur.fetchall()
    cur.execute("SELECT * FROM PoliceOfficers")
    officers = cur.fetchall()
    return render_template('assign_weapon.html', weapons=weapons, officers=officers)

@app.route('/assigned')
def assigned():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.assigned_date, w.weapon_name, p.name as officer_name, p.rank 
        FROM Assigned a
        JOIN Weapons w ON a.weapon_id = w.weapon_id
        JOIN PoliceOfficers p ON a.officer_id = p.officer_id
    """)
    data = cur.fetchall()
    conn.close()
    return render_template('assigned.html', assignments=data)

@app.route('/add_officer', methods=['GET', 'POST'])
def add_officer():
    if request.method == 'POST':
        name = request.form['name']
        rank = request.form['rank']
        department = request.form['department']
        conn = get_db()
        conn.execute("INSERT INTO PoliceOfficers (name, rank, department) VALUES (?, ?, ?)",
                     (name, rank, department))
        conn.commit()
        conn.close()
        return redirect('/assign_weapon')
    return render_template('add_officer.html')

if __name__ == '__main__':
    app.run(debug=True)
