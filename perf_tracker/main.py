from multiprocessing.spawn import import_main_path
from perf_tracker.input_controller import InputController


def main() -> int:
    InputController.parse_args()
    return 0