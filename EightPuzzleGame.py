#!/usr/bin/env python3

'''
Solving Eight Puzzle Game using Search Strategies
The eight-puzzle game is a 3 × 3 version of the 15-puzzle in which eight tiles can be moved around in nine spaces.
CSC 425 Artificial Intelligence
Instructor: Dr. Yangyang Tao
Semester: Fall 2022

Your name:
'''
from sre_constants import FAILURE
import time
import numpy as np
from EightPuzzleGame_State import State
from EightPuzzleGame_UinformedSearch import UninformedSearchSolver
from EightPuzzleGame_InformedSearch import InformedSearchSolver


class EightPuzzleGame:
    titles = 8
    def __init__(self, initial=[], goal=[], tiles=8):
        self.initial = initial
        self.goal = goal
        self.tiles = tiles

    def run(self,init_tile):
        """This function run breadth-first search and best-first search on a given initial state
        params: init_tile: initial tile state
        """
        init = State(init_tile, 0, 0)
        print("\nStart state:")
        init_str = np.array2string(init_tile, precision=2, separator=' ')
        print(init_str[1:-1])
        goal_tile = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        goal_str = np.array2string(goal_tile, precision=2, separator=' ')
        print("\nExpected goal state:\n",goal_str[1:-1])
        goal = State(goal_tile, 0, 0)


        self.tiles = 8
        if not (State.check_solvability(init)):
            print("The puzzle is unsolvable")

        else:
            print("Start Breadth-First Search:")
            t0 = time.time()
            UIS_solver = UninformedSearchSolver(init, goal)
            UIS_solver.run()
            t1 = time.time()
            computational_time = t1-t0
            print("It takes %f milliseconds to run Uninformed Search (Breadth-First Search) algorithm\n" % computational_time)

            print("Start Best-First Search Search:")
            t0 = time.time()
            IS_solver = InformedSearchSolver(init, goal)
            IS_solver.run()
            t1 = time.time()
            computational_time = t1-t0
            print("It takes %f milliseconds to run Informed Search (Best-First Search) algorithm\n" % computational_time)
            print('*'*100)

    def start(self):
        '''Please test your program with different start state to explore the feature of the algorithms'''
        # initialize the init state and goal state as 2d array

        #Uncomment to test different input

        #init_tile= np.array([[2, 3, 6], [1, 4, 8], [7, 5, 0]])
        #init_tile= np.array([[1, 2, 3], [0, 4, 6], [7, 5, 8]])
        #init_tile= np.array([[1, 2, 3], [5, 4, 6], [7, 0, 8]])
        #init_tile= np.array([[1, 2, 3], [0, 4, 6], [7, 5, 8]])
        init_tile= np.array([[0, 2, 3], [8, 4, 6], [7, 5, 1]])

        self.run(init_tile)



# start the puzzle game
epp = EightPuzzleGame()
epp.start()
