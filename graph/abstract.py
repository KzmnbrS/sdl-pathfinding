from collections import Hashable
from abc import ABC, abstractclassmethod


class Vertex(Hashable):

    def __init__(self, data):
        self._data, self.data = None, data

    data = property()

    @data.getter
    def data(self):
        return self._data

    @data.setter
    def data(self, new_val):
        if not isinstance(new_val, Hashable):
            raise TypeError(f'Vertex data must conform hashable protocol, '
                            f'but \'{type(new_val)}\' doesn\'t.')

        self._data = new_val

    def __hash__(self):
        return hash(self.data)

    def __eq__(self, other):
        return self.data == other.data

    def __repr__(self):
        return repr(self.data)


class Edge:

    def __init__(self, src: Vertex, dst: Vertex, weight):
        if src == dst:
            raise ValueError(f'Source and destination can\'t be the same vertex.')

        self.src = src
        self.dst = dst
        self.weight = weight

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return type(other) is Edge and self.__dict__ == other.__dict__

    def __repr__(self):
        return f'[{self.src} -> {self.dst} ({self.weight})]'


class EdgeType:
    """Enum used by graph implementations to
    create new edges.
    """

    @property
    def directed(self):
        """SOURCE -> DESTINATION"""
        return 0

    @property
    def undirected(self):
        """SOURCE <-> DESTINATION"""
        return 1


class Graph(ABC):

    @abstractclassmethod
    def create_vertex(self, data) -> Vertex:
        """Creates new vertex of passed data and appends
        it to the graph if it's not already there.

        Raises:
            TypeError: if passed data does not conform
                       Hashable protocol (collections module).

        Returns:
            Created vertex. Always.
        """
        pass

    @abstractclassmethod
    def connect(self, edge_type: EdgeType,
                src: Vertex, dst: Vertex, weight):
        """Connects two vertices within graph if both of them
        exist.

        Args:
            edge_type: EdgeType enum member which defines edge
                       direction.
            src:       Source vertex.
            dst:       Destination vertex.
            weight:    Edge weight.

        Raises:
            ValueError: if src == dst
        """
        pass

    @abstractclassmethod
    def vertices(self) -> {Vertex}:
        """Returns all vertices within graph wrapped in set container"""
        pass

    @abstractclassmethod
    def weight(self, src: Vertex, dst: Vertex):
        """Weights an edge between two vertices.

        Returns:
            None:   If one of passed vertices doesn't exist.
                    If vertices don't connected.
                    If edge is not weighted.
            Weight: In any other case.
        """
        pass

    @abstractclassmethod
    def __getitem__(self, item: Vertex) -> [Edge] or None:
        """Describes vertex neighbourhood.

        Returns:
            Edge list in case where vertex exists (you'll get
            an empty list if vertex hasn't got neighbours).

            None if vertex does not exist.
        """
        pass

    @abstractclassmethod
    def __setitem__(self, key: Vertex, value: [Edge]):
        """Sets $key vertex neighbourhood to $value, which
        must be an iterable container of edges. Does nothing if
        there's no such vertex in graph."""
        pass

    @abstractclassmethod
    def __delitem__(self, key: Vertex):
        """Removes $key vertex from the graph, also removes all edges connected
        with it."""
        pass
