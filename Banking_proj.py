#imports

from Banking_init import db,mycur
from art import *
import base64


#functions()

def AddAccount():
    print("\n\nCreating new account")
    ano = input("Account number:\n")
    fname = input("First Name:\n")
    lname=input("Last Name:\n")
    dob=input("Date Of Birth [yyyy-mm-dd]:\n")
    c_balance = input("Checking Account Balance:\n")
    s_balance = input("Savings Account Balance:\n")
    doa = input("Date Of Account Creation [yyyy-mm-dd]:\n")
    sql = "insert into accounts values("+ ano +",'" + fname + "','"+ lname+"','"+ dob + "'," +c_balance+ "," +s_balance+",'" +doa+"')"
    mycur.execute(sql)
    db.commit()
    print("\n\nAccount Created\n\n")
    temp=input()
    
def ViewAccount():
    sql="select * from accounts"
    mycur.execute(sql)
    r=mycur.fetchall()
    cnt=mycur.rowcount
    print("\n\nTotal number of rows :",cnt)

    print("~"*123)
    print("|%8s | %28s| %28s| %10s | %10s | %10s | %10s |" %("Acc_Num","First Name".ljust(28),"Last Name".ljust(28),"DOB","C_Balance","S_Balance","Created on"))
    print("~"*123)
    for ano,fname,lname,dob,c_balance,s_balance,doa in r:
        print("|%8d | %28s| %28s| %10s | %10.2f | %10.2f | %10s |" %(ano,fname.ljust(28),lname.ljust(28),dob,c_balance,s_balance,doa))
    print("~"*123+"\n\n")
    temp=input()

def SearchAccount():
    ano =input("\n\nEnter Account Number: ")
    sql = "select * from accounts where account_number = " + ano 
    mycur.execute(sql)
    r=mycur.fetchone()
    if r == None:
        print("\n\n[+]Account Not found\n\n")
        temp=input()
    else:
        print("\n\nFound...")
        print("Account Number :", r[0])
        print("First Name     :", r[1])
        print("Last Name      :", r[2])
        print("DOB            :", r[3])
        print("Total Balance  :", r[4]+r[5])
        print("C_Balance      :", r[4])
        print("S_Balance      :", r[5])
        print("Created On     :", r[6],"\n\n")
        temp=input()
    
def Deposit():
    ano =input("\n\nEnter Account Number: ")
    sql = "select * from accounts where account_number = "+ano
    mycur.execute(sql)
    r=mycur.fetchall()
    if r == ():
        print("\n\n[+]Account is not present\n\n")
        temp=input()
    else:
        amount=input("Enter Amount: ")
        CorS= input("Checking or Savings Account((C/c),(S/s)): ")
        if CorS in "cC":
            sql="update accounts set checkings_balance = checkings_balance + " + amount + " where account_number = " + ano
            mycur.execute(sql)
            print("\n\n[+] Deposited Successfully\n\n")
            temp=input()
        elif CorS in "Ss":
            sql="update accounts set savings_balance = savings_balance + " + amount + " where account_number = " + ano
            mycur.execute(sql)
            print("\n\n[+] Deposited Successfully\n\n")
            temp=input()
        else:
            print("\n\n[+] Enter a valid choice\n\n")
            temp=input()
        
        db.commit()
    
def Withdraw():
    ano =input("\n\nEnter Account Number: ")
    sql = "select * from accounts where account_number = "+ano
    mycur.execute(sql)
    r=mycur.fetchall()
    if r == ():
        print("\n\n[+] Account is not present\n\n")
        temp=input()
    else:
        amount=input("Enter Amount: ")
        CorS= input("Checking or Savings Account((C/c),(S/s)): ")
        if CorS in "cC":
            sql="update accounts set checkings_balance = checkings_balance - " + amount + " where account_number = " + ano
            mycur.execute(sql)
            print("\n\n[+] Successfull\n\n")
            temp=input()
        elif CorS in "Ss":
            sql="update accounts set savings_balance = savings_balance - " + amount + " where account_number = " + ano
            mycur.execute(sql)
            print("\n\n[+] Successfull\n\n")
            temp=input()
        else:
            print("\n\n[+] Enter a valid choice\n\n")
            temp=input()
        
        db.commit()    

def MoneyTransfer():
    ano=input("\n\nEnter your Account Number\n")
    sql="select * from accounts where account_number = "+ano
    mycur.execute(sql)
    r=mycur.fetchone()
    if r!=None:
        trans_amt=input("Amount to be transferred:\n")
        if float(trans_amt) >= float(r[4]):
            print("\n\n[+] Insufficient funds in Checkings Account\n\n")
            temp=input()
        else:
            target_account=input("Enter the Target Account Number:\n")
            sql="update accounts set checkings_balance = checkings_balance - " + trans_amt + " where account_number = " + ano
            mycur.execute(sql)
            sql="update accounts set checkings_balance = checkings_balance + " + trans_amt + " where account_number = " + target_account
            mycur.execute(sql)
            confirm="Do you wish to continue to transfer money from "+ano+" to "+ target_account+" (y/Y)\n"
            a=input(confirm)
            if a in "Yy":
                db.commit()
                print("\n\n[+] Successfull\n\n")
                temp=input()
            else:
                print("\n\n[+] Unsuccessfull\n\n")
                temp=input()

    else:
        print("\n\n[+] Account not present\n\n")

def CheckingSavingsTransfer():
    ano =input("\n\nEnter Account Number: ")
    sql = "select * from accounts where account_number = "+ano
    mycur.execute(sql)
    r=mycur.fetchone()
    if r == None:
        print("\n\n[+] Account is not present\n\n")
        temp=input()
    else:
        CorS= input("1. Checkings to Savings Account\n2. Savings to Checkings Account(s2c/S2C)\n")
        amount=input("Enter Amount: \n")
        
        if CorS == "1":
            if float(amount) >= float(r[4]):
                print("\n\n[+] Insufficient funds in Checkings Account\n\n")
                temp=input()
            else:
                sql="update accounts set checkings_balance = checkings_balance - " + amount + " where account_number = " + ano
                mycur.execute(sql)
                sql="update accounts set savings_balance = savings_balance + " + amount + " where account_number = " + ano
                mycur.execute(sql)
        elif CorS == "2":
            if float(amount) >= float(r[5]):
                print("\n\n[+] Insufficient funds in Savings Account\n\n")
                temp=input()
            else:
                sql="update accounts set savings_balance = savings_balance - " + amount + " where account_number = " + ano
                mycur.execute(sql)
                sql="update accounts set checkings_balance = checkings_balance + " + amount + " where account_number = " + ano
                mycur.execute(sql)
        else:
            print("\n\n[+] Enter a valid choice\n\n")
            temp=input()
        
        confirm="Do you wish to continue to transfer "+ amount+ " (Y/y)"
        a=input(confirm)
        if a in "Yy":
            db.commit()
        else:
            print("\n\n[+] Unsuccessfull\n\n")
            temp=input() 

def Delete():
    ano =input("\n\nEnter Account Number: ")
    sql = "select * from accounts where account_number = "+ano
    mycur.execute(sql)
    r=mycur.fetchall()
    if r == ():
        print("\n\n[+] Account is not present\n\n")
        temp=input()
    else:
        print(r)
        sql="delete from accounts where account_number = "+ano
        mycur.execute(sql)
        confirm=input("Type Y/y to confirm -> ")
        if confirm in "Yy":
            db.commit()
            print("\n\nAccount Deleted\n\n") 
            temp=input()

def DeleteAll():
    sql = "select * from accounts"
    mycur.execute(sql)
    r=mycur.fetchall()
    if r == ():
        print("\n\n[+] Account is not present\n\n")
        temp=input()
    else:
        print(r)
        sql="delete from accounts"
        mycur.execute(sql)
        confirm=input("Enter confirmation key -> ")
        res = bytes(confirm, 'utf-8') 
        if base64.b64encode(res) == b"ZGVhZHBvb2w=":
            db.commit() 
            print("\n\n[+] Successfully Entered the master key...\n[+] Deleting all RECORDS.....\n[+] Successfull\n\n")
            temp=input()
        else:
            print("\n\n[+] Changes not comitted\n\n")
            temp=input()




# _main_()

# Ascii Art  
tprint("Banking ",font="big",chr_ignore=True)
tprint("Management",font="big",chr_ignore=True)
tprint("System",font="big",chr_ignore=True)

# Menu
while True:
    ch=input(" A. Add Account\n V. View Account \n S. Search Account \n D. Deposit Money \n W. Withdraw Money\n B. Tranfer (Checkings-Savings and vica-versa) \n T. Money Transfer (One Account to another) \n L. Delete \n Q. Quit\nChoice -> ")
    if ch in "Aa":
        AddAccount()
    elif ch in "Vv":
        ViewAccount()
    elif ch in "Ss":
        SearchAccount()
    elif ch in "Dd":
        Deposit()
    elif ch in "Ww":
        Withdraw()
    elif ch in "Ll" :
        Delete()
    elif ch in "Tt":
        MoneyTransfer()
    elif ch in "bB":
        CheckingSavingsTransfer()
    elif ch in "qQ":
        break
    elif ch == "delall":
        DeleteAll()
    else:
        print("\n\n[+] Enter a valid choice\n\n")
db.close()