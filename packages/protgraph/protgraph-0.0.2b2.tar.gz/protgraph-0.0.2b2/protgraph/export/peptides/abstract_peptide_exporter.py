from abc import abstractmethod

import networkx

from protgraph.export.abstract_exporter import AExporter


class APeptideExporter(AExporter):
    """
    This is a abstract exporter for peptides in a graph. It can implement
    an export funtionality to a folder / database or more.
    """

    @property
    @abstractmethod
    def skip_x(self) -> bool:
        """ Skip Peptides, which contain X? """
        pass

    @property
    @abstractmethod
    def peptide_min_length(self) -> int:
        """ Minimum peptide length """
        pass

    @property
    @abstractmethod
    def max_miscleavages(self) -> int:
        """ Maximum number of miscleavages in a peptide """
        pass

    @property
    @abstractmethod
    def use_igraph(self) -> bool:
        """ Use Igraph? (or networkX?) """
        pass

    @property
    @abstractmethod
    def peptide_max_length(self) -> int:
        """ Maximum peptide length to limit possibilites. None to consider all. """
        pass

    @property
    @abstractmethod
    def batch_size(self) -> int:
        """ Batch size of peptides which will be processed at once. (list length)"""
        pass

    @abstractmethod
    def export_peptides(self, prot_graph, l_path_nodes, l_path_edges, l_peptide, l_miscleavages, queue):
        """ Here goes the actual implementation of exporting a list of peptides into a file/folder/database etc. """
        pass

    def export(self, prot_graph, queue):
        """
        This abstract exporter implements the actual peptide traversal
        in a graph and calls the peptide exporter
        """
        # Get start and end node
        [__start_node__] = prot_graph.vs.select(aminoacid="__start__")
        [__stop_node__] = prot_graph.vs.select(aminoacid="__end__")

        # Set batch lists
        l_path = []
        l_edge_ids = []
        l_aas = []
        l_cleaved = []
        # Iterate over all peptides
        for path in self._get_peps(prot_graph, __start_node__, __stop_node__):

            # Get the actual peptide (concatenated aminoacids)
            aas = "".join(prot_graph.vs[path[1:-1]]["aminoacid"])

            # Get the edge ids from a path
            edge_ids = prot_graph.get_eids(path=path)

            # Skip Peptides, which contain an X
            if self.skip_x and "X" in aas:
                continue

            # Filter by peptide length
            if len(aas) < self.peptide_min_length:
                continue

            # Get number of cleaved edges
            if "cleaved" in prot_graph.es[edge_ids[0]].attributes():
                cleaved = sum(filter(None, prot_graph.es[edge_ids]["cleaved"]))
            else:
                cleaved = -1

            # And filter by miscleavages
            if self.max_miscleavages != -1:
                if cleaved > self.max_miscleavages:
                    continue

            # Append information to list
            l_path.append(path)
            l_edge_ids.append(edge_ids)
            l_aas.append(aas)
            l_cleaved.append(cleaved)

            if len(l_path) >= self.batch_size:
                # We export the list of peptides here and reset those lists afterwards
                self.export_peptides(prot_graph, l_path, l_edge_ids, l_aas, l_cleaved, queue)
                l_path = []
                l_edge_ids = []
                l_aas = []
                l_cleaved = []

        if len(l_path) > 0:
            # Special case, we might have some peptides left
            self.export_peptides(prot_graph, l_path, l_edge_ids, l_aas, l_cleaved, queue)

    def _get_peps(self, prot_graph, s, e):
        """ Get peptides depending on selected method """
        # OFFSET +1 since we have dedicated start and end nodes!
        cutoff = self.peptide_max_length + 1 if self.peptide_max_length is not None else None
        if self.use_igraph and self.peptide_max_length is None:
            cutoff = -1

        if self.use_igraph:
            # This can consume lots of memory
            results = prot_graph.get_all_simple_paths(
                s.index,
                to=e.index,
                cutoff=cutoff
            )
            for r in results:
                yield r
        else:
            # This is a generator approach but is also considerably slower
            netx = prot_graph.to_networkx()
            yield from networkx.algorithms.simple_paths.all_simple_paths(
                netx,
                s.index,
                e.index,
                cutoff=cutoff
            )
