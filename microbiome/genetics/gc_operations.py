"""The operation that can be performed on a GC dictionary."""


def gc_stack(gca, gcb):
    """Stack gca on top of gcb.

    Graph A is stacked on B to make C by:
        B's inputs connect to A's outputs where possible
        C's inputs are A's inputs
        C's outputs are B's outputs

    Stacking only works if B's inputs can all be served by at least a
    subset of A's outputs.

    Args
    ----
    gca (gc): Graph to sit on top.
    gcb (gc): Graph to sit underneath.

    Returns
    -------
    (gc): C
    """
    stacked_graph = gc_graph(gca['graph']).stack(gcb['graph'])
    return None if stacked_graph is None else gcc = {
        'graph': stacked_graph
        'gca': gca['signature']
        'gcb': gcb['signature']
    }
