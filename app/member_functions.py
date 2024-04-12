def memberMenu():
    while True:
        #Prints all options
        print("\n0: Exit Program")
        print("1: View Achievements")
        print("2: Register for Class")
        print("3: View my Classes")
        print("4: Remove a Class")
        print("5: Manage Metrics")
        print("6: See Routines")

        #Takes in input and validates it
        choice = int(input("Please select an option: "))
        if choice < 0 or choice > 6:
            print("\nInvalid input. Please enter a number between 0 and 4.\n ")
        else:
            return choice
            
#Calls the appropriate CRUD function based on the user's choice
def memberexecuteChoice(choice,name,cur):
    match(choice):
        case 0:
            print("Connection Closed")
        case 1:
            getAchievements(name,cur)
        case 2:
            registerClass(name,cur)
        case 3:
            viewMyClassses(name,cur)
        case 4:
            deleteClass(name,cur)
        case 5:
            manageMetrics(name,cur)
        case 6:
            getRoutine(name,cur)
def getRoutine(name,cur):
    query = """
        SELECT description
        FROM exercise_routine er
        JOIN member m ON er.member_id = m.member_id
        WHERE m.name = %s;
        """
    cur.execute(query, (name,))
    routines = cur.fetchall()

    if routines:
        print(f"\n{name}'s Routine:")
        print("-" * 50)
        for routine in routines:
            print(routine[0])
        print("-" * 50)
    else:
        print(f"No routines found for {name}.")
def manageMetrics(name, cur):
    cur.execute("SELECT member_id FROM member WHERE name = %s", (name,))
    member_id = cur.fetchone()
    
    if member_id:
        cur.execute("SELECT weight, height, age FROM metrics WHERE member_id = %s", (member_id[0],))
        metrics = cur.fetchone()
        
        if metrics:
            weight, height, age = metrics
            print("\nCurrent Metrics:")
            print("-" * 50)
            print("Weight:", str(weight)+"kg")
            print("Height:", height+"cm")
            print("Age:", age)
            print("-" * 50)
            
            # Prompt for new metrics
            new_weight = input("Enter new weight: ")
            new_height = input("Enter new height: ")
            new_age = input("Enter new age: ")
            
            # Update metrics in the database
            cur.execute("UPDATE metrics SET weight = %s, height = %s, age = %s WHERE member_id = %s", (new_weight, new_height, new_age, member_id[0]))
            print("Metrics updated successfully!")
        else:
            print("No metrics found for the member.")
    else:
        print("Member not found.")

def deleteClass(name, cur):
    classId = input("Enter Class ID you want to remove: ")
    
    cur.execute("SELECT member_id FROM member WHERE name = %s", (name,))
    member_id = cur.fetchone()
    
    if member_id:
        cur.execute("DELETE FROM takes WHERE member_id = %s AND class_id = %s", (member_id[0], classId))
    
        cur.execute("UPDATE class SET current_num_attendees = current_num_attendees - 1 WHERE class_id = %s", (classId,))
        
        print("Deletion successful!")
    else:
        print("Member not found.")


def viewMyClassses(name, cur):
    query = """
    SELECT 
        c.class_id,
        c.start_time,
        c.end_time,
        c.date,
        c.purpose,
        c.description,
        e.name AS trainer_name,
        r.name AS room_name,
        r.room_number
    FROM 
        member m
    JOIN 
        takes t ON m.member_id = t.member_id
    JOIN 
        class c ON t.class_id = c.class_id
    JOIN 
        trainer tr ON c.trainer_id = tr.trainer_id
    JOIN 
        employee e ON tr.employee_id = e.employee_id
    JOIN
        booking b ON c.class_id = b.class_id
    JOIN
        room r ON b.room_id = r.room_id
    WHERE 
        m.name = %s;
    """
    cur.execute(query, (name,))
    rows = cur.fetchall()

    if rows:
        print("\nYour Classes:")
        print("-"*50)
        for row in rows:
            class_id = str(row[0])
            start_time = row[1]
            end_time = row[2]
            date = row[3]
            purpose = row[4]
            description = row[5]
            trainer = row[6]
            room_name = row[7]
            room_number = row[8]

            print("\nClass ID:", class_id)
            print(purpose, "Class with", trainer, "on", date, "from", start_time, "to", end_time)
            print("Description:", description)
            print("Room:", room_name, "(Room Number:", room_number, ")")
            print("-"*50)
    else:
        print("\nNo Classes found in the database.")

def registerClass(name,cur):
    print("1: Register for a group class")
    print("2: Register for personal class")

    choice = int(input("Please select an option: "))
    if choice < 0 or choice > 2:
        print("\nInvalid input. Please enter a number between 1 and 2.\n ")
    elif choice == 1:
        registerGroupClass(name,cur)
    elif choice == 2:
        registerPersonalClass(name,cur)


def registerGroupClass(name,cur):
    getAllClasses(cur)
    class_id = input("\nEnter the class ID you want to register for: ")
    # Execute SQL query to insert record into 'takes' table
    cur.execute("""
        INSERT INTO takes (member_id, class_id) VALUES (
            (SELECT member_id FROM member WHERE name = %s), 
            %s
        )
        """, (name, class_id,))
    
    cur.execute("""
        UPDATE class
        SET current_num_attendees = current_num_attendees + 1
        WHERE class_id = %s
        """, (class_id,))
    
    print("Class registration successful!")

def registerPersonalClass(name,cur):
    getAllTrainers(cur)
    trainer_id = input("\nEnter the trainer ID you want to take a class with: ")

    getAvailableTime(trainer_id, cur)
    available_time_id = input("\nEnter the available time ID you want to register for: ")
    # Execute SQL query to insert record into 'takes' table
    # Delete the booked available time from the available_time table
    cur.execute("""
        DELETE FROM available_time WHERE available_time_id = %s
        """, (available_time_id,))
    
    print("Class registration successful!")

def getAvailableTime(trainer_id, cur):
    cur.execute("""
    SELECT available_time_id, date, start_time, end_time
    FROM available_time
    WHERE trainer_id = %s
    ORDER BY date, start_time
    """, (trainer_id,))

    available_times = cur.fetchall()

    for time in available_times:
        print(f"Available Time ID: {time[0]}, Date: {time[1]}, Start Time: {time[2]}, End Time: {time[3]}")
    

def getAllClasses(cur):
    query = """
        SELECT 
            class.class_id,
            class.class_name,
            class.start_time,
            class.end_time,
            class.date,
            class.purpose,
            class.description,
            employee.name AS trainer_name,
            class.max_attendance,
            class.current_num_attendees,
            room.name AS room_name,
            room.room_number
        FROM 
            class
        JOIN 
            trainer ON class.trainer_id = trainer.employee_id
        JOIN 
            employee ON trainer.employee_id = employee.employee_id
        JOIN
            booking ON class.class_id = booking.class_id
        JOIN
            room ON booking.room_id = room.room_id;
    """
    cur.execute(query)
    rows = cur.fetchall()

    if rows:
        print("\nAvailable Classes:")
        for row in rows:
            id = str(row[0])
            name = row[1]
            stime = row[2]
            etime = row[3]
            date = row[4]
            purpose = row[5]
            desc = row[6]
            trainer = row[7]
            max = row[8]
            curr = row[9]
            roomName = row[10]
            roomNum = row[11]
            if(max!=curr):#checks if 
                print("\nClass ID: "+ id + ", name: " + name)
                print(purpose,"Class with",trainer, " from: ",stime, " to ", etime ,"on", date)
                print("Room: ",roomName, "(",roomNum,")")
                print("Description:",desc)
                print("Max Attendance: ", max)
                print("Current Attendance: ", curr)
    else:
        print("\nNo Classes found in the database.")

def getAllTrainers(cur):
    cur.execute("""
    SELECT t.trainer_id, e.name
    FROM trainer t
    JOIN employee e ON t.employee_id = e.employee_id
    """)
    
    # Fetch all rows from the executed query
    trainers = cur.fetchall()
    
    # Optionally, you can print the results here or process them as needed
    for trainer in trainers:
        print(f"Trainer ID: {trainer[0]}, Name: {trainer[1]}")
    
def getAchievements(name, cur):
    selectQuery = """
    SELECT g.description, g.date_completed
    FROM goal g
    JOIN member m ON g.member_id = m.member_id
    WHERE m.name = %s AND g.date_completed IS NOT NULL
    """
    cur.execute(selectQuery, (name,))
    achievements = cur.fetchall()

    if achievements:
        print("\nCompleted goals:")
        print("-" * 50)
        for achievement in achievements:
            description, date_completed = achievement
            print("\nDescription:", description, "on", date_completed)
            print("-" * 50)
    else:
        print("\nNo completed goals found in the database.")