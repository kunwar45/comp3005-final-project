def adminMenu(id,cur):
    cur.execute("SELECT name FROM employee WHERE employee_id=%s",id)
    name= cur.fetchone()[0]
    while True:
        #Prints all options
        print("\nHello Admin", name)
        print("0: Exit Program")
        print("1: View Bookings")
        print("2: Book Class")
        print("3: View equipment")

        #Takes in input and validates it
        choice = int(input("Please select an option: "))
        if choice < 0 or choice > 4:
            print("\nInvalid input. Please enter a number between 0 and 4.\n ")
        else:
            return choice
            
#Calls the appropriate CRUD function based on the user's choice
def adminExecuteChoice(choice,cur):
    match(choice):
        case 0:
            print("Connection Closed")
        case 1:
            getBookings(cur)
        case 2:
            bookClass(cur)
        case 3:
            viewEquipment(cur)

def viewEquipment(cur):
    query = """
    SELECT e.equipment_id, e.name AS equipment_name, e.description, r.name AS room_name, e.last_serviced
    FROM equipment e
    JOIN room r ON e.room_id = r.room_id
    """
    cur.execute(query)
    
    # Fetch all rows
    rows = cur.fetchall()

    if rows:
        print("Equipment Information:")
        print("-" * 50)
        for row in rows:
            equipment_id, equipment_name, condition, room_name, last_serviced = row
            print(f"Equipment ID: {equipment_id}")
            print(f"Name: {equipment_name}")
            print(f"Condition: {condition}")
            print(f"Room Name: {room_name}")
            print(f"Last Serviced: {last_serviced}")
            print("-" * 50)
    else:
        print("No equipment found.")
    
def bookClass(cur):
    getUnassingedClasses(cur)
    classID = input("Enter Class ID: ")
    cur.execute("SELECT time FROM class WHERE class_id = %s", (classID,))
    classTime = cur.fetchone()[0]

    query="""
        SELECT 
            room_id,
            room_number,
            name AS room_name
        FROM 
            room
        WHERE 
            room_id NOT IN (
                SELECT 
                    room_id 
                FROM 
                    booking
                JOIN 
                    class ON booking.class_id = class.class_id 
                WHERE 
                    class.time = %s
            )
        """
    cur.execute(query,(classTime,))
    rows = cur.fetchall()

    if rows:
        print("\nAvailable Rooms at:",classTime)
        print("-" * 50)
        for row in rows:
            room_id, room_number, room_name = row
            print("Room ID:", room_id)
            print("Room Number:", room_number)
            print("Room Name:", room_name)
            print("-" * 50)
    roomID = input("Enter a room ID: ")
    cur.execute("INSERT INTO booking (class_id, room_id) VALUES (%s, %s)", (classID, roomID))
        
def getUnassingedClasses(cur):
    query="""
        SELECT 
            class.class_id,
            class.time,
            class.purpose,
            class.description,
            employee.name AS trainer_name,
            class.max_attendance,
            class.current_num_attendees
        FROM 
            class
        JOIN 
            trainer ON class.trainer_id = trainer.employee_id
        JOIN 
            employee ON trainer.employee_id = employee.employee_id
        WHERE
            NOT EXISTS (
                SELECT 1 
                FROM booking 
                WHERE booking.class_id = class.class_id
            )
    """
    cur.execute(query)
    rows = cur.fetchall()

    if rows:
        print("\nUnassigned Classes:")
        print("-" * 50)
        for row in rows:
            id, time, purpose, description, trainer, max, curr = row
            print("\nClass ID:", id)
            print(purpose,"Class with",trainer, "at",time)
            print("Description:",description)
            print("Spots left:", max-curr)
            print("-" * 50)
    else:
        print("No available classes found.")
def getBookings(cur):
    query = """
            SELECT b.booking_id, c.*, r.*, e.name AS trainer_name
            FROM booking b
            JOIN class c ON b.class_id = c.class_id
            JOIN room r ON b.room_id = r.room_id
            JOIN trainer t ON c.trainer_id = t.employee_id
            JOIN employee e ON t.employee_id = e.employee_id
            """
    cur.execute(query)
        

    rows = cur.fetchall()
    for row in rows:
        bookingID = row[0]
        classID = row[1]
        time = row[2]
        purpose = row[3]
        description= row[4]
        roomID = row[9]
        roomNum = row[10]
        roomName = row[11]
        trainer = row[13]
        print("\nBooking ID:",bookingID,"Class ID:", classID, "Room ID:",roomID)
        print(purpose,"Class with",trainer, "at",time,"in",roomName, "("+str(roomNum)+")")
        print("Description:",description)


    

