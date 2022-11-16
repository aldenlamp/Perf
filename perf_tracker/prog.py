from concurrent.futures import process
from distutils.command.config import config
import subprocess
import time

from pathlib import Path

from perf_tracker.time_node import TimeNode


class Prog():

    def __init__(self,
                 name: str,
                 prog: str,
                 out_dir: Path,
                 commands: list[str] = [],
                 args: list[str] = ["$"],
                 x: list[int] = [1]):
        """Inits the Program"""
        self.name = name
        self.prog = prog
        self.out_dir = out_dir / name
        self.out_dir.mkdir()

        self.commands = commands
        self.args = args
        self.x = x

        self.time_node = TimeNode()

    def print(self):
        """Prints the entire time node tree for this program"""
        print(self.time_node.get_all_out_str())

    def get_config_str(self) -> str:
        """Returns a str of program as it would be in a config file"""
        name_str = f"{self.name}"

        commands_str = '\n>'.join(self.commands)
        if commands_str:
            commands_str = ">" + commands_str

        arg_lines = "\n".join([f"{i} {j}" for i, j in zip(self.x, self.args)])

        config_str = f"{name_str}\n{commands_str}\n{arg_lines}\n{self.prog}"

        return config_str

    def run_all_tests(self, iterations: int):
        """Runs all the iterations for all the arguments"""
        self.run_commands()
        for arg in self.args:
            (self.out_dir / f"arg_{arg}").mkdir()
            for i in range(iterations):
                self.run_test(arg, i)

        with open(self.out_dir / "average_runtimes.txt", "w+") as out_file:
            out_file.write(self.time_node.get_all_out_str())
        self.time_node.generate_all_pie_plots(self.out_dir / "pie_charts")

    def run_commands(self):
        """Runs the proceeding saved commands"""
        if not self.commands:
            return

        with open(self.out_dir / "command_outputs.txt", "w+") as output_file:
            command_count = 0
            for command in self.commands:
                print(f"PRECOMMAND RUNNING: {command}")
                process = subprocess.run(command,
                                         shell=True,
                                         capture_output=True)
                std_out = process.stdout.decode("utf-8")
                err_out = process.stderr.decode("utf-8")

                output_file.write((f"COMMAND ({command_count}): {command}\n"
                                   f"RETURN CODE: {process.returncode}\n"
                                   f"STD OUT: {std_out.rstrip()}\n"
                                   f"STD ERR: {err_out.rstrip()}\n\n"))
                command_count += 1

    def run_test(self, arg: str, index: int):
        """Runs a single test on an argument and an iteration"""
        prog = self.prog.replace("$", arg)
        print(f"RUNNING ({index}): {prog}")
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

        self.time_node.add_tree_time(["All", f"arg_{arg}"], elapsed_time)
        self._process_output(arg, process.stdout.decode("utf-8"))

    def _process_output(self, arg: str, stdout: str):
        """Processes the programs output to add to the timing node"""
        for line in stdout.split("\n"):
            if len(line) > 3 and line[0:3] == "::>":
                split_line = line[3:].strip().split(":")

                val = float(split_line[-1])

                partition_names = ["All", f"arg_{arg}"] + split_line[:-1]
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