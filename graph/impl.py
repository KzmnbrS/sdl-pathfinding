from graph.abstract import *


class AdjacencyMap(Graph):
    """Graph implementation based on adjacency lists.
    Basic idea is that each vertex holds a list of all outgoing
    connections (adjacency list). There's also an dict
    (adjacency map), which stores all {Vertex: [Edge]} pairs.
    """

    def __init__(self):
        self._adjMap = {}

    def create_vertex(self, data):
        v = Vertex(data)
        if v not in self._adjMap:
            self._adjMap[v] = []

        return v

    def connect(self, edge_type: EdgeType,
                src: Vertex, dst: Vertex, weight):

        def add_directed_edge(source, destination):
            edge = Edge(source, destination, weight)

            if edge not in self._adjMap[source]:
                self._adjMap[source].append(edge)

        if src not in self._adjMap or dst not in self._adjMap:
            return

        add_directed_edge(src, dst)

        if edge_type == EdgeType.undirected:
            add_directed_edge(dst, src)

    def vertices(self):
        return self._adjMap.keys()

    def weight(self, src: Vertex, dst: Vertex):
        if src in self._adjMap:
            for edge in self.edges(src):
                if edge.dst == dst:
                    return edge.weight

        return None

    def __getitem__(self, item):
        if item in self._adjMap:
            return self._adjMap[item]
        return None

    def __setitem__(self, key, value):
        if key in self._adjMap:
            self._adjMap[key] = value

    def __delitem__(self, key):
        if key in self._adjMap:
            del self._adjMap[key]
            for vertex, edges in self._adjMap.items():
                self._adjMap[vertex] = [e for e in edges if e.dst != key]

    def __repr__(self):
        def dst_n_weight(edge):
            return f'{repr(edge.dst)}' \
                   f'{" (%.3f)" % edge.weight if edge.weight else ""}'

        graph_repr = ''
        for v, edges in self._adjMap.items():
            graph_repr += f'{repr(v)}: [{", ".join([dst_n_weight(e) for e in edges])}]\n'
        return graph_repr
