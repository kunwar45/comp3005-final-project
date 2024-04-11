def memberMenu():
    while True:
        #Prints all options
        print("\n0: Exit Program")
        print("1: View Goals")
        print("2: Register for Class")
        print("3: View my Classes")
        print("4: Remove a Class")


        #Takes in input and validates it
        choice = int(input("Please select an option: "))
        if choice < 0 or choice > 4:
            print("\nInvalid input. Please enter a number between 0 and 4.\n ")
        else:
            return choice
            
#Calls the appropriate CRUD function based on the user's choice
def memberexecuteChoice(choice,id,cur):
    match(choice):
        case 0:
            print("Connection Closed")
        case 1:
            getGoals(id,cur)
        case 2:
            registerClass(id,cur)
        case 3:
            viewMyClassses(id,cur)
        case 4:
            deleteClass(id,cur)

def deleteClass(id, cur):
    classId= input("Enter Class ID you want to remove: ")
    cur.execute("DELETE FROM takes WHERE member_id = %s AND class_id = %s", (id, classId))
    print("Deletion successful!")

def viewMyClassses(id,cur):
    query=  """
    SELECT 
        class.class_id,
        class.time,
        class.purpose,
        class.description,
        employee.name AS trainer_name
    FROM 
        takes
    JOIN 
        class ON takes.class_id = class.class_id
    JOIN 
        trainer ON class.trainer_id = trainer.employee_id
    JOIN 
        employee ON trainer.employee_id = employee.employee_id
    WHERE 
        takes.member_id = %s;

    """
    cur.execute(query,(id,))
    rows = cur.fetchall()

    if rows:
        print("\nYour Classes:")
        for row in rows:
            
            id = str(row[0])
            time = row[1]
            purpose = row[2]
            description = row[3]
            trainer = row[4]

    
            print("\nClass ID: "+ id)
            print(purpose,"Class with ",trainer, "at",time)
            print("Description:",description)
               
    else:
        print("\nNo Classes found in the database.")
def registerClass(id,cur):
    getAllClasses(cur)
    class_id = input("\nEnter the class ID you want to register for: ")
    # Execute SQL query to insert record into 'takes' table
    cur.execute("INSERT INTO takes (member_id, class_id) VALUES (%s, %s)", (id, class_id))
    print("Class registration successful!")

def getAllClasses(cur):
    query = """
        SELECT 
            class.class_id,
            class.time,
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
            time = row[1]
            purpose = row[2]
            description = row[3]
            trainer = row[4]
            max = row[5]
            curr = row[6]
            roomName = row[7]
            roomNum = row[8]
            if(max!=curr):#checks if 
                print("\nClass ID: "+ id)
                print(purpose,"Class with",trainer, "at",time,"in",roomName, "("+str(roomNum)+")")
                print("Description:",description)
                print("Spots left!", max-curr)
    else:
        print("\nNo Classes found in the database.")
    
def getGoals(member_id,cur):
    selectQuery="SELECT goal_id,description FROM goal WHERE member_id = %s"
    cur.execute(selectQuery,member_id)
    goals = cur.fetchall()
    if goals:
        print("\nYour goals:")
        for goal in goals:
            print("\n"+ str(goal[0])+":"+goal[1])
    else:
        print("\nNo goals found in the database.")
    