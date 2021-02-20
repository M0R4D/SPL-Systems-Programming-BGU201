import sqlite3
import os         # for check the existance of file, remove it if necessary
import sys
import atexit

# start a connection with the "moncafe.db" database
# if the database isn't found we create it else remove it and build a new fresh one
if __name__ == '__main__':
    DBExist = os.path.isfile('moncafe.db')
    if not DBExist:
        conn = sqlite3.connect('moncafe.db')
        cursor = conn.cursor()
    else:
        os.remove('moncafe.db')  # remove the 'moncafe.db' file if it exist and call 'create_tables()' function
        conn = sqlite3.connect('moncafe.db')
        cursor = conn.cursor()


def close_db():
    conn.commit()
    conn.close()


# register close_db to be called when the interpreter terminates
atexit.register(close_db)


# ---------------------------------------------------------------------
#  create_tables() function
#  creates 5 database empty tables: 
#  'Coffee_stand', 'Products', 'Employees', 'Suppliers' and 'Activities'
# ---------------------------------------------------------------------
def create_tables():
    # build a new database 
    cursor.execute(""" CREATE TABLE Coffee_stands(id                  INTEGER PRIMARY KEY,
                                                location            TEXT NOT NULL,
                                                number_of_employees  INTEGER )
                        """)
    cursor.execute(""" CREATE TABLE Products(   id              INTEGER PRIMARY KEY,
                                                description     TEXT NOT NULL,
                                                quantity        INTEGER NOT NULL,
                                                price           REAL NOT NULL)
                        """)
    cursor.execute(""" CREATE TABLE Employees(   id              INTEGER PRIMARY KEY,
                                                name            TEXT NOT NULL,
                                                salary          REAL NOT NULL,
                                                coffee_stand    REFERENCES Coffee_stands(id))
                        """)
    cursor.execute(""" CREATE TABLE Suppliers(  id                     INTEGER PRIMARY KEY,
                                                name                    TEXT NOT NULL,
                                                contact_information     TEXT)
                        """)
    cursor.execute(""" CREATE TABLE Activities( product_id      INTEGER REFERENCES product(id),
                                                quantity        INTEGER NOT NULL,
                                                activator_id    INTEGER NOT NULL,
                                                date            DATE NOT NULL)
                        """)


# -----------------------------------------------------------------------
#  insert_data() function
#  insert given data from 'configfile.txt' to correct tables: 
#  "C" = coffee_stand, "P" = products, "E" = employee, "S" = suppliers 
# -----------------------------------------------------------------------
def insert_data(line):
    item = line.split(", ")
    s = item
    if item[0] == "C":
        # s = item.split(", ")
        add_stand(int(s[1]), s[2], int(s[3]))
    if item[0] == "S":
        # s = item.split(", ")
        add_supplier(int(s[1]), s[2], s[3])
    if item[0] == "E":
        # s = item.split(", ")
        add_employee(int(s[1]), s[2], float(s[3]), int(s[4]))
    if item[0] == "P":
        # s = item.split(", ")
        add_product(int(s[1]), s[2], float(s[3]))


def add_product(_id, _desc, _price):
    cursor.execute("""
        INSERT INTO Products (id, description, price, quantity) VALUES (?, ?, ?, ?)
    """, [_id, _desc, _price, 0])


def add_stand(_id, _loc, _empnum):
    cursor.execute("""
        INSERT INTO Coffee_stands (id, location, number_of_employees) VALUES (?, ?, ?)
    """, [_id, _loc, _empnum])


def add_employee(_id, _name, _salary, _standID):
    cursor.execute("""
        INSERT INTO Employees (id, name, salary, coffee_stand) VALUES (?, ?, ?, ?)
    """, [_id, _name, _salary, _standID])


def add_supplier(_id, _name, _coninfo):
    cursor.execute("""
        INSERT INTO Suppliers (id, name, contact_information) VALUES (?, ?, ?)
    """, [_id, _name, _coninfo])


# --------------------------------------------------------------
# 1. call to the create_tables() function to create new tables
# 2. read the given config file and store it into string
# 3. insert the data given by this file into the correct tables
# --------------------------------------------------------------
if __name__ == '__main__':
    create_tables()
    file_to_open = sys.argv[1]
    inputfile = open(file_to_open, "r")
    inputfile = inputfile.read()
    lines = inputfile.split("\n")
    for line in lines:
        # print(line) // this is very good tool for debugging and check the correctness for the inputfile :)
        insert_data(line)
