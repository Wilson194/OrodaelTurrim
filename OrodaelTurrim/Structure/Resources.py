class PlayerResources:
    """ Structure that hold information about player resources """


    def __init__(self, resources: int, income: int):
        self.__resources = resources
        self.__income = income


    def add_resources(self, amount: int) -> None:
        """ Add amount of resources """
        self.__resources += amount


    def remove_resources(self, amount: int) -> None:
        """ Remove amount of resources """
        self.__resources -= amount


    @property
    def resources(self) -> int:
        return self.__resources


    @property
    def income(self) -> int:
        return self.__income
