from pathlib import Path

import matplotlib.pyplot as plt


class Visualizer():

    @staticmethod
    def create_pie_chart(values: list[float],
                         labels: list[str],
                         out_dir: Path,
                         plot_name: str = "pie_plot"):

        _, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
        wedges, _ = ax.pie(values, startangle=0, labels=None)  # type: ignore
        box = ax.get_position()

        ax.set_position(
            [box.x0 - (.25 * box.width), box.y0, box.width, box.height])

        legend_labels = [
            f"{l} ({int(values[i])})" for i, l in enumerate(labels)
        ]

        ax.legend(wedges,
                  legend_labels,
                  loc="center left",
                  bbox_to_anchor=(0.9, 0, 0.5, 1))

        plt.savefig(out_dir / f"{plot_name}.png")