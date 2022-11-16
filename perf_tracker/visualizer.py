from pathlib import Path

import matplotlib.pyplot as plt


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