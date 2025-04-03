'''

@author Maurice Amon
'''
from abc import ABC, abstractmethod

from observer.Observable import Observable


class Observer(ABC):

    @abstractmethod
    def update(self, observable: Observable) -> None:
        pass