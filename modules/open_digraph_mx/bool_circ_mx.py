from __future__ import annotations


class bool_circ_mx:
    def sub_is_cyclic(self, *args: List[int]) -> bool:
        """Returns True if the subgraph defined by the nodes ids in args is cyclic.

        Parameters:
        -----------
        *args: List[int]
            The list of the node ids.
        Returns:
        --------
        bool
            True if the subgraph is cyclic.
        """
        if self.is_empty:
            return False

        leaves = []
        for node_id in self.nodes:
            node = self.get_node_by_id(node_id)
            if node.out_degree == 0:
                leaves.append(node)

        if not leaves:
            return True

        for leaf in leaves.copy:
            parents = self.get_nodes_by_ids(leaf.get_parent_ids)
            for parent in parents:
                if len(parent.children) == 1:
                    leaves.append(parent)
            leaves.remove(leaf)
            self.remove_node_by_id(leaf.get_id)

        return self.sub_is_cyclic(leaves)

    @property
    def is_cyclic(self) -> bool:
        """Returns True if the digraph is cyclic.

        Returns:
        --------
        bool
            True if the digraph is cyclic."""
        digraph = self.copy
        for input in self.inputs:
            digraph.remove_node_by_id(input)
        for output in self.outputs:
            digraph.remove_node_by_id(output)

        return digraph.sub_is_cyclic()

    @property
    def min_id(self) -> int:
        """Returns the minimum id of the digraph."""
        return min(self.nodes)

    @property
    def max_id(self) -> int:
        """Returns the maximum id of the digraph."""
        return max(self.nodes)

    def shift_indices(self, n: int) -> None:
        """Shifts the indices of the digraph by n."""
        for id in self.nodes:
            node = self.get_node_by_id(id)
            node.set_id(id + n)
            node.set_parent_ids({id + n: multi for id, multi in node.parents.items()})
            node.set_children_ids(
                {id + n: multi for id, multi in node.children.items()}
            )

        for i in range(len(self.inputs)):
            self.inputs[i] += n

        for j in range(len(self.outputs)):
            self.outputs[j] += n

        self.nodes = {node.id: node for node in self.nodes.values()}

    def iparallel(self, args: List[OpenDigraph]) -> None:
        """Parallel composition of the digraph with the digraphs in args. modifies self.

        Parameters:
        -----------
        args: List[OpenDigraph]
            The list of the digraphs to parallel compose with self.
        """
        "A TESTER"
        for g in args:
            g.shift_indices(self.max_id - g.min_id + 1)
            self.inputs.extend(g.inputs)
            self.outputs.extend(g.outputs)
            for node in g.get_nodes:
                self.nodes[node.id] = node

    def parallel(self, g: OpenDigraph) -> OpenDigraph:
        """Parallel composition of the digraph with g and return the new graph.

        Parameters:
        -----------
        g: OpenDigraph
            The digraph to parallel compose with self.

        Returns:
        --------
        OpenDigraph
            The new digraph."""
        "A TESTER"
        output = self.copy
        output.iparallel([g])
        return output

    def icompose(self, g: OpenDigraph) -> None:
        """Compose the digraph with g by modifies self.
        
        Parameters:
        -----------
        g: OpenDigraph
            The digraph to compose with self.
        """
        g.shift_indices(self.max_id - g.min_id + 1)
        if len(self.outputs) != len(g.inputs):
            raise Exception(f"Length of outputs of self are different from inputs of g")

        for node in g.get_nodes:
            self.nodes[node.id] = node

        for i in range(len(self.outputs)):
            node_o = self.get_node_by_id(self.outputs[i])
            node_i = self.get_node_by_id(g.inputs[i])
            self.add_edge(node_o.get_parent_ids[0], node_i.get_children_ids[0])
            self.remove_node_by_id(node_o.id, node_i.id)

        self.outputs = g.outputs

    def compose(self, g: OpenDigraph) -> OpenDigraph:
        """Compose the digraph with g without modifying self and return the new graph.
        
        Parameters:
        -----------
        g: OpenDigraph
            The digraph to compose with self.
        
        Returns:
        --------
        OpenDigraph
            The new digraph.
        """

        output = self.copy
        output.icompose(g)
        return output

    def dfs(self, visited, node, component):
        """Depth-first search. Updates the visited list and the component list.
        
        Parameters:
        -----------
        visited: List[bool]
            The list of the visited nodes.
        node: OpenDigraphNode
            The node to start the search.
        component: List[OpenDigraphNode]
            The list of the nodes of the component
        """
        if node not in visited:
            visited.add(node)
            component.append(node.id)
            voisins = node.get_parent_ids + node.get_children_ids
            for voisin in voisins:
                self.dfs(visited, self.get_node_by_id(voisin), component)

    @property
    def connected_components(self):
        """Returns the connected components of the digraph.
        
        Returns:
        --------
        nb_components: int
            The number of the connected components.
        output: Hashmap[id, connected_component : int]
            The list of the connected components.
        """
        visited = set()
        output = {}
        components = []
        for id in self.inputs:
            node = self[id]
            l = []
            self.dfs(visited, node, l)
            components.append(l)
        components = list(filter(lambda a: a != [], components))
        nb_component = len(components)
        k = 0
        for component in components:
            component.sort()
            for id in component:
                output[id] = k
            k += 1
        return nb_component, output
