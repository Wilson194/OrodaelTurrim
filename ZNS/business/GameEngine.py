from ZNS.business.GameMap import GameMap


class GameEngine:
    def __init__(self, turns, game_map: GameMap):
        self.__remaining_turns = turns
        self.__game_map = game_map
        self.__players = []
        self.__player_resources = {}
        self.__player_incomes = {}
        self.__player_units = {}
        self.__defender_bases = {}
        self.__game_object_hit_points = {}
        self.__game_object_effects = {}
        self.__game_object_positions = {}


    @property
    def game_map(self):
        return self.__game_map


    @game_map.setter
    def game_map(self, value):
        self.__game_map = value
