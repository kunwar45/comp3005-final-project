import psycopg2
def trainerMenu(name,cur):
    # cur.execute("SELECT employee_id FROM trainer WHERE name=%s", (name,))
    # id= cur.fetchone()[0]
    while True:
        #Prints all options
        print("\nHello trainer", name)
        print("0: Exit Program")
        print("1: Search member profile")
        print("2: Add Available Time")


        #Takes in input and validates it
        choice = int(input("Please select an option: "))
        if choice < 0 or choice > 2:
            print("\nInvalid input. Please enter a number between 0 and 4.\n ")
        else:
            return choice
            
#Calls the appropriate CRUD function based on the user's choice
def trainerExecuteChoice(choice,name,cur):
    match(choice):
        case 0:
            print("Connection Closed")
        case 1:
            searchMember(cur)
        case 2:
            addAvailableTime(cur,name)
def addAvailableTime(cur,name):
    try:
        cur.execute("SELECT trainer_id FROM trainer JOIN employee ON trainer.employee_id = employee.employee_id WHERE employee.name = %s", (name,))
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
    trainer_id = cur.fetchone()

    # Prompt the trainer for available time details
    date = input("Enter the date (YYYY-MM-DD): ")
    start_time = input("Enter the start time (HH:MM:SS): ")
    end_time = input("Enter the end time (HH:MM:SS): ")
    
    # Insert the available time into the database
    try:
        cur.execute("INSERT INTO available_time (date, start_time, end_time, trainer_id) VALUES (%s, %s, %s, %s)", (date, start_time, end_time, trainer_id[0]))
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
    print("Available time added successfully!")


        
def searchMember(cur):
    memberName = input("\nEnter member's name: ")

    checkMember = "SELECT COUNT(*) FROM member WHERE name = %s;"
    try:
        cur.execute(checkMember, (memberName,))
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
    exists = cur.fetchone()[0]

    if exists > 0:
        # Fetching member's goals
        queryGoals = """
            SELECT g.description
            FROM member m
            JOIN goal g ON m.member_id = g.member_id
            WHERE m.name = %s;
            """
        try:
            cur.execute(queryGoals, (memberName,))
        except psycopg2.Error as e:
            print(f"An error occurred: {e}")
        goals = cur.fetchall()

        if goals:
            print(memberName, "goals:")
            print("-" * 50)
            for goal in goals:
                print(goal[0])
                print("-" * 50)
        else:
            print(memberName, "has no goals.")

        queryMetrics = """
            SELECT weight, height, age
            FROM member m
            JOIN metrics mtr ON m.member_id = mtr.member_id
            WHERE m.name = %s;
            """
        try:
            cur.execute(queryMetrics, (memberName,))
        except psycopg2.Error as e:
            print(f"An error occurred: {e}")
        metrics = cur.fetchone()

        if metrics:
            weight, height, age = metrics
            print("\n" + memberName + "'s Metrics:")
            print("-" * 50)
            print("Weight:", weight)
            print("Height:", height)
            print("Age:", age)
            print("-" * 50)
        else:
            print(memberName, "has no metrics.")
    else:
        print("No member found with that name.")



def addClass(cur,id):
    time = input("Enter class time (HH:MM:SS): ")
    purpose = input("Enter class purpose: ")
    description = input("Enter class description: ")
    max = int(input("Enter max attendance: ")) 
    curr = 0  

    query="""
    INSERT INTO class (time, purpose, description, trainer_id, max_attendance, current_num_attendees)
            VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        cur.execute(query,(time, purpose, description, id, max, curr))
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
    print("Class added successfully!")