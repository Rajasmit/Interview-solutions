from graph import Graph, NonExistantVertex


class TrainRoutes:
    def __init__(self, adjacency_list):
        self.routes_graph = Graph(adjacency_list)

    def shortestPath(self, source, target):
        ret_dist_shortest = None
        if (source == target):
            # modifying the graph to reuse dijkstra's algorithm
            edge_weight_dict = self.routes_graph.getEdgeWeightDict()
            target_prime = "___ARTIFICIAL_TARGET___"

            new_weighted_edges = []
            for (start, end), weight in edge_weight_dict.items():
                if (end == source):
                    new_weighted_edges.append((start, target_prime, weight))

            self.routes_graph.modGraph(
                new_weighted_edges)
            try:
                ret_dist_shortest = self.routes_graph.dijkstra(
                    source, target_prime)[0][target_prime]
            except NonExistantVertex:
                ret_dist_shortest = float('inf')
            self.routes_graph.modUndo()
        else:
            try:
                ret_dist_shortest = self.routes_graph.dijkstra(source, target)[
                    0][target]
            except NonExistantVertex:
                ret_dist_shortest = float('inf')

        return ret_dist_shortest

    def distPath(self, path):
        dist_path = self.routes_graph.getWeightPath(path)
        if (dist_path < 0):
            return 'NO SUCH ROUTE'
        return self.routes_graph.getWeightPath(path)

    def numDiffPaths(self, start, end,
                     min_stops=0, max_stops=None,
                     max_dist=None):
        all_paths = self.routes_graph.getAllPathsBetween(
            start, end, min_stops, max_stops, max_dist)
        return len(all_paths)
