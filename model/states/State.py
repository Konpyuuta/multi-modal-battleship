'''

@author Maurice Amon
'''
from abc import ABC


class State(ABC):

    def handle_action(self, object):
        pass