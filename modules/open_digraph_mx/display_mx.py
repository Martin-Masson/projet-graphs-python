import os


class display_mx:
    def save_sa_dot_file(self, path: str, verbose: bool = False) -> None:
        """Saves the digraph in a dot file.
        Parameters:
        -----------
        path: str
            The path of the file.
        verbose: bool
            If True, displays the label of each node.
        """
        with open(path, "w") as file:
            file.write("digraph G {\n")

            for node_id in self.nodes:
                node = self.get_node_by_id(node_id)
                label = node.get_label

                if node_id in self.inputs:
                    file.write(f"    v{node_id} [color=blue];\n")
                if node_id in self.outputs:
                    file.write(f"    v{node_id} [color=red];\n")

                if verbose:
                    file.write(f'    v{node_id} [label="{label} id={node_id}"];\n')
                else:
                    file.write(f'    v{node_id} [label="{label}"];\n')

                for child_id in node.children:
                    for multiplicity in range(node.children[child_id]):
                        file.write(f"    v{node_id} -> v{child_id};\n")

            file.write("}")

    def display(self, verbose: bool = False) -> None:
        """Displays the digraph
        Parameters:
        -----------
        verbose: bool
            If True, displays the label of each node.
        """

        self.save_sa_dot_file("digraph.dot", verbose=verbose)
        os.system("dot -Tpdf digraph.dot -o digraph.pdf")
