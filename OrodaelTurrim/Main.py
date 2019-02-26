from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Business.Interface.Player import Player
from OrodaelTurrim.Business.MapGenerator import MapGenerator
from OrodaelTurrim.Presenter.Main import MainWindow
from OrodaelTurrim.Structure.Enums import GameObjectType
from OrodaelTurrim.Structure.GameObjects.GameObject import SpawnInformation
from OrodaelTurrim.Structure.Position import OffsetPosition
from OrodaelTurrim.Structure.Resources import PlayerResources


def main():
    # Generate the map
    game_map = MapGenerator(11, 11).generate()

    # Initialize game engine
    game_engine = GameEngine(game_map)

    player = Player()

    game_engine.register_player(player, PlayerResources(100, 10), [])
    game_engine.start(500)
    game_engine.spawn_unit(SpawnInformation(player, GameObjectType.BASE, OffsetPosition(0, 0), [], []))
    game_engine.spawn_unit(SpawnInformation(player, GameObjectType.ARCHER, OffsetPosition(1, 0), [], []))
    game_engine.spawn_unit(SpawnInformation(player, GameObjectType.ARCHER, OffsetPosition(2, 0), [], []))

    MainWindow(game_engine).execute()


if __name__ == '__main__':
    main()
