import argparse
import os
import sys

from pathlib import Path


class InputController():
    """Handles performance tester input from both args and config files."""

    @staticmethod
    def handle_inputs():
        """Handles inputs"""
        InputController._parse_args()

    @staticmethod
    def _parse_args():
        """Parses and validates command line arguments"""
        parser = argparse.ArgumentParser(
            description="Config",
            formatter_class=argparse.RawDescriptionHelpFormatter)

        InputController._add_arguments(parser)

        args = parser.parse_args()
        if args.gen_config:
            InputController._generate_config(args.name)

        if not args.file and not args.prog:
            sys.exit("No program or config file specified")

        out_dir = Path(args.output_dir)
        out_dir.mkdir(exist_ok=True)
        out_dir = out_dir / args.name
        InputController._generate_output_folder(out_dir)

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
                            nargs="*",
                            type=str,
                            required=False,
                            help="A single program to perf test")