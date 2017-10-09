import argparse

from core.game_looper import GameLooper


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Adversarial Game Server.")
    parser.add_argument('--port', '--p', default=8080, help='Port to run the server on')
    parser.add_argument('--game-file', default='sample/advshort.txt',
                        help='The game layout file to be loaded.')

    args = parser.parse_args()

    game = GameLooper('', args.port, args.game_file)
    game.run_game_loop()
