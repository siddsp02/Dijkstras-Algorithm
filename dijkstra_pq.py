"""An implementation of Dijkstra's algorithm (with priority queue) written in Python.
Dijkstra's algorithm finds the shortest path between two vertices when given a graph
with positive edge weights.

The priority queue data structure is emulated using the 'heapq' module.
"""

from collections import deque
from heapq import heappop, heappush
from math import inf
from typing import Any, Union

Graph = dict[Any, dict[Any, Union[int, float]]]


def dijkstra(graph: Graph, source: str, target: str = None) -> tuple[Any, Any]:
    """Dijkstra's algorithm, but with a priority queue."""
    
    if source not in graph or target not in graph:
        if target is not None:
            raise LookupError("Source or target vertex is not in graph.")

    previous, unvisited = {}, []

    # Excluding the source, all vertices are marked as having an
    # infinite distance since they have not been visited.
    for vertex in graph:
        heappush(unvisited, (0 if vertex is source else inf, vertex))

    distance = {cost: vertex for vertex, cost in unvisited}

    while unvisited:
        # Remove and get the next best vertex in the graph.
        _, nearest = heappop(unvisited)

        if nearest == target:
            break

        # Traverse the neighbours of the nearest sorted vertex.
        for neighbour, cost in graph[nearest].items():
            if cost < 0:
                raise ValueError("Edge cannot have a negative value.")
            alternative = distance[nearest] + cost
            if alternative < distance[neighbour]:
                distance[neighbour] = alternative
                previous[neighbour] = nearest

    # Predecessors are tracked from the target back
    # to the source to reconstruct the shortest path.
    if target is not None:
        path = deque()
        predecessor = target

        # Backtrack until the source is reached.
        while predecessor is not None:
            path.appendleft(predecessor)
            predecessor = previous.get(predecessor)
        return path, distance[target]

    return previous, distance
