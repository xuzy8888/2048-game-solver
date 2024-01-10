from __future__ import absolute_import, division, print_function
import copy, random
from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1 

# Tree node. To be used to construct a game tree. 
class Node: 
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        self.state = (copy.deepcopy(state[0]), state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        #TODO: complete this
        return (len(self.children) == 0)
        
        

# AI agent. To be used do determine a promising next move.
class AI:
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3): 
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    # recursive function to build a game tree
    def build_tree(self, node=None, depth=0, ec=False):
        if node == None:
            node = self.root
        if depth == self.search_depth: 
            return 
        if node.player_type == MAX_PLAYER:

            # TODO: find all children resulting from 
            # all possible moves (ignore "no-op" moves)
            
            # NOTE: the following calls may be useful:
            # self.simulator.reset(*(node.state))
            # self.simulator.get_state()
            # self.simulator.move(direction)

            
            if self.simulator.move(0):
                nxt_node = Node(self.simulator.get_state(),CHANCE_PLAYER)
                node.children.append((0,nxt_node))
                self.build_tree(nxt_node,depth+1,False)
            self.simulator.reset(*(node.state))

            if self.simulator.move(1):
                nxt_node = Node(self.simulator.get_state(),CHANCE_PLAYER)
                node.children.append((1,nxt_node))
                self.build_tree(nxt_node,depth+1,False)
            self.simulator.reset(*(node.state))

            if self.simulator.move(2):
                nxt_node = Node(self.simulator.get_state(),CHANCE_PLAYER)
                node.children.append((2,nxt_node))
                self.build_tree(nxt_node,depth+1,False)
            self.simulator.reset(*(node.state))

            if self.simulator.move(3):
                nxt_node = Node(self.simulator.get_state(),CHANCE_PLAYER)
                node.children.append((3,nxt_node))
                self.build_tree(nxt_node,depth+1,False)
            self.simulator.reset(*(node.state))
            

        elif node.player_type == CHANCE_PLAYER:

            open_tiles = self.simulator.get_open_tiles()
            if len(open_tiles) > 0:
                for i in open_tiles:
                    self.simulator.tile_matrix[i[0]][i[1]] = 2
                    nxt_node = Node(self.simulator.get_state(),MAX_PLAYER)
                    node.children.append((None,nxt_node))
                    self.build_tree(nxt_node,depth+1,False)
                    self.simulator.tile_matrix[i[0]][i[1]] = 0

            # TODO: find all children resulting from 
            # all possible placements of '2's
            # NOTE: the following calls may be useful
            # (in addition to those mentioned above):
            # self.simulator.get_open_tiles():
            
        # TODO: build a tree for each child of this node
        
    # expectimax implementation; 
    # returns a (best direction, best value) tuple if node is a MAX_PLAYER
    # and a (None, expected best value) tuple if node is a CHANCE_PLAYER
    def expectimaxEC(self, node = None):
        # TODO: delete this random choice but make sure the return type of the function is the same

        if node == None:
            node = self.root

        if node.is_terminal():
            # TODO: base case
            #score = node.state[1]
            child_mtx = node.state[0]
            length = len(child_mtx)
            score = 100
            total = 0
            for i in range(0,length):
                for j in range(0,length):
                    total=total+child_mtx[i][j]
            avg=total/length**2
            for i in range(0,length):
                for j in range(0,length-1):
                    if child_mtx[i][j]<child_mtx[i][j+1]:
                        score= score-5*((child_mtx[i][j+1]-child_mtx[i][j])/avg)
                    elif child_mtx[i][j]==child_mtx[i][j+1]:
                        score= score+child_mtx[i][j]
            for j in range(0,length):
                for i in range(0,length-1):
                    if child_mtx[i][j] < child_mtx[i+1][j]:
                        score= score-5*((child_mtx[i+1][j]-child_mtx[i][j])/avg)
                    elif child_mtx[i][j] == child_mtx[i+1][j]:
                        score= score+child_mtx[i][j]
            open_tiles = self.simulator.get_open_tiles()
            score = score + len(open_tiles)*2
            for i in range(0,length-1):
                temp = 0
                for j in range(0,i+1):
                    temp = temp + child_mtx[j][i-j]
                score = score + temp*(2**(length-i))      
           

            #score = child_mtx[0][0]*8
            # +(child_mtx[1][0]+child_mtx[0][1])*4
            # +(child_mtx[2][0]+child_mtx[1][1]+child_mtx[0][2])*2
            # +(child_mtx[3][0]+child_mtx[2][1]+child_mtx[1][2]+child_mtx[0][3])*1
            return (None,score)

        elif node.player_type == MAX_PLAYER:
            # TODO: MAX_PLAYER logic
            score = -999999
            direction = 0
            for n in node.children:
                
                score_new = self.expectimaxEC(n[1])[1]
                if score_new > score:
                    score = score_new
                    direction = n[0]    
            return (direction , score)

        elif node.player_type == CHANCE_PLAYER:
            # TODO: CHANCE_PLAYER logic
            chance = 1 / len(node.children)
            score = 0
            for n in node.children:
                score = score + self.expectimaxEC(n[1])[1] * chance
            return (None, score)
    
    def expectimax(self, node = None):
        # TODO: delete this random choice but make sure the return type of the function is the same

        if node == None:
            node = self.root

        if node.is_terminal():
            # TODO: base case
            score = node.state[1]
            

            #score = child_mtx[0][0]*8
            # +(child_mtx[1][0]+child_mtx[0][1])*4
            # +(child_mtx[2][0]+child_mtx[1][1]+child_mtx[0][2])*2
            # +(child_mtx[3][0]+child_mtx[2][1]+child_mtx[1][2]+child_mtx[0][3])*1
            return (None,score)

        elif node.player_type == MAX_PLAYER:
            # TODO: MAX_PLAYER logic
            score = -999999
            direction = 0
            for n in node.children:
                
                score_new = self.expectimax(n[1])[1]
                if score_new > score:
                    score = score_new
                    direction = n[0]    
            return (direction , score)

        elif node.player_type == CHANCE_PLAYER:
            # TODO: CHANCE_PLAYER logic
            chance = 1 / len(node.children)
            score = 0
            for n in node.children:
                score = score + self.expectimax(n[1])[1] * chance
            return (None, score)


    
    # Do not modify this function
    def compute_decision(self):
        self.build_tree()
        direction, _ = self.expectimax(self.root)
        return direction

    # TODO (optional): implement method for extra credits
    def compute_decision_ec(self):
        self.build_tree()
        direction, _ = self.expectimaxEC(self.root)
        return direction