import networkx as nx


def parseGraph(tsp_instance):
    G = nx.Graph()
    n = len(tsp_instance)
    for i in xrange(n):
        for j in xrange(i+1, n):
            G.add_edge(i, j, weight=tsp_instance[i][j])
    return G


def getSol(tsp_instance):
    G = parseGraph(tsp_instance)

    min_tour_cost = float('inf')
    best_tour_edges = None
    for start_node in G.nodes():
        visited = dict()
        tour = [start_node]
        visited[start_node] = 1
        cur_node = start_node

        while len(visited) != len(G.nodes()):
            min_cost = float('inf')
            best_node = None
            for node in G.nodes():
                if node not in visited:
                    dist = G[cur_node][node]['weight']
                    if dist < min_cost:
                        min_cost = dist
                        best_node = node
            visited[best_node] = 1
            tour.append(best_node)
            cur_node = best_node

        tour.append(start_node)   # make it cycle

        tour_edges = []
        cost = 0
        for i in xrange(len(tour)-1):
            node1 = tour[i]
            node2 = tour[i+1]
            dist = G[node1][node2]['weight']
            cost += dist
            tour_edges.append([node1, node2, dist])

        if cost < min_tour_cost:
            min_tour_cost = cost
            best_tour_edges = tour_edges

    return [min_tour_cost] + best_tour_edges
