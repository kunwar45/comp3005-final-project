def trainerMenu(id,cur):
    cur.execute("SELECT name FROM employee WHERE employee_id=%s",id)
    name= cur.fetchone()[0]
    while True:
        #Prints all options
        print("\nHello trainer", name)
        print("0: Exit Program")
        print("1: Add Class")
        print("2: Search member profile")


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

    checkMember= "SELECT COUNT(*) FROM member WHERE name = %s;"
    cur.execute(checkMember, (memberName,))
    exists = cur.fetchone()[0]

    if exists > 0:
        query = """
            SELECT g.description
            FROM member m
            JOIN goal g ON m.member_id = g.member_id
            WHERE m.name = %s;
            """
        
        cur.execute(query, (memberName,))
        rows = cur.fetchall()
        print(memberName,"goals:")
        for row in rows:
            print(row[0])
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