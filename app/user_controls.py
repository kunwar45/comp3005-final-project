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
    while choice!=0:
        choice = newMemberMenu()
        newMemberexecuteChoice(choice,cur)
        conn.commit()

def trainerControl(id,cur,conn):
    choice =-1
    while choice!=0:
        choice = trainerMenu(id,cur)
        trainerExecuteChoice(choice,id,cur)
        conn.commit()

def memberControl(id,cur,conn):
    choice =-1
    while choice!=0:
        choice = memberMenu(id,cur)
        memberexecuteChoice(choice,id,cur)
        conn.commit()