from ArtificialIntelligence.Main import AIPlayer
from ExpertSystem.Business.Player import Player
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Business.Logger import LogReceiver
from OrodaelTurrim.Business.MapGenerator import MapGenerator
from OrodaelTurrim.Business.Proxy import MapProxy, GameObjectProxy, GameControlProxy, GameUncertaintyProxy
from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Presenter.Main import MainWindow
from OrodaelTurrim.Structure.Exceptions import IllegalConfigState
from OrodaelTurrim.Structure.Filter.Factory import FilterFactory
from OrodaelTurrim.Structure.Resources import PlayerResources
import click

from OrodaelTurrim.config import Config


@click.command()
@click.option('--gui/--nogui', '/gui;/nogui', 'gui', default=True, help='Disable or enable gui')
@click.option('-r', '--round', 'rounds', type=int, default=1000, help='Specify maximum number of rounds')
@click.option('-l', '--log-output', 'log_output', type=click.Path(), help='Log file output')
def main(gui, rounds, log_output):
    # Load map configuration from config or generate random map
    height = Config.MAP_HEIGHT
    width = Config.MAP_WIDTH

    if (height is None or width is None) and Config.GAME_MAP:
        height = len(Config.GAME_MAP)
        width = len(Config.GAME_MAP[0])

    if height is None or width is None:
        raise IllegalConfigState('You must specify MAP_WIDTH and MAP_HEIGHT or GAME_MAP parameter in config file!')

    game_map = MapGenerator(width, height).generate(Config.GAME_MAP)

    # Initialize game engine
    game_engine = GameEngine(game_map)

    map_proxy = MapProxy(game_engine)
    game_object_proxy = GameObjectProxy(game_engine)
    game_control_proxy = GameControlProxy(game_engine)
    game_uncertainty_proxy = GameUncertaintyProxy(game_engine)

    # Initialize Filter factory
    FilterFactory(map_proxy, game_object_proxy)

    # Initialize Logger
    _ = LogReceiver(game_engine)

    # Register defender
    defender = Player(map_proxy, game_object_proxy, game_control_proxy, game_uncertainty_proxy)
    game_engine.register_player(defender, PlayerResources(500, 10), [])

    # Register attacker
    player2 = AIPlayer(map_proxy, game_object_proxy, game_control_proxy, game_uncertainty_proxy)
    game_engine.register_player(player2, PlayerResources(500, 10, 1), [])
    player2.initialize()

    game_engine.start(rounds)

    if gui:
        # Inicialize main widget
        main_window = MainWindow(game_engine)

        Connector().emit('redraw_ui')
        main_window.execute()

    else:
        current_round = 0
        game_history = game_engine.get_game_history()
        while rounds > current_round and not Connector().get_variable('game_over'):
            game_history.active_player.act()
            game_engine.simulate_rest_of_player_turn(game_history.active_player)

            if game_history.on_first_player:
                current_round += 1

        print('User survive {} rounds'.format(current_round))

    if log_output:
        text = game_engine.get_game_history()
        with open(log_output, 'w') as f:
            f.write(str(text))


if __name__ == '__main__':
    main()
