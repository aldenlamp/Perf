import sys
from pathlib import Path
import matplotlib.pyplot as plt
from numpy import partition


class Visualizer():

    @staticmethod
    def create_pie_chart(values: list[float],
                         labels: list[str],
                         out_dir: Path,
                         plot_name: str = "pie_plot"):
        """Creates and saves a pie plot"""

        _, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
        wedges, _ = ax.pie(values, startangle=90, labels=None)  # type: ignore
        box = ax.get_position()

        ax.set_position(
            [box.x0 - (.25 * box.width), box.y0, box.width, box.height])

        legend_labels = [
            f"{l} ({int(values[i] * 100) / 100})"
            for i, l in enumerate(labels)  # type: ignore
        ]

        ax.legend(wedges,
                  legend_labels,
                  loc="center left",
                  bbox_to_anchor=(0.9, 0, 0.5, 1))

        plt.savefig(out_dir / f"{plot_name}.png")
        plt.close()

    @staticmethod
    def create_line_chart(x_vals: list[list[float]],
                          values: list[list[float]],
                          std_devs: list[list[float]],
                          labels: list[str],
                          out_dir: Path,
                          plt_title: str = "Comparison Plot",
                          plot_name: str = "comparison_plt"):

        if len(x_vals) != len(values) or len(values) != len(std_devs):
            sys.exit("Number of programs failed in line chart")

        for i, x_val in enumerate(x_vals):
            vals = values[i]
            sds = std_devs[i]
            plt.errorbar(x_val, vals, yerr=sds, fmt="-o", label=labels[i])

        plt.title(f"{plt_title}")
        plt.xlabel("Provided X Values")
        plt.ylabel("Runtime (seconds)")
        plt.legend()

        out = out_dir / f"{plot_name}.png"
        plt.savefig(out, dpi=300, bbox_inches="tight")

    @staticmethod
    def create_bar_graph(values: list[list[int]], partitions_labels: list[str],
                         bar_labels: list[str]):

        bar_width = 1 / (len(values) + 1)
        x = [i for i in range(len(partitions_labels))]

        for i, value in enumerate(values):
            x_vals = [j + (i * bar_width) for j in x]
            plt.bar(x_vals, value, label=bar_labels[i], width=bar_width)

        plt.xlabel("Partitions")
        plt.ylabel("Runtime")
        plt.xticks([i + 0.5 - bar_width for i in x], partitions_labels)
        plt.legend()

        plt.show()