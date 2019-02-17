"""
Basic Exercise checker.
    1. Iterates over exercise directory.
    2. Copy unit tests.
    3. Execute.
    4. Write results.
"""
import argparse
import glob
import json
import os
import shutil
import subprocess

import xunitparser

__author__ = "Nir Moshe"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ex_dir", help="Exercise directory")
    parser.add_argument("--tests_dir", help="Tests directory")
    args = parser.parse_args()
    print(json.dumps(analyze_exercised_directory(args.ex_dir, args.tests_dir), indent=4))


def analyze_exercised_directory(exercises_dir, tests_dir):
    # Iterate over the exercises directory.
    results = {}
    for ex_dir in glob.glob(os.path.join(exercises_dir, "*")):
        results[ex_dir] = handle_single_exercise_directory(ex_dir, tests_dir)

    return results


def handle_single_exercise_directory(ex_dir, test_dir):
    try:
        ex = ExerciseTest(ex_dir, test_dir)
        return ex.get_test_results()

    except Exception:
        raise


class ExerciseTest(object):
    def __init__(self, ex_dir, test_dir):
        self.ex_dir = ex_dir
        self.test_dir = test_dir
        if not (os.path.isdir(self.ex_dir) and os.path.isdir(self.test_dir)):
            raise ValueError("%s or %s isn't a valid directory!" % (self.test_dir, self.ex_dir))

        self.test_files = os.listdir(self.test_dir)
        self._setup_test()

    def _setup_test(self):
        """
        1. Remove all the "old" test files.
        2. Install all the tests files.
        """
        for test_file in self.test_files:
            full_name = os.path.join(self.ex_dir, test_file)
            test_file_name = os.path.join(self.test_dir, test_file)
            if os.path.exists(full_name):
                if os.path.isdir(full_name):
                    shutil.rmtree(full_name)
                else:
                    os.remove(full_name)

            # Safe to copy.
            if os.path.isdir(test_file_name):
                shutil.copytree(test_file_name, full_name)
            else:
                shutil.copy(test_file_name, full_name)

    def get_test_results(self):
        out = self._execute_test()
        return self._parse_output(out)

    def _execute_test(self):
        output_file = os.path.join(self.ex_dir, "output.xml")
        p1 = subprocess.Popen(["nosetests", "--with-xunit", "--xunit-file=%s" % output_file], cwd=self.ex_dir)
        p1.wait(timeout=60)
        return output_file

    def _parse_output(self, output_file):
        with open(output_file) as output_fd:
            _, tr = xunitparser.parse(output_fd)
            return {
                "total": tr.testsRun,
                "failure or error": len(tr.errors) + len(tr.failures),
                "score": float(tr.testsRun - (len(tr.errors) + len(tr.failures))) / tr.testsRun * 100,
                "output_file": output_file
            }


if __name__ == "__main__":
    main()
