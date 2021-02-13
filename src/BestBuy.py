from BaseBot import BaseBot
from selenium import webdriver
import pickle

class BestBuyBot(BaseBot):
    def __init__(self, username, password, config_dict):
        self.username = username
        self.password = password
        self.config = config_dict
        # self.driver = webdriver.Chrome(chrome_options=webdriver.ChromeOptions())
    
    def navigate(self):
        pass
    
    def login(self):
        pass

    def add_to_cart(self):
        pass

    def checkout(self):
        pass