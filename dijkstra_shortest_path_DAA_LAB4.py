"""
Dijkstra's Algorithm - Shortest Path (Min-Heap Implementation)
=================================================================
An interactive command-line tool that lets the user:
  1. Enter their own weighted directed graph (or auto-generate a random one)
  2. Compute shortest paths from a chosen source vertex to all other vertices
  3. View the shortest distance and full path to any vertex

Time Complexity:  O((V + E) log V)
Space Complexity: O(V)

Author: (your name here)
"""

import heapq
import random


def dijkstra(graph, source):
    """
    Dijkstra's Algorithm using a Min-Heap.
    graph: dict {u: [(v, weight), ...]}, 0-indexed
    Returns (dist, prev)
    """
    n = len(graph)
    dist = [float('inf')] * n
    prev = [None] * n
    dist[source] = 0
    pq = [(0, source)]  # (distance, vertex)
    visited = set()

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)

        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    return dist, prev


def reconstruct_path(prev, source, target):
    """Rebuilds the path from source to target using the prev array."""
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()

    if path and path[0] == source:
        return path
    return []


# --------------------------------------------------------------------------
# Helper / input functions
# --------------------------------------------------------------------------

def get_graph_from_user():
    """
    Prompts the user to either type their own directed weighted graph or
    auto-generate a random one.
    Returns a graph dict {u: [(v, weight), ...]}, 0-indexed.
    """
    print("\nHow would you like to provide the graph?")
    print("  1. Enter it manually")
    print("  2. Auto-generate a random graph")
    choice = input("Choose an option (1/2): ").strip()

    if choice == "1":
        try:
            n = int(input("Number of vertices (labeled 0 to n-1): ").strip())
            e_count = int(input("Number of directed edges: ").strip())
        except ValueError:
            print("Please enter valid integers.")
            return get_graph_from_user()

        if n <= 0 or e_count < 0:
            print("Need at least 1 vertex and a non-negative number of edges.")
            return get_graph_from_user()

        graph = {i: [] for i in range(n)}
        print(f"Enter each directed edge as: u v weight  (u -> v, vertices between 0 and {n - 1})")
        for i in range(e_count):
            raw = input(f"  Edge {i + 1}: ").strip().replace(",", " ")
            parts = raw.split()
            if len(parts) != 3:
                print("  Invalid format, expected: u v weight. Try again.")
                return get_graph_from_user()
            try:
                u, v, w = int(parts[0]), int(parts[1]), int(parts[2])
            except ValueError:
                print("  Invalid numbers, try again.")
                return get_graph_from_user()
            if not (0 <= u < n and 0 <= v < n):
                print(f"  Vertices must be between 0 and {n - 1}. Try again.")
                return get_graph_from_user()
            if w < 0:
                print("  Dijkstra's algorithm requires non-negative weights. Try again.")
                return get_graph_from_user()
            graph[u].append((v, w))

        return graph

    elif choice == "2":
        try:
            n = int(input("Number of vertices? (e.g. 6): ").strip())
            max_weight = int(input("Maximum edge weight? (e.g. 10): ").strip())
            edge_prob = input("Edge density 0-1 (press Enter for default 0.3): ").strip()
            edge_prob = float(edge_prob) if edge_prob else 0.3
        except ValueError:
            print("Please enter valid numbers.")
            return get_graph_from_user()

        if n <= 0 or max_weight <= 0 or not (0 < edge_prob <= 1):
            print("Invalid values. Vertices/weight must be positive, density between 0 and 1.")
            return get_graph_from_user()

        graph = {i: [] for i in range(n)}

        # Guarantee every vertex is reachable from 0 by building a random chain
        order = list(range(n))
        random.shuffle(order)
        for i in range(1, n):
            u, v = order[i - 1], order[i]
            w = random.randint(1, max_weight)
            graph[u].append((v, w))

        # Add extra random directed edges for a richer graph
        for u in range(n):
            for v in range(n):
                if u == v:
                    continue
                if random.random() < edge_prob:
                    w = random.randint(1, max_weight)
                    graph[u].append((v, w))

        print(f"Generated directed graph with {n} vertices:")
        for u in graph:
            for v, w in graph[u]:
                print(f"  {u} -> {v} (weight {w})")

        return graph

    else:
        print("Invalid choice, please try again.")
        return get_graph_from_user()


def get_source(n):
    """Prompts for a valid source vertex."""
    while True:
        raw = input(f"\nEnter the source vertex (0 to {n - 1}): ").strip()
        try:
            source = int(raw)
        except ValueError:
            print("Please enter a valid integer.")
            continue
        if 0 <= source < n:
            return source
        print(f"Source must be between 0 and {n - 1}.")


def print_shortest_paths(graph, source):
    n = len(graph)
    dist, prev = dijkstra(graph, source)

    print(f"\nShortest paths from vertex {source}:")
    print(f'{"Vertex":>8} {"Distance":>10} {"Path":>30}')
    print('-' * 55)

    for v in range(n):
        path = reconstruct_path(prev, source, v)
        path_str = ' -> '.join(map(str, path)) if path else 'No path'
        d = dist[v] if dist[v] != float('inf') else 'INF'
        print(f'{v:>8} {str(d):>10} {path_str:>30}')


def query_specific_path(graph, source):
    """Lets the user look up the shortest path to a specific target vertex."""
    n = len(graph)
    dist, prev = dijkstra(graph, source)

    while True:
        raw = input(f"\nEnter a target vertex (0 to {n - 1}), or press Enter to go back: ").strip()
        if raw == "":
            return
        try:
            target = int(raw)
        except ValueError:
            print("Please enter a valid integer.")
            continue
        if not (0 <= target < n):
            print(f"Target must be between 0 and {n - 1}.")
            continue

        path = reconstruct_path(prev, source, target)
        if path:
            d = dist[target]
            print(f"Shortest distance from {source} to {target}: {d}")
            print(f"Path: {' -> '.join(map(str, path))}")
        else:
            print(f"No path exists from {source} to {target}.")


# --------------------------------------------------------------------------
# Main menu
# --------------------------------------------------------------------------

def main():
    print("=" * 60)
    print(" Dijkstra's Algorithm - Shortest Path - Interactive Demo")
    print("=" * 60)

    while True:
        print("\nMain Menu:")
        print("  1. Build/enter a graph and compute shortest paths")
        print("  2. Exit")
        choice = input("Choose an option (1/2): ").strip()

        if choice == "1":
            graph = get_graph_from_user()
            source = get_source(len(graph))
            print_shortest_paths(graph, source)
            query_specific_path(graph, source)

        elif choice == "2":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
