"""An implementation of Dijkstra's algorithm (with priority queue) written in Python.
Dijkstra's algorithm finds the shortest path between two vertices when given a graph
with positive edge weights.

The priority queue data structure is emulated using the 'heapq' module.
"""

import heapq
from collections import deque
from math import inf
from pprint import pprint
from typing import Any, Hashable, Union

Vertex = Hashable
Graph = dict[Vertex, dict[Vertex, Union[int, float]]]


def dijkstra(graph: Graph, source: Vertex, target: Vertex = None) -> tuple[Any, Any]:
    """Dijkstra's algorithm, but with a priority queue."""

    previous, unvisited = {}, []

    for vertex in graph:
        heapq.heappush(unvisited, (0 if vertex == source else inf, vertex))

    distance = dict(map(reversed, unvisited))

    while unvisited:
        # Remove and get next best vertex.
        _, nearest = heapq.heappop(unvisited)

        if nearest == target:
            break

        for neighbour, cost in graph[nearest].items():
            if cost < 0:
                raise ValueError("Edge cannot have a negative value.")
            alternative = distance[nearest] + cost
            if alternative < distance[neighbour]:
                distance[neighbour] = alternative
                previous[neighbour] = nearest
    else:
        return previous, distance

    path = deque()
    predecessor = target

    # Reconstruct the shortest path by traversing
    # from the target back to the source.
    while predecessor is not None:
        path.appendleft(predecessor)
        predecessor = previous.get(predecessor)

    return path, distance[target]
