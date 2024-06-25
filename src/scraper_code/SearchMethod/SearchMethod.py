import abc


class SearchMethod(abc.ABC):

    def __init__(self):
        self.method = ""

    @abc.abstractmethod
    def search(self, organisation_name):
        print("searchmethod/search" + organisation_name)
        pass