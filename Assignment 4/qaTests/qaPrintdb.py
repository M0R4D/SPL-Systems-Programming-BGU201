from qaPersistence import *


def get_employees_report():
    employees_locations = repo.execute_command("""
        SELECT employees.name, employees.salary, coffee_stands.location, employees.id
        FROM employees
        LEFT JOIN coffee_stands ON employees.coffee_stand=coffee_stands.id
        ORDER BY employees.name ASC
        """)
    for i, item in enumerate(employees_locations):
        activities = repo.execute_command("""
            SELECT activities.quantity, price
            FROM activities
            JOIN products ON activities.product_id=products.id
            WHERE activities.activator_id={}
            """.format(item[3]))
        total_sales = 0
        for activity in activities:
            total_sales -= activity[0]*activity[1]
        item = list(item)
        item[3] = total_sales
        employees_locations[i] = item
    return employees_locations

def get_activities():
    activities = repo.execute_command("""
        SELECT activities.date, products.description, activities.quantity, employees.name, suppliers.name
        FROM activities
        JOIN products ON activities.product_id=products.id
        LEFT JOIN employees ON employees.id=activities.activator_id
        LEFT JOIN suppliers ON suppliers.id=activities.activator_id
        ORDER BY activities.date ASC
        """)
    return activities

def printdb():
    output = ""
    print("Activities")
    for item in repo.execute_command("SELECT * FROM activities ORDER BY date ASC"):
        output += str(item)+'\n'
    output += ("Coffee stands")+'\n'
    for item in repo.execute_command("SELECT * FROM coffee_stands ORDER BY id ASC"):
        output += str(item)+'\n'
    output +=("Employees")+'\n'
    for item in repo.execute_command("SELECT * FROM employees ORDER BY id ASC"):
        output += str(item)+'\n'
    output +=("Products")+'\n'
    for item in repo.execute_command("SELECT * FROM products ORDER BY id ASC"):
        output += str(item)+'\n'
    output += ("Suppliers")+'\n'
    for item in repo.execute_command("SELECT * FROM suppliers ORDER BY id ASC"):
        output += str(item)+'\n'
    output += ("\nEmployees report\n")
    for item in get_employees_report():
        output += " ".join(str(x).replace("b\'","\'").replace("\'",'') for x in item)+'\n'
    a = get_activities();
    if len(a):
        output += ("\nActivities\n")
        for item in a:
            output += str(item)+'\n'

    #output = output.replace("b\'", "\'")
    print(output)

if __name__ == '__main__':
    printdb()


o=Product(1,'nnn', 10, 0)
