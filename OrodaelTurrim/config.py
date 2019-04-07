from OrodaelTurrim.Structure.Utils import ClassAttributeDefault


class Config(metaclass=ClassAttributeDefault):
    # ----------------- Random seeds -------------------------------------------
    MAP_RANDOM_SEED = 1820843222161343046930772513813123871493369355300037520031959908315255507407847757510
    AI_RANDOM_SEED = 11210686230018916906755194379495289740658359382637268484814676532218288310878131789222
    UNCERTAINTY_RANDOM_SEED = 48933658723568478790618969458655749561435917118099381875922444158914818283903

    # ----------------- Map generator configuration ----------------------------

    # Probability that river will be on the map
    RIVER_ON_MAP_PROBABILITY = 0.9

    # Frequency of each terran type
    MOUNTAIN_FREQUENCY = 0.1
    FIELD_FREQUENCY = 0.5
    HILL_FREQUENCY = 0.1
    FOREST_FREQUENCY = 0.2
    VILLAGE_FREQUENCY = 0.01

    # Percentage bonus for neighbour with same type
    NEIGHBOUR_ADD = 0.01

    MAP_HEIGHT = 11
    MAP_WIDTH = 11
    GAME_MAP = None
