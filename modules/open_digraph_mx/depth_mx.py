from typing import Dict, List, Tuple


class depth_mx:
    def dijkstra(
        self, src: int, tgt: int = None, direction: int = None
    ) -> Tuple[Dict[int, int], Dict[int, int]]:
        """Dijkstra's algorithm implementation for open_digraph

        Parameters
        ----------
        src : int
            The node from which the distances will be calculated

        Optionnal Parameters
        ----------
        tgt : int (default None)
            Stops the algo when the shortest path to tgt is found
        direction : int (default None)
            Specifes the searched neighours. Should either be None, -1 or 1.
             1 = children only
            -1 = parents only
            None = both

        Returns
        -------
        dist : Dict[int, int]
            The distance vector of src. Maps node ids with their distance to src
        prev : Dict[int, int]
            Maps node ids with the id of the previous node of the path from src
        """
        Q = [src]
        dist = {src: 0}
        prev = {}
        while Q != []:
            u = min(Q, key=lambda k: dist[k])
            Q.remove(u)
            if direction == None:
                neighbours = (
                    self.get_node_by_id(u).get_parent_ids
                    + self.get_node_by_id(u).get_children_ids
                )
            elif direction == -1:
                neighbours = self.get_node_by_id(u).get_parent_ids
            elif direction == 1:
                neighbours = self.get_node_by_id(u).get_children_ids
            for v in neighbours:
                if not (v in dist):
                    Q.append(v)
                if not (v in dist) or dist[v] > dist[u] + 1:
                    dist[v] = dist[u] + 1
                    prev[v] = u
                if tgt != None:
                    if v == tgt:
                        return dist, prev
        return dist, prev

    def shortest_path(self, u: int, v: int) -> List[int]:
        """Computes the shortest path from u to v

        Parameters
        ----------
        u : int
            The id of the start node
        v : int
            The id of the end node

        Returns
        -------
        path : List[int]
            List of the ids of all the nodes of the shortest path from u to v
            (u and v are both included)
        """
        _, prev = self.dijkstra(u, tgt=v, direction=1)
        path = []
        while v in prev:
            path.append(v)
            v = prev[v]
        path.append(u)
        return path[::-1]

    def common_ancestors(self, n1: int, n2: int) -> Dict[int, Tuple[int, int]]:
        """Maps all common ancestor of n1 and n2 to its distance from each node

        Parameters
        ----------
        n1 : int
            The id of the first node
        n2 : int
            The id of the second node

        Returns
        -------
        common_ancestors : Dict[int, Tuple[int, int]]
            Keys are the id of the common ancestors.
            Values are tuple (distance to n1, distance to n2)
        """
        common_ancestors = {}
        n1_ances, _ = self.dijkstra(n1, direction=-1)
        n2_ances, _ = self.dijkstra(n2, direction=-1)
        for ancester in n1_ances.keys() & n2_ances.keys():
            common_ancestors[ancester] = (n1_ances[ancester], n2_ances[ancester])
        return common_ancestors

    @property
    def tri_topologique(self) -> List[List[int]]:
        """An implementation of a topologic sort

        Returns
        -------
        sort : List[List[int]]
            The topologic sort. Each element of the list is a sublist containing all nodes
            of depth equal to the index of the sublist in the list
        """
        digraph = self.copy
        for input in self.inputs:
            digraph.remove_node_by_id(input)
        for output in self.outputs:
            digraph.remove_node_by_id(output)

        sort = []
        while digraph.nodes != {}:
            roots = []
            for node_id in digraph.nodes:
                node = digraph.get_node_by_id(node_id)
                if node.in_degree == 0:
                    roots.append(node_id)

            sort.append(roots)

            for root in roots:
                digraph.remove_node_by_id(root)

        return sort

    def node_depth(self, node_id: int) -> int:
        """Returns the depth of the node of id node_id"""
        tri = self.tri_topologique
        for level in tri:
            if node_id in level:
                return tri.index(level)

    @property
    def depth(self) -> int:
        """Returns the depth of the open digraph"""
        return len(self.tri_topologique)

    def longest_path(self, u: int, v: int) -> Tuple[List[int], int]:
        """Computes the longest path from u to v and its distance

        Parameters
        ----------
        u : int
            The id of the start node
        v : int
            The id of the end node

        Returns
        -------
        path : List[int]
            List of the ids of all the nodes of the longest path from u to v
            (u and v are both included)
        dist : int
            The distance of the path
        """
        dist = {u: 0}
        prev = {}
        li = self.tri_topologique
        lk = li[self.node_depth(u)]
        for l in li[li.index(lk) + 1 :]:
            for w in l:
                parents = self.get_node_by_id(w).get_parent_ids
                inter = list(set(parents) & set(dist.keys()))
                if inter != []:
                    p = max(inter, key=lambda k: dist[k])
                    dist[w] = dist[p] + 1
                    prev[w] = p
                if w == v:
                    break
        path = []
        while w in prev:
            path.append(w)
            w = prev[w]
        path.append(u)

        return path[::-1], dist[v]
