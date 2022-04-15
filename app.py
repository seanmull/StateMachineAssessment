import logging
import string
from os import getcwd
from random import sample
from subprocess import run

from flask import Flask

app = Flask(__name__)

logging.basicConfig(encoding="utf-8", level=logging.INFO)


def select_three_nodes_at_random(src) -> list:
    nodes_to_pick_from = set(string.ascii_uppercase)
    nodes_to_pick_from.remove(src)
    return sample(nodes_to_pick_from, 3)


def build_graph() -> dict:
    nodes = list(string.ascii_uppercase)
    nodes.remove("Z")
    graph = {"Z": ["A"]}

    for node in nodes:
        graph.update({node: select_three_nodes_at_random(node)})
    return graph


class graph_client:
    def __init__(self) -> None:
        self.graph = build_graph()
        self.current_node = "A"

    def __str__(self) -> str:
        return str({"current_node": self.current_node, "graph": self.graph})

    def create_graph_visualization(self) -> None:
        def parse_graph_for_dot_format(self) -> str:
            s = ""
            for src, dest in self.graph.items():
                if src == "Z":
                    a = dest[0]
                    s += "{src} -> {{{a}}};".format(src=src, a=a)
                else:
                    a, b, c = dest
                    s += "{src} -> {{{a} {b} {c}}};".format(src=src, a=a, b=b, c=c)
            return s

        PATH = getcwd() + "/visualizations/output.svg"
        command = "echo 'digraph {{{graph}}}' | dot -Tsvg > {path}".format(
            graph=parse_graph_for_dot_format(self), path=PATH
        )
        run(command, shell=True)

    def traverse_graph(self, picked_path) -> None:
        def validate_path(picked_path) -> bool:
            try:
                path_choice = int(picked_path) - 1
            except ValueError:
                logging.error(
                    "{picked_path} is not a valid path must be an integer".format(
                        picked_path=picked_path
                    )
                )
                return False
            if path_choice not in range(3):
                logging.error(
                    "{picked_path} is not a valid path must be a number between \
                    1 and 3".format(
                        picked_path=picked_path
                    )
                )
                return False
            return True

        if validate_path(picked_path):
            logging.info(
                "The old node was {current_node}".format(current_node=self.current_node)
            )
            self.current_node = self.graph[self.current_node][int(picked_path) - 1]
            logging.info(
                "The new node is {current_node}".format(current_node=self.current_node)
            )
            if self.current_node == "Z":
                self.current_node == "A"
                logging.info(
                    "The new node is {current_node}".format(
                        current_node=self.current_node
                    )
                )


@app.route("/path/<int:path_number>")
def get_updated_node(path_number) -> str:
    cl.traverse_graph(path_number)
    return cl.__str__()


if __name__ == "__main__":
    cl = graph_client()
    cl.create_graph_visualization()
    logging.info("Connection established")
    app.run(host="localhost", port=65432)
