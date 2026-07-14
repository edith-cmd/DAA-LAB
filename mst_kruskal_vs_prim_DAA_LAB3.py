"""
Minimum Spanning Tree: Kruskal's vs Prim's Algorithm
=======================================================
An interactive command-line tool that lets the user:
  1. Enter their own weighted graph (or auto-generate a random one)
  2. Compute the Minimum Spanning Tree (MST) using Kruskal's and Prim's algorithms
  3. Compare the resulting MST edges and total cost from both algorithms

Time Complexity:
  Kruskal's -> O(E log E)   (dominated by sorting the edges)
  Prim's    -> O(E log V)   (using a binary heap)

Space Complexity:
  Kruskal's -> O(V + E)
  Prim's    -> O(V + E)

Author: (your name here)
"""

import heapq
import random


# --------------------------------------------------------------------------
# Union-Find (Disjoint Set) for Kruskal's Algorithm
# --------------------------------------------------------------------------

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


# --------------------------------------------------------------------------
# MST Algorithms
# --------------------------------------------------------------------------

def kruskal(n, edges):
    """
    Kruskal's MST algorithm.
    edges: list of (weight, u, v)
    Returns (mst_edges, total_cost)
    """
    edges = sorted(edges)  # O(E log E)
    uf = UnionFind(n)
    mst = []
    cost = 0

    for w, u, v in edges:
        if uf.union(u, v):
            mst.append((u, v, w))
            cost += w
            if len(mst) == n - 1:
                break

    return mst, cost


def prim(n, adj, start=0):
    """
    Prim's MST algorithm.
    adj: adjacency list {u: [(v, w), ...]}
    Returns (mst_edges, total_cost)
    """
    INF = float('inf')
    key = [INF] * n
    parent = [-1] * n
    inMST = [False] * n

    key[start] = 0
    pq = [(0, start)]
    mst = []
    cost = 0

    while pq:
        w, u = heapq.heappop(pq)
        if inMST[u]:
            continue
        inMST[u] = True
        if parent[u] != -1:
            mst.append((parent[u], u, w))
            cost += w

        for v, wt in adj.get(u, []):
            if not inMST[v] and wt < key[v]:
                key[v] = wt
                parent[v] = u
                heapq.heappush(pq, (wt, v))

    return mst, cost


# --------------------------------------------------------------------------
# Helper / input functions
# --------------------------------------------------------------------------

def build_adjacency_list(n, edges):
    """Builds an adjacency list {u: [(v, w), ...]} from a list of (weight, u, v) edges."""
    adj = {i: [] for i in range(n)}
    for w, u, v in edges:
        adj.setdefault(u, []).append((v, w))
        adj.setdefault(v, []).append((u, w))
    return adj


def get_graph_from_user():
    """
    Prompts the user to either type their own graph or
    auto-generate a random connected graph.
    Returns (n, edges) where edges is a list of (weight, u, v).
    """
    print("\nHow would you like to provide the graph?")
    print("  1. Enter it manually")
    print("  2. Auto-generate a random connected graph")
    choice = input("Choose an option (1/2): ").strip()

    if choice == "1":
        try:
            n = int(input("Number of vertices (labeled 0 to n-1): ").strip())
            e_count = int(input("Number of edges: ").strip())
        except ValueError:
            print("Please enter valid integers.")
            return get_graph_from_user()

        if n <= 1 or e_count <= 0:
            print("Need at least 2 vertices and at least 1 edge.")
            return get_graph_from_user()

        edges = []
        print(f"Enter each edge as: u v weight  (vertices between 0 and {n - 1})")
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
            edges.append((w, u, v))

        return n, edges

    elif choice == "2":
        try:
            n = int(input("Number of vertices? (e.g. 7): ").strip())
            max_weight = int(input("Maximum edge weight? (e.g. 15): ").strip())
        except ValueError:
            print("Please enter valid integers.")
            return get_graph_from_user()

        if n <= 1 or max_weight <= 0:
            print("Need at least 2 vertices and a positive max weight.")
            return get_graph_from_user()

        # Guarantee connectivity: build a random spanning chain first
        edges = []
        seen_pairs = set()
        vertices = list(range(n))
        random.shuffle(vertices)
        for i in range(1, n):
            u, v = vertices[i - 1], vertices[i]
            w = random.randint(1, max_weight)
            edges.append((w, u, v))
            seen_pairs.add((min(u, v), max(u, v)))

        # Add some extra random edges for a richer graph
        extra_edges = random.randint(n // 2, n)
        attempts = 0
        while extra_edges > 0 and attempts < extra_edges * 10:
            attempts += 1
            u, v = random.randint(0, n - 1), random.randint(0, n - 1)
            if u == v:
                continue
            pair = (min(u, v), max(u, v))
            if pair in seen_pairs:
                continue
            w = random.randint(1, max_weight)
            edges.append((w, u, v))
            seen_pairs.add(pair)
            extra_edges -= 1

        print(f"Generated graph with {n} vertices and {len(edges)} edges:")
        for w, u, v in edges:
            print(f"  ({u} - {v}) Weight: {w}")

        return n, edges

    else:
        print("Invalid choice, please try again.")
        return get_graph_from_user()


def print_mst(title, mst, cost):
    print(f"\n=== {title} ===")
    if not mst:
        print("  (No edges found - check that the graph is connected)")
    for u, v, w in mst:
        print(f"  Edge ({u} - {v}) Weight: {w}")
    print(f"  Total MST Cost: {cost}")


def run_mst_comparison(n, edges):
    adj = build_adjacency_list(n, edges)

    k_mst, k_cost = kruskal(n, edges[:])
    p_mst, p_cost = prim(n, adj)

    print_mst("Kruskal's MST", k_mst, k_cost)
    print_mst("Prim's MST", p_mst, p_cost)

    if len(k_mst) < n - 1 or len(p_mst) < n - 1:
        print("\nNote: The graph may be disconnected -- MST does not span all vertices.")

    if k_cost == p_cost and len(k_mst) == len(p_mst):
        print(f"\nBoth algorithms agree on total MST cost: {k_cost}")
    else:
        print(f"\nCost mismatch! Kruskal: {k_cost}, Prim: {p_cost} "
              f"(this can happen if the graph is disconnected).")


# --------------------------------------------------------------------------
# Main menu
# --------------------------------------------------------------------------

def main():
    print("=" * 60)
    print(" Minimum Spanning Tree: Kruskal's vs Prim's - Interactive Demo")
    print("=" * 60)

    while True:
        print("\nMain Menu:")
        print("  1. Build/enter a graph and compute its MST")
        print("  2. Exit")
        choice = input("Choose an option (1/2): ").strip()

        if choice == "1":
            n, edges = get_graph_from_user()
            run_mst_comparison(n, edges)

        elif choice == "2":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
