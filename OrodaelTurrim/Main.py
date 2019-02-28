from ArtificialIntelligence.Main import AIPlayer
from ExpertSystem.Business.Player import Player
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Business.MapGenerator import MapGenerator
from OrodaelTurrim.Business.Proxy import MapProxy, GameObjectProxy
from OrodaelTurrim.Presenter.Main import MainWindow
from OrodaelTurrim.Structure.Enums import GameObjectType
from OrodaelTurrim.Structure.Filter.MoveFilter import MoveToNearestEnemyFilter, MoveToBaseFilter
from OrodaelTurrim.Structure.GameObjects.GameObject import SpawnInformation
from OrodaelTurrim.Structure.Position import OffsetPosition
from OrodaelTurrim.Structure.Resources import PlayerResources


def main():
    # Generate the map
    game_map = MapGenerator(11, 11).generate()

    # Initialize game engine
    game_engine = GameEngine(game_map)

    # Inicialize main widget
    main_window = MainWindow(game_engine)

    map_proxy = MapProxy(game_engine)
    game_object_proxy = GameObjectProxy(game_engine)

    # Register defender
    defender = Player()
    game_engine.register_player(defender, PlayerResources(100, 10), [])

    # Register attacker
    player2 = AIPlayer()
    game_engine.register_player(player2, PlayerResources(100, 10), [])

    game_engine.start(500)
    game_engine.spawn_unit(SpawnInformation(defender, GameObjectType.BASE, OffsetPosition(0, 0), [], []))
    game_engine.spawn_unit(SpawnInformation(defender, GameObjectType.ARCHER, OffsetPosition(1, 0), [], []))
    game_engine.spawn_unit(SpawnInformation(defender, GameObjectType.ARCHER, OffsetPosition(2, 0), [], []))

    game_engine.spawn_unit(
        SpawnInformation(player2, GameObjectType.DEMON, OffsetPosition(3, 0), [],
                         [MoveToNearestEnemyFilter(map_proxy, game_object_proxy),
                          MoveToBaseFilter(map_proxy, game_object_proxy)]))

    main_window.execute()


if __name__ == '__main__':
    main()
