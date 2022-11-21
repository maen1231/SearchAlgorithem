from itertools import tee
from sre_constants import SUCCESS
import numpy as np
from EightPuzzleGame_State import State

'''
This class implement the Best-First-Search (BFS) algorithm along with the Heuristic search strategies

In this algorithm, an Open list is used to store the unexplored states and 
a Closed list is used to store the visited state. Open list is a priority queue (First-In-First-Out). 
The priority is insured through sorting the Open list each time after new states are generated 
and added into the list. The heuristics are used to decide which node should be visited next.

In this informed search, reducing the state space search complexity is the main criterion. 
We define heuristic evaluations to reduce the states that need to be checked every iteration. 
Evaluation function is used to express the quality of informedness of a heuristic algorithm. 

'''


class InformedSearchSolver:
    current = State()
    goal = State()
    openlist = []
    closed = []
    # states_path = []
    depth = 0

    def __init__(self, current, goal):
        self.current = current
        self.goal = goal
        self.openlist.append(current)

    def sortFun(self, e):
        # this is used to sort the openlist in ascending order accoring to the heuristic value of state
        e.sort(key=lambda x: x.weight)
        return e

    def check_inclusive(self, s):
        """
         * The check_inclusive function is designed to check if the expanded state is in open list or closed list
         * This is done to prevent looping. (You can use a similar code from uninformedsearch program)
         * @param s: state of interest
         * @return
        """
        in_open = 0
        in_closed = 0
        ret = -1

        # TODO your code start here

        # the child is not in open or closed
        if not (any(np.array_equal(s, x) for x in self.openlist) or any(np.array_equal(s, x) for x in self.closed)):
            ret = 1
        # the child is already in open
        if (any(np.array_equal(s, x) for x in self.openlist)):
            ret = 2

        # the child is already in closed
        if (any(np.array_equal(s, x) for x in self.openlist)):
            ret = 3
        return ret

    def check_child(self, state, ret):
        """
         * The check_child function is designed to put the state we just explored to the correct list

         * @param state: state explored
                   ret: the flag from check_inclusive function
         * @return
        """

        # if flag = 1 //not in open and closed
        # assign the child a heuristic value via heuristic_test(temp state);
        # add the child to open
        if ret == 1:
            state.depth = self.depth
            state.weight = self.heuristic_test(state)
            self.openlist.append(state)

        # if flag = 2 //in the open list
        # if the child was reached by a shorter path (with lower heuristic)
        # then assign the state in open list with lower heuristic
        if ret == 2:
            for s in self.openlist:
                if np.array_equal(s.tile_seq, state.tile_seq):
                    if state.weight < s.weight:
                        s.weight = state.weight

        # if flag = 3 //in the closed list
        # if the child was reached by a shorter path then
        # remove the state from closed and add the child to open
        if ret == 3:
            temp_idx = 0
            for s in self.closed:
                if np.array_equal(s.tile_seq, state.tile_seq):
                    temp_idx = self.closed.index(s)
            for s in self.closed:
                if (self.heuristic_test(state) > s.weight):
                    self.openlist.append(self.closed[temp_idx])
                    self.closed.pop(temp_idx)

    def state_walk(self):
        """
        * The following state_walk function is designed to move the blank tile --> perform actions
        * There are four types of possible actions/walks of for the blank tile, i.e.,
        *  ↑ ↓ ← → (move up, move down, move left, move right)
        * Note that in this framework the blank tile is represent by '0'
        """

        # do the next steps according to flag

        # move to the next heuristic state
        walk_state = self.current.tile_seq
        row = 0
        col = 0

        for i in range(len(walk_state)):
            for j in range(len(walk_state[i])):
                if walk_state[i, j] == 0:
                    row = i
                    col = j
                    break

        ''' The following program is used to do the state space actions
         The 4 conditions for moving the tiles all use similar logic, they only differ in the location of the 
         tile that needs to be swapped.'''
        # TODO your code start here

        ### ↑(move up) action ###
        if (row - 1) >= 0:
            tile_seq_arr = walk_state.copy()
            temp = tile_seq_arr[row - 1, col]
            tile_seq_arr[row - 1, col] = tile_seq_arr[row, col]
            tile_seq_arr[row, col] = temp
            ret = self.check_inclusive(tile_seq_arr)
            temp_state1 = State(tile_seq=tile_seq_arr, parent=self.current)
            self.check_child(temp_state1, ret)

        ### ↓(move down) action ###
        if (row + 1) <= 2:
            tile_seq_arr = walk_state.copy()
            temp = tile_seq_arr[row + 1, col]
            tile_seq_arr[row + 1, col] = tile_seq_arr[row, col]
            tile_seq_arr[row, col] = temp
            ret = self.check_inclusive(tile_seq_arr)
            temp_state2 = State(tile_seq=tile_seq_arr, parent=self.current)
            self.check_child(temp_state2, ret)

        ### ←(move left) action ###
        if (col - 1) >= 0:
            tile_seq_arr = walk_state.copy()
            temp = tile_seq_arr[row, col - 1]
            tile_seq_arr[row, col - 1] = tile_seq_arr[row, col]
            tile_seq_arr[row, col] = temp
            ret = self.check_inclusive(tile_seq_arr)
            temp_state3 = State(tile_seq=tile_seq_arr, parent=self.current)
            self.check_child(temp_state3, ret)
        ### →(move right) action ###
        if (col + 1) <= 2:
            tile_seq_arr = walk_state.copy()
            temp = tile_seq_arr[row, col + 1]
            tile_seq_arr[row, col + 1] = tile_seq_arr[row, col]
            tile_seq_arr[row, col] = temp
            ret = self.check_inclusive(tile_seq_arr)
            temp_state4 = State(tile_seq=tile_seq_arr, parent=self.current)
            self.check_child(temp_state4, ret)

        # sort the open list first by heuristic function
        self.sortFun(self.openlist)
        self.depth += 1

    def heuristic_test(self, current):
        """
        * Solve the game using heuristic search strategies

        * There are three types of heuristic rules:
        * (1) Tiles out of place
        * (2) Sum of distances out of place
        * (3) 2 x the number of direct tile reversals

        * evaluation function
        * g(n) is the distance from start state to the current state
        * h(n) is the distance from current to the goal state
        * f(n) = g(n) + h(n)
        * g(n) = depth of path length to start state
        * h(n) = (1) + (2) + (3)
        """

        curr_seq = current.tile_seq
        goal_seq = self.goal.tile_seq

        # (1) Tiles out of place
        h1 = 0
        """
         *loop over the curr_seq
         *check the every entry in curr_seq with goal_seq
        """
        for i in range(len(curr_seq)):
            for j in range(len(curr_seq[i])):
                if curr_seq[i][j] != goal_seq[i][j]:
                    h1 += 1

        # (2) Sum of distances out of place
        h2 = 0
        """
         *loop over the goal_seq and curr_seq in nested way
         *locate the entry which has the same value in 
         *curr_seq and goal_seq then calculate the offset
         *through the absolute value of two differences
         *of curr_row-goal_row and curr_col-goal_col
         *absoulte value can be calculated by abs(...)
        """

        for i in range(len(goal_seq)):
            for j in range(len(goal_seq[i])):
                if curr_seq[i][j] != goal_seq[i][j]:
                    curr_idx = np.argwhere(curr_seq == goal_seq[i][j])[0]
                    h2 += abs(curr_idx[0] - i) + abs(curr_idx[1] - j)

        # (3) 2 x the number of direct tile reversals
        h3 = 0
        # TODO your code start here
        """
         *loop over the curr_seq
         *use a Γ(gamma)shap slider to walk throught curr_seq and goal_seq
         *rule out the entry with value 0
         *set the boundry restriction
         *don't forget to time 2 at last
         *for example 
         *goal_seq  1 2 3   curr_seq  2 1 3 the Γ shape starts 
         *       4 5 6          4 5 6
         *       7 8 0          7 8 0
         *with 1 2 in goal_seq and 2 1 in curr_seq thus the 
         *    4             4
         *reversal is 1 2 and 2 1
        """
        goal_2_tiles_hor = np.lib.stride_tricks.sliding_window_view(goal_seq, 2, axis=1)
        curr_2_tiles_hor = np.lib.stride_tricks.sliding_window_view(curr_seq, 2, axis=1)
        curr_2_tiles_hor_flip = np.flip(curr_2_tiles_hor, 1)

        goal_2_tiles_ver = np.lib.stride_tricks.sliding_window_view(goal_seq, 2, axis=0)
        curr_2_tiles_ver = np.lib.stride_tricks.sliding_window_view(curr_seq, 2, axis=0)
        curr_2_tiles_ver_flip = np.flip(curr_2_tiles_ver, 1)

        for i in range(len(goal_2_tiles_hor)):
            if not (np.array_equal(goal_2_tiles_hor[i], curr_2_tiles_hor_flip[i])):
                h3 += 1

        for i in range(len(goal_2_tiles_ver)):
            if not (np.array_equal(goal_2_tiles_ver[i], curr_2_tiles_ver_flip[i])):
                h3 += 1

        h3 *= 2

        h = h1 + h2 + h3
        g = current.depth
        f = h + g
        # update the heuristic value for current state
        return f

    def run(self):
        # output the goal state
        target = self.goal.tile_seq
        target_str = np.array2string(target, precision=2, separator=' ')
        print(target_str[1:-1])

        # breadth first search

        while self.openlist:
            # First you need to remove the current node from the open array and move it to the closed array
            self.current = self.openlist.pop(0)
            path = 0

            while not self.current.equals(self.goal):
                self.closed.append(self.current.tile_seq)
                self.state_walk()

                # print('Visited State number ', path + 1)
                # pathstate_str = np.array2string(self.current.tile_seq, precision=2, separator=' ')
                # print(pathstate_str[1:-1])
                path += 1
                self.current = self.openlist.pop(0)

            if self.current.equals(self.goal):
                self.closed.append(self.current.tile_seq)
                print("\nReached goal state")
                print("\nIt took ", path, " iterations to reach to the goal state")
                goal_path = State.path(self.current)
                print("The length of the path is: ", len(goal_path))
                print("The path to goal state is:\n", goal_path)
                return "success"
