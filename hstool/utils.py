import os
import random
from functools import partial


def wrapper(path, instance, filename):
    filename = filename.replace(' ', '_')
    return os.path.join(path, filename)


def path_and_rename_sources(instance, filename):
    return wrapper('files/sources', instance, filename)


def path_and_rename_figures(instance, filename):
    return wrapper('files/figures', instance, filename)


def path_and_rename_indicators(instance, filename):
    return wrapper('files/indicators', instance, filename)

def connected_components(neighbors):
    seen = set()

    def component(node):
        nodes = set([node])
        while nodes:
            node = nodes.pop()
            seen.add(node)
            nodes |= neighbors[node] - seen
            yield node

    for node in neighbors:
        if node not in seen:
            yield component(node)


def get_components(nodes, relations):
    graph_dict = {
        node.id:
        set(r.source.id for r in relations if r.destination.id == node.id) |
        set(r.destination.id for r in relations if r.source.id == node.id)
        for node in nodes
    }
    return connected_components(graph_dict)


def get_nodes_from_components(nodes, relations):
    components = get_components(nodes, relations)
    return [random.choice(list(component)) for component in components]
