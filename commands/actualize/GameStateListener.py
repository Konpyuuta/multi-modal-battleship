'''

@author Maurice Amon
'''
from observer.Observable import Observable
from observer.Observer import Observer


class GameStateListener(Observer):

    def __init__(self):
        pass

    def update(self, observable: Observable):


