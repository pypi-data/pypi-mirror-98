from abc import ABC, abstractmethod


class Stage(ABC):

    def __init__(self, configs):
        self.configs = configs

    @abstractmethod
    def perform(self, state):
        pass
