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
    
    def __init__(self, parent_node, level_matrix, player_row, player_column, depth, chosen_dir, h_value, appleCount,takenSteps, applePositions):
        self.parent_node = parent_node
        self.level_matrix = level_matrix
        self.player_row = player_row
        self.player_col = player_column
        self.depth = depth
        self.chosen_dir = chosen_dir
        self.h = h_value + self.depth
        self.appleCount = appleCount
        self.applePositions = applePositions
        self.takenSteps = takenSteps
        self.seq = ""
        if (self.chosen_dir == "X"):
            pass
        else:
            self.seq = parent_node.seq + self.chosen_dir
    
    def __lt__(self, other):
        return self.depth + self.h < other.depth + other.h
       

class PriorityQueue: 
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

    def count(self):
        return len(self.elements)
    
class AStarAgent(Agent):

    def __init__(self):
        super().__init__()
        self.astarPQ = PriorityQueue()


    def solve(self, level_matrix, player_row, player_column):
        super().solve(level_matrix, player_row, player_column)
        move_sequence = []
        applePositions = []
        self.extendedLevels = []
        #heuristic is the distance to closest apple + distance walked
        """
            YOUR CODE STARTS HERE
            fill move_sequence list with directions chars
        """
        

        #get apple positions
        for row in range(len(level_matrix)):
            for col in range(len(level_matrix[0])):
                if level_matrix[row][col] == 'A':
                    applePositions.append((row,col))



        initial_level_matrix = [list(row) for row in level_matrix] #deepcopy(level_matrix)
        initial_h= distance_to_closest_apple(applePositions, player_row, player_column)  #  fill this value with your heuristic function
        matrix_row = len(initial_level_matrix)
        matrix_col = len(initial_level_matrix[0])

        appleCount = 0
        if initial_level_matrix[player_row][player_column] == 'A':
            appleCount += 1
            applePositions.remove((player_row, player_column))
        s0 = Node(None, initial_level_matrix, player_row, player_column, 0, "X", initial_h, appleCount,0,  deepcopy(applePositions))
        self.astarPQ.put( s0, initial_h)
        maxSize = 0

        while not self.astarPQ.empty():
            curr_state = self.astarPQ.get()
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
                    temp_apple_positions = deepcopy(curr_state.applePositions)
                    if temp_level_matrix[curr_state.player_row-1][curr_state.player_col] == 'A':
                        appleCount += 1

                    temp_level_matrix[curr_state.player_row-1][curr_state.player_col] = 'P'
                    if temp_level_matrix not in self.extendedLevels:
                        #self.extendedLevels.append(temp_level_matrix)
                        heur_val = distance_to_closest_apple(temp_apple_positions, curr_state.player_row-1, curr_state.player_col)
                        if appleCount > 0:
                            if (curr_state.player_row-1, curr_state.player_col) in temp_apple_positions:
                                temp_apple_positions.remove((curr_state.player_row-1, curr_state.player_col))
                        tempNode = Node(curr_state, temp_level_matrix, curr_state.player_row-1, curr_state.player_col, curr_state.depth+1, 'U',heur_val, curr_state.appleCount + appleCount, curr_state.takenSteps +1, temp_apple_positions)
                        self.generated_node_count +=1
                        self.astarPQ.put(tempNode, heur_val + tempNode.takenSteps)

                if curr_state.player_row < matrix_row-1 and not curr_state.level_matrix[curr_state.player_row+1][curr_state.player_col] == 'W':
                    appleCount = 0
                    temp_level_matrix = deepcopy(curr_state.level_matrix)
                    temp_apple_positions = deepcopy(curr_state.applePositions)
                    if temp_level_matrix[curr_state.player_row+1][curr_state.player_col] == 'A':
                        appleCount += 1
                    temp_level_matrix[curr_state.player_row+1][curr_state.player_col] = 'P'
                    if temp_level_matrix not in self.extendedLevels:
                        #self.extendedLevels.append(temp_level_matrix)
                        heur_val = distance_to_closest_apple(temp_apple_positions, curr_state.player_row+1, curr_state.player_col)
                        if appleCount > 0:
                            if (curr_state.player_row+1, curr_state.player_col) in temp_apple_positions:
                                temp_apple_positions.remove((curr_state.player_row+1, curr_state.player_col))
                        tempNode = Node(curr_state, temp_level_matrix, curr_state.player_row+1, curr_state.player_col, curr_state.depth+1, 'D', heur_val, curr_state.appleCount + appleCount,curr_state.takenSteps +1, temp_apple_positions)
                        self.generated_node_count += 1
                        self.astarPQ.put(tempNode, heur_val+tempNode.takenSteps)

                if curr_state.player_col > 0 and not curr_state.level_matrix[curr_state.player_row][curr_state.player_col-1] == 'W':
                    appleCount = 0
                    temp_level_matrix = deepcopy(curr_state.level_matrix)
                    temp_apple_positions = deepcopy(curr_state.applePositions)
                    if temp_level_matrix[curr_state.player_row][curr_state.player_col-1] == 'A':
                        appleCount +=1
                    temp_level_matrix[curr_state.player_row][curr_state.player_col-1] = 'P'
                    if temp_level_matrix not in self.extendedLevels:
                        #self.extendedLevels.append(temp_level_matrix)
                        heur_val = distance_to_closest_apple(temp_apple_positions, curr_state.player_row, curr_state.player_col-1)
                        if appleCount > 0:
                            if (curr_state.player_row, curr_state.player_col-1) in temp_apple_positions:
                                temp_apple_positions.remove((curr_state.player_row, curr_state.player_col-1))
                        tempNode = Node(curr_state, temp_level_matrix, curr_state.player_row, curr_state.player_col-1, curr_state.depth+1, 'L',heur_val, curr_state.appleCount + appleCount, curr_state.takenSteps +1, temp_apple_positions)
                        self.generated_node_count += 1
                        self.astarPQ.put(tempNode, heur_val+tempNode.takenSteps)

                if curr_state.player_col < matrix_col-1 and not curr_state.level_matrix[curr_state.player_row][curr_state.player_col+1] == 'W':
                    appleCount = 0
                    temp_level_matrix = deepcopy(curr_state.level_matrix)
                    temp_apple_positions = deepcopy(curr_state.applePositions)
                    if temp_level_matrix[curr_state.player_row][curr_state.player_col+1] == 'A':
                        appleCount +=1
                    temp_level_matrix[curr_state.player_row][curr_state.player_col+1] = 'P'
                    if temp_level_matrix not in self.extendedLevels:
                        #self.extendedLevels.append(temp_level_matrix)
                        heur_val = distance_to_closest_apple(temp_apple_positions, curr_state.player_row, curr_state.player_col+1)
                        if appleCount > 0:
                            if (curr_state.player_row, curr_state.player_col+1) in temp_apple_positions:
                                temp_apple_positions.remove((curr_state.player_row, curr_state.player_col+1))
                        tempNode = Node(curr_state, temp_level_matrix, curr_state.player_row, curr_state.player_col+1, curr_state.depth+1, 'R',heur_val, curr_state.appleCount + appleCount,curr_state.takenSteps +1,  temp_apple_positions)
                        self.generated_node_count += 1
                        self.astarPQ.put(tempNode,heur_val+tempNode.takenSteps)

                if self.astarPQ.count() > maxSize:
                    maxSize = self.astarPQ.count()


        #if break was taken -> make solved state true, get sequence by getting curr_state.seq
        self.maximum_node_in_memory_count = maxSize


        """
            YOUR CODE ENDS HERE
            return move_sequence
        """
        return move_sequence

def distance_to_closest_apple(applePositions, agent_row, agent_col):
    min_val = 100000
    for item in applePositions:
        x_distance = agent_row - item[0]
        y_distance = agent_col - item[1]
        distance_val = x_distance + y_distance
        if  distance_val< min_val:
            min_val = distance_val
    return min_val

def distance_to_all_apples(applePositions, agent_row, agent_col):
    minVals = []
    for item in applePositions:
        x_distance = agent_row - item[0]
        y_distance = agent_col - item[1]
        distance_val = int((x_distance**2 + y_distance **2)**0.5)
        minVals.append(distance_val)
    return minVals