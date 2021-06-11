
import csv
import os
my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../data/customers.csv")

class Customer:
    
    #init with csv headers as attributes
    def __init__(self, id, first_name, last_name, current_video_rentals):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.current_video_rentals = current_video_rentals

    #str dunder for printing if needing to print objects
    def __str__(self) -> str:
        return f"ID: {self.id}, Name: {self.first_name} {self.last_name}, Rentals: {self.current_video_rentals}"
    
    #csv reader class method to output customer objects
    @classmethod
    def get_all_customers(cls):
        with open(path, 'r') as customers_file:
            customers = csv.DictReader(customers_file)
            customers_list = []
            for customer in customers:
                new_customer = Customer(customer['id'], customer['first_name'], customer['last_name'],customer['current_video_rentals'])
                customers_list.append(new_customer)
            return customers_list
