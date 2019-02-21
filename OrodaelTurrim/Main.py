from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Business.MapGenerator import MapGenerator
from OrodaelTurrim.Presenter.Main import MainWindow


def main():
    # Generate the map
    game_map = MapGenerator(11, 11).generate()

    # Initialize game engine
    game_engine = GameEngine(1, game_map)

    MainWindow(game_engine).execute()


if __name__ == '__main__':
    main()
