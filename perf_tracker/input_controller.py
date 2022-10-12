import argparse


class InputController():

    @staticmethod
    def parse_args():
        print("Hello World")
        parser = argparse.ArgumentParser(
            description="Config",
            formatter_class=argparse.RawDescriptionHelpFormatter)

        InputController._add_arguments(parser)

        print(parser.parse_args())

    @staticmethod
    def _add_arguments(parser: argparse.ArgumentParser):
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
                            required=True,
                            help="The config file to use")

        parser.add_argument("-p",
                            "--program",
                            dest="prog",
                            nargs="*",
                            type=str,
                            required=True)