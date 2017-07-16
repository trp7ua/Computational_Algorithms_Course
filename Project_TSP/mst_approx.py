import networkx as nx


def parseGraph(tsp_instance):
    G = nx.Graph()
    n = len(tsp_instance)
    for i in xrange(n):
        for j in xrange(i+1, n):
            G.add_edge(i, j, weight=tsp_instance[i][j])
    return G


def prim(G):
    MST = nx.Graph()
    visited = dict()
    visited[0] = 1
    all_nodes = G.nodes()
    while len(visited) != len(all_nodes):
        min_dist = float('inf')
        min_edge = None
        for node_in in all_nodes:
            for node_out in all_nodes:
                if node_in in visited and node_out not in visited:
                    dist = G[node_in][node_out]['weight']
                    if dist < min_dist:
                        min_dist = dist
                        min_edge = [node_in, node_out]
        MST.add_edge(min_edge[0], min_edge[1], weight=min_dist)
        visited[min_edge[1]] = 1
    return MST


def getSol(tsp_instance):
    G = parseGraph(tsp_instance)
    MST = prim(G)

    def dfs(G, node, visited, tour):
        if node not in visited:
            visited[node] = 1
            tour.append(node)
            for neighbor in G.neighbors(node):
                dfs(G, neighbor, visited, tour)

    min_cost = float('inf')
    best_tour_edges = None
    for start_node in MST.nodes():
        visited = dict()
        tour = []
        dfs(MST, start_node, visited, tour)
        tour.append(tour[0])  # make it cycle

        tour_edges = []
        cost = 0
        for i in xrange(len(tour)-1):
            node1 = tour[i]
            node2 = tour[i+1]
            dist = G[node1][node2]['weight']
            cost += dist
            tour_edges.append([node1, node2, dist])

        if cost < min_cost:
            min_cost = cost
            best_tour_edges = tour_edges

    return [min_cost] + best_tour_edges
