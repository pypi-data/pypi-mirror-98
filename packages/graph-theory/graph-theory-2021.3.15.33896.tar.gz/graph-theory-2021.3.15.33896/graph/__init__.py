from collections import defaultdict, deque, Iterable
from heapq import heappop, heappush
from itertools import combinations, chain
from bisect import insort


from graph.visuals import plot_3d

__description__ = """
The graph-theory library is organised in the following way for clarity of structure:

1. BasicGraph (class) - with general methods for all subclasses.
2. All methods for class Graph in same order as on Graph.
3. Graph (class)
4. Graph3D (class) 

"""


class BasicGraph(object):
    """
    BasicGraph is the base graph that all methods use.

    For methods, please see the documentation on the
    individual functions, by importing them separately.
    """

    def __init__(self, from_dict=None, from_list=None):
        """
        :param from_dict: creates graph for dictionary {n1:{n2:d} ...
        :param from_list: creates graph from list of edges(n1,n2,d)
        """
        self._nodes = {}
        self._edges = defaultdict(dict)
        self._reverse_edges = defaultdict(dict)
        self._in_degree = defaultdict(int)
        self._out_degree = defaultdict(int)

        if from_dict is not None:
            self.from_dict(from_dict)
        elif from_list is not None:
            self.from_list(from_list)

    def __getitem__(self, item):
        raise ValueError("Use g.node(n1) or g.edge(n1,n2)")

    def __setitem__(self, key, value):
        raise ValueError("Use add_edge(node1, node2, value)")

    def __delitem__(self, key):
        raise ValueError("Use del_edge(node1, node2)")

    def __contains__(self, item):
        """
        :returns bool: True if node in Graph.
        """
        return item in self._nodes

    def __len__(self):
        raise ValueError("Use len(g.nodes()) or len(g.edges())")

    def add_edge(self, node1, node2, value=1, bidirectional=False):
        """
        :param node1: hashable node
        :param node2: hashable node
        :param value: numeric value (int or float)
        :param bidirectional: boolean.
        """
        if isinstance(value, (dict, list, tuple)):
            raise ValueError("value cannot be {}".format(type(value)))
        if node1 not in self._nodes:
            self.add_node(node1)
        if node2 not in self._nodes:
            self.add_node(node2)

        self._edges[node1][node2] = value
        self._out_degree[node1] += 1
        self._in_degree[node2] += 1
        self._reverse_edges[node2][node1] = value

        if bidirectional:
            self.add_edge(node2, node1, value, bidirectional=False)

    def edge(self, node1, node2, default=None):
        """Retrieves the edge (node1, node2)

        Alias for g[node1][node2]

        :param node1: node id
        :param node2: node id
        :param default: returned value if edge doesn't exist.
        :return: edge(node1,node2)
        """
        try:
            return self._edges[node1][node2]
        except KeyError:
            return default

    def reverse_edge(self, node2, node1, default=None):
        """ retrieves the edge from node2 to node1 """
        try:
            return self._reverse_edges[node2][node1]
        except KeyError:
            return default

    def del_edge(self, node1, node2):
        """
        removes edge from node1 to node2
        :param node1: node
        :param node2: node
        """
        del self._edges[node1][node2]
        del self._reverse_edges[node2][node1]
        self._out_degree[node1] -= 1
        self._in_degree[node2] -= 1

    def add_node(self, node_id, obj=None):
        """
        :param node_id: any hashable node.
        :param obj: any object that the node should refer to.

        PRO TIP: To retrieve the node obj use g.node(node_id)

        """
        if node_id in self._nodes:  # it's an object update.
            self._nodes[node_id] = obj
        else:
            self._nodes[node_id] = obj
            self._out_degree[node_id] = 0
            self._in_degree[node_id] = 0

    def node(self, node_id):
        """
        Retrieves the node object

        :param node_id: id of node in graph.
        :return: node object
        """
        return self._nodes.get(node_id, None)

    def del_node(self, node_id):
        """
        Deletes the node and all its connections.
        :param node_id: node_id
        :return: None
        """
        try:
            del self._nodes[node_id]
        except KeyError:
            return

        # outgoing
        for n2, d in self._edges[node_id].copy().items():
            self.del_edge(node_id, n2)
        del self._edges[node_id]

        # incoming
        for n1, d in self._reverse_edges[node_id].copy().items():
            self.del_edge(n1, node_id)
        del self._reverse_edges[node_id]  # removes outgoing edges

    def nodes(self,
              from_node=None, to_node=None,
              in_degree=None, out_degree=None):
        """
        :param from_node (optional) return nodes with edges from 'from_node'
        :param to_node (optional) returns nodes with edges into 'to_node'
        :param in_degree (optional) returns nodes with in_degree=N
        :param out_degree (optional) returns nodes with out_degree=N

        :return list of node ids.
        """
        inputs = sum([1 for i in (from_node, to_node, in_degree, out_degree) if i is not None])
        if inputs > 1:
            m = []
            a = (from_node, to_node, in_degree, out_degree)
            b = ("from_node", "to_node", "in_degree", "out_degree")
            for i in zip(a, b):
                if i is not None:
                    m.append("{}={}".format(b, a))
            raise ValueError("nodes({}) has too many inputs. Pick one.".format(m))

        if inputs == 0:
            return list(self._nodes.keys())

        if from_node is not None:
            if from_node in self._edges:
                return list(self._edges[from_node])
            return []

        if to_node is not None:
            return list(self._reverse_edges[to_node])

        if in_degree is not None:
            if not isinstance(in_degree, int) or in_degree < 0:
                raise ValueError("in_degree must be int >= 0")
            return [n for n, cnt in self._in_degree.items() if cnt == in_degree]

        if out_degree is not None:
            if not isinstance(out_degree, int) or out_degree < 0:
                raise ValueError("out_degree must be int >= 0")
            return [n for n, cnt in self._out_degree.items() if cnt == out_degree]

    def edges(self, path=None, from_node=None, to_node=None):
        """
        :param path (optional) list of nodes for which the edges are wanted.
        :param from_node (optional) for which outgoing edges are returned.
        :param to_node (optional) for which incoming edges are returned.
        :return list of edges (n1, n2, value)
        """
        inputs = sum([1 for i in (from_node, to_node, path) if i is not None])
        if inputs > 1:
            m = []
            a = (path, from_node, to_node)
            b = ("path", "from_node", "to_node")
            for i in zip(a, b):
                if i is not None:
                    m.append("{}={}".format(b, a))
            raise ValueError("edges({}) has too many inputs. Pick one.".format(m))

        if path:
            if not isinstance(path, list):
                raise ValueError("expects a list")
            if len(path) < 2:
                raise ValueError("path of length 1 is not a path.")

            return [(path[ix], path[ix + 1], self._edges[path[ix]][path[ix + 1]])
                    for ix in range(len(path) - 1)]

        if from_node:
            if from_node in self._edges:
                return [(from_node, n2, cost) for n2, cost in self._edges[from_node].items()]
            else:
                return []

        if to_node:
            if to_node in self._reverse_edges:
                return [(n1, to_node, value) for n1, value in self._reverse_edges[to_node].items()]
            else:
                return []

        return [(n1, n2, out[n2]) for n1, out in self._edges.items() for n2 in out]

    def from_dict(self, dictionary):
        """
        Updates the graph from dictionary
        :param dictionary:

        d = {1: {2: 10, 3: 5},
             2: {4: 1, 3: 2},
             3: {2: 3, 4: 9, 5: 2},
             4: {5: 4},
             5: {1: 7, 4: 6}}

        G = Graph(from_dict=d)

        :return: None
        """
        assert isinstance(dictionary, dict)
        for n1, e in dictionary.items():
            if not e:
                self.add_node(n1)
            else:
                for n2, v in e.items():
                    self.add_edge(n1, n2, v)

    def to_dict(self):
        """ creates a nested dictionary from the graph.
        :return dict d[n1][n2] = distance
        """
        d = {n: {} for n in self.nodes()}
        for n1, n2, dist in self.edges():
            d[n1][n2] = dist
        return d

    def from_list(self, links):
        """
        updates the graph from a list of links.
        :param links: list

        links = [
            (1, 2, 18),
            (1, 3, 10),
            (2, 4, 7),
            (2, 5, 6),
            (3, 4, 2),
            (11,)      # node with no links.
        ]
        """
        assert isinstance(links, Iterable)
        for item in links:
            assert isinstance(item, (list, tuple))
            if len(item) > 1:
                self.add_edge(*item)
            else:
                self.add_node(item[0])

    def to_list(self):
        """ returns list of edges and nodes."""
        return self.edges() + [(i,) for i in self.nodes()]

    def is_connected(self, n1, n2):
        """ helper determining if two nodes are connected using BFS. """
        if n1 in self._edges:
            q = [n1]
            visited = set()
            while q:
                n = q.pop(0)
                if n not in visited:
                    visited.add(n)
                for c in self._edges[n]:
                    if c == n2:
                        return True  # <-- Exit if connected.
                    if c in visited:
                        continue
                    else:
                        q.append(c)
        return False  # <-- Exit if not connected.


# Graph functions
# -----------------------------
def shortest_path(graph, start, end):
    """ single source shortest path algorithm.
    :param graph: class Graph
    :param start: start node
    :param end: end node
    :return: distance, path (as list),
             returns float('inf'), [] if no path exists.
    """
    q, visited, minimums = [(0, 0, start, ())], set(), {start: 0}
    i = 1
    while q:
        (cost, _, v1, path) = heappop(q)
        if v1 not in visited:
            visited.add(v1)
            path = (v1, path)

            if v1 == end:  # exit criteria.
                L = []
                while path:
                    v, path = path[0], path[1]
                    L.append(v)
                L.reverse()
                return cost, L

            for _, v2, dist in graph.edges(from_node=v1):
                if v2 in visited:
                    continue
                prev = minimums.get(v2, None)
                next_node = cost + dist
                if prev is None or next_node < prev:
                    minimums[v2] = next_node
                    heappush(q, (next_node, i, v2, path))
                    i += 1
    return float("inf"), []


def breadth_first_search(graph, start, end):
    """ Determines the path from start to end with fewest nodes.
    :param graph: class Graph
    :param start: start node
    :param end: end node
    :return: path
    """
    visited = {start: None}
    q = deque([start])
    while q:
        node = q.popleft()
        if node == end:
            path = deque()
            while node is not None:
                path.appendleft(node)
                node = visited[node]
            return list(path)
        for next_node in graph.nodes(from_node=node):
            if next_node not in visited:
                visited[next_node] = node
                q.append(next_node)
    return []


def breadth_first_walk(graph, start, end=None, reversed_walk=False):
    """
    :param graph: Graph
    :param start: start node
    :param end: end node.
    :param reversed_walk: if True, the BFS traverse the graph backwards.
    :return: generator for walk.

    To walk all nodes use: `[n for n in g.breadth_first_walk(start)]`
    """
    visited = {start: None}
    q = deque([start])
    while q:
        node = q.popleft()
        yield node
        if node == end:
            break
        L = graph.nodes(from_node=node) if not reversed_walk else graph.nodes(to_node=node)
        for next_node in L:
            if next_node not in visited:
                visited[next_node] = node
                q.append(next_node)


def depth_first_search(graph, start, end):
    """
    Determines path from start to end using
    'depth first search' with backtracking.

    :param graph: class Graph
    :param start: start node
    :param end: end node
    :return: path as list of nodes.
    """
    if start not in graph:
        raise ValueError(f"{start} not in graph")
    if end not in graph:
        raise ValueError(f"{end} not in graph")

    q = [start]
    path = []
    visited = set()
    while q:
        n1 = q.pop()
        visited.add(n1)
        path.append(n1)
        if n1 == end:
            return path  # <-- exit if end is found.
        for n2 in graph.nodes(from_node=n1):
            if n2 in visited:
                continue
            q.append(n2)
            break
        else:
            path.remove(n1)
            while not q and path:
                for n2 in graph.nodes(from_node=path[-1]):
                    if n2 in visited:
                        continue
                    q.append(n2)
                    break
                else:
                    path = path[:-1]
    return None  # <-- exit if not path was found.


def depth_scan(graph, start, criteria):
    """ traverses the descendants of node `start` using callable `criteria` to determine
    whether to terminate search along each branch in `graph`.

    :param graph: class Graph
    :param start: start node
    :param criteria: function to terminate scan along a branch must return bool
    :return: set of nodes
    """
    if not callable(criteria):
        raise TypeError(f"Expected {criteria} to be callable")
    if start not in graph:
        raise ValueError(f"{start} not in graph")
    if not criteria(start):
        return set()

    q = [start]
    path = []
    visited = set()
    while q:
        n1 = q.pop()
        visited.add(n1)
        path.append(n1)
        for n2 in graph.nodes(from_node=n1):
            if n2 in visited:
                continue
            if not criteria(n2):
                visited.add(n2)
                continue
            q.append(n2)
            break
        else:
            path.remove(n1)
            while not q and path:
                for n2 in graph.nodes(from_node=path[-1]):
                    if n2 in visited:
                        continue
                    if not criteria(n2):
                        visited.add(n2)
                        continue
                    q.append(n2)
                    break
                else:
                    path = path[:-1]
    return visited


def distance(graph, path):
    """ Calculates the distance for the path in graph
    :param graph: class Graph
    :param path: list of nodes
    :return: distance
    """
    assert isinstance(path, (tuple, list))
    cache = defaultdict(dict)
    path_length = 0
    for idx in range(len(path) - 1):
        n1, n2 = path[idx], path[idx + 1]

        # if the edge exists...
        d = graph.edge(n1, n2, default=None)
        if d:
            path_length += d
            continue

        # if we've seen the edge before...
        d = cache.get((n1, n2), None)
        if d:
            path_length += d
            continue

        # if there no alternative ... (search)
        d, _ = shortest_path(graph, n1, n2)
        if d == float('inf'):
            return float('inf')  # <-- Exit if there's no path.
        else:
            cache[(n1, n2)] = d
        path_length += d
    return path_length


def maximum_flow(graph, start, end):
    """
    Returns the maximum flow graph
    :param graph: instance of Graph
    :param start: node
    :param end: node
    :return: flow, graph
    """
    inflow = sum(d for s, e, d in graph.edges(from_node=start))
    outflow = sum(d for s, e, d in graph.edges(to_node=end))
    unassigned_flow = min(inflow, outflow)  # search in excess of this 'flow' is a waste of time.
    total_flow = 0
    # -----------------------------------------------------------------------
    # The algorithm
    # I reviewed a number of algorithms, such as Ford-fulkerson algorithm,
    # Edmonson-Karp and Dinic, but I didn't like them due to their naive usage
    # of DFS, which leads to a lot of node visits.
    #
    # I therefore choose to invert the capacities of the graph so that the
    # capacity any G[u][v] = c becomes 1/c in G_inverted.
    # This allows me to use the shortest path method to find the path with
    # most capacity in the first attempt, resulting in a significant reduction
    # of unassigned flow.
    #
    # By updating G_inverted, with the residual capacity, I can keep using the
    # shortest path, until the capacity is zero, whereby I remove the links
    # When the shortest path method returns 'No path' or when unassigned flow
    # is zero, I exit the algorithm.
    #
    # Even on small graphs, this method is very efficient, despite the overhead
    # of using shortest path. For very large graphs, this method outperforms
    # all other algorithms by orders of magnitude.
    # -----------------------------------------------------------------------

    edges = [(n1, n2, 1 / d) for n1, n2, d in graph.edges() if d > 0]
    inverted_graph = Graph(from_list=edges)  # create G_inverted.
    capacity_graph = Graph()  # Create structure to record capacity left.
    flow_graph = Graph()  # Create structure to record flows.

    while unassigned_flow:
        # 1. find the best path
        d, path = shortest_path(inverted_graph, start, end)
        if d == float('inf'):  # then there is no path, and we must exit.
            return total_flow, flow_graph
        # else: use the path and lookup the actual flow from the capacity graph.

        path_flow = min([min(d, capacity_graph.edge(s, e, default=float('inf')))
                         for s, e, d in graph.edges(path=path)])

        # 2. update the unassigned flow.
        unassigned_flow -= path_flow
        total_flow += path_flow

        # 3. record the flows and update the inverted graph, so that it is
        #    ready for the next iteration.
        edges = graph.edges(path)
        for n1, n2, d in edges:

            # 3.a. recording:
            v = flow_graph.edge(n1, n2, default=None)
            if v is None:
                flow_graph.add_edge(n1, n2, path_flow)
                c = graph.edge(n1, n2) - path_flow
            else:
                flow_graph.add_edge(n1, n2, value=v + path_flow)
                c = graph.edge(n1, n2) - (v + path_flow)
            capacity_graph.add_edge(n1, n2, c)

            # 3.b. updating:
            # if there is capacity left: update with new 1/capacity
            # else: remove node, as we can't do 1/zero.
            if c > 0:
                inverted_graph.add_edge(n1, n2, 1 / c)
            else:
                inverted_graph.del_edge(n1, n2)
    return total_flow, flow_graph


def maximum_flow_min_cut(graph, start, end):
    """
    Finds the edges in the maximum flow min cut.
    :param graph: Graph
    :param start: start
    :param end: end
    :return: list of edges
    """
    flow, mfg = maximum_flow(graph, start, end)
    if flow == 0:
        return []

    working_graph = Graph(from_list=mfg.to_list())

    min_cut = []
    for n1 in mfg.breadth_first_walk(start, end):
        n2s = mfg.nodes(from_node=n1)
        for n2 in n2s:
            if graph.edge(n1, n2) - mfg.edge(n1, n2) == 0:
                working_graph.del_edge(n1, n2)
                min_cut.append((n1, n2))

    min_cut_nodes = set(working_graph.nodes(out_degree=0))
    min_cut_nodes.remove(end)
    min_cut = [(n1, n2) for (n1, n2) in min_cut if n1 in min_cut_nodes]
    return min_cut


def minimum_cost_flow_using_successive_shortest_path(costs, inventory, capacity=None):
    """
    Calculates the minimum cost flow solution using successive shortest path.
    :param costs: Graph with `cost per unit` as edge
    :param inventory: dict {node: stock, ...}
        stock < 0 is demand
        stock > 0 is supply
    :param capacity: None or Graph with `capacity` as edge.
        if capacity is None, capacity is assumed to be float('inf')
    :return: total costs, flow graph
    """
    assert isinstance(costs, Graph)
    assert isinstance(inventory, dict)

    if not all(d >= 0 for s, e, d in costs.edges()):
        raise ValueError("negative costs?")
    if not isinstance(inventory, dict):
        raise TypeError("inventory is expected as dict")
    if not all(isinstance(v, (float, int)) for v in inventory.values()):
        raise ValueError("not all stock is numeric.")

    if capacity is None:
        capacity = Graph(from_list=[(s, e, float('inf')) for s, e, d in costs.edges()])
    else:
        if not isinstance(capacity, Graph):
            raise TypeError("Expected capacity as a Graph")
        if any(d < 0 for s, e, d in capacity.edges()):
            nn = [(s, e) for s, e, d in capacity.edges() if d < 0]
            raise ValueError(f"negative capacity on edges: {nn}")
        if {(s, e) for s, e, d in costs.edges()} != {(s, e) for s, e, d in capacity.edges()}:
            raise ValueError("cost and capacity have different links")

    # successive shortest path algorithm begins ...
    # ------------------------------------------------
    paths = costs.copy()  # initialise a copy of the cost graph so edges that
    # have exhausted capacities can be removed.
    flows = Graph()  # initialise F as copy with zero flow
    capacities = Graph()  # initialise C as a copy of capacity, so used capacity
    # can be removed.
    balance = [(v, k) for k, v in inventory.items() if v != 0]  # list with excess/demand, node id
    balance.sort()

    distances = paths.all_pairs_shortest_paths()

    while balance:  # while determine excess / imbalances:
        D, Dn = balance[0]  # pick node Dn where the demand D is greatest
        if D > 0:
            break  # only supplies left.
        balance = balance[1:]  # remove selection.

        supply_sites = [(distances[En][Dn], E, En) for E, En in balance if E > 0]
        if not supply_sites:
            break  # supply exhausted.
        supply_sites.sort()
        dist, E, En = supply_sites[0]  # pick nearest node En with excess E.
        balance.remove((E, En))  # maintain balance by removing the node.

        if E < 0:
            break  # no supplies left.
        if dist == float('inf'):
            raise Exception("bad logic: Case not checked for.")

        cost, path = paths.shortest_path(En, Dn)  # compute shortest path P from E to a node in demand D.

        # determine the capacity limit C on P:
        capacity_limit = min(capacities.edge(s, e, default=capacity.edge(s, e)) for s, e in zip(path[:-1], path[1:]))

        # determine L units to be transferred as min(demand @ D and the limit C)
        L = min(E, abs(D), capacity_limit)
        for s, e in zip(path[:-1], path[1:]):
            flows.add_edge(s, e, L + flows.edge(s, e, default=0))  # update F.
            new_capacity = capacities.edge(s, e, default=capacity.edge(s, e)) - L
            capacities.add_edge(s, e, new_capacity)  # update C

            if new_capacity == 0:  # remove the edge from potential solutions.
                paths.del_edge(s, e)
                distances = paths.all_pairs_shortest_paths()

        # maintain balance, in case there is excess or demand left.
        if E - L > 0:
            insort(balance, (E - L, En))
        if D + L < 0:
            insort(balance, (D + L, Dn))

    total_cost = sum(d * costs.edge(s, e) for s, e, d in flows.edges())
    return total_cost, flows


def tsp_branch_and_bound(graph):
    """
    Solve the traveling salesman's problem for the graph.
    :param graph: instance of class Graph
    :return: tour_length, path

    solution quality 100%
    """
    assert isinstance(graph, Graph)

    def lower_bound(graph, nodes):
        """ Calculates the lower bound of distances for given nodes. """
        L = []
        edges = set()
        for n in nodes:

            L2 = [(d, e) for s, e, d in graph.edges(from_node=n) if e in nodes - {n}]
            if not L2:
                continue
            L2.sort()

            for d, n2 in L2:
                if (n2, n) in edges:  # Solution is not valid as it creates a loop.
                    continue
                else:
                    edges.add((n, n2))  # remember!
                    L.append((n, n2, d))
                    break

        return L

    global_lower_bound = sum(d for n, n2, d in lower_bound(graph, set(graph.nodes())))

    q = []
    all_nodes = set(graph.nodes())

    # create initial tree.
    start = graph.nodes()[0]
    for start, end, distance in graph.edges(from_node=start):
        lb = lower_bound(graph, all_nodes - {start})
        dist = sum(d for s, e, d in lb)
        insort(q,
               (distance + dist,  # lower bound of distance.
                -2,  # number of nodes in tour.
                (start, end))  # locations visited.
               )

    hit, switch, q2 = 0, True, []
    while q:  # walk the tree.
        d, _, tour = q.pop(0)
        tour_set = set(tour)

        if tour_set == all_nodes:
            if hit < len(all_nodes):  # to overcome premature exit.
                hit += 1
                insort(q2, (d, tour))
                continue
            else:
                d, tour = q2.pop(0)
                assert d >= global_lower_bound, "Solution not possible."
                return d, list(tour[:-1])

        remaining_nodes = all_nodes - tour_set

        for n2 in remaining_nodes:

            new_tour = tour + (n2, )

            lb_set = remaining_nodes - {n2}
            if len(lb_set) > 1:
                lb_dists = lower_bound(graph, lb_set)
                lb = sum(d for n, n2, d in lb_dists)
                new_lb = graph.distance_from_path(new_tour) + lb
            elif len(lb_set) == 1:
                last_node = lb_set.pop()
                new_tour = new_tour + (last_node, tour[0])
                new_lb = graph.distance_from_path(new_tour)
            else:
                raise Exception("bad logic!")

            insort(q, (new_lb, -len(new_tour), new_tour))

    return float('inf'), []  # <-- exit path if not solvable.


def tsp_greedy(graph):
    """
    Solves the traveling salesman's problem for the graph.

    Runtime approximation: seconds = 10**(-5) * (nodes)**2.31
    Solution quality: Range 98.1% - 100% optimal.

    :param graph: instance of class Graph
    :return: tour_length, path
    """

    def shortest_links_first(graph):
        """ returns a list of (distance, node1, node2) with shortest on top."""
        c = combinations(graph.nodes(), 2)
        distances = [(graph.edge(a, b), a, b) for a, b in c if graph.edge(a, b)]
        distances.sort()
        return distances

    def join_endpoints(endpoints, a, b):
        """ Join segments [...,a] + [b,...] into one segment. Maintain `endpoints`.
        :param endpoints:
        :param a: node
        :param b: node
        :return:
        """
        a_seg, b_seg = endpoints[a], endpoints[b]
        if a_seg[-1] is not a:
            a_seg.reverse()
        if b_seg[0] is not b:
            b_seg.reverse()
        a_seg += b_seg
        del endpoints[a]
        del endpoints[b]
        endpoints[a_seg[0]] = endpoints[a_seg[-1]] = a_seg
        return a_seg

    def tsp_tour_length(graph, tour):
        """ The TSP tour length WITH return to the starting point."""
        return sum(graph.edge(tour[i - 1], tour[i]) for i in range(len(tour)))
        # note to above: If there's an error it's probably because the graph isn't
        # fully connected.

    def improve_tour(graph, tour):
        assert tour, "no tour to improve?"
        n = len(tour)

        # Return (i, j) pairs denoting tour[i:j] sub_segments of a tour of length N.
        sub_segments = [(i, i + length) for length in reversed(range(2, n)) for i in reversed(range(n - length + 1))]

        while True:
            improvements = {reverse_segment_if_improvement(graph, tour, i, j) for (i, j) in sub_segments}
            if improvements == {None} or len(improvements) == 0:
                return tour

    def reverse_segment_if_improvement(graph, tour, i, j):
        """If reversing tour[i:j] would make the tour shorter, then do it."""
        # Given tour [...A,B...C,D...], consider reversing B...C to get [...A,C...B,D...]
        a, b, c, d = tour[i - 1], tour[i], tour[j - 1], tour[j % len(tour)]
        # are old links (ab + cd) longer than new ones (ac + bd)? if so, reverse segment.
        A, B, C, D = graph.edge(a, b), graph.edge(c, d), graph.edge(a, c), graph.edge(b, d)
        # if all are not None and improvement is shorter than previous ...
        if all((A, B, C, D)) and A + B > C + D:
            tour[i:j] = reversed(tour[i:j])  # ..retain the solution.
            return True

    # The core TSP solver
    # -----------------------
    # 1. create a path using greedy algorithm (picks nearest peer)
    new_segment = []
    endpoints = {n: [n] for n in graph.nodes()}
    L = shortest_links_first(graph)
    for _, a, b in L:
        if a in endpoints and b in endpoints and endpoints[a] != endpoints[b]:
            new_segment = join_endpoints(endpoints, a, b)
            if len(new_segment) == len(graph.nodes()):
                break  # return new_segment
    assert len(new_segment) == len(graph.nodes()), "there's an unconnected component."
    first_tour = new_segment[:]
    first_path_length = tsp_tour_length(graph, first_tour)

    # 2. run improvement on the created path.
    improved_tour = improve_tour(graph, new_segment)
    assert set(graph.nodes()) == set(improved_tour)

    second_path_length = tsp_tour_length(graph, improved_tour)

    assert first_path_length >= second_path_length, "first path was better than improved tour?! {} {}".format(
        first_path_length, second_path_length
    )

    return second_path_length, improved_tour


def subgraph(graph, nodes):
    """ Creates a subgraph as a copy from the graph
    :param graph: class Graph
    :param nodes: set or list of nodes
    :return: new instance of Graph.
    """
    assert isinstance(nodes, (set, list))
    node_set = set(nodes)
    G = object.__new__(graph.__class__)
    assert isinstance(G, BasicGraph)
    G.__init__()
    for n1 in nodes:
        obj = graph.node(n1)
        G.add_node(n1, obj)
        for n2 in graph.nodes(from_node=n1):
            if n2 in node_set:
                G.add_edge(n1, n2, graph.edge(n1, n2))
    return G


def is_subgraph(graph1, graph2):
    """
    Checks if graph1 is subgraph in graph2
    :param graph1: instance of Graph
    :param graph2: instance of Graph
    :return: boolean
    """
    assert isinstance(graph1, BasicGraph)
    assert isinstance(graph2, BasicGraph)
    if not set(graph1.nodes()).issubset(set(graph2.nodes())):
        return False
    if not set(graph1.edges()).issubset(set(graph2.edges())):
        return False
    return True


def is_partite(graph, n):
    """ Checks if graph is n-partite
    :param graph: class Graph
    :param n: int, number of partitions.
    :return: boolean and partitions as dict[colour] = set(nodes) or None.
    """
    assert isinstance(graph, BasicGraph)
    assert isinstance(n, int)
    colours_and_nodes = {i: set() for i in range(n)}
    nodes_and_colours = {}
    n1 = set(graph.nodes()).pop()
    q = [n1]
    visited = set()
    colour = 0
    while q:
        n1 = q.pop()
        visited.add(n1)

        if n1 in nodes_and_colours:
            colour = nodes_and_colours[n1]
        else:
            colours_and_nodes[colour].add(n1)
            nodes_and_colours[n1] = colour

        next_colour = (colour + 1) % n
        neighbours = graph.nodes(from_node=n1) + graph.nodes(to_node=n1)
        for n2 in neighbours:
            if n2 in nodes_and_colours:
                if nodes_and_colours[n2] == colour:
                    return False, None
                # else:  pass  # it already has a colour and there is no conflict.
            else:  # if n2 not in nodes_and_colours:
                colours_and_nodes[next_colour].add(n2)
                nodes_and_colours[n2] = next_colour
                continue
            if n2 not in visited:
                q.append(n2)

    return True, colours_and_nodes


def has_cycles(graph):
    """ Checks if graph has a cycle
    :param graph: instance of class Graph.
    :return: bool
    """
    for n1, n2, d in graph.edges():
        if n1 == n2:
            return True
        if graph.is_connected(n2, n1):
            return True
    return False


def components(graph):
    """ Determines the components of the graph
    :param graph: instance of class Graph
    :return: list of sets of nodes. Each set is a component.
    """
    assert isinstance(graph, BasicGraph)
    nodes = set(graph.nodes())
    sets_of_components = []
    while nodes:
        new_component = set()
        sets_of_components.append(new_component)
        n = nodes.pop()  # select random node
        new_component.add(n)  # add it to the new component.

        new_nodes = set(graph.nodes(from_node=n))
        new_nodes.update(set(graph.nodes(to_node=n)))
        while new_nodes:
            n = new_nodes.pop()
            new_component.add(n)
            new_nodes.update(set(n for n in graph.nodes(from_node=n) if n not in new_component))
            new_nodes.update(set(n for n in graph.nodes(to_node=n) if n not in new_component))
        nodes = nodes - new_component
    return sets_of_components


def network_size(graph, n1, degrees_of_separation=None):
    """ Determines the nodes within the range given by
    a degree of separation
    :param graph: Graph
    :param n1: start node
    :param degrees_of_separation: integer
    :return: set of nodes within given range
    """
    assert isinstance(graph, BasicGraph)
    assert n1 in graph.nodes()
    if degrees_of_separation is not None:
        assert isinstance(degrees_of_separation, int)

    network = {n1}
    q = set(graph.nodes(from_node=n1))

    scan_depth = 1
    while True:
        if not q:  # then there's no network.
            break

        if degrees_of_separation is not None:
            if scan_depth > degrees_of_separation:
                break

        new_q = set()
        for peer in q:
            if peer in network:
                continue
            else:
                network.add(peer)
                new_peers = set(graph.nodes(from_node=peer)) - network
                new_q.update(new_peers)
        q = new_q
        scan_depth += 1
    return network


def phase_lines(graph):
    """ Determines the phase lines of a directed graph.
    :param graph: Graph
    :return: dictionary with node id : phase in cut.
    """
    phases = {n: 0 for n in graph.nodes()}
    sinks = {n: set() for n in phases}  # sinks[e] = {s1,s2}
    edges = {n: set() for n in phases}
    for s, e, d in graph.edges():
        sinks[e].add(s)
        edges[s].add(e)

    cache = {}

    level = 0
    while sinks:
        sources = [e for e in sinks if not sinks[e]]  # these nodes have in_degree=0
        if not sources:
            raise AttributeError("The graph does not have any sinks.")
        for s in sources:
            phases[s] = level  # let's update the phase value
            del sinks[s]  # and let's remove their sink entry.
            # and remove their set item from the sinks dict
            for e in edges[s]:
                if e not in sinks:
                    continue
                sinks[e].discard(s)
                # but also check if their descendants are loops.
                for s2 in list(sinks[e]):

                    con = cache.get((e, s2))  # check if the edge has been seen before.
                    if con is None:
                        con = graph.is_connected(e, s2)  # if not seen before, search...
                        cache[(e, s2)] = con

                    if con:
                        sinks[e].discard(s2)
        level += 1

    return phases


def sources(graph, n):
    """ Determines the set of sources of node 'n' in a DAG.
    :param graph: Graph
    :param n: node for which the sources are sought.
    :return: set of nodes
    """
    nodes = {n}
    q = [n]
    while q:
        new = q.pop(0)
        for src in graph.nodes(to_node=new):
            if src not in nodes:
                nodes.add(src)
            if src not in q:
                q.append(src)
    nodes.remove(n)
    return nodes


def same_path(path1, path2):
    """ Compares two paths to verify whether they're the same despite being offset.
    Very useful when comparing results from TSP as solutions may be rotations of
    the same path.
    :param path1: list of nodes.
    :param path2: list of nodes.
    :return: boolean.
    """
    if path1 is path2:  # use id system to avoid work.
        return True
    if len(path1) != len(path2) or set(path1) != set(path2):
        return False

    starts = (ix for ix, n2 in enumerate(path2) if path1[0] == n2)
    return any(all(a == b for a, b in zip(path1, chain(path2[start:], path2[:start]))) for start in starts)


def adjacency_matrix(graph):
    """Converts directed graph to an adjacency matrix.
    :param graph:
    :return: dictionary

    The distance from a node to itself is 0 and distance from a node to
    an unconnected node is defined to be infinite. This does not mean that there
    is no path from a node to another via other nodes.

    Example:
        g = Graph(from_dict=
            {1: {2: 3, 3: 8, 5: -4},
             2: {4: 1, 5: 7},
             3: {2: 4},
             4: {1: 2, 3: -5},
             5: {4: 6}})

        adjacency_matrix(g)
        {1: {1: 0, 2: 3, 3: 8, 4: inf, 5: -4},
         2: {1: inf, 2: 0, 3: inf, 4: 1, 5: 7},
         3: {1: inf, 2: 4, 3: 0, 4: inf, 5: inf},
         4: {1: 2, 2: inf, 3: -5, 4: 0, 5: inf},
         5: {1: inf, 2: inf, 3: inf, 4: 6, 5: 0}}
    """
    assert isinstance(graph, BasicGraph)
    return {v1: {v2: 0 if v1 == v2 else graph.edge(v1, v2, default=float('inf'))
                 for v2 in graph.nodes()}
            for v1 in graph.nodes()}


def all_pairs_shortest_paths(graph):
    """Find the cost of the shortest path between every pair of vertices in a
    weighted graph. Uses the Floyd-Warshall algorithm.

    Example:
        inf = float('inf')
        g = Graph(from_dict=(
            {0: {0: 0,   1: 1,   2: 4},
             1: {0: inf, 1: 0,   2: 2},
             2: {0: inf, 1: inf, 2: 0}})

        fw(g)
        {0: {0: 0,   1: 1,   2: 3},
        1: {0: inf, 1: 0,   2: 2},
        2: {0: inf, 1: inf, 2: 0}}

        h = {1: {2: 3, 3: 8, 5: -4},
             2: {4: 1, 5: 7},
             3: {2: 4},
             4: {1: 2, 3: -5},
             5: {4: 6}}

        fw(adj(h)) #
            {1: {1: 0, 2:  1, 3: -3, 4: 2, 5: -4},
             2: {1: 3, 2:  0, 3: -4, 4: 1, 5: -1},
             3: {1: 7, 2:  4, 3:  0, 4: 5, 5:  3},
             4: {1: 2, 2: -1, 3: -5, 4: 0, 5: -2},
             5: {1: 8, 2:  5, 3:  1, 4: 6, 5:  0}}
    """
    g = graph.adjacency_matrix()
    assert isinstance(g, dict)
    vertices = g.keys()

    for v2 in vertices:
        g = {v1: {v3: min(g[v1][v3], g[v1][v2] + g[v2][v3])
                  for v3 in vertices}
             for v1 in vertices}
    return g


def minsum(graph):
    """ finds the mode(s) that have the smallest sum of distance to all other nodes. """
    assert isinstance(graph, Graph)
    adj_mat = graph.all_pairs_shortest_paths()
    for n in adj_mat:
        adj_mat[n] = sum(adj_mat[n].values())
    smallest = min(adj_mat.values())
    return [k for k, v in adj_mat.items() if v == smallest]


def minmax(graph):
    """ finds the node(s) with shortest distance to all other nodes. """
    assert isinstance(graph, Graph)
    adj_mat = graph.all_pairs_shortest_paths()
    for n in adj_mat:
        adj_mat[n] = max(adj_mat[n].values())
    smallest = min(adj_mat.values())
    return [k for k, v in adj_mat.items() if v == smallest]


def shortest_tree_all_pairs(graph):
    """
       'minimize the longest distance between any pair'

    Note: This algorithm is not shortest path as it jumps
    to a new branch when it has exhausted a branch in the tree.
    :return: path
    """
    g = all_pairs_shortest_paths(graph)
    assert isinstance(g, dict)

    distance = float('inf')
    best_starting_point = -1
    # create shortest path gantt diagram.
    for start_node in g.keys():
        if start_node in g:
            dist = sum(v for k, v in g[start_node].items())
            if dist < distance:
                best_starting_point = start_node
            # else: skip the node as it's isolated.
    g2 = g[best_starting_point]  # {1: 0, 2: 1, 3: 2, 4: 3}

    inv_g2 = {}
    for k, v in g2.items():
        if v not in inv_g2:
            inv_g2[v] = set()
        inv_g2[v].add(k)

    all_nodes = set(g.keys())
    del g
    path = []
    while all_nodes and inv_g2.keys():
        v_nearest = min(inv_g2.keys())
        for v in inv_g2[v_nearest]:
            all_nodes.remove(v)
            path.append(v)
        del inv_g2[v_nearest]
    return path


def has_path(graph, path):
    """ checks if path exists is graph
    :param graph: instance of Graph
    :param path: list of nodes
    :return: boolean
    """
    assert isinstance(graph, BasicGraph)
    assert isinstance(path, (list, tuple))
    v1 = path[0]
    for v2 in path[1:]:
        if graph.edge(v1, v2) is None:
            return False
        else:
            v1 = v2
    return True


def all_simple_paths(graph, start, end):
    """
    finds all simple (non-looping) paths from start to end
    :param start: node
    :param end: node
    :return: list of paths
    """
    if start == end:
        raise ValueError("start is end")
    if not graph.is_connected(start, end):
        return []

    paths = []
    q = [(start,)]
    while q:
        path = q.pop(0)
        for s, e, d in graph.edges(from_node=path[0]):
            if e in path:
                continue
            new_path = (e,) + path
            if e == end:
                paths.append(new_path)
            else:
                q.append(new_path)
    return [list(reversed(p)) for p in paths]


def all_paths(graph, start, end):
    """ finds all paths from start to end by traversing each fork once only.
    :param graph: instance of Graph
    :param start: node
    :param end: node
    :return: list of paths unique from start to end.
    """
    cache = {}

    if start == end:
        raise ValueError("start is end")
    if not graph.is_connected(start, end):
        return []
    paths = [(start,)]
    q = [start]
    skip_list = set()
    while q:
        n1 = q.pop(0)
        if n1 == end:
            continue

        n2s = graph.nodes(from_node=n1)
        new_paths = [p for p in paths if p[-1] == n1]
        for n2 in n2s:
            if n2 in skip_list:
                continue
            n3s = graph.nodes(from_node=n2)

            con = cache.get((n2, n1))
            if con is None:
                con = graph.is_connected(n2, n1)
                cache[(n2, n1)] = con

            if len(n3s) > 1 and con:
                # it's a fork and it's a part of a loop!
                # is the sequence n2,n3 already in the path?
                for n3 in n3s:
                    for path in new_paths:
                        a = [n2, n3]
                        if any(all(path[i+j] == a[j] for j in range(len(a))) for i in range(len(path))):
                            skip_list.add(n3)

            for path in new_paths:
                if path in paths:
                    paths.remove(path)

                new_path = path + (n2,)
                if new_path not in paths:
                    paths.append(new_path)

            if n2 not in q:
                q.append(n2)

    paths = [list(p) for p in paths if p[-1] == end]
    return paths


def degree_of_separation(graph, n1, n2):
    """ Calculates the degree of separation between 2 nodes."""
    assert n1 in graph.nodes()
    p = breadth_first_search(graph, n1, n2)
    return len(p)-1


def loop(graph, start, mid, end=None):
    """ Returns a loop passing through a defined mid-point and returning via a different set of nodes to the outward
        journey. If end is None we return to the start position. """
    _, p = graph.shortest_path(start, mid)
    g2 = graph.copy()
    if end is not None:
        for n in p[:-1]:
            g2.del_node(n)
        _, p2 = g2.shortest_path(mid, end)
    else:
        for n in p[1:-1]:
            g2.del_node(n)
        _, p2 = g2.shortest_path(mid, start)
    lp = p + p2[1:]
    return lp


def avoids(graph, start, end, obstacles):
    """ Returns a path through the graph avoiding the obstacles"""
    g2 = graph.copy()
    for each in obstacles:
        assert isinstance(each, int)
    for o in obstacles:
        g2.del_node(o)
    _, p = g2.shortest_path(start, end)
    return p


class ScanThread(object):
    __slots__ = ['cost', 'n1', 'path']

    """ search thread for bidirectional search """
    def __init__(self, cost, n1, path=()):
        assert isinstance(path, tuple)
        self.cost = cost
        self.n1 = n1
        self.path = path

    def __lt__(self, other):
        return self.cost < other.cost

    def __str__(self):
        return f"{self.cost}:{self.path}"


class SPLength(object):
    def __init__(self):
        self.value = float('inf')


class BiDirectionalSearch(object):
    """ data structure for organizing bidirectional search """
    forward = True
    backward = False

    def __str__(self):
        if self.forward == self.direction:
            return "forward scan"
        return "backward scan"

    def __init__(self, graph, start, direction=True):
        """
        :param graph: class Graph.
        :param start: first node in the search.
        """
        self.q = []
        self.q.append(ScanThread(cost=0, n1=start))
        self.graph = graph
        self.boundary = set()  # visited.
        self.mins = {start: 0}
        self.paths = {start: ()}
        self.direction = direction
        self.sp = ()
        self.sp_length = float('inf')

    def update(self, sp, sp_length):
        if sp_length > self.sp_length:
            raise ValueError("Bad logic!")
        self.sp = sp
        self.sp_length = sp_length

    def search(self, other):
        assert isinstance(other, BiDirectionalSearch)
        if not self.q:
            return

        sp, sp_length = self.sp, self.sp_length

        st = self.q.pop(0)
        assert isinstance(st, ScanThread)
        if st.cost > self.sp_length:
            return

        self.boundary.add(st.n1)

        if st.n1 in other.boundary:  # if there's an intercept between the two searches ...
            if st.cost + other.mins[st.n1] < self.sp_length:
                sp_length = st.cost + other.mins[st.n1]
                if self.direction == self.forward:
                    sp = tuple(reversed(st.path)) + (st.n1,) + other.paths[st.n1]
                else:  # direction == backward:
                    sp = tuple(reversed(other.paths[st.n1])) + (st.n1,) + st.path

                self.q = [a for a in self.q if a.cost < sp_length]

        if self.direction == self.forward:
            edges = sorted((d, e) for s, e, d in self.graph.edges(from_node=st.n1))
        else:
            edges = sorted((d, s) for s, e, d in self.graph.edges(to_node=st.n1))

        for dist, n2 in edges:
            n2_dist = st.cost + dist
            if n2_dist > self.sp_length:  # no point pursuing as the solution is worse.
                continue
            if n2 in other.mins and n2_dist + other.mins[n2] > self.sp_length:  # already longer than lower bound.
                continue

            # at this point we can't dismiss that n2 will lead to a better solution, so we retain it.
            prev = self.mins.get(n2, None)
            if prev is None or n2_dist < prev:
                self.mins[n2] = n2_dist
                path = (st.n1,) + st.path
                self.paths[n2] = path
                insort(self.q, ScanThread(n2_dist, n2, path))

        self.update(sp, sp_length)
        other.update(sp, sp_length)


def shortest_path_bidirectional(graph, start, end, reverse_graph=None):
    """ Bidirectional search using lower bound.
    :param graph: Graph
    :param start: start node
    :param end: end node
    :param reverse_graph: an existing reverse graph of graph
    :return: shortest path

    In Section 3.4.6 of Artificial Intelligence: A Modern Approach, Russel and
    Norvig write:

    Bidirectional search is implemented by replacing the goal test with a check
    to see whether the frontiers of the two searches intersect; if they do,
    a solution has been found. It is important to realize that the first solution
    found may not be optimal, even if the two searches are both breadth-first;
    some additional search is required to make sure there isn't a shortcut
    across the gap.

    To overcome this limit for weighted graphs, I've added a lower bound, so
    that when the two searches intersect, the lower bound is updated and the
    lower bound path is stored. In subsequent searches any path shorter than
    the lower bound, leads to an update of the lower bound and shortest path.
    The algorithm stops when all nodes on the frontier exceed the lower bound.

    ----------------

    The algorithms works as follows:

    Lower bound = float('infinite')
    shortest path = None

    Two queues (forward scan and backward scan) are initiated with respectively
    the start and end node as starting point for each scan.

    while there are nodes in the forward- and backward-scan queues:
        1. select direction from (forward, backward) in alternations.
        2. pop the top item from the queue of the direction.
           (The top item contains the node N that is nearest the starting point for the scan)
        3. Add the node N to the scan-directions frontier.
        4. If the node N is in the other directions frontier:
            the path distance from the directions _start_ to the _end_ via
            the point of intersection (N), is compared with the lower bound.

            If the path distance is less than the lower bound:
            *lower bound* is updated with path distance, and,
            the *shortest path* is recorded.

        5. for each node N2 (to N if backward, from N if forward):
            the distance D is accumulated

            if D > lower bound, the node N2 is ignored.

            if N2 is within the other directions frontier and D + D.other > lower bound, the node N2 is ignored.

            otherwise:
                the path P recorded
                and N2, D and P are added to the directions scan queue

    The algorithm terminates when the scan queues are exhausted.
    ----------------

    Given that:
    - `c` is the connectivity of the nodes in the graph,
    - `R` is the length of the path,
    the explored solution landscape can be estimated as:

    A = c * (R**2), for single source shortest path
    A = c * 2 * (1/2 * R) **2, for bidirectional shortest path
    """
    assert isinstance(graph, Graph)
    forward = BiDirectionalSearch(graph, start=start, direction=BiDirectionalSearch.forward)
    backward = BiDirectionalSearch(graph, start=end, direction=BiDirectionalSearch.backward)

    while any((forward.q, backward.q)):
        forward.search(other=backward)
        backward.search(other=forward)

    return forward.sp_length, list(forward.sp)


class ShortestPathCache(object):
    """
    Data structure optimised for repeated calls to shortest path.
    Used by shortest path when using keyword `memoize=True`
    """
    def __init__(self, graph):
        if not isinstance(graph, Graph):
            raise TypeError(f"expected type Graph, not {type(graph)}")
        self.graph = graph
        self.cache = {}

    def _update_cache(self, path):
        """ private method for updating the cache for future lookups.
        :param path: tuple of nodes

        Given a shortest path, all steps along the shortest path,
        also constitute the shortest path between each pair of steps.
        """
        assert isinstance(path, (list, tuple))
        b = len(path)
        if b < 2:
            return
        if b == 2:
            dist = self.graph.distance_from_path(path)
            self.cache[(path[0], path[-1])] = (dist, tuple(path))

        for a, _ in enumerate(path):
            section = tuple(path[a:b - a])
            if len(section) < 3:
                break
            dist = self.graph.distance_from_path(section)
            self.cache[(section[0], section[-1])] = (dist, section)

        for ix, start in enumerate(path[1:-1]):
            section = tuple(path[ix:])
            dist = self.graph.distance_from_path(section)
            self.cache[(section[0], section[-1])] = (dist, section)

    def shortest_path(self, start, end):
        """ Shortest path method that utilizes caching and bidirectional search """
        d = 0 if start == end else None
        p = ()

        if d is None:  # is it cached?
            d, p = self.cache.get((start, end), (None, None))

        if d is None:  # search for it.
            _, p = shortest_path_bidirectional(self.graph, start, end)
            self._update_cache(p)
            d, p = self.cache[(start, end)]
        return d, list(p)


class Graph(BasicGraph):
    """
    Graph is the base graph that all methods use.

    For methods, please see the documentation on the
    individual functions, by importing them separately.

    """

    def __init__(self, from_dict=None, from_list=None):
        super().__init__(from_dict=from_dict, from_list=from_list)
        self._cache = None

    def copy(self):
        g = Graph()
        for n in self._nodes:
            g.add_node(n, obj=self._nodes[n])
        for s, e, d in self.edges():
            g.add_edge(s, e, d)
        return g

    def shortest_path(self, start, end, memoize=False):
        """
        :param start: start node
        :param end: end node
        :param memoize: boolean (stores paths in a cache for faster repeated lookup)
        :return: distance, path as list
        """
        if not memoize:
            return shortest_path(graph=self, start=start, end=end)

        if self._cache is None:
            self._cache = ShortestPathCache(graph=self)
        return self._cache.shortest_path(start, end)

    def shortest_path_bidirectional(self, start, end):
        """
        :param start: start node
        :param end: end node
        :return: distance, path as list
        """
        return shortest_path_bidirectional(self, start, end)

    def breadth_first_search(self, start, end):
        """ Determines the path with fewest nodes.
        :param start: start node
        :param end: end nodes
        :return: nodes, path as list
        """
        return breadth_first_search(graph=self, start=start, end=end)

    def breadth_first_walk(self, start, end=None, reversed_walk=False):
        """
        :param start: start node
        :param end: end node
        :param reversed_walk: if True, the BFS walk is backwards.
        :return: generator for breadth-first walk
        """
        return breadth_first_walk(graph=self, start=start, end=end, reversed_walk=reversed_walk)

    def depth_first_search(self, start, end):
        """
        Finds a path from start to end using DFS.
        :param start: start node
        :param end: end node
        :return: path
        """
        return depth_first_search(graph=self, start=start, end=end)

    def depth_scan(self, start, criteria):
        """
        traverses the descendants of node `start` using callable `criteria` to determine
        whether to terminate search along each branch in `graph`.

        :param start: start node
        :param criteria: function to terminate scan along a branch must return bool
        :return: set of nodes
        """
        return depth_scan(graph=self, start=start, criteria=criteria)

    def distance_from_path(self, path):
        """
        :param path: list of nodes
        :return: distance along the path.
        """
        return distance(graph=self, path=path)

    def maximum_flow(self, start, end):
        """ Determines the maximum flow of the graph between
        start and end.
        :param start: node (source)
        :param end: node (sink)
        :return: flow, graph of flow.
        """
        return maximum_flow(self, start, end)

    def maximum_flow_min_cut(self, start, end):
        """
        Finds the edges in the maximum flow min cut.
        :param start: start
        :param end: end
        :return: list of edges
        """
        return maximum_flow_min_cut(self, start, end)

    def minimum_cost_flow(self, inventory, capacity=None):
        """
        :param self: Graph with `cost per unit` as edge
        :param inventory: dict {node: stock, ...}
            stock < 0 is demand
            stock > 0 is supply
        :param capacity: None or Graph with `capacity` as edge.
        :return: total costs, graph of flows in solution.
        """
        return minimum_cost_flow_using_successive_shortest_path(self, inventory, capacity)

    def solve_tsp(self, method='greedy'):
        """ solves the traveling salesman problem for the graph
        (finds the shortest path through all nodes)

        :param method: str: 'greedy'

        options:
            'greedy' see tsp_greedy
            'bnb' see tsp_branch_and_bound

        :return: tour length (path+return to starting point),
                 path travelled.
        """
        methods = {
            'greedy': tsp_greedy,
            'bnb': tsp_branch_and_bound
        }
        solver = methods.get(method, 'greedy')
        return solver(self)

    def subgraph_from_nodes(self, nodes):
        """
        constructs a copy of the graph containing only the
        listed nodes (and their links)
        :param nodes: list of nodes
        :return: class Graph
        """
        return subgraph(graph=self, nodes=nodes)

    def is_subgraph(self, other):
        """ Checks if self is a subgraph in other.
        :param other: instance of Graph
        :return: boolean
        """
        return is_subgraph(self, other)

    def is_partite(self, n=2):
        """ Checks if self is n-partite
        :param n: int the number of partitions.
        :return: tuple: boolean, partitions as dict
                        (or None if graph isn't n-partite)
        """
        return is_partite(self, n)

    def has_cycles(self):
        """ Checks if the graph has a cycle
        :return: bool
        """
        return has_cycles(graph=self)

    def components(self):
        """ Determines the number of components
        :return: list of sets of nodes. Each set is a component.
        """
        return components(graph=self)

    def network_size(self, n1, degrees_of_separation=None):
        """ Determines the nodes within the range given by
        a degree of separation
        :param n1: start node
        :param degrees_of_separation: integer
        :return: set of nodes within given range
        """
        return network_size(self, n1, degrees_of_separation)

    def phase_lines(self):
        """ Determines the phase lines (cuts) of the graph
        :returns: dictionary with phase: nodes in phase
        """
        return phase_lines(self)

    def sources(self, n):
        """ Determines the DAG sources of node n """
        return sources(graph=self, n=n)

    @staticmethod
    def same_path(p1, p2):
        """ compares two paths to determine if they're the same, despite
        being in different order.

        :param p1: list of nodes
        :param p2: list of nodes
        :return: boolean
        """
        return same_path(p1, p2)

    def adjacency_matrix(self):
        """
        Converts directed graph to an adjacency matrix.
        Note: The distance from a node to itself is 0 and distance from a node to
        an unconnected node is defined to be infinite. This does not mean that there
        is no path from a node to another via other nodes.
        :return: dict
        """
        return adjacency_matrix(graph=self)

    def minsum(self):
        """ Finds the mode(s) that have the smallest sum of distance to all other nodes.
        :return: list of nodes
        """
        return minsum(self)

    def minmax(self):
        """ Finds the node(s) with shortest distance to all other nodes.
        :return: list of nodes
        """
        return minmax(self)

    def all_pairs_shortest_paths(self):
        """
        Find the cost of the shortest path between every pair of vertices in a
        weighted graph. Uses the Floyd-Warshall algorithm.
        :return: dict {node 1: {node 2: distance}, ...}
        """
        return all_pairs_shortest_paths(graph=self)

    def shortest_tree_all_pairs(self):
        """
        :return:
        """
        return shortest_tree_all_pairs(graph=self)

    def has_path(self, path):
        """
        :param path: list of nodes
        :return: boolean, if the path is in G.
        """
        return has_path(graph=self, path=path)

    def all_simple_paths(self, start, end):
        """
        finds all simple (non-looping) paths from start to end
        :param start: node
        :param end: node
        :return: list of paths
        """
        return all_simple_paths(self, start, end)

    def all_paths(self, start, end):
        """ finds all paths from start to end by traversing each fork once only.
        :param start: node
        :param end: node
        :return: list of paths
        """
        return all_paths(graph=self, start=start, end=end)

    def degree_of_separation(self, n1, n2):
        """ determines the degree of separation between 2 nodes
        :param n1: node
        :param n2: node
        :return: degree
        """
        return degree_of_separation(self, n1, n2)

    def loop(self, start, mid, end=None):
        """ finds a looped path via a mid-point
        :param start: node
        :param mid: node, midpoint for loop.
        :param end: node
        :return: path as list
        """
        return loop(self, start, mid, end)

    def avoids(self, start, end, obstacles):
        """ finds the shortest path between start and end avoiding the obstacles
        :param start: node
        :param end: node
        :param obstacles: nodes as iterable
        :return: path as list
        """
        return avoids(self, start, end, obstacles)


class Graph3D(Graph):
    """ a graph where all (x,y)-positions are unique. """

    def __init__(self, from_dict=None, from_list=None):
        super().__init__(from_dict=from_dict, from_list=from_list)

    def copy(self):
        g = Graph3D(from_dict=self.to_dict())
        return g

    # spatial only function
    # ---------------------
    @staticmethod
    def _check_tuples(n1):
        if not isinstance(n1, tuple):
            raise TypeError(f"expected tuple, not {type(n1)}")
        if len(n1) != 3:
            raise ValueError(f"expected tuple in the form as (x,y,z), got {n1}")
        if not all(isinstance(i, (float, int)) for i in n1):
            raise TypeError(f"expected all values to be integer or float, but got {n1}")

    @staticmethod
    def distance(n1, n2):
        """ returns the distance between to xyz tuples coordinates
        :param n1: (x,y,z)
        :param n2: (x,y,z)
        :return: float
        """
        Graph3D._check_tuples(n1)
        Graph3D._check_tuples(n2)
        (x1, y1, z1), (x2, y2, z2) = n1, n2
        a = abs(x2 - x1)
        b = abs(y2 - y1)
        c = abs(z2 - z1)
        return (a * a + b * b + c * c) ** (1 / 2)

    def add_edge(self, n1, n2, value=None, bidirectional=False):
        self._check_tuples(n1)
        self._check_tuples(n2)
        assert value is not None
        super().add_edge(n1, n2, value, bidirectional)

    def add_node(self, node_id, obj=None):
        self._check_tuples(node_id)
        super().add_node(node_id, obj)
        """
        :param node_id: any hashable node.
        :param obj: any object that the node should refer to.

        PRO TIP: To retrieve the node obj use g.node(node_id)
        """
        self._nodes[node_id] = obj

    def n_nearest_neighbours(self, node_id, n=1):
        """ returns the node id of the `n` nearest neighbours. """
        self._check_tuples(node_id)
        if not isinstance(n, int):
            raise TypeError(f"expected n to be integer, not {type(n)}")
        if n < 1:
            raise ValueError(f"expected n >= 1, not {n}")

        d = [(self.distance(n1=node_id, n2=n), n) for n in self.nodes() if n != node_id]
        d.sort()
        if d:
            return [b for a, b in d][:n]
        return None

    def plot(self, nodes=True, edges=True, rotation='xyz', maintain_aspect_ratio=False):
        """ plots nodes and links using matplotlib3
        :param nodes: bool: plots nodes
        :param edges: bool: plots edges
        :param rotation: str: set view point as one of [xyz,xzy,yxz,yzx,zxy,zyx]
        :param maintain_aspect_ratio: bool: rescales the chart to maintain aspect ratio.
        :return: None. Plots figure.
        """
        return plot_3d(self, nodes, edges, rotation, maintain_aspect_ratio)
