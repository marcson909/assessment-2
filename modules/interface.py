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
    
    #main menu that loops until user enters 6
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

    # main menu input string to choose from
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
    
    #prints all all inventory objects and their attributes excluding ID
    def view_video_inventory(self):
        print("Video Inventory:\n----------------")
        for inventory in self.all_inventory:
            print(inventory)
        input("Press Enter to continue...")
        
    #ask customer to enter id
    #search for matching id in all customers list
    #if match, convert customer rentals to list and output rentals
    def view_customer_rentals(self):
        cust_id = input("Enter customer id: ")
        for customer in self.all_customers:
            if customer.id == cust_id:
                rental_list = customer.current_video_rentals.split('/')
                rentals = ", ".join(rental_list)
                print(f"Customer: {customer.first_name} {customer.last_name}")
                print(f"Current Rentals: {rentals}")
        input("Press Enter to continue...")
    
    #helper function for bad menu command
    def bad_command(self):
        print ("Command not recognized. Try again\n")
        input("Press Enter to continue...")

    #input new customer info and auto assign customer id as next number in series
    #append new customer info to all_customers object
    #save csv file with new customer data
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
    
    #have customer enter id and check if they have any rentals
    #if rentals > convert customer rentals from string to list
    #enumerate through list and create an ouput list to select which video to return
    #get customer input and pop the selection out of the video list
    #update customer video rental string with new list
    #loop through all inventory and match inventory.title to returned movie title
    #increase inventory.copies_available by 1
    #save updated info to customer csv and inventory csv
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
                        movie_to_be_returned = rental_list[selection-1]
                        rental_list.pop(selection-1)
                        customer.current_video_rentals = "/".join(rental_list)
                        for inventory in self.all_inventory:
                            if movie_to_be_returned == inventory.title:
                                new_copy_count = int(inventory.copies_available) + 1
                                inventory.copies_available = new_copy_count
                        print("Video returned")
                        self.save_customers()
                        self.save_inventory()
                        input("Press Enter to continue...")


    #get customer id and check if customer has less than 3 videos
    #if < 3 videos create a selection menu based on title for customer to pick
    #get customer input and match input to id in csv and then append video title to customer video list
    #decrement video inventory count by 1
    #update customer and inventory csv
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
                                if rental_list == ['']:
                                    rental_list.append(inventory.title)
                                    customer.current_video_rentals = "".join(rental_list)
                                    new_copy_count = int(inventory.copies_available) - 1
                                    inventory.copies_available = new_copy_count
                                else:
                                    rental_list.append(inventory.title)
                                    customer.current_video_rentals = "/".join(rental_list)
                                    new_copy_count = int(inventory.copies_available) - 1
                                    inventory.copies_available = new_copy_count
                        print("Video rental successful")
                        self.save_customers()
                        self.save_inventory()
                    input("Press Enter to continue...")

    #write new data to csv
    def save_customers(self):
        with open(customer_path, 'w') as csvfile:
            customer_csv = csv.writer(csvfile, delimiter=',')
            customer_csv.writerow(['id', 'first_name', 'last_name', 'current_video_rentals'])
            for customer in self.all_customers:
                customer_csv.writerow([customer.id, customer.first_name, customer.last_name, customer.current_video_rentals])
    
    #write new data to csv
    def save_inventory(self):
        with open(inventory_path, 'w') as csvfile:
            inventory_csv = csv.writer(csvfile, delimiter=',')
            inventory_csv.writerow(['id', 'title', 'rating', 'copies_available'])
            for inventory in self.all_inventory:
                inventory_csv.writerow([inventory.id, inventory.title, inventory.rating, inventory.copies_available])