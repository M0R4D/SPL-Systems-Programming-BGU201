from qaPersistence import *

import sys

from qaPrintdb import printdb

def main(args):
    inputfilename = args[1]
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline = line.strip().split(", ")
            activity = Activitie(*splittedline)
            #check if product exists
            product = repo.products.find(id=activity.product_id)
            if(len(product) < 1):
                continue
            product = product[0]
            activator = repo.suppliers.find(id = activity.activator_id)+repo.employees.find(id = activity.activator_id)
            #check if the activator exists
            if(len(activator) < 1):
                continue
            product.quantity += int(activity.quantity)
            #check if we have enough to sell
            if (product.quantity < 0):
                continue
            #update product in database
            repo.products.delete(id=product.id)
            repo.products.insert(product)
            #insert activity
            repo.activities.insert(activity)

   # printdb()

if __name__ == '__main__':
    main(sys.argv)
