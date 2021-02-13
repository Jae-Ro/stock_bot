from abc import ABCMeta, abstractmethod

class BaseBot(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def navigate(self):
        pass

    @abstractmethod
    def login(self):
        pass
    
    @abstractmethod
    def add_to_cart(self):
        pass

    @abstractmethod
    def checkout(self):
        pass

    @abstractmethod
    def finish(self):
        pass