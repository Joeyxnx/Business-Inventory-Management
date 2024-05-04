import sqlite3

'''
Exercise 0:
Create the required database for the subsequent exercise. You may use a separate tool (e.g. https://sqlitebrowser.org/ (Links to an external site.)) or handle this in Python as you prefer.

CREATE database python_db;

CREATE TABLE `python_db`.`Hospital` ( `Hospital_Id` INT UNSIGNED NOT NULL , `Hospital_Name` TEXT NOT NULL , `Bed_Count` INT ,
PRIMARY KEY (`Hospital_Id`))

INSERT INTO `hospital` (`Hospital_Id`, `Hospital_Name`, `Bed Count`) VALUES
('1', 'Toronto General Hospital', '471'),
('2', 'St. Joseph's Health Centre', '376'),
('3', 'Mississauga Hospital', '751'),
('4', 'Credit Valley Hospital', '382')

CREATE TABLE `python_db`.`Doctor`
( `Doctor_Id` INT UNSIGNED NOT NULL ,
`Doctor_Name` TEXT NOT NULL ,
`Hospital_Id` INT NOT NULL ,
`Joining_Date` DATE NOT NULL ,
`Speciality` TEXT NULL ,
`Salary` INT NULL ,
`Experience` INT NULL ,
PRIMARY KEY (`Doctor_Id`))

INSERT INTO `doctor` (`Doctor_Id`, `Doctor_Name`, `Hospital_Id`, `Joining_Date`, `Speciality`, `Salary`, `Experience`) VALUES
('101', 'Duemler', '1', '2005-2-10', 'Pediatric', '140000', NULL),
('102', 'McBroom', '1', '2018-07-23', 'Oncologist', '120000', NULL),
('103', 'El-Ashry', '2', '2016-05-19', 'Surgeon', '125000', NULL),
('104', 'Chan', '2', '2017-12-28', 'Pediatric ', '128000', NULL),
('105', 'Platonov', '3', '2004-06-04', 'Psychiatrist', '142000', NULL),
('106', 'Izukaw', '3', '2012-09-11', 'Dermatologist', '130000', NULL),
('107', 'Jhas', '4', '2014-08-21', 'Obstetrician/Gynecologist', '132000', NULL),
('108', 'Marmor', '4', '2011-10-17', 'Radiologist', '130000', NULL)
'''

def connect_database():
    global conn, cur
       
    conn = sqlite3.connect('python_db.db') # will connect to db if exists, or create a new one.

    cur = conn.cursor()    
    
def create_database():
    cur.execute('''DROP TABLE IF EXISTS hospital;''')
    cur.execute('''CREATE TABLE IF NOT EXISTS "hospital" (
            "Hospital_Id"	INTEGER NOT NULL,
            "Hospital_Name"	TEXT NOT NULL,
            "Bed_Count"	INTEGER,
            PRIMARY KEY("Hospital_Id")
            );''')
    
    
    cur.execute('''INSERT INTO hospital ('Hospital_Id', 'Hospital_Name', 'Bed_Count') VALUES
                ('1', 'Toronto General Hospital', '471'),
                ('2', "St. Joseph's Health Centre", '376'),
                ('3', 'Mississauga Hospital', '751'),
                ('4', 'Credit Valley Hospital', '382')''')
    
    cur.execute('''DROP TABLE IF EXISTS "doctor";''')
    
    cur.execute('''CREATE TABLE "doctor" (
            "Doctor_Id"	INTEGER NOT NULL,
            "Doctor_Name"	TEXT NOT NULL,
            "Hospital_Id"	INTEGER NOT NULL,
            "Joining_Date"	TEXT NOT NULL,
            "Speciality"	TEXT,
            "Salary"	INTEGER,
            "Experience"	INTEGER,
            PRIMARY KEY("Doctor_Id")
            );''')
    
    cur.execute('''INSERT INTO 'doctor' 
    ('Doctor_Id', 'Doctor_Name', 'Hospital_Id', 'Joining_Date', 'Speciality', 'Salary', 'Experience') VALUES
            ('101', 'Duemler', '1', '2005-02-10', 'Pediatric', '140000', NULL),
            ('102', 'McBroom', '1', '2018-07-23', 'Oncologist', '120000', NULL),
            ('103', 'El-Ashry', '2', '2016-05-19', 'Surgeon', '125000', NULL),
            ('104', 'Chan', '2', '2017-12-28', 'Pediatric ', '128000', NULL),
            ('105', 'Platonov', '3', '2004-06-04', 'Psychiatrist', '142000', NULL),
            ('106', 'Izukaw', '3', '2012-09-11', 'Dermatologist', '130000', NULL),
            ('107', 'Jhas', '4', '2014-08-21', 'Obstetrician/Gynecologist', '132000', NULL),
            ('108', 'Marmor', '4', '2011-10-17', 'Radiologist', '130000', NULL)''')

def exercise_1():
'''
Exericse 1:
List all doctors by specialty. First, list the name of the specialty. Then list all doctors associated with the specialty.
Their names should be displayed as "Dr. Lastname". Both the specialties and doctors should be listed in alphabetical order.
'''
    
    cur.execute("SELECT Speciality, Doctor_Name FROM doctor ORDER BY Speciality, Doctor_Name")
    
    rows = cur.fetchall()
    
    for row in rows:
        # this is for SELECT * FROM doctor
        print(f"{row[0]:<26} Dr. {row[1]}")

def exercise_2():
'''
Exercise 2:
Display a numbered list of all the hospitals and allow the user to choose one. Ensure they choose a valid number, otherwise continually prompt them for a correct number.
Then, display all doctors associated with that hospital. Their names should be displayed as "Dr. Lastname -- Specialty"
'''
    cur.execute("SELECT * FROM hospital")    
    
    rows = cur.fetchall()
    for row in rows:
        print(f"{row[0]:<3} {row[1]:<27} {row[2]}")
    
    num = -1
            
    data = None
    while data == None:
        try:
            num = int(input("Select a hospital ID: "))
            cur.execute("SELECT * FROM hospital WHERE Hospital_Id=(?)", (num, ))            
            data = cur.fetchone()
            #print(data)
        except ValueError:
            num = -1

    # inner join the 2 tables
    cur.execute('''DROP TABLE IF EXISTS "hospital_employee"''')    
    cur.execute('''CREATE TABLE "hospital_employee" AS
    SELECT Hospital_Name, doctor.Doctor_Name, Speciality, Doctor_Id, Experience, hospital.Hospital_Id
    FROM hospital
    INNER JOIN doctor ON doctor.Hospital_Id = hospital.Hospital_Id''')
    
    #cur.execute("""SELECT * FROM hospital_employee WHERE Hospital_Id=:num""", {"num":num})
    cur.execute("""SELECT * FROM hospital_employee WHERE Hospital_Id=(?)""", (num,)) # add the comma otherwise it thinks its a tuple
    
    rows = cur.fetchall()
    print(f"\nFor {rows[0][0]}, there are the following doctors:")
    for row in rows:
        #print(row)
        print(f" Dr. {row[1]} -- {row[2]}")

def exercise_3():
'''
Exercise 3:
Ask the user to specify a number of years. Then, display all doctors who have been with the hospital at least that long.
Use the difference between the joining date and today's date to calculate that number.
Their names should be displayed as "Dr. Lastname (Hospital Name)"

Tips:
Define the parameterized query.
Use cursor.execute() to execute query.
Fetch result using cursor.fetchall().
'''
    # date difference
    cur.execute("""SELECT Doctor_Id, Doctor_Name, Experience, Joining_Date FROM doctor""")    
    rows = cur.fetchall()
    
    for row in rows:
        #print(row)
    
        cur.execute("SELECT julianday('now') - julianday(Joining_Date) FROM doctor WHERE Doctor_Id=(?)", (row[0],))
        dates = cur.fetchone()
        for date in dates:
            #print(date)
            year = date // 365
            cur.execute("UPDATE doctor SET Experience=(?) WHERE Doctor_Id=(?)", (year, row[0],))
            cur.execute("UPDATE hospital_employee SET Experience=(?) WHERE Doctor_Id=(?)", (year, row[0],))
    
    # not insert into - creates new rows
    # use update as there's data already
    
    # get input, etc.
    num_years = -1
    while num_years < 0:
        try:
            num_years = int(input("Search for doctors with at least (years) of experience: "))
        except ValueError:
            num_years = -1     
    
    cur.execute("SELECT * from hospital_employee WHERE Experience > (?)", (num_years,))
    rows = cur.fetchall()
    
    for row in rows:
        #print(row)
        print(f"Dr. {row[1]} at {row[0]} has {row[4]} years of experience.")    
   
    if len(rows) == 0:
        print("There's no one with this amount of experience.")


def close_database():
    conn.commit()
    conn.close()
    
if __name__ == '__main__':
    connect_database()
    create_database()
    exercise_1()
    exercise_2()
    exercise_3()
    close_database()
