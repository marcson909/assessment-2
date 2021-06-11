from modules.customer import Customer
from modules.inventory import Inventory

import csv
import os
my_path = os.path.abspath(os.path.dirname(__file__))
customer_path = os.path.join(my_path, "../data/customers.csv")
inventory_path = os.path.join(my_path, "../data/inventory.csv")

class Interface:
    def __init__(self):
        self.all_customers = Customer.get_all_customers()
        self.all_inventory = Inventory.get_all_inventory()
    

    def run(self):
        input = self.main_menu()
        while input !=6:
            if input == 1:
                self.view_video_inventory()
                return self.run()
            elif input == 2:
                self.view_customer_rentals()
                return self.run()
            elif input == 3:
                self.rent_video()
                return self.run()
            elif input == 4:
                self.return_video()
                return self.run()
            elif input == 5:
                self.add_new_customer()
                return self.run()
            elif input == 6:
                print("Good bye!")
                break
            else:
                self.bad_command()
                return self.run()


    def main_menu(self):
        return int(input("""
Welcome to Code Platoon Video!
Enter the number associated with the menu item to proceed.
1. View video inventory
2. View customer's rented videos
3. Rent video
4. Return video
5. Add new customer
6. Exit
        """))
    
    def view_video_inventory(self):
        print("Video Inventory:\n----------------")
        for inventory in self.all_inventory:
            print(inventory)
        input("Press Enter to continue...")
        
    def view_customer_rentals(self):
        cust_id = input("Enter customer id: ")
        for customer in self.all_customers:
            if customer.id == cust_id:
                rental_list = customer.current_video_rentals.split('/')
                rentals = ", ".join(rental_list)
                print(f"Customer: {customer.first_name} {customer.last_name}")
                print(f"Current Rentals: {rentals}")
        input("Press Enter to continue...")
    
    def bad_command(self):
        print ("Command not recognized. Try again\n")
        input("Press Enter to continue...")

    def add_new_customer(self):
        new_customer = {'current_video_rentals':""}
        print("Enter Customer Information Below:\n")
        new_customer['first_name'] = input("First name: ")
        new_customer['last_name'] = input("Last name: ")
        new_customer['id'] = int(self.all_customers[len(self.all_customers)-1].id) + 1
        
        self.all_customers.append(Customer(**new_customer))
        print("\nNew Customer successfully created!\n")
        self.save_customers()
        input("Press Enter to continue...")
    

    def return_video(self):
        cust_id = input("Enter customer id: ")
        for customer in self.all_customers:
            if customer.id == cust_id:
                if len(customer.current_video_rentals) == 0:
                    print("You have no rentals to return")
                else:
                    rental_list = customer.current_video_rentals.split('/')
                    for i,rental in enumerate(rental_list):
                        print(f"{i+1}: {rental}")
                    selection = int(input("Which video do you want to return?\nPress 0 to abort\n"))
                    if selection == 0:
                        break
                    else: 
                        rental_list.pop(selection-1)
                        customer.current_video_rentals = "/".join(rental_list)
                        print("Video returned")
                        self.save_customers()
                        input("Press Enter to continue...")

    def rent_video(self):
        cust_id = input("Enter customer id: ")
        for customer in self.all_customers:
            
            if customer.id == cust_id:
                rental_list = customer.current_video_rentals.split('/')
                if len(rental_list) >= 3:
                    print("You can't rent more than 3 videos at a time")
                    input("Press Enter to continue...")
                else:
                    
                    for i, inventory in enumerate(self.all_inventory):
                        if int(inventory.copies_available) > 0:
                            print(f"{i+1}: {inventory.title}")
                    selection = int(input("Which video do you want to rent?\nPress 0 to abort\n"))
                    if selection == 0:
                        break
                    else: 
                        for i, inventory in enumerate(self.all_inventory):
                            if selection == i+1:
                                rental_list.append(inventory.title)
                                customer.current_video_rentals = "/".join(rental_list)
                                print(customer.current_video_rentals)
                                new_copy_count = int(inventory.copies_available) - 1
                                inventory.copies_available = new_copy_count
                        print("Video rental successful")
                        self.save_customers()


                        # rental_list = customer.current_video_rentals.split('/')
                        # for i,rental in enumerate(rental_list):
                        #     print(f"{i+1}: {rental}")
                        # selection = int(input("Which video do you want to return?\nPress 0 to abort\n"))
                        # if selection == 0:
                        #     break
                        # else: 
                        #     rental_list.pop(selection-1)
                        #     customer.current_video_rentals = "/".join(rental_list)
                        #     print("Video returned")
                        #     self.save_customers()
                    input("Press Enter to continue...")

    def save_customers(self):
        with open(customer_path, 'w') as csvfile:
            customer_csv = csv.writer(csvfile, delimiter=',')
            customer_csv.writerow(['id', 'first_name', 'last_name', 'current_video_rentals'])
            for customer in self.all_customers:
                customer_csv.writerow([customer.id, customer.first_name, customer.last_name, customer.current_video_rentals])
    
    def save_inventory(self):
        with open(inventory_path, 'w') as csvfile:
            inventory_csv = csv.writer(csvfile, delimiter=',')
            inventory_csv.writerow(['id', 'title', 'rating', 'copies_available'])
            for inventory in self.all_inventory:
                inventory_csv.writerow([inventory.id, inventory.title, inventory.rating, inventory.copies_available])