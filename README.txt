Reinforment Learning (Q-Learning):

The following code is provided to find the optimal path of a given agent into
gridworld. This program is built, so it can be run from the user's command prompt, like the following:

>>python <name of .py file> <name of .txt file> <reward> <gamma> <time_limit> <probability_of_success>

The inputs of the algorithm, which will be introduce by the user, are the Q-learning hyperamenters (Learning rate,gamma,probability,and reward/penalty).

In addition, the user will prompt to input a gridworld board which is read as a .txt file in the following format:

0 0 0 0 0 8
0 X 0 0 0 -1
0 0 0 0 0 0
0 0 0 1 0 0
0 0 0 0 0 0
S 0 0 0 0 0

Values in thhe same line should be separated by a space.

After it is run, the program will print the following outputs:

-----------------RESULTS---------------
POLICY
['→', '→', '→', '→', '→', 8.0]
['↑', 'X', '↑', '↑', '↑', -1.0]
['↑', '→', '↑', '↑', '↑', '←']
['↑', '↑', '↑', 1.0, '↑', '←']
['↑', '↑', '↑', '→', '↑', '←']
['↑', '↑', '↑', '←', '←', '←']
------------------
HEATMAP
[9.7, 9.7, 10.1, 9.9, 8.4, 8]
[7.9, 'X', 0.6, 0.3, 0.2, -1]
[9.4, 0.5, 0.7, 0.1, 0.1, 0.0]
[9.8, 0.5, 0.4, 1, 0.0, 0.0]
[10.0, 0.4, 0.2, 0.0, 0.0, 0.0]
[10.3, 0.3, 0.1, 0.0, 0.0, 0.0]
------------------
MEAN REWARD
7.33


Note: The program was developed using Python 3, specifically using the Pycharm IDE.