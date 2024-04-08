import psycopg2

#Adds Student To Database
def addStudent(cur):
    firstName = input("Enter Student's First Name: ")
    lastName = input("Enter Student's Last Name: ")
    email = input("Enter Student's email: ")
    enrollDate = input("Please Student's Enrollement Date (YYYY-MM-DD): ")
    studentTuple = (firstName,lastName,email,enrollDate)

    insert_query = "INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s)"
    cur.execute(insert_query, studentTuple)
    return 0

#Prints all the information of every student
def getAllStudents(cur):
    selectQuery = "SELECT * FROM students"
    cur.execute(selectQuery)
    students = cur.fetchall()

    if students:
        print("\nAll students in the database:")
        for student in students:
            print("\nStudent ID:", student[0])
            print("First Name:", student[1])
            print("Last Name:", student[2])
            print("Email:", student[3])
            print("Enrollment Date:", student[4],"\n")
    else:
        print("\nNo students found in the database.")

#Deletes a student by ID in database
def deleteStudent(cur):
    id = int(input("Enter the ID of the student you want to delete: "))
    try:
    
        
        cur.execute("SELECT * FROM students WHERE student_id = %s", (id,))
        existing_student = cur.fetchone()

        if existing_student!=None:
            deleteQuery = "DELETE FROM students WHERE student_id = %s"
            
            cur.execute(deleteQuery, (id,))
            
            print("\nStudent with ID", id, "deleted successfully.\n")
        else:
            print("\nNo student with ID", id, "was found.\n")
    except psycopg2.Error as e:
        print("Error deleting student:", e)

#Changes the email of a student with given ID
def updateStudentEmail(cur):
    id = int(input("Enter the ID of the student that you want to update: "))
    email = input("Enter a new email for the student: ")

    try:
        cur.execute("SELECT * FROM students WHERE student_id = %s", (id,))
        existing_student = cur.fetchone()
        if existing_student!=None:
            delete_query = "UPDATE students SET email = %s WHERE student_id = %s"
            
            cur.execute(delete_query, (email,id))
            
            print("\nStudent with ID ", id, " email changed successfully.\n")
        else:
            print("\nNo student with ID", id, "was found.\n")
    except psycopg2.Error as e:
        print("Error deleting student:", e)