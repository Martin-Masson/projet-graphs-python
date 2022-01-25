class node:

    def __init__(self, identity, label, parents, children):
        '''
        identity: int; its unique id in the graph
        label: string;
        parents: int->int dict; maps a parent node's id to its multiplicity
        children: int->int dict; maps a child node's id to its multiplicity
        '''
        self.id = identity
        self.label = label
        self.parents = parents
        self.children = children
	
	def __str__(self):
        return 'node(' + str(self.id) + ', ' + self.label + ', ' + str(self.parents) + ', ' + str(self.children) + ')'

    def __repr__(self):
        return str(self)

    def copy(self):
        return node(self.id, self.label, self.parents, self.children)
	
    def get_id(self):
        return self.id

    def get_label(self):
        return self.label

    def get_parent_ids(self):
    	return self.parents.keys()

    def get_children_ids(self):
        return self.children.keys()

    def set_id(self, id):
        self.id = id

    def set_label(self, label):
        self.label = label

    def set_parent_ids(self, parents):
        self.parents = parents

	def set_children_ids(self, children):
		self.children = children
	
	def add_child_id(self, new_child_id, multi=1):
        self.children[new_child_id] = multi
	
	def add_parent_id(self, new_parent_id, multi=1):
        self.children[new_parent_id] = multi

    def remove_parent_once(self, parent_id):
        if self.parents[parent_id] < 2:
            del self.parents[parent_id]
        else:
            self.parents[parent_id] -= 1

    def remove_child_once(self, children_id):
        if self.children[children_id] < 2:
            del self.children[children_id]
        else:
            self.children[children_id] -= 1
    
    def remove_parent_id(self, parent_id):
        del self.parents[parent_id]
    
    def remove_child_id(self, children_id):
        del self.children[children_id]

class open_digraph:  # for open directed graph
	
    def __init__(self, inputs, outputs, nodes):
        '''
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        '''
        self.inputs = inputs
        self.outputs = outputs
        # self.nodes: <int,node> dict
        self.nodes = {node.id: node for node in nodes}
		
	def __str__(self):
        output = ''
        for node in self.nodes.values():
            output += 'n' + str(node.id) + ' = ' + str(node) + '\n'
        return output

    def __repr__(self):
        return str(self)

    @classmethod
    def empty(self):
        return open_digraph([], [], [])

    def copy(self):
        return open_digraph(self.inputs, self.outputs, self.nodes)

	def get_input_ids(self):
        return self.inputs

    def get_output_ids(self):
        return self.outputs

    def get_id_node_map(self):
        return self.nodes

    def get_nodes(self):
        return self.nodes.values()

    def get_node_ids(self):
        return self.nodes.keys()

    def get_node_by_id(self, id):
        return self.nodes[id]

    def get_nodes_by_ids(self, ids):
        output = []
        for id in ids:
            output.append(get_node_by_id(id))
        return output
	
	def set_input_ids(self, inputs):
        self.inputs = inputs

    def set_output_ids(self, outputs):
        self.outputs = outputs

    def add_input_id(self, new_input):
        self.inputs.append(new_input)

    def add_output_id(self, new_output):
        self.outputs.append(new_output)

    def new_id(self):
        return len(self.nodes)

	def add_edge(self, src, tgt):
		tgt_node = get_node_by_id(tgt)
		src_node = get_node_by_id(src)
		if tgt_node.parents.has_key(src) and src_node.children.has_key(tgt):
			tgt_node.parents[src] += 1
			src_node.children[tgt] += 1
		else:
			tgt_node.parents[src] = 1
			src_node.children[tgt] = 1

    def add_node(self, label='', parents, children):
		node_id = self.new_id()
		new_node = node(node_id, label, parents, children)
		self.nodes[node_id] = new_node
		for parent, child in zip(parents.keys(), childrens.keys()):
			self.add_edge(parent, node_id)
			self.add_edge(node_id, children)

    '''
    def remove_edge(self, src, tgt):
        tgt_node = get_node_by_id(tgt)
		src_node = get_node_by_id(src)
		if tgt_node.parents[src] > 1 and src_node.children.[tgt] > 1:
			tgt_node.parents[src] -= 1
			src_node.children[tgt] -= 1
		else:
			del tgt_node.parents[src]
			del src_node.children[tgt]
    '''

    # *args is a tuple of tuples (src, tgt)
    def remove_edges(self, *args):
        for arg in args:
            tgt = arg[0]
            src = arg[1]
            tgt_node = get_node_by_id(tgt)
		    src_node = get_node_by_id(src)
            if tgt_node.parents[src] > 1 and src_node.children.[tgt] > 1:
			    tgt_node.parents[src] -= 1
			    src_node.children[tgt] -= 1
		    else:
			    del tgt_node.parents[src]
			    del src_node.children[tgt]
    
    '''
    def remove_parallel_edge(self, src, tgt):
        src_node = get_node_by_id(src)
        tgt_node = get_node_by_id(tgt)
        del src_node.children[tgt]
		del tgt_node.parents[src]
    '''

    def remove_parallel_edges(self, *args):
        for arg in args:
            tgt = arg[0]
            src = arg[1]
            src_node = get_node_by_id(src)
            tgt_node = get_node_by_id(tgt)
            del src_node.children[tgt]
		    del tgt_node.parents[src]

    '''
    def remove_node_by_id(self, tgt_id):
        tgt_node = get_node_by_id(tgt_id)
        tgt_node.set_parent_ids({})
        tgt_node.set_children_ids({})
    '''

    def removes_node_by_id(self, *args):
        for arg in args:
            tgt_id = arg[0]
            tgt_node = get_node_by_id(tgt_id)

            for parent in tgt.node.parents:
                parent.remove_child_id(tgt_id)

            for child in tgt.children:
                child.remove_parent_id(tgt_id)

            tgt_node.set_parent_ids({})
            tgt_node.set_children_ids({})
    
    def is_well_formed(self):
        # Checking if all intput nodes are in the graph, have no parents and have a single child of multiplicity 1
        for in_node in inputs:
            if not(self.nodes.has_key(in_node)):
                raise Exception(f"Input node {in_node} isn't in the graph")
            if in_node.parents:
                raise Exception(f"Input node {in_node} has parents")
            if in_node.children.values() != [1]:
                raise Exception(f"Intput node {in_node} has more than 1 children or its multiplicity is greater than 1")

        # Checking if all output nodes are in the graph, have no children and have a single parent of multiplicity 1
        for out_node in outputs:
            if not(self.nodes.has_key(out_node)):
                raise Exception(f"Output node {in_node} isn't in the graph")
            if out_node.children:
                raise Exception(f"Output node {in_node} has children")
            if out_node.parents.values() != [1]:
                raise Exception(f"Output node {in_node} has more than 1 parent or its multiplicity is greater than 1")
            
        # Checking if all the keys in nodes are paired with a node of id equal to the key
        if self.nodes.keys() != node_id for node_id in self.nodes.values():
            raise Exception(f"A key of <id,node> in nodes is invalid")

        for node in self.nodes:

            # Checking if all the childrens of all the nodes have that same node as a parent with their respective multiplicity
            for parent_id, multi in node.parents.items():
                childrens = get_node_by_id(parent_id).children
                if not(node.id in childrens) or not(multi == childrens[node.id]):
                    raise Exception(f"node {parent_id} isn't a parent of node {node_id} or their multiplicity are different")

            # Checking if all the parents of all the nodes have that same node as a child with their respective multiplicity
            for child_id, multi in node.children.items():
                parents = get_node_by_id(parent_id).parents
                if not(node.id in parents) or not(multi == parents[node.id]):
                    raise Exception(f"node {child_id} isn't a child of node {node_id} or their multiplicity are different")
