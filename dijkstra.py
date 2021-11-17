# !usr/bin/env python3

"""An implementation of Dijkstra's algorithm written in Python. Dijkstra's algorithm
finds the shortest path between two vertices when given a graph
with positive edge weights.

Note:
    - The implementation of this algorithm differs from the version given
    in the references because the input for the graph is in the form of
    nested dictionaries instead of arrays, and Python does not have "pointers",
    with the exception of reference types.
    - Dijkstra's algorithm does not work with negative edge weights.
    - The following code is original, and has not been taken from anywhere else,
    apart from taking some ideas from the pseudocode from Wikipedia.

References:
    - https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    - https://www.youtube.com/watch?v=GazC3A4OQTE&ab_channel=Computerphile
    - https://www.youtube.com/watch?v=XB4MIexjvY0&ab_channel=AbdulBari
"""

from collections import deque
from math import inf
from pprint import pprint
from typing import Any, Union

Graph = dict[Any, dict[Any, Union[int, float]]]


def dijkstra(graph: Graph, source: str, target: str = None) -> tuple[Any, Any]:
    """Returns the shortest distance (or path) between any two vertices
    when given a graph.

    Arguments:
        graph (Graph): The graph to traverse the vertices and edges of.
        source (str): The vertex to start at when pathfinding.
        target (str, optional): The vertex to find the shortest path to.
        Defaults to None.

    Raises:
        LookupError: If the source or target vertex is not in the graph.
        ValueError: If the weight of an edge is a negative integer.

    Returns:
        tuple[Any, Any]: A summary of the shortest paths as a dictionary
        if no target vertex is specified. Otherwise, an integer value
        for the shortest distance between the source
        and target vertex in the graph.
    """

    if source not in graph or target not in graph:  # Prevent invalid lookups.
        if target is not None:
            raise LookupError("Source or target vertex is not in graph.")

    if source == target:
        return None, 0

    # Excluding the source, all vertices are marked as having a distance
    # that is unbounded ('inf') since they are unvisited.
    unvisited = set(graph)
    distance = {vertex: 0 if vertex is source else inf for vertex in unvisited}
    previous = {}

    while unvisited:
        # Get the vertex with the shortest distance in the mapping
        # of vertices to distances only if the vertex is unvisited.
        nearest = next(
            vertex
            for vertex in sorted(distance, key=distance.get)  # type: ignore
            if vertex in unvisited
        )
        unvisited.remove(nearest)

        if nearest is target:  # Early break from search.
            if distance[target] == inf:
                return "unreachable", inf

        # Traverse the graph through the neighbours
        # of the nearest sorted vertex.
        for neighbour in graph[nearest]:
            if neighbour not in unvisited:  # Skip over visited vertices.
                continue
            if graph[nearest][neighbour] < 0:  # Prevent negative cycles.
                raise ValueError("Edge cannot have a negative value.")
            if nearest is source:
                distance[neighbour] = graph[nearest][neighbour]
                previous[neighbour] = source
            else:
                new_distance = distance[nearest] + graph[nearest][neighbour]
                if distance[neighbour] > new_distance:
                    distance[neighbour] = new_distance
                    previous[neighbour] = nearest

    if target is not None:
        # Predecessors are tracked from the target back
        # to the source to reconstruct the shortest path
        # taken from the source to the target.
        path = deque()
        predecessor = target

        # Backtracks until the source is reached.
        while predecessor != source:
            path.appendleft(predecessor)
            predecessor = previous[predecessor]
        return path, distance[target]

    return distance, previous  # Reached only if no target is specified.


def test_pathfinding(graph: Graph) -> None:
    print("\nTesting the following graph:\n")
    pprint(graph)
    print()
    target = "d"
    for vertex in graph:
        print(f"Source as {vertex=!r} to {target=!r}: ", end="")
        path, distance = dijkstra(graph, source=vertex, target=target)
        print(f"{path=}, {distance=}")


def main() -> None:
    test_graph = {
        "s": {"a": 1, "b": 5},
        "a": {"b": 2, "c": 2, "d": 1},
        "b": {"d": 2},
        "c": {"d": 3, "e": 1},
        "d": {"e": 2},
        "e": {},
    }
    test_graph_2 = {
        "a": {"b": 4, "c": 2},
        "b": {"c": 5, "d": 10},
        "c": {"e": 3},
        "d": {"f": 11},
        "e": {"d": 4},
        "f": {},
    }
    test_pathfinding(graph=test_graph)
    test_pathfinding(graph=test_graph_2)


if __name__ == "__main__":
    main()
