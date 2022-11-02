from queue import PriorityQueue
import math
import pygame

#heuristic function for finding manhattan distance
def h(startNode, endNode):
    row1, col1 = startNode.get_pos() #doing row, col position instead of x, y because our f, g, and h-scores are row, col based
    row2, col2 = endNode.get_pos()
    return (abs(row1 - row2) + abs(col1 - col2))

#used to reconstruct the path from end node to start node
def create_path(draw, came_from, current):
    while current in came_from:
        current = came_from[current]
        current.set_path() 
        draw()
    current.set_start()

#a* algorithm which uses f(n) = g(n) + h(n)
def aStar(draw, grid, startNode, endNode):
    count = 0 #this is for tie breakers if two things have the same f-score but one came earlier !!!!!is this needed since all edges have equal weight?
    open_nodes = PriorityQueue() #use priority queue because it can efficiently get the smallest element out of it, since the tuple begins wit f-score it will give the node with smallest f
    open_nodes.put((h(startNode, endNode), count, startNode)) #contains (f-score, count, node) and start is initialized with 0 f-score !!!!!!!!!!Double check if it should be 0
    came_from = {} #keeps track of where each node came from, used to return the path once the end node has been found

    open_nodes_hash = {startNode} #this is used to check if a node is in open_nodes

    g_score = {node: math.inf for row in grid for node in row} #this initializes every node to have a g-score of infinity
    g_score[startNode] = 0 #startNode has g_score of 0 since it is 0 distance from start

    f_score = {node: math.inf for row in grid for node in row} #initializes every node to have a f-score of infinity
    f_score[startNode] = h(startNode, endNode)

    while open_nodes:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_nodes.get()[2]
        open_nodes_hash.remove(current)

        if current == endNode:
            current.set_end()
            create_path(draw, came_from, current)
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1 #g_score of neighbor is updated by one because all edges weigh the same

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = g_score[neighbor] + h(neighbor, endNode)

                if neighbor not in open_nodes_hash:
                    count += 1
                    open_nodes.put((f_score[neighbor], count, neighbor))
                    open_nodes_hash.add(neighbor)
                    neighbor.set_open()
        
        if current != startNode:
            current.set_closed()
        
        draw()
    
    return False