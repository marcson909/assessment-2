import csv
import os
my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../data/inventory.csv")

class Inventory:
    
    #init with csv headers
    def __init__(self,id,title,rating,copies_available):
        self.id = id
        self.title = title
        self.rating = rating
        self.copies_available = copies_available
    
    #str dunder if needing to output objects
    def __str__(self):
        return f"""Title: {self.title},Rating: {self.rating}, Copies Available: {self.copies_available}
        """

    #class method to read in csv data and output to inventory object that can be imported in interface
    @classmethod
    def get_all_inventory(cls):
        with open(path, 'r') as inventory_file:
            inv_reader = csv.DictReader(inventory_file)
            inventory_list = []
            for inventory in inv_reader:
                new_inventory = Inventory(inventory['id'], inventory['title'], inventory['rating'],inventory['copies_available'])
                inventory_list.append(new_inventory)
            return inventory_list