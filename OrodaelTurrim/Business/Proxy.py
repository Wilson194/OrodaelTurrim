from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from OrodaelTurrim.Business.GameEngine import GameEngine


class MapProxy:
    def __init__(self, game_engine: "GameEngine"):
        self.get_bases_positions = game_engine.get_bases_positions
        self.get_terrain_type = game_engine.get_terrain_type
        self.player_have_base = game_engine.player_have_base

        self.get_resources = game_engine.get_resources
        self.get_income = game_engine.get_income

        self.border_tiles = game_engine.get_game_map().border_tiles
        del game_engine


class GameObjectProxy:
    def __init__(self, game_engine: "GameEngine"):
        self.get_visible_enemies = game_engine.get_visible_enemies
        self.get_object_type = game_engine.get_object_type
        self.get_current_hit_points = game_engine.get_current_hit_points
        self.get_attribute = game_engine.get_attribute
        self.get_attack_effects = game_engine.get_attack_effect
        self.get_resistances = game_engine.get_resistances
        del game_engine


class GameControlProxy:
    def __init__(self, game_engine: "GameEngine"):
        self.spawn_unit = game_engine.spawn_unit
        del game_engine


class GameUncertaintyProxy:
    def __init__(self, game_engine: "GameEngine"):
        self.spawn_information = game_engine.spawn_information
        del game_engine
