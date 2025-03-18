from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required,current_user
import pyodbc
from werkzeug.security import check_password_hash
import hashlib
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text



app = Flask(__name__)
app.secret_key = 'coolKey'

server = r'TS-0009\SQLEXPRESS'
database = 'SpaceX'
username = 'marceli'
password = 'karman'


conn_str = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://marceli:karman@TS-0009\\SQLEXPRESS/SpaceX?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

data = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username

@login_manager.user_loader
def load_user(username):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Login WHERE Login = ?", (username,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        user_id, username, _ = user_data
        return User(user_id, username)

    return None


def verify_password(username, password):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT Password FROM Login WHERE Login = ?", (username,))
    password_hash = cursor.fetchone()
    conn.close()
    if password_hash:
        hashed_password_db = password_hash[0]
        hashed_password_input = hashlib.md5(password.encode()).digest()
        print(hashed_password_db)
        print(hashed_password_input)
        return hashed_password_db == hashed_password_input
    return False


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_password(username, password):
            session['username'] = username
            flash('Login successful', 'success')
            return redirect(url_for('login'))
        flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.pop('username', None)
        flash('Logged out successfully', 'success')
        return redirect(url_for('login'))
    else:

        return redirect(url_for('login'))


@app.route('/')
def index():
    try:

        conn = pyodbc.connect(conn_str)


        cursor = conn.cursor()


        cursor.execute("select * from vw_CurrentMission where Name ='Mars'")
        mars_rows = cursor.fetchall()


        cursor.execute("select * from vw_CurrentMission where Name ='Moon'")
        moon_rows = cursor.fetchall()


        cursor.execute("select * from vw_CurrentMission where Name ='AroundEarth'")
        AroundEarth_rows = cursor.fetchall()


        conn.close()


        return render_template('index.html', mars_rows=mars_rows, moon_rows=moon_rows, AroundEarth_rows=AroundEarth_rows)


    except Exception as e:
        return str(e)


@app.route('/mission')
def mission():
    try:
        sort_by = request.args.get('sort_by', 'LaunchDate')
        sort_order = request.args.get('sort_order', 'asc')

        valid_columns = ['LaunchDate', 'ReturnDate', 'TeamName', 'Name']

        if sort_by not in valid_columns:
            sort_by = 'LaunchDate'

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        query = f"SELECT DISTINCT * FROM vw_MissionsAndData ORDER BY {sort_by} {sort_order}"

        cursor.execute(query)
        mission_rows = cursor.fetchall()
        conn.close()

        return render_template('mission.html', mission_rows=mission_rows)

    except Exception as e:
        return str(e)

@app.route('/spaceman')
def spaceman():
    try:
        sort_by = request.args.get('sort_by', 'StartDate')
        sort_order = request.args.get('sort_order', 'asc')

        valid_columns = ['StartDate', 'FirstName', 'LastName', 'Salary', 'MissionExperience', 'RoleName']

        if sort_by not in valid_columns:
            sort_by = 'StartDate'

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        query = f"SELECT DISTINCT * FROM vw_SpacemanAndCaptains WHERE RoleName = 'Captain' OR RoleName = 'Spaceman' ORDER BY {sort_by} {sort_order}"

        cursor.execute(query)
        spaceman_rows = cursor.fetchall()
        conn.close()

        return render_template('spaceman.html', spaceman_rows=spaceman_rows)

    except Exception as e:
        return str(e)
@app.route('/scientist')
def scientist():
    try:
        sort_by = request.args.get('sort_by', 'MissionExperience')
        sort_order = request.args.get('sort_order', 'asc')

        valid_columns = ['MissionExperience', 'FirstName', 'LastName', 'Salary', 'StartDate']

        if sort_by not in valid_columns:
            sort_by = 'MissionExperience'

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        query = f"SELECT DISTINCT * FROM vw_Scientist ORDER BY {sort_by} {sort_order}"

        cursor.execute(query)
        scientist_rows = cursor.fetchall()
        conn.close()

        return render_template('scientist.html', scientist_rows=scientist_rows)

    except Exception as e:
        return str(e)

@app.route('/workwithus')
def workwithus():
    return render_template('workwithus.html')


def insert_job_application(first_name, last_name, dob, email, phone, role_id):
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO JobApplication (FirstName, LastName, DateOfBirth, Email, Phone, JobApplicationRoleId) VALUES (?, ?, ?, ?, ?, ?)",
                       (first_name, last_name, dob, email, phone, role_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Error inserting data:", e)
        return False

@app.route('/submit_cv', methods=['POST'])
def submit_cv():
    if request.method == 'POST':
        first_name = request.form['name']
        last_name = request.form['surname']
        dob = request.form['dob']
        email = request.form['email']
        phone = request.form['phone']
        position = request.form['position']
        role_id = 1 if position == 'scientist' else 2
        if insert_job_application(first_name, last_name, dob, email, phone, role_id):
            submission_status = 'CV submitted successfully'
        else:
            submission_status = 'Failed to submit CV'
        return render_template('workwithus.html', submission_status=submission_status)


class Role(data.Model):
    __tablename__ = 'Role'

    RoleId = data.Column(data.Integer, primary_key=True)
    RoleName = data.Column(data.String(50), nullable=False)

class Employee(data.Model):
    __tablename__ = 'Employee'

    EmployeeId = data.Column(data.Integer, primary_key=True)
    FirstName = data.Column(data.String(50), nullable=False)
    LastName = data.Column(data.String(100), nullable=False)
    StartDate = data.Column(data.Date, nullable=False)
    Salary = data.Column(data.Integer, nullable=False)
    MissionExperience = data.Column(data.Integer)
    EmployeeRoleId = data.Column(data.Integer, data.ForeignKey('Role.RoleId'), nullable=False)

    role = data.relationship('Role', backref=data.backref('employees', lazy=True))


class MissionTeam(data.Model):
    __tablename__ = 'MissionTeam'

    MissionTeamId = data.Column(data.Integer, primary_key=True)
    TeamName = data.Column(data.String(50), nullable=False)

class Mission(data.Model):
    __tablename__ = 'Mission'

    MissionId = data.Column(data.Integer, primary_key=True)
    Name = data.Column(data.String(50), nullable=False)
    LaunchDate = data.Column(data.Date, nullable=False)
    ReturnDate = data.Column(data.Date)
    MissionMissionTeamId = data.Column(data.Integer, data.ForeignKey('MissionTeam.MissionTeamId'), nullable=False)

    MissionTeam = data.relationship('MissionTeam', backref=data.backref('missions', lazy=True))

class JobApplication(data.Model):
    __tablename__ = 'JobApplication'

    JobApplicationId = data.Column(data.Integer, primary_key=True, autoincrement=True)
    FirstName = data.Column(data.String(50), nullable=False)
    LastName = data.Column(data.String(100), nullable=False)
    DateOfBirth = data.Column(data.Date)
    Email = data.Column(data.String(100), nullable=False)
    Phone = data.Column(data.String(15), nullable=False)
    JobApplicationRoleId = data.Column(data.Integer, data.ForeignKey('Role.RoleId'), nullable=False)


    role = data.relationship('Role', backref=data.backref('job_applications', lazy=True))


@app.route('/management')
def management():

    employees = Employee.query.all()
    missions = Mission.query.all()
    job_applications = JobApplication.query.all()

    return render_template('management.html', employees=employees, missions=missions, job_applications=job_applications)


@app.route('/add_employee', methods=['POST'])
def add_employee():
    if request.method == 'POST':

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        start_date = request.form['start_date']
        salary = request.form['salary']
        mission_experience = request.form['mission_experience']
        employee_role_id = request.form['employee_role_id']


        new_employee = Employee(
            FirstName=first_name,
            LastName=last_name,
            StartDate=start_date,
            Salary=salary,
            MissionExperience=mission_experience,
            EmployeeRoleId=employee_role_id
        )

        data.session.add(new_employee)

        data.session.commit()

        flash('Employee added successfully', 'success')

        return redirect(url_for('management'))


@app.route('/delete_employee', methods=['POST'])
def delete_employee():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        employee = Employee.query.get(employee_id)
        if employee:
            data.session.delete(employee)
            data.session.commit()
            flash('Employee deleted successfully', 'success')
        else:
            flash('Employee not found', 'error')
        return redirect('/management')


@app.route('/add_mission', methods=['POST'])
def add_mission():
    if request.method == 'POST':
        name = request.form['name']
        launch_date = request.form['launch_date']
        return_date = request.form['return_date']
        mission_team_id = request.form['mission_team_id']

        new_mission = Mission(Name=name, LaunchDate=launch_date, ReturnDate=return_date, MissionMissionTeamId=mission_team_id)
        data.session.add(new_mission)
        data.session.commit()

        flash('Mission added successfully', 'success')
        return redirect('/management')

@app.route('/delete_mission', methods=['POST'])
def delete_mission():
    if request.method == 'POST':
        mission_id = request.form['MissionId']

        mission = Mission.query.get(mission_id)

        if mission:
            data.session.delete(mission)
            data.session.commit()
            flash('Mission deleted successfully', 'success')
        else:
            flash('Mission not found', 'error')

        return redirect('/management')


@app.route('/move_job_application', methods=['POST'])
def move_job_application_to_employee():
    job_application_id = request.form['job_application_id']
    salary = request.form['salary']
    mission_experience = request.form['mission_experience']

    try:
        data.session.execute(
            text("EXEC sp_MoveJobApplicationToEmployee :JobApplicationId, :Salary, :MissionExperience"),
            {"JobApplicationId": job_application_id, "Salary": salary, "MissionExperience": mission_experience}
        )

        data.session.commit()

        flash('Job application moved to employee successfully', 'success')
    except Exception as e:
        data.session.rollback()
        flash('Error: ' + str(e), 'error')

    return redirect(url_for('management'))


if __name__ == '__main__':
    app.run(debug=True)
