from copy import deepcopy
from types import GeneratorType
from typing import Any, Dict, List, Union

from pipedown.nodes.base.cache import Cache
from pipedown.nodes.base.input import Input
from pipedown.nodes.base.primary import Primary
from pipedown.utils.empty import EMPTY


def run_dag(
    inputs: Dict[str, Any], outputs: Union[str, List[str]], mode, nodes
):
    """Run the dag between inputs and outputs"""

    # Default output nodes are all nodes without children
    if isinstance(outputs, str):
        outputs = [outputs]
    if len(outputs) == 0:
        outputs = [n.name for n in nodes if n.num_children() == 0]

    # To store cached outputs
    cached_outputs = {}
    output_data = {}

    # Run each node in reverse post-order
    node_outputs = None
    for node in get_dag_eval_order(inputs, outputs, nodes):

        # Check inputs are supplied
        if isinstance(node, Input) and node.name not in inputs:
            raise RuntimeError(f"No input supplied for {node.name}")

        # Get node's inputs
        if node.num_parents() == 0:
            node_inputs = inputs.get(node.name)
        elif node.num_parents() == 1:
            parent_name = node.get_parents()[0].name
            if parent_name in cached_outputs:
                node_inputs = deepcopy(cached_outputs[parent_name])
            else:  # only child / single parent -> we ran this last step
                node_inputs = node_outputs
        else:  # >1 parent, all of whose outputs will have been cached
            node_inputs = (
                deepcopy(cached_outputs[p.name]) for p in node.get_parents()
            )

        # Run the node
        node_outputs = run_node(node, node_inputs, mode)

        # Cache this node's outputs if it has multiple children
        # or if any of its children have multiple parents
        # TODO: there's definitely a more efficient way to be doing this...
        # should delete data as soon as it won't be needed by further nodes
        # and way you've currently got it set up there's an extra copy made
        if node.num_children() > 1 or any(
            c.num_parents() > 1 for c in node.get_children()
        ):
            cached_outputs[node.name] = deepcopy(node_outputs)

        # And store the output if this node is an output node
        if node.name in outputs:
            output_data[node.name] = node_outputs

    # Return output data
    if len(outputs) == 1:
        return output_data[outputs[0]]
    else:
        return output_data


def get_dag_eval_order(
    inputs: Dict[str, Any],
    outputs: Union[str, List[str]],
    nodes,
):
    """Get a list of nodes in the subset of the DAG connecting the inputs
    and outputs, in reverse post-order.
    """

    if isinstance(outputs, str):
        outputs = [outputs]

    visited = set()
    visit_order = []

    def dfs_walk_reverse_post_order(node):
        if (  # truncate the walk at inputs and cached caches
            node.name not in inputs
            and not (isinstance(node, Cache) and node.is_cached())
        ):
            for parent in node.get_parents():
                if parent not in visited:
                    dfs_walk_reverse_post_order(parent)
        visited.add(node)
        visit_order.append(node)

    # Run a DFS starting at each output node
    for node in nodes:
        if node.name in outputs:
            dfs_walk_reverse_post_order(node)

    # Ensure there aren't any cycles in the graph
    for i, node in enumerate(visit_order):
        for child in node.get_children():
            if child in visit_order and visit_order.index(child) < i:
                raise RuntimeError("Your graph has a cycle in it!")

    return visit_order


def run_node(node, node_inputs, mode):
    if node_inputs is EMPTY:  # don't run nodes with empty input
        return EMPTY
    if isinstance(node, Primary):
        return node.run(node_inputs, mode)
    if isinstance(node_inputs, GeneratorType):
        node_inputs = tuple(node_inputs)
    if node_inputs is None:
        if mode == "train":
            node.fit()
        return node.run()
    elif isinstance(node_inputs, tuple):
        node_inputs = [e for e in node_inputs]
        if mode == "train":
            node.fit(*node_inputs)
        return node.run(*node_inputs)
    else:
        if mode == "train":
            node.fit(node_inputs)
        return node.run(node_inputs)
