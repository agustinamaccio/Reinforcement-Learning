import numpy as np
import random
import time as tm
from time import perf_counter
import sys


def read_file(file, option=0):
    # file = input('enter file name: ')

    with open(file) as f:
        lines = f.read().splitlines()

        grid = np.zeros((len(lines), len(lines[0].split(' '))))

        num_wins = 0
        num_lose = 0
        win_list = []
        lose_list = []
        win_values = []
        lose_values = []
        barrier = []
        negative = ['-9', '-8', '-7', '-6', '-5', '-4', '-3', '-2', '-1']
        positive = ['9', '8', '7', '6', '5', '4', '3', '2', '1']

        for line in lines:
            values = line.split()
            for i in values:
                if i in positive:
                    num_wins += 1
                    col = values.index(i)
                    row = lines.index(line)
                    grid[row][col] = int(i)
                    win = [lines.index(line), values.index(i)]
                    win_list.append(win)
                    win_values.append(int(i))

                if i in negative:
                    num_lose += 1
                    col = values.index(i)
                    row = lines.index(line)
                    grid[row][col] = int(i)
                    lose = [lines.index(line), values.index(i)]
                    lose_list.append(lose)
                    lose_values.append(int(i))

                if i == 'S':
                    start = [lines.index(line), values.index(i)]

                if i == 'X':
                    barrier.append([lines.index(line), values.index(i)])

    if option == 0:
        return [win_list, lose_list, start, barrier, win_values, lose_values]
    else:
        return grid


def takeAction(s, a, n_rows, n_cols, barrier):
    if a == "up":
        nextState = [s[0] - 1, s[1]]

    elif a == "down":
        nextState = [s[0] + 1, s[1]]

    elif a == "left":
        nextState = [s[0], s[1] - 1]

    elif a == "right":
        nextState = [s[0], s[1] + 1]

    elif a == "two-up":
        firstState = [s[0] - 1, s[1]]
        if isActionValid(firstState, n_rows, n_cols, barrier) is True:
            secondState = [s[0] - 1, s[1]]
            if isActionValid(secondState, n_rows, n_cols, barrier) is True:
                nextState = secondState
        else:
            nextState = firstState

    elif a == "two-down":
        firstState = [s[0] + 1, s[1]]  # HAY QUE CAMBIARLO
        if isActionValid(firstState, n_rows, n_cols, barrier) is True:
            secondState = [s[0] + 1, s[1]]
            if isActionValid(secondState, n_rows, n_cols, barrier) is True:
                nextState = secondState
        else:
            nextState = firstState

    elif a == "two-left":
        firstState = [s[0], s[1] - 1]  # HAY QUE CAMBIARLO
        if isActionValid(firstState, n_rows, n_cols, barrier) is True:
            secondState = [s[0], s[1] - 1]
            if isActionValid(secondState, n_rows, n_cols, barrier) is True:
                nextState = secondState
        else:
            nextState = firstState

    elif a == "two-right":
        firstState = [s[0], s[1] + 1]
        if isActionValid(firstState, n_rows, n_cols, barrier) is True:
            secondState = [s[0], s[1] + 1]
            if isActionValid(secondState, n_rows, n_cols, barrier) is True:
                nextState = secondState
        else:
            nextState = firstState

    return nextState


def isActionValid(state, n_rows, n_cols, barrier):
    if (state[0] < 0) or (state[0] >= n_rows):
        return False

    if (state[1] < 0) or (state[1] >= n_cols):
        return False

    if state in barrier:
        return False

    else:
        return True


def chooseActionProb(P, action):
    # action = ExploreOrExploit(exp_rate)

    if action == "up":
        return np.random.choice(["up", "two-up", "down"], p=[P, (1 - P) / 2, (1 - P) / 2])
    if action == "down":
        return np.random.choice(["down", "two-down", "up"], p=[P, (1 - P) / 2, (1 - P) / 2])
    if action == "left":
        return np.random.choice(["left", "two-left", "right"], p=[P, (1 - P) / 2, (1 - P) / 2])
    if action == "right":
        return np.random.choice(["right", "two-right", "left"], p=[P, (1 - P) / 2, (1 - P) / 2])


def ExploreOrExploit(exp_rate, state, up_grid, down_grid, left_grid, right_grid):
    if random.uniform(0, 1) < exp_rate:
        # explore: select a random action
        return np.random.choice(["up", "down", "left", "right"], p=[0.25, 0.25, 0.25, 0.25])

    else:
        # exploit: choose highest
        values = [up_grid[state[0], state[1]], down_grid[state[0], state[1]], left_grid[state[0], state[1]],
                  right_grid[state[0], state[1]]]
        best_value = max(values)

        if values.index(best_value) == 0:
            return "up"
        if values.index(best_value) == 1:
            return "down"
        if values.index(best_value) == 2:
            return "left"
        if values.index(best_value) == 3:
            return "right"


def showPolicy(grid, up_grid, down_grid, left_grid, right_grid, barrier):

    policy_grid = []

    for r in range(len(grid)):
        line = []
        for c in range(len(grid[r])):
            if grid[r][c] == 0 and [r, c] not in barrier:
                up = up_grid[r][c]
                down = down_grid[r][c]
                left = left_grid[r][c]
                right = right_grid[r][c]
                policy = max(up, down, left, right)

                if policy == up:
                    line.append('↑')
                elif policy == down:
                    line.append('↓')
                elif policy == left:
                    line.append('←')
                elif policy == right:
                    line.append('→')

            elif [r, c] in barrier:
                line.append('X')

            else:
                line.append(grid[r][c])

        policy_grid.append(line)

    for i in policy_grid:
        print(i)


def showHeatmap(state_list, n_rows, n_cols, barrier, win_position, win_values, lose_position, lose_values):
    heatmap = np.zeros((n_rows, n_cols))

    for i in range(n_rows):
        for j in range(n_cols):
            n = 0
            for value in state_list:
                if [i, j] == value:
                    n += 1
            heatmap[i][j] = (n/len(state_list))*100

    heatmap = np.around(heatmap, decimals=1)
    heatmap.tolist()
    heatmap_toshow = []

    for i in range(len(heatmap)):
        line = []
        for j in range(len(heatmap[i])):
            if [i, j] in barrier:
                line.append('X')
            elif [i, j] in win_position:
                line.append(win_values[win_position.index([i, j])])
            elif [i, j] in lose_position:
                line.append(lose_values[lose_position.index([i, j])])
            else:
                line.append(heatmap[i][j])
        heatmap_toshow.append(line)

    for i in heatmap_toshow:
        print(i)


def main():

    if len(sys.argv) != 6:
        print("Format: rl.py <filename> <reward> <gamma> <time to learn> < movement probability > ")
        exit(1)
    else:
        file_name = sys.argv[1]
        R = float(sys.argv[2])
        gamma = float(sys.argv[3])
        time_limit = float(sys.argv[4])
        P = float(sys.argv[5])
        print("This program will read in", file_name)
        print("It will run for", time_limit, "seconds")
        print("Its discount factor is", gamma, "and the reward per action is ", R)
        print("Its transition model will move the agent properly with p =", P)

    grid = read_file(file_name, 1)
    start_lst = read_file(file_name, 0)

    win = start_lst[0]  # positions of the win states
    lose = start_lst[1]  # positions of the lose states
    start = start_lst[2]  # position where the agent starts
    barrier = start_lst[3]  # positions of the barriers
    win_values = start_lst[4]  # values (rewards) of the win states
    lose_values = start_lst[5]  # values of the lose states
    n_rows = len(grid)
    n_cols = len(grid[0])
    up_grid = np.zeros([n_rows, n_cols])  # grid with Q values for up action
    down_grid = np.zeros([n_rows, n_cols])  # grid with Q values for down action
    left_grid = np.zeros([n_rows, n_cols])  # grid with Q values for left action
    right_grid = np.zeros([n_rows, n_cols])  # grid with Q values for right action

    state = start.copy()
    states_list = [start]
    lr = 0.7  # learning rate
    #R = -0.1  # reward per step
    #gamma = 0.9
    exp_rate = 0.3  # exploration rate (epsilon)
    #P = 0.7  # probability action succeed
    time_start = tm.time()  # initial time
    #time_limit = 20  # time limit for the loop
    total_R = 0
    total_R_list = []
    num_gets_terminal = 0
    n = 1

    while tm.time() < time_start + time_limit:
        while tm.time() - time_start <= n*0.1:
            chosen_action = ExploreOrExploit(exp_rate, state, up_grid, down_grid, left_grid, right_grid)
            action = chooseActionProb(P, chosen_action)
            next_state = takeAction(state, action, n_rows, n_cols, barrier)

            if isActionValid(next_state, n_rows, n_cols, barrier) is False:
                next_state = state

            states_list.append(state)

            if chosen_action == 'up':
                max_q = max(up_grid[next_state[0], next_state[1]], down_grid[next_state[0], next_state[1]],
                            left_grid[next_state[0], next_state[1]], right_grid[next_state[0], next_state[1]])
                up_grid[state[0], state[1]] = (1 - lr) * up_grid[state[0], state[1]] + \
                                                (lr * (R + grid[next_state[0], next_state[1]] + gamma * max_q))

                total_R += R + grid[next_state[0], next_state[1]]

            if chosen_action == 'down':
                max_q = max(up_grid[next_state[0], next_state[1]], down_grid[next_state[0], next_state[1]],
                            left_grid[next_state[0], next_state[1]], right_grid[next_state[0], next_state[1]])
                down_grid[state[0], state[1]] = (1 - lr) * down_grid[state[0], state[1]] + \
                                                (lr * (R + grid[next_state[0], next_state[1]] + gamma * max_q))
                total_R += R + grid[next_state[0], next_state[1]]

            if chosen_action == 'left':
                max_q = max(up_grid[next_state[0], next_state[1]], down_grid[next_state[0], next_state[1]],
                            left_grid[next_state[0], next_state[1]], right_grid[next_state[0], next_state[1]])
                left_grid[state[0], state[1]] = (1 - lr) * left_grid[state[0], state[1]] + \
                                                (lr * (R + grid[next_state[0], next_state[1]] + gamma * max_q))
                total_R += R + grid[next_state[0], next_state[1]]

            if chosen_action == 'right':
                max_q = max(up_grid[next_state[0], next_state[1]], down_grid[next_state[0], next_state[1]],
                            left_grid[next_state[0], next_state[1]], right_grid[next_state[0], next_state[1]])
                right_grid[state[0], state[1]] = (1 - lr) * right_grid[state[0], state[1]] + \
                                                 (lr * (R + grid[next_state[0], next_state[1]] + gamma * max_q))
                total_R += R + grid[next_state[0], next_state[1]]

            state = next_state

            if state in win or state in lose:
                state = start.copy()
                num_gets_terminal += 1

        total_R_list.append(total_R/num_gets_terminal)
        n += 1

        if exp_rate > 0:
            exp_rate = exp_rate - 0.005

    print('-----------------RESULTS---------------')
    print('POLICY')
    showPolicy(grid, up_grid, down_grid, left_grid, right_grid, barrier)
    print('------------------')
    print('HEATMAP')
    showHeatmap(states_list, n_rows, n_cols, barrier, win, win_values, lose, lose_values)
    print('------------------')
    print('MEAN REWARD')
    print(round(total_R/num_gets_terminal, 2))


if __name__ == "__main__":
    main()
