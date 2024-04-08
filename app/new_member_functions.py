def newMemberMenu():
    while True:
        #Prints all options
        print("Welcome newcomer!")
        print("\n0: Exit Program")
        print("1: View Subscriptions")
        print("2: Register")


        #Takes in input and validates it
        choice = int(input("Please select an option: "))
        if choice < 0 or choice > 2:
            print("\nInvalid input. Please enter a number between 0 and 4.\n ")
        else:
            return choice
#Calls the appropriate CRUD function based on the user's choice
def newMemberexecuteChoice(choice,cur):
    match(choice):
        case 0:
            print("Connection Closed")
        case 1:
            getTiers(cur)
        case 2:
            addMember(cur)
        
#Adds Member to Database
def addMember(cur):
    name = input("Enter your Name: ")
    tier = input("Enter the tier number: ")
    memberTuple = (name,tier)

    insert_query = "INSERT INTO member (name, subscription_id) VALUES (%s, %s)"
    cur.execute(insert_query, memberTuple)
    return 0
#Prints all the tiers of every student
def getTiers(cur):
    selectQuery = "SELECT * FROM subscription"
    cur.execute(selectQuery)
    tiers = cur.fetchall()
    #(id,tier,desc,price)

    if tiers:
        print("\nAll available subscriptions:")
        for tier in tiers:
            print("\n"+ tier[1]+" ID:", tier[0])
            print("Description:", tier[2])
            print("Price:",str(tier[3]) +"$ montly")
    else:
        print("\nNo subscriptions found in the database.")
