from multiprocessing.spawn import import_main_path
from perf_tracker.input_controller import InputController
from perf_tracker.time_node import TimeNode


def main() -> int:
    InputController.handle_inputs()
    return 0