from queue import PriorityQueue
from itertools import count
from dataclasses import dataclass
from typing import Any

from math import inf as infinity
from graphs import load_graph, retrace, by_distance, City
import os

@dataclass(order=True)
class Element:
    priority: float
    count: int
    value: Any
    
def dijkstra(graph, source, destination, weight_factory):
    previous = {}
    visited = set()
    counter = count()

    # assign all paths from source node to the next node to infinity
    # this gives us a dictionary where we can look up the cost values by providing a node
    distance = {node: infinity for node in graph.nodes}
    distance[source] = 0 # set source node to be 0 distance

    unvisited = PriorityQueue() # min-heap implementation
    for node in graph.nodes:
        unvisited.put((Element(distance[node], next(counter), node)))
    unvisited.put(Element(distance[source], next(counter), source))

    while not unvisited.empty():
        node = unvisited.get()
        current_cost = node.priority
        current_node = node.value
        visited.add(current_node) # mark current node as visited
        for neighbor, weights in graph[current_node].items():
            if neighbor not in visited:
                weight = weight_factory(weights)
                new_distance = current_cost + weight
                if new_distance < distance[neighbor]:
                    # update the distance dictionary with the new cost then add it to the queue
                    distance[neighbor] = new_distance
                    unvisited.put(Element(distance[neighbor], next(counter), neighbor))
                    # link the current node to the neighbor
                    previous[neighbor] = current_node

    return retrace(previous, source, destination)

filepath = os.path.join(os.path.dirname(__file__), 'input/roadmap.dot')
nodes, graph = load_graph(filepath, City.from_dict)

city1 = nodes["london"]
city2 = nodes["edinburgh"]

for city in dijkstra(graph, city1, city2, by_distance):
    print(city.name)