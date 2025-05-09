'''

@author Maurice Amon
'''
from abc import ABC, abstractmethod

from observer.Observer import Observer


class Observable(ABC):

    @abstractmethod
    def add_observer(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def remove_observer(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass