from snake_env_class import SnakeEnv
from stable_baselines3 import DQN

if __name__ == '__main__':
    game = SnakeEnv()
    model = DQN('MlpPolicy', game, verbose=1)
    model.learn(total_timesteps=500_000, log_interval=10, eval_freq=100)
    model.save("model/snake_model")
