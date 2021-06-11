import unittest
from modules.interface import Interface
import csv
import os

my_path = os.path.abspath(os.path.dirname(__file__))
customer_path = os.path.join(my_path, "../data/customers.csv")
inventory_path = os.path.join(my_path, "../data/inventory.csv")

class VideoInventoryManagerTestCase(unittest.TestCase):
    pass


    