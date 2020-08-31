from queue import Queue

import graph.impl
from graph.abstract import *


REGULAR = 1
WALL = 2
START = 3
FINISH = 4
PATH = 5


class Cell(Hashable):

    def __init__(self, i, j, kind):
        self.i = i
        self.j = j
        self.kind = kind

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return type(other) is Cell and self.__dict__ == other.__dict__

    def __repr__(self):
        return '(%d, %d, %d)' % (self.i, self.j, self.kind)


class Maze:

    def __init__(self, i_size, j_size, graph_impl=None):
        self.i_size = i_size
        self.j_size = j_size

        self._start = None
        self._finish = None

        self.graph = graph_impl or graph.impl.AdjacencyMap()
        self.index_map = {}

        for i in range(i_size):
            for j in range(j_size):
                current = self.graph.create_vertex(Cell(i, j, REGULAR))

                if i != 0:
                    upper = Vertex(self.cell_for_index(i - 1, j))
                    self.graph.connect(EdgeType.undirected, current, upper, 1)

                if j != 0:
                    left = Vertex(self.cell_for_index(i, j - 1))
                    self.graph.connect(EdgeType.undirected, current, left, 1)

    start = property()

    @start.getter
    def start(self):
        return self._start

    @start.setter
    def start(self, new_start):
        if self._start:
            self.set(self._start, REGULAR)
        self._start = self.set(new_start, START)

    finish = property()

    @finish.getter
    def finish(self):
        return self._finish

    @finish.setter
    def finish(self, new_finish):
        if self._finish:
            self.set(self._finish, REGULAR)
        self._finish = self.set(new_finish, FINISH)

    def cell_for_index(self, i_key, j_key):
        for vertex in self.graph.vertices():
            cell = vertex.data

            if cell.i == i_key and cell.j == j_key:
                return cell
        return None

    def set(self, target_cell, new_kind):
        for old_vertex in self.graph.vertices():
            cell = old_vertex.data

            if cell == target_cell:
                if cell.kind == new_kind:
                    return cell

                # Preventing case where internal _start / _finish
                # variable holds cell which was redefined with
                # different kind.
                if target_cell == self._start \
                        and new_kind != START:
                    self._start = None
                elif target_cell == self._finish \
                        and new_kind != FINISH:
                    self._finish = None

                old_neighbours = self.graph[old_vertex]

                del self.graph[old_vertex]
                new_vertex = self.graph.create_vertex(Cell(cell.i, cell.j,
                                                           new_kind))

                for connection in old_neighbours:
                    connection.src = new_vertex

                self.graph[new_vertex] = old_neighbours
                
                for neighbour in [conn.dst for conn in old_neighbours]:
                    # Graph implementation should to get rid of all
                    # edges directed to the old_vertex on del self.graph[old_vertex] call
                    self.graph[neighbour].append(Edge(neighbour, new_vertex, 1))

                return new_vertex.data

    def bfs_path(self, source, destination):
        source, destination = Vertex(source), Vertex(destination)

        unexplored = Queue()
        unexplored.put(source)

        visits = {}
        while not unexplored.empty():
            current = unexplored.get()

            if current == destination:
                wayback = []

                while current != source:
                    current = visits[current].src
                    wayback.append(current)

                # Start is not part of the path,
                # neither finish is.
                return [v.data for v in reversed(wayback[:-1])]

            neighbours = self.graph[current]

            for conn in neighbours:
                if conn.dst.data.kind == WALL:
                    continue

                if conn.dst not in visits:
                    visits[conn.dst] = conn
                    unexplored.put(conn.dst)

        return None
