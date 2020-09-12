class NonExistantVertex(Exception):
    '''No such vertex found in graph'''


class Graph:
    def __init__(self, adjacency_list):
        '''
        @param: adjacency_list must be a list of tuples, each tuple
        with minimum length of 3. First two elements of tuple must
        be immutable. Third element a Number
        '''

        # set of vertices
        self.verticies = set()

        # Key is 2-tuple (Vertex, Vertex), Value is weight of edge
        self.edge_weight_dict = {}

        # Key is vertex, Value is a set representing adjacent vertices
        self.adjacnecy_only_dict = {}

        for (start, end, weight) in adjacency_list:
            self.verticies.add(start)
            self.verticies.add(end)
            self.edge_weight_dict[(start, end)] = weight
            if (start not in self.adjacnecy_only_dict):
                self.adjacnecy_only_dict[start] = set()
            self.adjacnecy_only_dict[start].add(end)

        self.previous_states = []

    def dijkstra(self, source, target=None):
        verticies = self.verticies.copy()

        if (source not in verticies or
                (target is not None and target not in verticies)):
            raise NonExistantVertex(
                'Source or Target vertex does not exist in graph')

        dist = {}
        prev = {}
        for vertex in verticies:
            dist[vertex] = float("inf")
            prev[vertex] = None
        dist[source] = 0

        while len(verticies) != 0:
            min_vert = self._minDist(dist, verticies)
            verticies.remove(min_vert)

            if (target == min_vert):
                return (dist, prev)

            for (start, end), weight in self.edge_weight_dict.items():

                if start != min_vert:
                    continue
                temp = dist[min_vert] + weight
                if temp < dist[end]:
                    dist[end] = temp
                    prev[end] = min_vert

        return (dist, prev)

    def _minDist(self, dict_distances, vertices):
        min_dist = float("inf")
        min_vert = None
        for vertex in vertices:
            if (dict_distances[vertex] <= min_dist):
                min_dist = dict_distances[vertex]
                min_vert = vertex
        return min_vert

    def getWeightPath(self, path):
        '''
        @param: path Can be string or list or tuple
                        If List: [A,B,C]
                        If String: "A-B-C"
        '''
        if (isinstance(path, list) or isinstance(path, tuple)):
            list_path = path
        else:
            list_path = path.split('-')
        total_distance = 0
        try:
            for i in range(len(list_path)-1):
                start, end = list_path[i], list_path[i+1]
                total_distance += self.edge_weight_dict[(start, end)]
        except KeyError:
            return -1
        return total_distance

    def getAllPathsBetween(self,
                           start, end,
                           min_len=0, max_len=None,
                           max_weight=None):
        '''
        If both max_len and max_weight are None, then max_len is set to number
        of vertices in graph.
        If both max_len and max_weight are given, then both will be satisfied.
        '''
        if (max_len is None and max_weight is None):

            max_len = len(self.verticies)
        if (max_len is None and max_weight is not None):
            max_len = float('inf')
        if (max_len is not None and max_weight is None):
            max_weight = float('inf')

        if (start not in self.verticies or end not in self.verticies):
            raise NonExistantVertex(
                'Starting or Ending vertex does not exist in graph')
        list_paths = []

        last_vert_dict = {}
        for vertex in self.verticies:
            last_vert_dict[vertex] = set()
        last_vert_dict[start].add((start,))
        queue = [start]

        while len(queue) != 0:
            focus = queue.pop(0)
            path_to_focus = last_vert_dict[focus]
            if focus not in self.adjacnecy_only_dict:

                continue
            for adj_vert in self.adjacnecy_only_dict[focus]:
                new_path_to_adj_vert = False
                all_paths_too_long = True
                for path_tuple in path_to_focus:
                    path_to_adj_vert = path_tuple + (adj_vert,)

                    if (path_to_adj_vert not in last_vert_dict[adj_vert]):
                        new_path_to_adj_vert = True
                    else:
                        continue

                    last_vert_dict[adj_vert].add(path_to_adj_vert)

                    path_len = len(path_to_adj_vert) - 1
                    path_weight = self.getWeightPath(path_to_adj_vert)

                    all_paths_too_long = all_paths_too_long and (
                        path_len > max_len or path_weight >= max_weight)

                    if (adj_vert == end
                            and min_len <= path_len and path_len <= max_len
                            and path_weight < max_weight):
                        list_paths.append(path_to_adj_vert)

                if (new_path_to_adj_vert and not all_paths_too_long):

                    queue.append(adj_vert)

        return list_paths

    def getAdjacencyDict(self):
        return self.adjacnecy_only_dict

    def getEdgeWeightDict(self):
        return self.edge_weight_dict

    def modGraph(self, adjacency_list):
        '''
        Adds, Removes, or Edits the list of given edges to/from current graph.

        If the weight of the edge is set to float('inf'), "inf", or is None,
        then that edge will be removed if such an edge exists.
        '''
        if (len(adjacency_list) == 0):

            self.previous_states.append(None)
            return
        # Copy current state
        curr_state = {}
        curr_state['verticies'] = self.verticies.copy()
        curr_state['edge_weights'] = self.edge_weight_dict.copy()
        curr_state['adjacency_only'] = {}
        for vertex, adjacency_set in self.adjacnecy_only_dict.items():
            curr_state['adjacency_only'][vertex] = adjacency_set.copy()

        # Save a copy of current state
        self.previous_states.append(curr_state)

        # Modifying the current state
        for (start, end, weight) in adjacency_list:
            if (weight == float('inf') or weight == 'inf' or weight is None):
                # remove edge from graph
                if (start, end) in self.edge_weight_dict:
                    del self.edge_weight_dict[(start, end)]
                if start in self.adjacnecy_only_dict:
                    self.adjacnecy_only_dict.discard(end)
            else:
                # add edge to graph
                self.verticies.add(start)
                self.verticies.add(end)
                self.edge_weight_dict[(start, end)] = weight
                if (start not in self.adjacnecy_only_dict):
                    self.adjacnecy_only_dict[start] = set()
                self.adjacnecy_only_dict[start].add(end)

    def modUndo(self):
        '''Undo a graph modification if there exists a modification to undo.'''
        if (len(self.previous_states) == 0):
            return

        most_recent_prev_state = self.previous_states.pop()
        if (most_recent_prev_state is None):

            return
        self.verticies = most_recent_prev_state['verticies']
        self.edge_weight_dict = most_recent_prev_state['edge_weights']
        self.adjacnecy_only_dict = most_recent_prev_state['adjacency_only']
