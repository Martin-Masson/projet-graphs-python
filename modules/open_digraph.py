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
		if tgt_node.parents.has_key(tsrc) && src_node.children.has_key(tgt):
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
