from perf_tracker.prog import Prog

from pathlib import Path


class PerfController():
    """The controller to run the performance tests"""

    def __init__(self, iterations: int, out_dir: Path, val: bool,
                 progs: list[Prog]):

        self.iterations = iterations
        self.out_dir = out_dir
        self.progs = progs
        self.valgrind = val
        self._copy_config()

    def _copy_config(self):
        """Copies the information to a config file"""

        with open(self.out_dir / "config.txt", "w+") as config_file:
            num_prog = len(self.progs)
            num_vars = len(self.progs[0].args)
            config_file.write((f"# iterations: {self.iterations}\n"
                               f"# valgrind: {self.valgrind}\n\n"))
            config_file.write(f"{num_prog}\n{num_vars}\n\n")
            for prog in self.progs:
                config_file.write(f"{prog.get_config_str()}\n\n\n")

    def run_tests(self):
        for prog in self.progs:
            prog.run_all_tests(self.iterations)
            # prog.print()
            # prog.time_node.generate_all_pie_plots(out_dir / "pie_charts")