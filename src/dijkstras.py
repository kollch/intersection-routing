class Graph:
    def __init__(self):
        self.vertices = {}

    def __str__(self):
        return self.vertices.__str__()

    def __contains__(self, node):
        return node in self.vertices

    def add_node(self, name):
        if name in self.vertices:
            raise ValueError
        self.vertices[name] = {}

    def add_edge(self, src, dest, length):
        if src not in self.vertices or dest not in self.vertices:
            raise KeyError
        if dest in self.vertices[src] or length < 0:
            raise ValueError
        self.vertices[src][dest] = length

    def adjacent(self, node):
        if node not in self.vertices:
            raise KeyError
        return list(self.vertices[node].keys())

    def dist(self, src, dest):
        if (src not in self.vertices
                or dest not in self.vertices
                or dest not in self.vertices[src]):
            raise KeyError
        return self.vertices[src][dest]


class PriorityQueue:
    """Min priority queue, sorted by cost in (key, prev, cost).
    Only accepts unique (key, prev) combos; keeps (key, prev) combo
    with lowest cost
    """

    def __init__(self, init_node=None):
        self.queue = []
        if init_node is not None:
            self.queue.append(init_node)

    def __len__(self):
        return len(self.queue)

    def __str__(self):
        return list(reversed(self.queue)).__str__()

    def push(self, node):
        """node is formatted as (key, prev, cost)"""
        try:
            (key, prev, cost) = node
        except ValueError:
            raise ValueError("not enough values in the parameter")
        for i, val in enumerate(self.queue):
            if key == val[0] and prev == val[1]:
                if cost < val[2]:
                    self.queue.pop(i)
                    self.queue.append(node)
                    self.queue.sort(key=lambda x: x[2], reverse=True)
                break
        else:
            self.queue.append(node)
            self.queue.sort(key=lambda x: x[2], reverse=True)

    def pop(self):
        return self.queue.pop()


def dijkstra(graph, src, dest):
    if src not in graph:
        raise ValueError("source does not exist in graph")
    if dest not in graph:
        raise ValueError("destination does not exist in graph")
    (curr, prev, cost) = (src, None, 0)

    frontier = PriorityQueue((curr, prev, cost))

    explored = []

    while True:
        if not frontier:
            return None

        # gets node from frontier with smallest cost
        (curr, prev, cost) = frontier.pop()

        explored.append((curr, prev))

        if curr == dest:
            # found solution
            # backtrace from node to src
            return backtrace(curr, explored)

        for adj in graph.adjacent(curr):
            if (adj, curr) not in explored:
                frontier.push((adj, curr, cost + graph.dist(curr, adj)))

def backtrace(key, explored):
    result = []
    while key is not None:
        result.append(key)
        key = next(x for x in explored if x[0] == key)[1]
    result.reverse()
    return result

test_graph = Graph()
test_graph.add_node("a")
test_graph.add_node("b")
test_graph.add_node("c")
test_graph.add_node("d")
test_graph.add_node("e")
test_graph.add_node("f")
test_graph.add_node("g")
test_graph.add_edge("a", "b", 2)
test_graph.add_edge("b", "a", 2)
test_graph.add_edge("a", "c", 3)
test_graph.add_edge("c", "a", 3)
test_graph.add_edge("a", "d", 5)
test_graph.add_edge("d", "a", 5)
test_graph.add_edge("a", "g", 1)
test_graph.add_edge("g", "a", 1)
test_graph.add_edge("c", "d", 1)
test_graph.add_edge("d", "c", 1)
test_graph.add_edge("d", "g", 7)
test_graph.add_edge("g", "d", 7)
test_graph.add_edge("d", "f", 12)
test_graph.add_edge("f", "d", 12)
test_graph.add_edge("d", "e", 5)
test_graph.add_edge("e", "d", 5)
test_graph.add_edge("e", "f", 6)
test_graph.add_edge("f", "e", 6)

print(dijkstra(test_graph, "a", "f"))
