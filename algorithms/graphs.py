from typing import NamedTuple
from queue import Queue, LifoQueue
from collections import deque
import networkx as nx
import os

class City(NamedTuple):
    name: str
    country: str
    year: int | None
    latitude: float
    longitude: float

    @classmethod
    def from_dict(cls, attrs):
        return cls(
            name=attrs["xlabel"],
            country=attrs["country"],
            year=int(attrs["year"]) or None,
            latitude=float(attrs["latitude"]),
            longitude=float(attrs["longitude"]),
        )
    
# helper functions
def load_graph(filename, node_factory) -> tuple:
    graph = nx.nx_agraph.read_dot(filename)
    nodes = {
        name: node_factory(attributes)
        for name, attributes in graph.nodes(data=True)
    }

    return nodes, nx.Graph(
        (nodes[name1], nodes[name2], weights)
        for name1, name2, weights in graph.edges(data=True)
    )

def is_twentieth_century(city):
    return 1901 <= city.year <= 2000

def sort_by(neighbors, strategy):
    return sorted(neighbors.items(), key=lambda item: strategy(item[1]))

def by_distance(weights):
    return float(weights["distance"])

def by_latitude(city):
    return city.latitude

def order(neighbors):
    def by_latitude(city):
        return city.latitude
    return iter(sorted(neighbors, key=by_latitude, reverse=True))

def breadth_first_traverse(graph, source, order_by=None):
    queue = Queue()
    queue.put(source) # add starting node to the queue
    visited = set(source) # mark the starting node as already visited

    while not queue.empty():
        yield (node := queue.get()) # alternatively we can first assign the result of queue.get() to node then yield it
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor) # mark as visited
                queue.put(neighbor) # then add it to the queue to be processed

def depth_first_traverse(graph, source, order_by=None):
    stack = LifoQueue()
    stack.put(source) # add source node to stack
    visited = set() # create an empty set, do not mark the node as visited just yet

    while not stack.empty():
        if (node := stack.get()) not in visited:
            yield node # do work
            visited.add(node) # mark current node as visited
            neighbors = list(graph.neighbors(node)) # get its neighbors

            if order_by:
                neighbors.sort(key=order_by)
            
            for neighbor in reversed(neighbors):
                stack.put(neighbor) # place its neighbor on the stack to be processed

def recursive_depth_first_traverse(graph, source, order_by=None):
    visited = set()

    def visit(node):
        yield node
        visited.add(node)
        neighbors = list(graph.neighbors(node))

        if order_by:
            neighbors.sort(key=order_by)

        for neighbor in neighbors:
            if neighbor not in visited:
                yield from visit(neighbor)
    return visit(source)

def breadth_first_search(graph, source, predicate, order_by=None):
    return search(breadth_first_traverse, graph, source, predicate, order_by)

def depth_first_search(graph, source, predicate, order_by=None):
    return search(depth_first_traverse, graph, source, predicate, order_by)

def search(traverse, graph, source, predicate, order_by=None):
    for node in traverse(graph, source, order_by):
        if predicate(node):
            return node
        
def shortest_path(graph, source, destination, order_by=None, ascending=False):
    queue = Queue()
    queue.put(source) # add first node to the queue
    visited = set(source) # mark it as visited
    previous = dict() # maintain a dictionary for fast lookup of previous nodes given a neighbor

    while not queue.empty():
        node = queue.get()
        neighbors = list(graph.neighbors(node))

        if order_by:
            neighbors.sort(key=order_by, reverse=ascending)

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.put(neighbor)
                previous[neighbor] = node
                if neighbor == destination:
                    return retrace(previous, source, destination)

def is_connected(graph, source, destination):
    return shortest_path(graph, source, destination) is not None
                
def retrace(previous, source, destination):
    path = deque() # double-ended queue or doubly linked list for fast "prepends" and "appends"
    current = destination

    while current != source:
        path.appendleft(current)
        current = previous.get(current)
        if current is None:
            return None
        
    path.appendleft(source)
    return list(path)        

def main():
    filepath = os.path.join(os.path.dirname(__file__), 'input/roadmap.dot')
    nodes, graph = load_graph(filepath, City.from_dict)

    print("__DFS__")
    for city in depth_first_traverse(graph, nodes["edinburgh"]):
        print(city.name)

    # for city in recursive_depth_first_traverse(graph, nodes["edinburgh"]):
    #     print(city.name)

    print("__BFS__")
    city = breadth_first_search(graph, nodes["edinburgh"], is_twentieth_century)
    print("City found:", city.name)

    for city in breadth_first_traverse(graph, nodes["edinburgh"]):
        print(city.name)

if __name__ == "__main__":
    main()