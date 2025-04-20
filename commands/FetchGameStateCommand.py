'''

@author Maurice Amon
'''
from commands.Command import Command
from commands.requests.FetchGameStateRequest import FetchGameStateRequest


class FetchGameStateCommand(Command):

    def __init__(self, request: FetchGameStateRequest, conn):
        pass
