import sqlite3
import sys
import atexit
# import printdb

# connect to 'moncafe.db' database
_conn = sqlite3.connect('moncafe.db')
cursor = _conn.cursor()


def close_db():
    _conn.commit()
    _conn.close()


# register close_db to be called when the interpreter terminates
atexit.register(close_db)


# small bug here that add only add selled activities (activities with positive quantity only)
def update_data_base(line_activity):
    action = line_activity.split(", ")
    _id = int(action[0]); # print(_id)
    action_quantity = int(action[1]); # print(action_quantity)
    activator_id = int(action[2]); # print(activator_id)
    date = int(action[3]); # print(date)
    products_we_have = get_quantity(_id); # print(products_we_have)  # here the problem NoneType, SOLVED new problem
    new_quan = check_legality(products_we_have, action_quantity)
    if new_quan >= 0:
        add_activity(_id, action_quantity, activator_id, date)
        update_product_quantity(_id, new_quan); # print(get_quantity(_id))


def add_activity(_id, quantity, activator_id, date):
    cursor.execute("""
        INSERT INTO Activities (product_id, quantity, activator_id, date) VALUES (?, ?, ?, ?)
    """, [_id, quantity, activator_id, date])  # UPDATE product info with given ID


def get_quantity(_id):
    cursor.execute("""SELECT quantity FROM Products WHERE id =({})""".format(_id))
    quan = cursor.fetchone()
    return quan[0]


def check_legality(current_quantity, action_quantity):
    return current_quantity + action_quantity


def update_product_quantity(product_id, updated_quantity):
    cursor.execute("""
            UPDATE  Products SET quantity = {} WHERE id = {}
        """.format(updated_quantity, product_id))


def print_data_base():
    _conn.commit()
    import printdb


if __name__ == '__main__':
    # DBExist = os.path.isfile('moncafe.db')
    file_to_open = sys.argv[1]
    # with open(file_to_open) as inputfile:  # open the given .txt file in terminal #UPDATE: DONE..
    inputfile = open(file_to_open, "r")
    inputfile = inputfile.read()
    lines = inputfile.split("\n"); #print (lines)
    for line in lines:
        if (line != ''): #print (line)
            update_data_base(line)  
    print_data_base()
