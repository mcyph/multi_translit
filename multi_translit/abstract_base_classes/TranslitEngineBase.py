from abc import ABC, abstractmethod
from iso_tools.ISOTools import ISOTools


class TranslitEngineBase(ABC):
    def __init__(self):
        self.DEngines = self.get_D_engines()

    @abstractmethod
    def get_D_engines(self):
        pass

    def get_possible_conversions_list(self):
        return tuple(self.DEngines.keys())

    @abstractmethod
    def translit(self, from_, to, s):
        """

        :param from_:
        :param to:
        :param s:
        :return:
        """
        pass
