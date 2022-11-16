from ast import Str
import math
from pathlib import Path
import sys

from perf_tracker.visualizer import Visualizer


class TimeNode():
    """A class for keeping track of program run times"""

    def __init__(self, name="All", full_path=None):
        """Init the time node object"""
        self.name = name
        self.full_path = full_path
        self.times = []
        self.children = []

    def get_out_str(self, level=0) -> str:
        """Returns a string representing this time node as a string"""
        ind = '  ' * level
        if len(self.times) > 0:
            format_str = "{} {:<25} {:<5} {:<10} {:<5} {:<10}"
            out = format_str.format(ind, self.name, "avg: ",
                                    str(self.get_avg_time())[:8], "sd: ",
                                    str(self.get_sd_time())[:8])
            return out
        else:
            return "{} {:<25}".format(ind, self.name)

    def get_all_out_str(self, level=0) -> str:
        """Gets a string representing the entire time node tree"""
        curr_str = f"{self.get_out_str(level)}\n"
        child_strs = [i.get_all_out_str(level + 1) for i in self.children]

        return curr_str + "".join(child_strs)

    def generate_pie_plots(self, out_dir: Path, level: int = 0):
        """Creates a pie chart for this time node"""
        partitioned_times = [child.get_avg_time() for child in self.children]
        labels = [child.name for child in self.children]

        total_time = self.get_avg_time()

        partitioned_sum = sum(partitioned_times)
        if partitioned_sum < total_time:
            partitioned_times.append(total_time - partitioned_sum)
            labels.append("Other")

        out_dir.mkdir(parents=True, exist_ok=True)
        Visualizer.create_pie_chart(partitioned_times, labels, out_dir,
                                    f"{level}-{self.name}")

    def generate_all_pie_plots(self, out_dir: Path, level: int = 0):
        """Recursively generates pie plots for all times nodes in the tree"""
        self.generate_pie_plots(out_dir, level)
        for child in self.children:
            child.generate_all_pie_plots(out_dir, level + 1)

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
        if not self.times:
            return 0
        return sum(self.times) / len(self.times)

    def get_sd_time(self) -> float:
        """Gets the standard deviation of this time node"""
        avg = self.get_avg_time()
        return math.sqrt(
            sum([pow((i - avg), 2) for i in self.times]) / len(self.times))
