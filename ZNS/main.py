from PyQt5.QtWidgets import QApplication

from ZNS.business.GameEngine import GameEngine
from ZNS.business.GameMap import GameMap
from ZNS.business.MapGenerator import MapGenerator
from ZNS.presenter.Main import MainWindow
from ZNS.structure.Enums import TerrainType


tiles = [
    [TerrainType.RIVER, TerrainType.FIELD, TerrainType.FIELD, TerrainType.FOREST, TerrainType.VILLAGE],
    [TerrainType.MOUNTAIN, TerrainType.FIELD, TerrainType.MOUNTAIN, TerrainType.FIELD, TerrainType.MOUNTAIN],
    [TerrainType.FOREST, TerrainType.MOUNTAIN, TerrainType.FIELD, TerrainType.FIELD, TerrainType.RIVER],
    [TerrainType.VILLAGE, TerrainType.MOUNTAIN, TerrainType.HILL, TerrainType.HILL, TerrainType.HILL],
    [TerrainType.RIVER, TerrainType.FIELD, TerrainType.FOREST, TerrainType.FIELD, TerrainType.FOREST],
]

if __name__ == '__main__':
    game_map = MapGenerator(11, 11).generate()
    # game_map = GameMap(5, 5, generated_tiles)

    print(game_map)
    game_engine = GameEngine(1, game_map)
    MainWindow(game_engine).execute()
