from queue import PriorityQueue
from math import inf as infinity
from graphs import load_graph, retrace, by_distance, City
import os
    
def dijkstra(graph, source, destination, weight_factory):
    previous = {}
    visited = set()

    # assign all paths from source node to the next node to infinity
    # this gives us a dictionary where we can look up the cost values by providing a node
    distance = {node: infinity for node in graph.nodes}
    distance[source] = 0 # set source node to be 0 distance

    unvisited = PriorityQueue() # min-heap implementation
    unvisited.put((distance[source], source)) # tuple (priority, value)

    while not unvisited.empty():
        current_cost, current_node = unvisited.get()
        visited.add(current_node) # mark current node as visited
        for neighbor, weights in graph[current_node].items():
            if neighbor not in visited:
                weight = weight_factory(weights)
                new_distance = current_cost + weight
                if new_distance < distance[neighbor]:
                    # update the distance dictionary with the new cost then add it to the queue
                    distance[neighbor] = new_distance
                    # link the current node to the neighbor
                    previous[neighbor] = current_node
                    unvisited.put((distance[neighbor], neighbor))

    return retrace(previous, source, destination)

filepath = os.path.join(os.path.dirname(__file__), 'input/roadmap.dot')
nodes, graph = load_graph(filepath, City.from_dict)

city1 = nodes["london"]
city2 = nodes["edinburgh"]

for city in dijkstra(graph, city1, city2, by_distance):
    print(city.name)