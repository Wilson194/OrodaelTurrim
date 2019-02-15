class PlayerResources:
    def __init__(self, resources: int, income: int):
        self.__resources = resources
        self.__income = income

    def add_resources(self, amount: int) -> None:
        self.__resources += amount

    def remove_resources(self, amount: int) -> None:
        self.__resources -= amount

    @property
    def resources(self):
        return self.__resources

    @property
    def income(self):
        return self.__income
