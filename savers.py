from abc import ABC, abstractmethod


class Saver(ABC):
    pass


class SaverJSON(Saver):
    pass


class SaverCSV(Saver):
    pass


class SaverXLS(Saver):
    pass
