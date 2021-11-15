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

from math import inf
from pprint import pprint

Graph = dict[str | int, dict[str | int, int]]  # Type alias for a Graph.

# Type hints need to be fixed.


def dijkstra(graph: Graph, source: str, target: str = None) -> dict[str, int] | int:
    """Returns the shortest path (or distance) between any two vertices
    when given a graph.

    Arguments:
        graph (Graph): The graph to traverse the vertices and edges of.
        source (str): The vertex to start at when pathfinding.
        target (str, optional): The vertex to find the shortest path to.
        Defaults to None.

    Raises:
        LookupError: If the source or target vertex is not in the graph.
        ValueError: If the weight of an edge is a negative integer.
        LookupError: If the target vertex is unreachable from the source.

    Returns:
        dict[str, int] | int: A summary of the shortest paths as
        a dictionary if no target vertex is specified. Otherwise,
        an integer value for the shortest distance between
        the source and target vertex in the graph.
    """

    if source not in graph or target not in graph:  # Prevent invalid lookups.
        if target is not None:
            raise LookupError("Source or target vertex is not in graph.")

    # Excluding the source, all vertices are marked as having a distance
    # that is unbounded ("inf") since they are unvisited.
    unvisited = set(graph.keys())
    distance = {vertex: 0 if vertex is source else inf for vertex in unvisited}

    while unvisited:
        # Get the vertex with the shortest distance in the mapping
        # of vertices to distances.
        nearest = next(
            vertex
            for vertex in sorted(distance, key=distance.get)
            if vertex in unvisited
        )
        unvisited.remove(nearest)

        # Traverse the graphs through the neighbours
        # of the nearest sorted vertex.
        for neighbour in graph[nearest]:
            if graph[nearest][neighbour] < 0:  # Prevent negative cycles.
                raise ValueError("Edge cannot have a negative value.")
            if neighbour in unvisited and nearest is source:
                distance[neighbour] = graph[nearest][neighbour]
                if neighbour is target:
                    return distance[target]
            else:
                distance[neighbour] = min(
                    distance[nearest] + graph[nearest][neighbour],
                    distance[neighbour],
                )

    try:
        # If the distance to the target was still marked as "inf",
        # then the target vertex was not reached.
        if distance[target] == inf:
            raise LookupError("Target vertex is unreachable from source.")
    except KeyError:
        # Target was not assigned, or assigned to None.
        if target is None:
            return distance


def test_pathfinding(graph) -> None:
    print("\n\nTesting the following graph:\n")
    pprint(graph)
    for vertex in graph:
        print(
            f"\nSource as vertex {vertex!r}\n",
            dijkstra(graph, source=vertex),
            sep="\n",
        )


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
