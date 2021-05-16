#Initialistion of the Banking Management System


import pymysql    
db=pymysql.connect(host="localhost",user="strix",password="Netflix_101")
mycur=db.cursor() 
try:
    mycur.execute("create database banking")
    print("[+] Database is created....")
except:
    print("[+] Database already exists")
    mycur.execute("use banking")

try:
	mycur.execute("create table accounts(account_number int primary key, first_name char(28), last_name char(28), DOB date, checkings_balance decimal(8,2), savings_balance decimal(8,2), date_of_creation date)")
	print("[+] Accounts table created")
except:
	print("[+] Table already exists")
