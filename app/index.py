import psycopg2
from CRUD import *
from user_controls import *

def isTrainer(id,cur):
    cur.execute("SELECT EXISTS(SELECT 1 FROM Trainer WHERE employee_id = %s)", (id,))
    return cur.fetchone()[0]

# Function to check if ID exists in Admin table
def isAdmin(id,cur):
    cur.execute("SELECT EXISTS(SELECT 1 FROM Admin WHERE employee_id = %s)", (id,))
    return cur.fetchone()[0]

def isMember(id,cur):
    cur.execute("SELECT EXISTS(SELECT 1 FROM member WHERE member_id = %s)", (id,))
    return cur.fetchone()[0]

# def isRole(id, role, cur):
#     cur.execute("SELECT EXISTS(SELECT 1 FROM member WHERE %s_id = %s)", (role,id,))
#     return cur.fetchone()[0]

def loginMenu(cur,conn):
    while True:
        #Prints all options
        print("\n0: Exit")
        print("1: Employee Sign In")
        print("2: Member Sign In")
        print("3: New Member Sign In")

        #Takes in input and validates it
        choice = int(input("Please select an option: "))
        if choice < 0 or choice > 3:
            print("\nInvalid input. Please enter a number between 0 and 3.\n ")
        else:
            break
    
    if (choice==0):
        print("Connection Closed")
        return
    elif (choice==1):
        id = input("Enter your ID: ")
        if(isAdmin(id,cur)):
            adminControl(id,cur,conn)
        elif (isTrainer(id,cur)):
            trainerControl(id,cur,conn)
        else:
            print("You are not an employee.")
    elif(choice ==2):
        id = input("Enter your ID: ")
        if(isMember(id,cur)):
            memberControl(id,cur,conn)
        else:
            print("No member with that ID.")
    elif(choice==3):
        newMemberControl(cur,conn)

#Main Control Flow. Repeatedly prints the menu for user to choose an option from.
def main():

    username = "postgres"
    password = "db"
    db_port = "5432"
    db_name = "Final"
    database_url = f"postgresql://{username}:{password}@localhost:{db_port}/{db_name}"
    #Attempts to connect to database
    try:
        conn = psycopg2.connect(database_url,)
        cur = conn.cursor()
        print("Connected to database")
        
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
    #Control Flow, prints the seleciton menu and commits changes to the database 
    loginMenu(cur,conn)
    conn.close()
    
if __name__ == "__main__":
    main()