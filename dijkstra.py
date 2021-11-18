# !usr/bin/env python3

"""An implementation of Dijkstra's algorithm (No heap or priority queue) written in Python.
Dijkstra's algorithm finds the shortest path between two vertices when given a graph
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
        tuple[Any, Any]: A summary of the shortest paths as a dictionary if
        no target vertex is specified. Otherwise, an integer value for the
        shortest distance between the source and target vertex in the graph.
    """

    if source not in graph or target not in graph:
        if target is not None:
            raise LookupError("Source or target vertex is not in graph.")

    # Excluding the source, all vertices are marked as having an
    # infinite distance since they have not been visited.
    previous, unvisited = {}, set(graph)
    distance = {vertex: 0 if vertex is source else inf for vertex in unvisited}

    while unvisited:
        # Get the next best vertex in the graph.
        nearest = next(
            vertex
            for vertex in sorted(distance, key=distance.get)  # type: ignore
            if vertex in unvisited
        )
        unvisited.remove(nearest)

        if nearest == target:
            break

        # Traverse neighbours of the nearest sorted vertex.
        for neighbour, cost in graph[nearest].items():
            if cost < 0:
                raise ValueError("Edge cannot have a negative value.")
            if neighbour in unvisited:
                alternative = distance[nearest] + cost
                if alternative < distance[neighbour]:
                    distance[neighbour] = alternative
                    previous[neighbour] = nearest

    # Predecessors are tracked from the target back
    # to the source to reconstruct the shortest path
    # from the source to the target.
    if target is not None:
        path = deque()
        predecessor = target

        # Backtrack until the source is reached.
        while predecessor is not None:
            path.appendleft(predecessor)
            predecessor = previous.get(predecessor)
        return path, distance[target]

    return distance, previous


def test_pathfinding(graph: Graph, target: str = "a") -> None:
    print("\nTesting the following graph:\n")
    pprint(graph)
    print()
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
    test_pathfinding(graph=test_graph, target="e")
    test_pathfinding(graph=test_graph_2, target="e")


if __name__ == "__main__":
    main()
