from snake_env_class import SnakeEnv
from stable_baselines3 import DQN
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num_of_games", default=5,
                help="Path to trained model", type=int)
args = vars(ap.parse_args())

if __name__ == '__main__':
    game = SnakeEnv()
    model = DQN.load("model/snake_model", game)

    num_of_games = args['num_of_games']
    obs = game.reset()
    for i in range(1, num_of_games + 1):
        while True:
            game.render()
            action, _states = model.predict(obs, deterministic=True)
            obs, rewards, done, info = game.step(action)
            if done:
                print(f"[INFO] GAME {i}: SCORE {game.score}")
                obs = game.reset()
                break
