# !usr/bin/env python3

"""An implementation of Dijkstra's algorithm (No heap or priority queue)
written in Python. Dijkstra's algorithm finds the shortest path between
two vertices when given a graph with non-negative edge weights.

Note:
    - The implementation of this algorithm differs from the version given
    in the references because the input for the graph is in the form of
    nested dictionaries instead of arrays.
    - Dijkstra's algorithm does not work with negative edge weights.
    - The following code is original, and has not been taken from anywhere else,
    apart from borrowing some ideas from the pseudocode in the Wikipedia entry.

References:
    - https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    - https://www.youtube.com/watch?v=GazC3A4OQTE&ab_channel=Computerphile
    - https://www.youtube.com/watch?v=XB4MIexjvY0&ab_channel=AbdulBari
"""

from collections import deque
from math import inf
from pprint import pprint
from typing import Any, Hashable, Union, overload

Vertex = Hashable
Graph = dict[Vertex, dict[Vertex, Union[int, float]]]
Distances = dict[Vertex, Union[int, float]]
Predecessors = dict[Vertex, Vertex]
Path = deque[Vertex]
Cost = Union[int, float]


@overload
def dijkstra(graph: Graph, source: Vertex) -> tuple[Distances, Predecessors]:
    ...


@overload
def dijkstra(graph: Graph, source: Vertex, target: Vertex) -> tuple[Path, Cost]:
    ...


def dijkstra(graph: Graph, source: Vertex, target: Vertex = None) -> tuple[Any, ...]:
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
        tuple[Any, ...]: The shortest distance from the source vertex to
        all other vertices, and the predecessor of every vertex, which
        can be used for path reconstruction if no target is specified
        or the target does not exist within the graph. If a target vertex
        is specified, then the shortest path will be returned,
        along with the cost of the path.
    """

    previous, unvisited = {}, set(graph)
    distance = {vertex: inf for vertex in graph}

    distance[source] = 0

    while unvisited:
        # Get and remove the best unvisited vertex.
        nearest = next(
            vertex
            for vertex in sorted(distance, key=distance.__getitem__)
            if vertex in unvisited
        )
        unvisited.remove(nearest)

        if nearest == target:
            break

        for neighbour, cost in graph[nearest].items():
            if cost < 0:
                raise ValueError("Edge cannot be negative.")
            if neighbour in unvisited:
                alternative = distance[nearest] + cost
                if alternative < distance[neighbour]:
                    distance[neighbour] = alternative
                    previous[neighbour] = nearest
    else:
        return distance, previous

    path = deque()
    predecessor = target

    # Reconstruct the shortest path by traversing
    # from the target back to the source.
    while predecessor is not None:
        path.appendleft(predecessor)
        predecessor = previous.get(predecessor)

    return path, distance[target]


def test_pathfinding(graph: Graph, target: str = "e") -> None:
    """Short test for dijkstra's algorithm."""

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
    test_pathfinding(graph=test_graph)
    test_pathfinding(graph=test_graph_2)


if __name__ == "__main__":
    main()
