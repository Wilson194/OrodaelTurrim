from OrodaelTurrim.Business.GameEngine import GameEngine


class ActionProxy:
    def __init__(self, game_engine: GameEngine):
        del game_engine


class DataProxy:
    def __init__(self, game_engine: GameEngine):
        self.get_map_size = game_engine.game_map.size

        del game_engine
