import argparse
import os
import sys

from pathlib import Path

from perf_tracker.prog import Prog
from perf_tracker.perf_controller import PerfController


class InputController():
    """Handles performance tester input from both args and config files."""

    @staticmethod
    def handle_inputs() -> PerfController:
        """Handles inputs and returns a list of programs and output dir"""

        # Create and set up parser
        parser = argparse.ArgumentParser(
            description="Config",
            formatter_class=argparse.RawDescriptionHelpFormatter)

        InputController._add_arguments(parser)

        args = parser.parse_args()
        if args.gen_config:
            InputController._generate_config(args.name)

        # Set up outpuf folder
        out_dir = Path(args.output_dir)
        out_dir_arg = out_dir / args.name

        out_dir.mkdir(exist_ok=True)
        InputController._generate_output_folder(out_dir_arg)

        # Get programs
        prog_list = InputController._input_prog(args.prog, args.file,
                                                out_dir_arg)

        # Verify inputs
        if not prog_list:
            sys.exit("No programs parsed")

        if args.count < 1:
            sys.exit("Iterations must be greater than 0")

        names = [i.name for i in prog_list]
        if len(names) != len(set(names)):
            sys.exit("All programs must have a unique name")

        # Create perf controller
        controller_args = {
            "iterations": args.count,
            "val": args.valgrind,
            "out_dir": out_dir_arg,
            "progs": prog_list
        }

        return PerfController(**controller_args)

    @staticmethod
    def _generate_output_folder(out_dir: Path):
        """Safely generate output directory"""
        if out_dir.exists():
            while True:
                response = input((f"{out_dir} already exists. "
                                  "Would you like to override it? [y/n]: "))

                if response == "n" or response == "N":
                    sys.exit(1)
                elif response == "y" or response == "Y":
                    break
                else:
                    print(f"Invalid input: '{response}'")
            InputController._remove_dir(out_dir)
        out_dir.mkdir()

    @staticmethod
    def _remove_dir(path: Path):
        """Delete a directory and all of its contents"""
        for sub_path in path.iterdir():
            if not sub_path.is_dir():
                os.remove(sub_path)
            else:
                InputController._remove_dir(sub_path)
        path.rmdir()

    @staticmethod
    def _generate_config(name: str):
        """Copies the example config file in the cwd"""
        file_text = ""
        with open("perf_tracker/example_config.txt", "r") as template_config:
            file_text = template_config.read()

        with open(f"perf_{name}_config.txt", "w+") as out_config:
            out_config.write(file_text)
        sys.exit(0)

    @staticmethod
    def _input_prog(prog: str, config_file: str, out_dir: Path) -> list[Prog]:
        """Gets a list of progs to test"""
        if prog is None and config_file is None:
            sys.exit("Missing a config file or a program to run")
        if config_file:
            if prog:
                print(("program and config file both specified, "
                       "only config file will be used"))
            return InputController._input_file(Path(config_file), out_dir)
        p_name = prog.split()[0]
        if p_name[:2] == "./":
            p_name = p_name[2:]

        return [Prog(p_name, prog, out_dir)]

    @staticmethod
    def _parse_arg_line(line: str) -> tuple[int, str]:
        """Parses a line with arguments and x values"""
        split_line = line.split()
        if len(split_line) != 2:
            sys.exit((f"Could not process line '{line}'."
                      "Strictly two args are necessary."))
        if not split_line[0].isdigit():
            sys.exit(f"Could not process '{split_line[0]}' as int")
        return int(split_line[0]), split_line[1]

    @staticmethod
    def _input_file(file_name: Path, out_dir: Path) -> list[Prog]:
        """Inputs a list of progs from a config file"""
        progs = []
        if not file_name.exists():
            sys.exit(f"File not found: {file_name}")

        num_prog = None
        num_var = None
        line_count = -1
        prog_args = {}

        with open(file_name, "r", encoding="utf-8") as file:
            for line in file:
                if line[0] == "#" or line == "\n":
                    continue
                line = line.rstrip()

                if num_prog is None and num_var is None and not line.isdigit():
                    sys.exit((f"Could not parse '{line}' as an int"))
                if num_prog is None:
                    num_prog = int(line)
                    continue
                if num_var is None:
                    num_var = int(line)
                    continue

                line_count += 1

                # Handles prog name
                if line_count % (num_var + 2) == 0:
                    prog_args["name"] = line
                    continue

                # Handles commands
                if "commands" not in prog_args:
                    prog_args["commands"] = []

                if line[0] == ">" or line[0] == "$" or line[0] == "%":
                    prog_args["commands"].append(line[1:])
                    line_count -= 1
                    continue

                # Handles Program line (along with making the program)
                if line_count % (num_var + 2) == num_var + 1:
                    prog_args["prog"] = line
                    prog_args["out_dir"] = out_dir
                    progs.append(Prog(**prog_args))
                    prog_args = {}
                    continue

                # Handles prog argument line
                curr_x, curr_arg = InputController._parse_arg_line(line)

                if "args" not in prog_args:
                    prog_args["args"] = []
                    prog_args["x"] = []

                prog_args["args"].append(curr_arg)
                prog_args["x"].append(curr_x)

        return progs

    @staticmethod
    def _add_arguments(parser: argparse.ArgumentParser):
        """Adds arguments to an arg parser"""
        parser.add_argument("-n",
                            "--name",
                            dest="name",
                            type=str,
                            required=True,
                            help="The name of the perftest")

        parser.add_argument("-o",
                            "--output",
                            dest="output_dir",
                            type=str,
                            default="perf_output",
                            help="The directory to output to")

        parser.add_argument("-v",
                            "--valgrind",
                            dest="valgrind",
                            action="store_true",
                            help="Generates a valgrind output for the program")

        parser.add_argument("-i",
                            "--iterations",
                            dest="count",
                            type=int,
                            default=10,
                            help="The number of times to run each program")

        parser.add_argument("-g",
                            "--gen-config",
                            dest="gen_config",
                            action="store_true",
                            help="Generates example config file")

        parser.add_argument("-f",
                            "--config_file",
                            dest="file",
                            type=str,
                            required=False,
                            help="The config file to use")

        parser.add_argument("-p",
                            "--program",
                            dest="prog",
                            type=str,
                            required=False,
                            help="A single program to perf test")
