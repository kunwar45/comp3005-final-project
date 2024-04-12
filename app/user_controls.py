from new_member_functions import *
from member_functions import *
from admin_functions import *
from trainer_functions import *
def adminControl(id,cur,conn): 
    choice =-1
    while choice!=0:
   
        choice = adminMenu(id,cur)
        adminExecuteChoice(choice,cur)
        conn.commit()    

def newMemberControl(cur,conn):
    choice =-1
    while choice!=0 and choice!=2:
      
        choice = newMemberMenu()
        name = newMemberexecuteChoice(choice,cur)
        if (choice==2):
            print("You have been successfully registered!")
            memberControl(name,cur,conn)
        conn.commit()

def trainerControl(name,cur,conn):
    choice =-1
    while choice!=0:
        choice = trainerMenu(id,cur)
        trainerExecuteChoice(choice,name,cur)
        conn.commit()

def memberControl(name,cur,conn):
    choice =-1
    while choice!=0:
        choice = memberMenu()
        memberexecuteChoice(choice,name,cur)
        conn.commit()