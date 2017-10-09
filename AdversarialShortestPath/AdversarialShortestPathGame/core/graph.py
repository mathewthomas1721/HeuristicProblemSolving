from __future__ import print_function

import math
import heapq
import sys


class Graph(object):
    def __init__(self, edges, initial_cost=1.):
        self.nodes = Graph.make_nodes(edges)
        self.edges_and_costs = Graph.map_edge_costs(edges, initial_cost)
        self.adjacency_list = Graph.make_adjacency_list(self.nodes, edges)

    @staticmethod
    def make_nodes(edges):
        nodes = set()
        for edge in edges:
            nodes.add(edge[0])
            nodes.add(edge[1])
        return nodes

    @staticmethod
    def make_adjacency_list(nodes, edges):
        adjacency_list = dict()
        for node in nodes:
            adjacency_list[node] = []
        for edge in edges:
            adjacency_list[edge[0]].append(edge[1])
            adjacency_list[edge[1]].append(edge[0])
        return adjacency_list

    @staticmethod
    def map_edge_costs(edges, initial_cost):
        edges_costs = dict()
        for edge in edges:
            edges_costs[Graph.hash(edge)] = initial_cost
        return edges_costs

    @staticmethod
    def hash(edge):
        node_start, node_end = min(edge), max(edge)
        return str(node_start) + '_' + str(node_end)

    def scale_edge_cost(self, edge, cost_scale=1):
        if self.is_edge(edge):
            self.edges_and_costs[Graph.hash(edge)] *= cost_scale
            return self.edges_and_costs[Graph.hash(edge)]
        else:
            return 0

    def is_edge(self, edge):
        return Graph.hash(edge) in self.edges_and_costs

    def get_edge_cost(self, edge):
        return self.edges_and_costs.get(Graph.hash(edge), -1)

    def path_length(self, start_node, end_node):
        path_lengths = dict()
        for node in self.nodes:
            path_lengths[node] = sys.maxint
        path_lengths[start_node] = 0
        priority_queue = []
        visited_nodes = set()
        heapq.heappush(priority_queue, (path_lengths[start_node], start_node))

        while priority_queue:
            current_dist, current_node = heapq.heappop(priority_queue)
            if current_node in visited_nodes:
                continue
            visited_nodes.add(current_node)

            for next_node in self.adjacency_list[current_node]:
                if path_lengths[next_node] > current_dist + 1:
                    path_lengths[next_node] = current_dist + 1
                    heapq.heappush(priority_queue, (current_dist + 1, next_node))

        return path_lengths[end_node]


class GraphMapState(object):
    def __init__(self, graph, start_node, end_node):
        self.graph = graph
        self.start_node = start_node
        self.end_node = end_node

        self.current_position = self.start_node

    @staticmethod
    def init_from_textfile(filepath):
        with open(filepath, 'r') as f:
            lines = [(line.strip('\n')).strip() for line in f.readlines()]
            # First line is the start edge
            start_node = (lines[0].split(':')[1]).strip()
            # second line is the end edge
            end_node = (lines[1].split(':')[1]).strip()

            # Third line is the header
            # From fourth line to the end of file, it should be edges
            edges = []
            for line in lines[3:]:
                if len(line) > 0:
                    edge = line.split(' ')
                    assert len(edge) == 2, 'File has wrong edge'
                    edges.append(edge)

            graph = Graph(edges)
            return GraphMapState(graph, start_node, end_node)

    def move_edge(self, edge):
        if self.current_position == edge[0] and self.graph.is_edge(edge):
            self.current_position = edge[1]
            cost = self.graph.get_edge_cost(edge)
        else:
            cost = 0
        return cost, self.current_position == self.end_node

    def node_cost_factor(self, node):
        return 1 + math.sqrt(self.graph.path_length(node, self.end_node))

    def get_scale_factor(self, edge):
        return min(self.node_cost_factor(edge[0]), self.node_cost_factor(edge[1]))

    def update_edge(self, edge):
        new_cost = 0
        if self.graph.is_edge(edge):
            factor = self.get_scale_factor(edge)
            new_cost = self.graph.scale_edge_cost(edge, factor)
        return new_cost


if __name__ == "__main__":
    graph_map = GraphMapState.init_from_textfile('sample/advshort.txt')
    print(vars(graph_map))
    print(vars(graph_map.graph))
    print(graph_map.graph.path_length(graph_map.start_node, graph_map.end_node))
