from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import csv

app = Flask(__name__)

DB_PATH = "research_data.db"

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS research_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            age INTEGER,
            sex TEXT,
            diagnosis TEXT,
            doa TEXT,
            dod TEXT,
            discharge_status TEXT,
            organism TEXT,
            antibiotic TEXT,
            comorbidities TEXT,
            apache_ii INTEGER,
            sofa_score INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    organisms = [
        "Burkholderia", "Candida", "Elizabethkingia",
        "Klebsiella Pneumoniae (CRE)", "Scrub Typhus", "Stenotrophomonas Maltophilia"
    ]
    antibiotics = [
        "Ceftriaxone", "Cefoperazone Sulbactam", "Cefepime", "Ceftizoxime",
        "Cefotaxime", "Piperacillin Tazobactam", "Meropenem", "Imipenem", "Biapenem",
        "Polymyxin B", "Colistin", "Clarithromycin/Azithromycin", "Doxycycline",
        "Minocycline", "Levofloxacin", "Metronidazole", "Clindamycin", "Flucloxacillin",
        "Vancomycin", "Teicoplanin", "Acyclovir", "Fluconazole", "Voriconazole",
        "Caspofungin", "Tigecycline", "Ampicillin Sulbactam", "Trimethoprim/Sulfamethoxazole",
        "Anidulafungin", "Micafungin", "Other"
    ]
    comorbidities_list = [
        "Diabetes", "Hypertension", "Chronic Kidney Disease (CKD)",
        "Chronic Liver Disease", "Heart Disease", "Cancer", "COPD",
        "Immunosuppression", "Others"
    ]
    discharge_options = ["Discharged", "LAMA", "Death"]

    if request.method == 'POST':
        selected_antibiotics = request.form.getlist('antibiotic')
        antibiotic_combination = ", ".join(selected_antibiotics) if selected_antibiotics else "None"

        selected_comorbidities = request.form.getlist('comorbidities')
        comorbidity_combination = ", ".join(selected_comorbidities) if selected_comorbidities else "None"

        apache_ii = request.form.get('apache_ii', '0')
        sofa_score = request.form.get('sofa_score', '0')
        discharge_status = request.form.get('discharge_status', 'Unknown')
        dod = request.form.get('dod', '')

        data = (
            request.form['patient_name'], request.form.get('age', '0'), request.form.get('sex', 'Unknown'),
            request.form.get('diagnosis', 'Unknown'), request.form.get('doa', ''), dod,
            discharge_status, request.form.get('organism', 'Unknown'), antibiotic_combination,
            comorbidity_combination, int(apache_ii), int(sofa_score)
        )

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO research_data (
                patient_name, age, sex, diagnosis, doa, dod, discharge_status, organism, antibiotic,
                comorbidities, apache_ii, sofa_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('index.html', organisms=organisms, antibiotics=antibiotics, comorbidities_list=comorbidities_list, discharge_options=discharge_options)

@app.route('/download_csv')
def download_csv():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM research_data")
    data = cursor.fetchall()
    conn.close()

    with open("research_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "ID", "Patient Name", "Age", "Sex", "Diagnosis", "DOA", "DOD",
            "Discharge Status", "Organism", "Antibiotic(s)", "Comorbidities",
            "APACHE II Score", "SOFA Score"
        ])
        writer.writerows(data)

    return send_file("research_data.csv", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import csv
import os

app = Flask(__name__)

DB_PATH = "research_data.db"

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS research_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            age INTEGER,
            sex TEXT,
            diagnosis TEXT,
            doa TEXT,
            dod TEXT,
            discharge_status TEXT,
            organism TEXT,
            antibiotic TEXT,
            comorbidities TEXT,
            apache_ii INTEGER,
            sofa_score INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    organisms = [
        "Burkholderia", "Candida", "Elizabethkingia",
        "Klebsiella Pneumoniae (CRE)", "Scrub Typhus", "Stenotrophomonas Maltophilia"
    ]
    antibiotics = [
        "Ceftriaxone", "Cefoperazone Sulbactam", "Cefepime", "Ceftizoxime",
        "Cefotaxime", "Piperacillin Tazobactam", "Meropenem", "Imipenem", "Biapenem",
        "Polymyxin B", "Colistin", "Clarithromycin/Azithromycin", "Doxycycline",
        "Minocycline", "Levofloxacin", "Metronidazole", "Clindamycin", "Flucloxacillin",
        "Vancomycin", "Teicoplanin", "Acyclovir", "Fluconazole", "Voriconazole",
        "Caspofungin", "Tigecycline", "Ampicillin Sulbactam", "Trimethoprim/Sulfamethoxazole",
        "Anidulafungin", "Micafungin", "Other"
    ]
    comorbidities_list = [
        "Diabetes", "Hypertension", "Chronic Kidney Disease (CKD)",
        "Chronic Liver Disease", "Heart Disease", "Cancer", "COPD",
        "Immunosuppression", "Others"
    ]
    discharge_options = ["Discharged", "LAMA", "Death"]

    if request.method == 'POST':
        selected_antibiotics = request.form.getlist('antibiotic')
        antibiotic_combination = ", ".join(selected_antibiotics) if selected_antibiotics else "None"

        selected_comorbidities = request.form.getlist('comorbidities')
        comorbidity_combination = ", ".join(selected_comorbidities) if selected_comorbidities else "None"

        apache_ii = request.form.get('apache_ii', '0')
        sofa_score = request.form.get('sofa_score', '0')
        discharge_status = request.form.get('discharge_status', 'Unknown')
        dod = request.form.get('dod', '')

        data = (
            request.form['patient_name'], request.form.get('age', '0'), request.form.get('sex', 'Unknown'),
            request.form.get('diagnosis', 'Unknown'), request.form.get('doa', ''), dod,
            discharge_status, request.form.get('organism', 'Unknown'), antibiotic_combination,
            comorbidity_combination, int(apache_ii), int(sofa_score)
        )

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO research_data (
                patient_name, age, sex, diagnosis, doa, dod, discharge_status, organism, antibiotic,
                comorbidities, apache_ii, sofa_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('index.html', organisms=organisms, antibiotics=antibiotics, comorbidities_list=comorbidities_list, discharge_options=discharge_options)

@app.route('/download_csv')
def download_csv():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM research_data")
    data = cursor.fetchall()
    conn.close()

    with open("research_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "ID", "Patient Name", "Age", "Sex", "Diagnosis", "DOA", "DOD",
            "Discharge Status", "Organism", "Antibiotic(s)", "Comorbidities",
            "APACHE II Score", "SOFA Score"
        ])
        writer.writerows(data)

    return send_file("research_data.csv", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import csv
import os

app = Flask(__name__)

DB_PATH = "research_data.db"

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS research_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            age INTEGER,
            sex TEXT,
            diagnosis TEXT,
            doa TEXT,
            dod TEXT,
            discharge_status TEXT,
            organism TEXT,
            antibiotic TEXT,
            comorbidities TEXT,
            apache_ii INTEGER,
            sofa_score INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    organisms = [
        "Burkholderia", "Candida", "Elizabethkingia",
        "Klebsiella Pneumoniae (CRE)", "Scrub Typhus", "Stenotrophomonas Maltophilia"
    ]
    antibiotics = [
        "Ceftriaxone", "Cefoperazone Sulbactam", "Cefepime", "Ceftizoxime",
        "Cefotaxime", "Piperacillin Tazobactam", "Meropenem", "Imipenem", "Biapenem",
        "Polymyxin B", "Colistin", "Clarithromycin/Azithromycin", "Doxycycline",
        "Minocycline", "Levofloxacin", "Metronidazole", "Clindamycin", "Flucloxacillin",
        "Vancomycin", "Teicoplanin", "Acyclovir", "Fluconazole", "Voriconazole",
        "Caspofungin", "Tigecycline", "Ampicillin Sulbactam", "Trimethoprim/Sulfamethoxazole",
        "Anidulafungin", "Micafungin", "Other"
    ]
    comorbidities_list = [
        "Diabetes", "Hypertension", "Chronic Kidney Disease (CKD)",
        "Chronic Liver Disease", "Heart Disease", "Cancer", "COPD",
        "Immunosuppression", "Others"
    ]
    discharge_options = ["Discharged", "LAMA", "Death"]

    if request.method == 'POST':
        selected_antibiotics = request.form.getlist('antibiotic')
        antibiotic_combination = ", ".join(selected_antibiotics) if selected_antibiotics else "None"

        selected_comorbidities = request.form.getlist('comorbidities')
        comorbidity_combination = ", ".join(selected_comorbidities) if selected_comorbidities else "None"

        apache_ii = request.form.get('apache_ii', '0')
        sofa_score = request.form.get('sofa_score', '0')
        discharge_status = request.form.get('discharge_status', 'Unknown')
        dod = request.form.get('dod', '')

        data = (
            request.form['patient_name'], request.form.get('age', '0'), request.form.get('sex', 'Unknown'),
            request.form.get('diagnosis', 'Unknown'), request.form.get('doa', ''), dod,
            discharge_status, request.form.get('organism', 'Unknown'), antibiotic_combination,
            comorbidity_combination, int(apache_ii), int(sofa_score)
        )

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO research_data (
                patient_name, age, sex, diagnosis, doa, dod, discharge_status, organism, antibiotic,
                comorbidities, apache_ii, sofa_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('index.html', organisms=organisms, antibiotics=antibiotics, comorbidities_list=comorbidities_list, discharge_options=discharge_options)

@app.route('/download_csv')
def download_csv():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM research_data")
    data = cursor.fetchall()
    conn.close()

    with open("research_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "ID", "Patient Name", "Age", "Sex", "Diagnosis", "DOA", "DOD",
            "Discharge Status", "Organism", "Antibiotic(s)", "Comorbidities",
            "APACHE II Score", "SOFA Score"
        ])
        writer.writerows(data)

    return send_file("research_data.csv", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
