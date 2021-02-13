from BaseBot import BaseBot
from selenium import webdriver
import pickle

class WalmartBot(BaseBot):
    def __init__(self, username, password, config_dict):
        self.username = username
        self.password = password
        self.config = config_dict
        options = webdriver.FirefoxOptions()
        # options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)
    
    def navigate(self, url):
        self.driver.get(url)
        pass

    def login(self):
        pass

    def add_to_cart(self):
        pass

    def checkout(self):
        pass

    def finish(self):
        self.driver.close()
        return