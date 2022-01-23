

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

        def get_id():
            return self.id

        def get_label():
            return self.label

        def get_parents():
            return self.parents

        def get_children():
            return self.children


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

        def get_input_ids():
            return self.inputs
        def get_output_ids():
            return self.outputs
        def get_id_node_map():
            return self.nodes
        def get_nodes():
            return self.nodes.values
        def get_node_ids():
            return self.nodes.keys()
        def get_node_by_id(id):
            return self.nodes[id]
        def get_nodes_by_ids(ids):
            l = []
            for id in ids:
                l.append(get_node_by_id(id))
            return l
        def new_id():
            return max(get_node_ids()) + 1

        def add_edge(self, src, tgt):
            n = self.nodes[src]
            if n.parents.has_key(tgt):
                n.parents[tgt] += 1
            else :
                n.parents[tgt] = 1
        
        def add_node(self, label='', parents=, children=):
            
