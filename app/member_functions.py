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
        print("7: View/Set Goals")

        #Takes in input and validates it
        choice = int(input("Please select an option: "))
        if choice < 0 or choice > 7:
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
        case 7:
            manageGoals(name,cur)

def manageGoals(name, cur):
    # Fetch member_id based on the given name
    cur.execute("SELECT member_id FROM member WHERE name = %s", (name,))
    member_id = cur.fetchone()
    
    if member_id:
        # Fetch existing goals for the member
        cur.execute("SELECT goal_id, description, date_completed FROM goal WHERE member_id = %s", (member_id,))
        goals = cur.fetchall()
        
        if goals:
            print(f"\n{name}'s Goals:")
            print("-" * 50)
            for goal in goals:
                goal_id, description, date_completed = goal
                completed_status = "Completed on: " + str(date_completed) if date_completed else "Not completed"
                print(f"Goal ID: {goal_id}, Description: {description}, Status: {completed_status}")
            print("-" * 50)
            
            # Ask if the user wants to update any goal's completion date
            update_choice = input("Do you want to set/update a completion date for a goal? (yes/no): ")
            if update_choice.lower() == 'yes':
                goal_id = input("Enter the Goal ID to update: ")
                new_date = input("Enter the new completion date (YYYY-MM-DD): ")
                cur.execute("UPDATE goal SET date_completed = %s WHERE goal_id = %s AND member_id = %s", (new_date, goal_id, member_id))
                print("Goal updated successfully!")
        else:
            print("No goals found for this member.")
        
        # Ask if the user wants to add a new goal
        new_goal_choice = input("Do you want to add a new goal? (yes/no): ")
        if new_goal_choice.lower() == 'yes':
            new_description = input("Enter the description of the new goal: ")
            cur.execute("INSERT INTO goal (member_id, description) VALUES (%s, %s)", (member_id, new_description))
            print("New goal added successfully!")
    else:
        print(f"Member named {name} not found.")

def getRoutine(name, cur):
    cur.execute("SELECT member_id FROM member WHERE name = %s", (name,))
    member_id = cur.fetchone()

    if member_id:
        query = """
            SELECT description
            FROM exercise_routine
            WHERE member_id = %s;
            """
        cur.execute(query, (member_id,))
        routines = cur.fetchall()

        if routines:
            print(f"\n{name}'s Routine:")
            print("-" * 50)
            for routine in routines:
                print(routine[0])
            print("-" * 50)
        else:
            print(f"You have no routines.")
            # Ask the user if they want to add a new routine
            new_routine = input("Enter your new routine: ")
            cur.execute("INSERT INTO exercise_routine (member_id, description) VALUES (%s, %s)", (member_id[0], new_routine))
            print("New routine added successfully!")
    else:
        print(f"Member named {name} not found.")

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
            print("Weight:", str(weight) + "kg")
            print("Height:", str(height) + "cm")
            print("Age:", age)
            print("-" * 50)
            
            # Prompt for new metrics
            new_weight = input("Enter new weight (kg): ")
            new_height = input("Enter new height (cm): ")
            new_age = input("Enter new age: ")
            
            # Update metrics in the database
            cur.execute("UPDATE metrics SET weight = %s, height = %s, age = %s WHERE member_id = %s",
                        (new_weight, new_height, new_age, member_id[0]))
            print("Metrics updated successfully!")
        else:
            print("No metrics found for the member. Let's initialize your metrics.")
            new_weight = input("Enter weight (kg): ")
            new_height = input("Enter height (cm): ")
            new_age = input("Enter age: ")
            
            # Insert new metrics into the database
            cur.execute("INSERT INTO metrics (member_id, weight, height, age) VALUES (%s, %s, %s, %s)",
                        (member_id[0], new_weight, new_height, new_age))
            print("Metrics initialized successfully!")
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