import math
import pygame
from queue import PriorityQueue

def create_path(draw, came_from, current):
    while current in came_from:
        current = came_from[current]
        current.set_path()
        draw()
    current.set_start()

def dijkstra(draw, grid, startNode, endNode):
    distance = {node: math.inf for row in grid for node in row}
    distance[startNode] = 0

    count = 0

    came_from = {}
    
    open_nodes = PriorityQueue()
    open_nodes.put((distance[startNode], count, startNode))
    open_nodes_hash = {startNode}


    while open_nodes:
        current = open_nodes.get()[2]

        if current == endNode:
            current.set_end()
            create_path(draw, came_from, current)
            return True

        for neighbor in current.neighbors:
            temp_distance = distance[current] + 1 #adding 1 because all the edges weigh the same

            if temp_distance < distance[neighbor]:
                came_from[neighbor] = current
                distance[neighbor] = temp_distance

                if neighbor not in open_nodes_hash:
                    count += 1
                    open_nodes.put((distance[neighbor], count, neighbor))
                    open_nodes_hash.add(neighbor)
                    neighbor.set_open()
        
        if current != startNode:
            current.set_closed()
        
        draw()

    return False

                




