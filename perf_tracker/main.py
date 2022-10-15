from multiprocessing.spawn import import_main_path
from perf_tracker.input_controller import InputController
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

    progs = InputController.handle_inputs()
    for prog in progs:
        print(prog.name)
        print(prog.args)
        print(prog.x)
        print("")
    for prog in progs:
        prog.run_all_tests(2)
        prog.print()

    return 0