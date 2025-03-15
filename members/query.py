import models
from django.db import connection

def IsAdmin(self):
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM Account WHERE id = %s and admin = 'True'", [self.id])
        row = cursor.fetchone()
    cursor.close()
    if(row == None): return False
    return True

def checkLogin(self):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Account WHERE email = %s and password = %s", [self.email], [self.password])
        row = cursor.fetchall()
    cursor.close()
    if(row == None): return False
    return cursor

def IsProvider(self):
    with connection.cursor() as cursor:
        cursor.execute("SELECT p.id FROM Property WHERE ownerid = %s", [self.id])
        row = cursor.fetchone()
    cursor.close()
    if(row == None): return False
    return True

def getAccount(self):
    with connection.cursor() as cursor:
        cursor.execute("SELECT p.id FROM Account WHERE ownerid = %s", [self.id])
        row = cursor.fetchall()
    cursor.close()
    return row
    
def getPropertyDetail(self):
    with connection.cursor() as cursor:
        cursor.execute("SELECT p.id FROM Property WHERE ownerid = %s", [self.id])
        row = cursor.fetchall()
    cursor.close()
    return row




## using Account's id, find whether there is available m -> how about distance?
# def IsSizeAvailable(self):
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT * FROM Account as p Join vechicle as v on v.id = p.vechicleid Join Property as pr on pr.owner = p.id WHERE p.id = %s and v.size_width <= pr.size_width and v.size_length <= pr.size_length ", [self.id])
#         row = cursor.fetchone()
        
#     if(row == None): return False
#     return True


## example codes for the rows and records
# import sqlite3

# def getAllRows():
#     try:
#         connection = sqlite3.connect('SQLite_Python.db')
#         cursor = connection.cursor()
#         print("Connected to SQLite")

#         sqlite_select_query = """SELECT * from database_developers"""
#         cursor.execute(sqlite_select_query)
#         records = cursor.fetchall()
#         print("Total rows are:  ", len(records))
#         print("Printing each row")
#         for row in records:
#             print("Id: ", row[0])
#             print("Name: ", row[1])
#             print("Email: ", row[2])
#             print("Salary: ", row[3])
#             print("\n")

#         cursor.close()

