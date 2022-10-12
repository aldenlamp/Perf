import subprocess
import time

from pathlib import Path

from perf_tracker.time_node import TimeNode


class Prog():

    def __init__(self,
                 name: str,
                 prog: str,
                 out_dir: Path,
                 args: list[str] = ["$"],
                 x: list[int] = [1]):
        """Inits the Program"""
        self.name = name
        self.prog = prog
        self.out_dir = out_dir / name
        self.out_dir.mkdir()

        self.args = args
        self.x = x

        self.time_node = TimeNode()

    def print(self):
        """Prints the entire time node tree for this program"""
        self.time_node.print_all_outputs()

    def run_all_tests(self, iterations: int):
        """Runs all the iterations for all the arguments"""
        for arg in self.args:
            (self.out_dir / f"arg_{arg}").mkdir()
            for i in range(iterations):
                self.run_test(arg, i)

    def run_test(self, arg: str, index: int):
        """Runs a single test on an argument and an iteration"""
        prog = self.prog.replace("$", arg)
        start_time = time.perf_counter()
        process = subprocess.run(prog, shell=True, capture_output=True)
        end_time = time.perf_counter()

        elapsed_time = 1000 * (end_time - start_time)

        save_file = self.out_dir / f"arg_{arg}" / f"iteration{index}.txt"

        with open(save_file, "w+") as out_file:

            out_file.write(f"Return Code: {process.returncode}")

            if process.returncode != 0:
                out_file.write("\n\n======STDERR======\n")
                out_file.write(process.stderr.decode("utf-8"))
                print(f"Failed to run iteration '{index}' of '{prog}'")
                return

            out_file.write("\n\n======STDOUT======\n")
            out_file.write(process.stdout.decode("utf-8"))

            out_file.write("\n\n======TIMER======\n")
            out_file.write(f"time: {elapsed_time}")

        self.time_node.add_tree_time(["All", arg], elapsed_time)
        self._process_output(arg, process.stdout.decode("utf-8"))

    def _process_output(self, arg: str, stdout: str):
        """Processes the programs output to add to the timing node"""
        for line in stdout.split("\n"):
            if len(line) > 3 and line[0:3] == "::>":
                split_line = line[3:].strip().split(":")

                val = float(split_line[-1])

                partition_names = ["All", arg] + split_line[:-1]
                self.time_node.add_tree_time(partition_names, val)

    def run_valgrind(self):
        """Runs valgrind on the first program args"""
        val_out_dir = self.out_dir / "valgrind"
        val_out_dir.mkdir()

        ex_prog = self.prog
        if "$" in self.prog and self.args:
            ex_prog = self.prog.replace("$", self.args[0])

        # TODO (Alden): Run CacheGrind as well
        val_process = subprocess.run(f"valgrind {ex_prog}",
                                     shell=True,
                                     capture_output=True)

        if val_process.returncode != 0:
            print("Could not run valgrind")
            return

        # TODO (Alden): Correctly output valgrinds output

        # print("=========OUTPUT=========")
        # output = val_process.stdout.decode("utf-8")
        # print(output)
        # print("=========ERR=========")
        # error = val_process.stdout.decode("utf-8")
        # print(error)