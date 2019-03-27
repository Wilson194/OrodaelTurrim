from ArtificialIntelligence.Main import AIPlayer
from ExpertSystem.Business.Player import Player
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Business.MapGenerator import MapGenerator
from OrodaelTurrim.Business.Proxy import MapProxy, GameObjectProxy, GameControlProxy, GameUncertaintyProxy
from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Presenter.Main import MainWindow
from OrodaelTurrim.Structure.Resources import PlayerResources
import click


@click.command()
@click.option('--gui/--nogui', '/gui;/nogui', 'gui', default=True, help='Disable or enable gui')
@click.option('-r', '--round', 'rounds', type=int, default=1000, help='Specify maximum number of rounds')
@click.option('-l', '--log-output', 'log_output', type=click.Path(), help='Log file output')
def main(gui, rounds, log_output):
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
    game_engine.register_player(player2, PlayerResources(500, 10), [])
    player2.initialize()

    game_engine.start(500)

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
