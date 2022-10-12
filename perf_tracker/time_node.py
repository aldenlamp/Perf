import math
import sys


class TimeNode():
    """A class for keeping track of program run times"""

    def __init__(self, name="All", full_path=None):
        """Init the time node object"""
        self.name = name
        self.full_path = full_path
        self.times = []
        self.children = []

    def add_child(self, node):
        """Add a child time node"""
        if not self.children:
            self.children = []
        self.children.append(node)

    def add_tree_time(self, path: list[str], time: float, layer=0):
        """Adds a time to the time tree structure (creates missing nodes)"""
        if path[layer] != self.name:
            sys.exit("Error in generating time tree")

        if layer == len(path) - 1:
            self.add_time(time)
            return

        child_ind = self._find_child(path[layer + 1])
        if child_ind == -1:
            new_node = TimeNode(path[layer + 1], ":".join(path[:layer + 1]))
            self.add_child(new_node)
            child_ind = len(self.children) - 1

        self.children[child_ind].add_tree_time(path, time, layer + 1)

    def _find_child(self, child: str):
        """Returns the index of the child or -1 if it doesnt exist"""
        if not self.children:
            return -1
        children_names = [c.name for c in self.children]
        if child in children_names:
            return children_names.index(child)
        return -1

    def add_time(self, time: float):
        """Adds a time to this time node"""
        self.times.append(time)

    def get_avg_time(self) -> float:
        """Gets the average time of this node"""
        return sum(self.times) / len(self.times)

    def get_sd_time(self) -> float:
        """Gets the standard deviation of this time node"""
        avg = self.get_avg_time()
        return math.sqrt(
            sum([pow((i - avg), 2) for i in self.times]) / len(self.times))
