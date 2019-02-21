from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from OrodaelTurrim.Business.GameEngine import GameEngine


class MapProxy:
    def __init__(self, game_engine: "GameEngine"):
        self.bases_position = game_engine.bases_positions
        self.get_terrain_type = game_engine.get_terrain_type
        del game_engine


class GameObjectProxy:
    def __init__(self, game_engine: "GameEngine"):
        self.get_visible_enemies = game_engine.get_visible_enemies
        self.get_type = game_engine.get_type
        self.get_current_hit_points = game_engine.get_current_hit_points
        self.get_attribute = game_engine.get_attribute
        self.get_attack_effects = game_engine.get_attack_effect
        self.get_resistances = game_engine.get_resistances
        del game_engine
