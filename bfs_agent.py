import time
import random
from copy import deepcopy
from agent import Agent


#  use whichever data structure you like, or create a custom one
import queue
import heapq
from collections import deque


"""
  you may use the following Node class
  modify it if needed, or create your own
"""
class Node():
    
    def __init__(self, parent_node, level_matrix, player_row, player_column, depth, chosen_dir, appleCount):
        self.parent_node = parent_node
        self.level_matrix = level_matrix
        self.player_row = player_row
        self.player_col = player_column
        self.depth = depth
        self.appleCount = appleCount
        self.chosen_dir = chosen_dir

        self.seq = ""
        if (self.chosen_dir == "X"):
            pass
        else:
            self.seq = parent_node.seq + self.chosen_dir



class BFSAgent(Agent):

    def __init__(self):
        super().__init__()
        self.bfsQueue = queue.Queue()
        self.extendedLevels = []


    def solve(self, level_matrix, player_row, player_column):
        super().solve(level_matrix, player_row, player_column)
        move_sequence = []

        """
            YOUR CODE STARTS HERE
            fill move_sequence list with directions chars
        """
        
        initial_level_matrix = [list(row) for row in level_matrix] #deepcopy(level_matrix)
        matrix_row = len(initial_level_matrix)
        matrix_col = len(initial_level_matrix[0])

        appleCount = 0
        if initial_level_matrix[player_row][player_column] == 'A':
            appleCount += 1
        s0 = Node(None, initial_level_matrix, player_row, player_column, 0, "X", appleCount)
        self.bfsQueue.put(s0)
        maxSize = 0

        while not self.bfsQueue.empty():

            curr_state = self.bfsQueue.get()
            self.expanded_node_count += 1

            if curr_state.level_matrix not in self.extendedLevels:
                self.extendedLevels.append(deepcopy(curr_state.level_matrix))

                if curr_state.appleCount == self.apple_count:
                    move_sequence =[c for c in curr_state.seq]
                    break


                curr_state.level_matrix[curr_state.player_row][curr_state.player_col] = 'F'

                if curr_state.player_row > 0 and not curr_state.level_matrix[curr_state.player_row-1][curr_state.player_col]=='W':
                    appleCount = 0 
                    temp_level_matrix = deepcopy(curr_state.level_matrix)
                    if temp_level_matrix[curr_state.player_row-1][curr_state.player_col] == 'A':
                        appleCount +=1
                    temp_level_matrix[curr_state.player_row-1][curr_state.player_col] = 'P'
                    if temp_level_matrix not in self.extendedLevels:
                        #self.extendedLevels.append(temp_level_matrix)
                        tempNode = Node(curr_state, temp_level_matrix, curr_state.player_row-1, curr_state.player_col, curr_state.depth+1, 'U', curr_state.appleCount + appleCount)
                        self.generated_node_count +=1
                        self.bfsQueue.put(tempNode)

                if curr_state.player_row < matrix_row-1 and not curr_state.level_matrix[curr_state.player_row+1][curr_state.player_col] == 'W':
                    appleCount = 0
                    temp_level_matrix = deepcopy(curr_state.level_matrix)
                    if temp_level_matrix[curr_state.player_row+1][curr_state.player_col] == 'A':
                        appleCount += 1
                    temp_level_matrix[curr_state.player_row+1][curr_state.player_col] = 'P'
                    if temp_level_matrix not in self.extendedLevels:
                        #self.extendedLevels.append(temp_level_matrix)
                        tempNode = Node(curr_state, temp_level_matrix, curr_state.player_row+1, curr_state.player_col, curr_state.depth+1, 'D', curr_state.appleCount + appleCount)
                        self.generated_node_count += 1
                        self.bfsQueue.put(tempNode)

                if curr_state.player_col > 0 and not curr_state.level_matrix[curr_state.player_row][curr_state.player_col-1] == 'W':
                    appleCount = 0
                    temp_level_matrix = deepcopy(curr_state.level_matrix)
                    if temp_level_matrix[curr_state.player_row][curr_state.player_col-1] == 'A':
                        appleCount +=1
                    temp_level_matrix[curr_state.player_row][curr_state.player_col-1] = 'P'
                    if temp_level_matrix not in self.extendedLevels:
                        #self.extendedLevels.append(temp_level_matrix)
                        tempNode = Node(curr_state, temp_level_matrix, curr_state.player_row, curr_state.player_col-1, curr_state.depth+1, 'L', curr_state.appleCount + appleCount)
                        self.generated_node_count += 1
                        self.bfsQueue.put(tempNode)

                if curr_state.player_col < matrix_col-1 and not curr_state.level_matrix[curr_state.player_row][curr_state.player_col+1] == 'W':
                    appleCount = 0
                    temp_level_matrix = deepcopy(curr_state.level_matrix)
                    if temp_level_matrix[curr_state.player_row][curr_state.player_col+1] == 'A':
                        appleCount +=1
                    temp_level_matrix[curr_state.player_row][curr_state.player_col+1] = 'P'
                    if temp_level_matrix not in self.extendedLevels:
                        #self.extendedLevels.append(temp_level_matrix)
                        tempNode = Node(curr_state, temp_level_matrix, curr_state.player_row, curr_state.player_col+1, curr_state.depth+1, 'R', curr_state.appleCount + appleCount)
                        self.generated_node_count += 1
                        self.bfsQueue.put(tempNode)

                if self.bfsQueue.qsize() > maxSize:
                    maxSize = self.bfsQueue.qsize()
        #if break was taken -> make solved state true, get sequence by getting curr_state.seq
        self.maximum_node_in_memory_count = maxSize

        """
            YOUR CODE ENDS HERE
            return move_sequence
        """

        return move_sequence