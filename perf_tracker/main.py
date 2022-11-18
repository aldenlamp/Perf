from cProfile import label
from multiprocessing.spawn import import_main_path
from perf_tracker.input_controller import InputController
from perf_tracker.visualizer import Visualizer
from perf_tracker.time_node import TimeNode
from perf_tracker.prog import Prog

from pathlib import Path


def main() -> int:
    # InputController.handle_inputs()
    # p = [
    #     "./sparse", "-m_est_var", "-g", "data/compare/$k", "-p",
    #     "data/compare/sims/$k.pheno", "-a", "data/compare/sims/$k_annot.txt",
    #     "-perf"
    # ]
    # prog_name = " ".join(p)

    # prog = Prog("sparse", prog_name, Path("perf"), ["1", "10"], [1, 10])

    # prog.run_all_tests(2)
    # prog.print()

    # progs, out_dir = InputController.handle_inputs()
    # Visualizer.create_pie_chart([10, 40, 50],
    #                             ["small", "middle", "bigger than middle"],
    #                             Path("perf_output/dev_test"))

    # x_vals = [[10, 40, 1000] for i in range(3)]
    # values = [[1, 4, 20], [5, 20, 50], [10, 100, 500], [60, 300, 400]]
    # labels = ["a", "b", "c", "d"]
    values = [[1, 4, 20], [5, 20, 50], [10, 100, 500], [60, 300, 400],
              [60, 300, 400]]
    labels = ["a", "b", "c", "d", "e"]
    part_labels = ["p1", "p2", "p3"]

    Visualizer.create_bar_graph(values, part_labels, labels)

    # std_devs = [[3, 3, 3], [4, 4, 4], [5, 5, 5]]

    # Visualizer.create_line_chart(x_vals, values, std_devs,
    #                              ["plt1", "plt2", "plt3"], Path("."))

    # controller = InputController.handle_inputs()
    # controller.run_tests()

    # for prog in progs:
    #     print(prog.name)
    #     print(prog.args)
    #     print(prog.x)
    #     print(prog.commands)
    #     print("")
    # for prog in progs:
    #     prog.run_all_tests(1)
    #     prog.print()
    #     prog.time_node.generate_all_pie_plots(out_dir / "pie_charts")

    return 0