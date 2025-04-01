import re
from pyvis.network import Network
from itertools import cycle


def extract_triplets(text: str) -> list[tuple[str, str, str]]:
    triplet_pattern = re.compile(r"\(\s*([^,]+?)\s*,\s*([^,]+?)\s*,\s*([^)]+?)\s*\)")

    # Find all matches in the text
    matches = triplet_pattern.findall(text)
    triplets = [tuple(match) for match in matches]

    return triplets


def generate_graph(triplets: list[tuple]) -> str:
    g = Network(
        width="1600px",
        height="800px",  # "600px",
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
    for entity1, relation, entity2 in triplets:
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
