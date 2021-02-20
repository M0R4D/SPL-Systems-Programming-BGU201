import sqlite3
import atexit

conn = sqlite3.connect('moncafe.db')
cursor = conn.cursor()


def close_db():
    conn.commit()
    conn.close()


# register close_db to be called when the interpreter terminates
atexit.register(close_db)


# --------------------------------------------------------------------------------------
#  print_tables function
#  this function calls another function to print the info in the database tables
# --------------------------------------------------------------------------------------
def print_tables():
    print("Activities")
    check = print_activities()  # to check if we want to print Employees Report or no there activities now
    print("Coffee stands")
    print_specific_table("Coffee_stands")
    print("Employees")
    print_specific_table("Employees")
    print("Products")
    print_specific_table("Products")
    print("Suppliers")
    print_specific_table("Suppliers")
    return check


def print_specific_table(table):
    cursor.execute('SELECT * FROM ' + table + ' ORDER BY id ASC')
    table_list = cursor.fetchall()
    i = 0  # actually this var was added for no reason
    for item in table_list:
        i = i + 1
        print("{}".format(str(item)))


def print_activities():
    cursor.execute("SELECT * FROM Activities ORDER BY date ASC")
    activities_list = cursor.fetchall()
    i = 0
    for activity in activities_list:
        i = i+1
        print(activity)
    return i


def employees_report():
    print()
    print("Employees report")
    cursor.execute("SELECT empl.name, empl.salary, coff.location FROM Employees empl "
                   "JOIN Coffee_stands coff ON empl.coffee_stand = coff.id ORDER BY empl.name ASC")
    list = cursor.fetchall()
    cursor.execute("""SELECT empl.name,act.quantity,pro.price FROM Activities act
                      JOIN Products pro ON act.Product_id=pro.id 
                      Join Employees empl ON act.activator_id=empl.id ORDER BY empl.name ASC""")
    list2 = cursor.fetchall()
    total_sale = []
    names = []
    for item in list2:
        if float(item[1]) < 0:
            new = True
            i = 0
            for s in names:
                if s == item[0]:
                    total_sale[i] = total_sale[i] + (-1 * float(item[1]) * float(item[2]))
                    new = False
                    break
                else:
                    i += 1
            if new:
                total_sale.append(-1 * float(item[1]) * float(item[2]))
                names.append(str(item[0]))
    for item in list:
        i = 0
        there = True
        for name in names:
            if name == str(item[0]):
                print(str(item[0] + " " + str(item[1]) + " " + str(item[2]) + " " + str(total_sale[i])))
                there = False
                break
            else:
                i += 1
        if there:
            print(str(item[0]) + " " + str(item[1]) + " " + str(item[2]) + " 0")


def activity_report():
    cursor.execute("""SELECT act.date, pro.description, act.quantity,empl.name,supp.name FROM Activities act
                       JOIN Products pro ON act.Product_id = pro.id
                       LEFT JOIN Employees empl ON act.activator_id = empl.id
                       LEFT JOIN Suppliers supp ON act.activator_id = supp.id ORDER BY date ASC""")
    detailed = cursor.fetchall()
    if detailed:
        print()
        print("Activities")
        for item in detailed:
            print(item)


def main():
    i = print_tables()  # just a trick to not print employees report when the Activities table is EMPTY
    # if i > 0:
    employees_report()
    activity_report()


main()
