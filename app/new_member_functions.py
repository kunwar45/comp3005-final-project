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
            return addMember(cur)
        
#Adds Member to Database
def addMember(cur):
    name = input("Enter your Name: ")
    tier = input("Enter the tier number (1,2,3): ")
    tier_name = {"1":"Bronze","2":"Silver","3":"Gold"}
    memberTuple = (name,tier_name[tier])

    insert_query = "INSERT INTO member (name, subscription_id) VALUES (%s, (SELECT subscription_id FROM subscription WHERE tier_name = %s))"
    cur.execute(insert_query, memberTuple)
    return name

#Prints all the tiers of every student
def getTiers(cur):
    selectQuery = "SELECT * FROM subscription"
    cur.execute(selectQuery)
    tiers = cur.fetchall()
    #(id,tier,desc,price)

    if tiers:
        print("\nAll available subscriptions:")
        for i, tier in enumerate(tiers):
            print("\nTier " + str(i+1) + ": " + tier[1])
            print("Description:", tier[2])
            print("Price:",str(tier[3]) +"$ montly")
    else:
        print("\nNo subscriptions found in the database.")
