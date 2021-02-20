from qaPersistence import *

import sys
import os

def add_coffee_stand(splittedline):
    repo.coffee_stands.insert(Coffee_stand(*splittedline))

def add_supplier(splittedline):
    repo.suppliers.insert(Supplier(*splittedline))

def add_product(splittedline):
    repo.products.insert(Product(*splittedline, 0))

def add_employee(splittedline):
    repo.employees.insert(Employee(*splittedline))

adders = {  "C": add_coffee_stand,
            "S": add_supplier,
            "P": add_product,
            "E": add_employee}

def main(args):
    inputfilename = args[1]
    # delete the database file if it exists
    repo._close()
    if os.path.isfile("moncafe.db"):
        os.remove("moncafe.db")
    repo.__init__()
    repo.create_tables()
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline = line.strip().split(", ")
            adders.get(splittedline[0])(splittedline[1:])

if __name__ == '__main__':
    main(sys.argv)
