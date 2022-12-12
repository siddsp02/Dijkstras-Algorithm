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
from pprint import pprint
from typing import Mapping, TypeVar, overload


TEST_GRAPHS = [
    {
        "s": {"a": 1, "b": 5},
        "a": {"b": 2, "c": 2, "d": 1},
        "b": {"d": 2},
        "c": {"d": 3, "e": 1},
        "d": {"e": 2},
        "e": {},
    },
    {
        "a": {"b": 4, "c": 2},
        "b": {"c": 5, "d": 10},
        "c": {"e": 3},
        "d": {"f": 11},
        "e": {"d": 4},
        "f": {},
    },
]

INF = float("inf")

K = TypeVar("K")
V = TypeVar("V", bound=float)


@overload
def dijkstra(graph: Mapping[K, Mapping[K, V]], src: K) -> tuple[dict[K, V], dict[K, K]]:
    ...


@overload
def dijkstra(graph: Mapping[K, Mapping[K, V]], src: K, dst: K) -> tuple[deque[K], V]:
    ...


def dijkstra(graph, src, dst=None):  # type: ignore
    """Returns the shortest distance (or path) between any two vertices
    when given a weighted graph.

    References:
        - https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    """
    dist = dict.fromkeys(graph, INF)
    prev = dict.fromkeys(graph, None)
    dist[src] = 0
    unmarked = set(graph)
    while unmarked:
        u = min(unmarked, key=dist.get)  # type: ignore
        unmarked.remove(u)
        if u == dst:
            break
        neighbours = graph[u].keys()
        for v in neighbours & unmarked:
            alt = dist[u] + graph[u][v]
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
    else:
        return dist, prev
    path = deque[K]()
    pred = dst
    while pred is not None:
        path.appendleft(pred)
        pred = prev.get(pred)
    return path, dist[dst]


def test_pathfinding(graph: Mapping[K, Mapping[K, V]], dst: K) -> None:
    print("\nTesting the following graph:\n")
    pprint(graph)
    print()
    for src in graph:
        print(f"{src=!r} to {dst=!r}: ", end="")
        path, dist = dijkstra(graph, src, dst)
        print(f"{path=}, {dist=}")


def main() -> None:
    for graph in TEST_GRAPHS:
        test_pathfinding(graph, dst="e")


if __name__ == "__main__":
    main()
