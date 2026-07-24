import cProfile
import pstats
import pytest

def run_profile():
    profiler = cProfile.Profile()
    profiler.enable()

    pytest.main(["tests/unit/test_profiling.py"])

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.strip_dirs().sort_stats("cumulative").print_stats(10)

if __name__ == "__main__":
    run_profile()
