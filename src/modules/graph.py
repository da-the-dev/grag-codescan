import re
from pyvis.network import Network
from itertools import cycle

from src.modules.structured_output.graph import Triplet


def generate_graph(triplets: list[Triplet]) -> str:
    g = Network(
        width="1600px",
        height="800px",
        directed=True,
        notebook=False,
        font_color="#ffffff",
        bgcolor="#000000",
    )
    g.barnes_hut(
        gravity=-3000,
        central_gravity=0.3,
        spring_length=50,
        spring_strength=0.001,
        damping=0.09,
        overlap=0,
    )

    colorgenerator = cycle(
        [
            "red",
            "coral",
            "lightsalmon",
            "darkorange",
            "gold",
            "yellow",
            "lime",
            "cyan",
            "royalblue",
            "darkviolet",
            "hotpink",
        ]
    )
    for triplet in triplets:
        entity1, relation, entity2 = triplet.node_from, triplet.relation, triplet.node_to

        if entity1 not in g.get_nodes():
            g.add_node(entity1, label=entity1, color=next(colorgenerator))

        if entity2 not in g.get_nodes():
            g.add_node(entity2, label=entity2, color=next(colorgenerator))

        g.add_edge(entity1, entity2, label=relation)

    # g.show(filename, notebook=False)
    html = g.generate_html()
    # need to remove ' from HTML
    html = html.replace("'", '"')

    iframe = f"""<iframe style="width: 1600px; height: 800px; margin: 0; padding: 0;" name="result" sandbox="allow-modals allow-forms 
    allow-scripts allow-same-origin allow-popups 
    allow-top-navigation-by-user-activation allow-downloads" allowfullscreen="" 
    frameborder="0" srcdoc='{html}'></iframe>"""

    return iframe
