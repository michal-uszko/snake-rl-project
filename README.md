# AI playing Snake (Reinforcement Learning)

## General Info

Teaching agent to play Snake in custom gym environment made with PyGame. 
The agent was taught using Deep Q Network (DQN) from stable-baselines3 library.

To see the performance of the trained agent type: 

```
python run.py
```

In default, the agent will play 5 games. If you want to change the number of games (for example to 10) type:

```
python run.py -n 10
```

Or:

```
python run --num_of_games 10
```

## Used libraries
* stable-baselines3 (installation: https://stable-baselines3.readthedocs.io/en/master/guide/install.html)
* PyGame (installation: https://www.pygame.org/wiki/GettingStarted#Pygame%20Installation)
* gym (installation: https://gym.openai.com/docs/)

All dependencies are included in ```requirements.txt``` file.

Instead of installing all libraries manually, you can also try to setup your environment by installing all dependencies from this text file. To do so run the command below:
```
pip install -r requirements.txt
```
