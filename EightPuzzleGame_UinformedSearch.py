from asyncio.windows_events import NULL
import numpy as np
from EightPuzzleGame_State import State


'''
This class implement one of the Uninformed Search (Breadth-first Search) algorithm


python list insert (index,item), append (item), extend (anotherList), remove (item), pop (index)

'''


class UninformedSearchSolver:
    current = State()
    goal = State()
    openlist = []
    closed = []
    depth = 0

    def __init__(self, current, goal):
        self.current = current
        self.goal = goal
        self.openlist.append(current)

    def check_inclusive(self, s):
        """
        * The check_inclusive function is designed to check if the expanded state is or is not in open list or closed list
        * This is done to prevent looping
        * @param s
        * @return
        """
        ret = -1

        # TODO your code start here
        if (any(np.array_equal(s, x) for x in self.openlist)):
            ret = 1

        if (any(np.array_equal(s, x) for x in self.closed)):
            ret = 1
        # TODO your code end here
        return ret

    def state_walk(self):
        """
        * The following state_walk function is designed to move the blank tile =0 --> perform actions
         * There are four types of possible actions/walks of for the blank tile, i.e.,
         *  ↑ ↓ ← → (move up, move down, move left, move right)
         * Note that in this framework the blank tile is represent by '0'
        """

        walk_state = self.current.tile_seq
        row = 0
        col = 0

        # Loop to find the location of the blank space
        for i in range(len(walk_state)):
            for j in range(len(walk_state[i])):
                if walk_state[i, j] == 0:
                    row = i
                    col = j
                    break

        ''' The following program is used to do the state space actions
            The 4 conditions for moving the tiles all use similar logic, they only differ in the location of the 
            tile that needs to be swapped. That being the case, I will only comment the first subroutine
        '''
        # TODO your code start here
        ### ↑(move up) action ###
        # (row - 1) is checked to prevent out of bounds errors, the tile is swapped with the one above it
        if (row - 1) >= 0:
            tile_seq_arr = walk_state.copy()
            temp = tile_seq_arr[row - 1, col]
            tile_seq_arr[row - 1, col] = tile_seq_arr[row, col]
            tile_seq_arr[row, col] = temp
            ret = self.check_inclusive(tile_seq_arr)
            temp_state1 = State(tile_seq=tile_seq_arr, parent=self.current)
            if ret != 1:
                self.openlist.append(temp_state1)
        ### ↓(move down) action ###
        if (row + 1) <= 2:
            tile_seq_arr = walk_state.copy()
            temp = tile_seq_arr[row + 1, col]
            tile_seq_arr[row + 1, col] = tile_seq_arr[row, col]
            tile_seq_arr[row, col] = temp
            ret = self.check_inclusive(tile_seq_arr)
            temp_state2 = State(tile_seq=tile_seq_arr, parent=self.current)
            if ret != 1:
                self.openlist.append(temp_state2)
        ### ←(move left) action ###
        if (col - 1) >= 0:
            tile_seq_arr = walk_state.copy()
            temp = tile_seq_arr[row, col - 1]
            tile_seq_arr[row, col - 1] = tile_seq_arr[row, col]
            tile_seq_arr[row, col] = temp
            ret = self.check_inclusive(tile_seq_arr)
            temp_state3 = State(tile_seq=tile_seq_arr, parent=self.current)
            if ret != 1:
                self.openlist.append(temp_state3)
        ### →(move right) action ###
        if (col + 1) <= 2:
            tile_seq_arr = walk_state.copy()
            temp = tile_seq_arr[row, col + 1]
            tile_seq_arr[row, col + 1] = tile_seq_arr[row, col]
            tile_seq_arr[row, col] = temp
            ret = self.check_inclusive(tile_seq_arr)
            temp_state4 = State(tile_seq=tile_seq_arr, parent=self.current)
            if ret != 1:
                self.openlist.append(temp_state4)

        self.depth += 1
        # TODO your code end here

    # # You can change the following code to print all the states on the search path
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


