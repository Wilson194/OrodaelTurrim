from ArtificialIntelligence.Main import AIPlayer
from ExpertSystem.Business.Player import Player
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Business.MapGenerator import MapGenerator
from OrodaelTurrim.Business.Proxy import MapProxy, GameObjectProxy, GameControlProxy, GameUncertaintyProxy
from OrodaelTurrim.Presenter.Connector import Connector
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

    map_proxy = MapProxy(game_engine)
    game_object_proxy = GameObjectProxy(game_engine)
    game_control_proxy = GameControlProxy(game_engine)
    game_uncertainty_proxy = GameUncertaintyProxy(game_engine)

    # Register defender
    defender = Player(map_proxy, game_object_proxy, game_control_proxy, game_uncertainty_proxy)
    game_engine.register_player(defender, PlayerResources(20, 10), [])

    # Register attacker
    player2 = AIPlayer(map_proxy, game_object_proxy, game_control_proxy, game_uncertainty_proxy)
    game_engine.register_player(player2, PlayerResources(100, 10), [])
    player2.initialize()

    game_engine.start(500)

    # Inicialize main widget
    main_window = MainWindow(game_engine)

    Connector().emit('redraw_ui')
    main_window.execute()


if __name__ == '__main__':
    main()
