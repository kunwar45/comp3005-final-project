def adminMenu(name,cur):
    # cur.execute("SELECT name FROM employee WHERE employee_id=%s",id)
    # name= cur.fetchone()[0]
    while True:
        #Prints all options
        print("\nHello Admin", name)
        print("0: Exit Program")
        print("1: View Bookings")
        print("2: Book Class")
        print("3: View equipment")
        print("4: View Billings")
        print("5: Update Class Schedule")

        #Takes in input and validates it
        choice = int(input("Please select an option: "))
        if choice < 0 or choice > 6:
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
        case 4:
            getBillings(cur)
        case 5:
            updateClass(cur)
def updateClass(cur):
    print("Current Classes:")
    getBookings(cur)
    
    class_id = input("Enter the Class ID you want to update: ")
    
    # Get the current class details
    cur.execute("SELECT start_time, end_time, date, trainer_id FROM class WHERE class_id = %s", (class_id,))
    class_info = cur.fetchone()
    
    if class_info:
        current_start_time, current_end_time, current_date, trainer_id = class_info
        print("Current Date:", current_date)
        print("Current Start Time:", current_start_time)
        print("Current End Time:", current_end_time)
        
        new_date = input("Enter the new date (YYYY-MM-DD): ")
        new_start_time = input("Enter the new start time (HH:MM:SS): ")
        new_end_time = input("Enter the new end time (HH:MM:SS): ")
        
        # Check if the trainer is available at the new time
        trainer_available_query = """
            SELECT EXISTS (
                SELECT 1
                FROM available_time
                WHERE date = %s AND start_time = %s AND end_time = %s AND trainer_id = %s
            )
        """
        cur.execute(trainer_available_query, (new_date, new_start_time, new_end_time, trainer_id))
        trainer_available = cur.fetchone()[0]
        
        if trainer_available:
            # Update the class with the new details
            update_query = """
                UPDATE class
                SET start_time = %s, end_time = %s, date = %s
                WHERE class_id = %s
            """
            cur.execute(update_query, (new_start_time, new_end_time, new_date, class_id))
            print("Class details updated successfully!")
        else:
            print("The trainer is not available at the specified time.")
    else:
        print("Invalid Class ID.")




def getBillings(cur):
    # SQL query to fetch all billing information along with member details
    query = """
    SELECT b.billing_id, m.name AS member_name, b.date_billed, b.payed
    FROM billing b
    JOIN member m ON b.member_id = m.member_id
    ORDER BY b.date_billed DESC
    """
    cur.execute(query)

    # Fetch all rows
    rows = cur.fetchall()

    if rows:
        print("Billing Information:")
        print("-" * 50)
        for row in rows:
            billing_id, member_name, date_billed, payed = row
            status = "Paid" if payed else "Pending"
            print(f"Billing ID: {billing_id}")
            print(f"Member Name: {member_name}")
            print(f"Date Billed: {date_billed.strftime('%Y-%m-%d')}")
            print(f"Status: {status}")
            print("-" * 50)
    else:
        print("No billing records found.")

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
    getUnassignedClasses(cur)
    classID = input("Enter Class ID: ")
    cur.execute("SELECT start_time, end_time, date FROM class WHERE class_id = %s", (classID,))
    classInfo = cur.fetchone()

    if classInfo:
        start_time, end_time, class_date = classInfo
        query = """
        SELECT 
            r.room_id,
            r.room_number,
            r.name AS room_name
        FROM 
            room r
        WHERE 
            r.room_id NOT IN (
                SELECT 
                    b.room_id 
                FROM 
                    booking b
                JOIN 
                    class c ON b.class_id = c.class_id 
                WHERE 
                    c.start_time = %s AND c.end_time = %s AND c.date = %s
            )
        """
        cur.execute(query, (start_time, end_time, class_date))
        rows = cur.fetchall()

        if rows:
            print("\nAvailable Rooms for Class ID", classID, "on", class_date, "from", start_time, "to", end_time)
            print("-" * 50)
            for row in rows:
                room_id, room_number, room_name = row
                print("Room ID:", room_id)
                print("Room Number:", room_number)
                print("Room Name:", room_name)
                print("-" * 50)
            roomID = input("Enter a room ID: ")
            cur.execute("INSERT INTO booking (class_id, room_id) VALUES (%s, %s)", (classID, roomID))
            print("Booking successful!")
        else:
            print("No available rooms for the selected class.")
    else:
        print("Invalid Class ID.")

        
def getUnassignedClasses(cur):
    query = """
    SELECT 
        c.class_id,
        c.class_name,
        c.start_time,
        c.end_time,
        c.date,
        c.purpose,
        c.description,
        e.name AS trainer_name,
        c.max_attendance,
        c.current_num_attendees
    FROM 
        class c
    LEFT JOIN 
        booking b ON c.class_id = b.class_id
    LEFT JOIN 
        trainer t ON c.trainer_id = t.trainer_id
    LEFT JOIN 
        employee e ON t.employee_id = e.employee_id
    WHERE 
        b.booking_id IS NULL;
    """
    cur.execute(query)
    rows = cur.fetchall()

    if rows:
        print("\nUnassigned Classes:")
        print("-" * 50)
        for row in rows:
            class_id, class_name, start_time, end_time, date, purpose, description, trainer_name, max_attendance, curr_attendees = row
            print("\nClass ID:", class_id)
            print("Class Name:", class_name)
            print("Date:", date)
            print("Time:", start_time, "-", end_time)
            print("Purpose:", purpose)
            print("Description:", description)
            print("Trainer:", trainer_name)
            print("Maximum Attendance:", max_attendance)
            print("Current Number of Attendees:", curr_attendees)
            print("-" * 50)
    else:
        print("No available classes found.")

def getBookings(cur):
    query = """
        SELECT 
            b.booking_id, 
            c.class_id, 
            c.start_time, 
            c.end_time, 
            c.date, 
            c.purpose, 
            c.description, 
            r.room_id, 
            r.room_number, 
            r.name AS room_name, 
            e.name AS trainer_name
        FROM 
            booking b
        JOIN 
            class c ON b.class_id = c.class_id
        JOIN 
            room r ON b.room_id = r.room_id
        JOIN 
            trainer t ON c.trainer_id = t.trainer_id
        JOIN 
            employee e ON t.employee_id = e.employee_id
    """
    cur.execute(query)

    rows = cur.fetchall()
    print("Bookings:")
    print("-"*50)
    for row in rows:
        bookingID = row[0]
        classID = row[1]
        start_time = row[2]
        end_time = row[3]
        date = row[4]
        purpose = row[5]
        description = row[6]
        roomID = row[7]
        roomNum = row[8]
        roomName = row[9]
        trainer = row[10]
        print("\nBooking ID:", bookingID, "Class ID:", classID, "Room ID:", roomID)
        print(purpose, "Class with", trainer, "at", start_time, "to", end_time, "on", date, "in", roomName, "(" + str(roomNum) + ")")
        print("Description:", description)
        print("-"*50)

    

