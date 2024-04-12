def trainerMenu(name,cur):
    # cur.execute("SELECT employee_id FROM trainer WHERE name=%s", (name,))
    # id= cur.fetchone()[0]
    while True:
        #Prints all options
        print("\nHello trainer", name)
        print("0: Exit Program")
        print("1: Add Class")
        print("2: Search member profile")
        print("3: Add Available Time")


        #Takes in input and validates it
        choice = int(input("Please select an option: "))
        if choice < 0 or choice > 4:
            print("\nInvalid input. Please enter a number between 0 and 4.\n ")
        else:
            return choice
            
#Calls the appropriate CRUD function based on the user's choice
def trainerExecuteChoice(choice,id,cur):
    match(choice):
        case 0:
            print("Connection Closed")
        case 1:
            addClass(cur,id)
        case 2:
            searchMember(cur)
        
def searchMember(cur):
    memberName = input("\nEnter member's name: ")

    checkMember = "SELECT COUNT(*) FROM member WHERE name = %s;"
    cur.execute(checkMember, (memberName,))
    exists = cur.fetchone()[0]

    if exists > 0:
        # Fetching member's goals
        queryGoals = """
            SELECT g.description
            FROM member m
            JOIN goal g ON m.member_id = g.member_id
            WHERE m.name = %s;
            """
        cur.execute(queryGoals, (memberName,))
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
        cur.execute(queryMetrics, (memberName,))
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
    cur.execute(query,(time, purpose, description, id, max, curr))
    print("Class added successfully!")