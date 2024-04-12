import psycopg2
from user_controls import *

def isTrainer(name,cur):
    cur.execute("SELECT EXISTS(SELECT 1 FROM trainer JOIN employee ON trainer.employee_id = employee.employee_id WHERE employee.name = %s)", (name,))
    return cur.fetchone()[0]

# Function to check if ID exists in Admin table
def isAdmin(name,cur):
    cur.execute("SELECT EXISTS(SELECT 1 FROM admin JOIN employee ON admin.employee_id = employee.employee_id WHERE employee.name = %s)", (name,))
    return cur.fetchone()[0]

def isMember(name,cur):
    cur.execute("SELECT EXISTS(SELECT 1 FROM member WHERE name = %s)", (name,))
    return cur.fetchone()[0]

def loginMenu(cur,conn):
    choice = -1
    while choice != 0:
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
        id = input("Enter your Name: ")
        if(isAdmin(id,cur)):
            adminControl(id,cur,conn)
        elif (isTrainer(id,cur)):
            trainerControl(id,cur,conn)
        else:
            print("You are not an employee.")
    elif(choice ==2):
        name = input("Enter your Name: ")
        if(isMember(name,cur)):
            memberControl(name,cur,conn)
        else:
            print("No member with that name.")
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