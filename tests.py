#!/usr/bin/env python3

import random
import getopt
import sys
from infection import *

def test_size(teacher, size):
    """Tests whether the size of given classroom is accurate.

    @param teacher : the classroom to check
    @param size : the presumed number of students in the classroom
    """
    assert teacher.num_students == size
    assert teacher.num_users == size + 1

def test_infected(teacher, infected = True):
    """Tests whether the infection status of the classroom is accurate.

    @param teacher : the classroom to check
    @param infected : whether the classroom ought to be infected, default True
    """
    assert teacher.infected == infected
    assert teacher.num_infected == (teacher.num_users if infected else 0)
    for i in range(teacher.num_students):
        student = teacher.get_student(i)
        assert student.infected == infected

def test(verbose, num_tests):
    """Runs randomized correctness tests.

    Aborts on error, or prints a success message if all tests were passed."""

    print("Running {} tests...\n".format(num_tests))

    classrooms = []
    for i in range(num_tests):
        if verbose:
            print("\n### Randomized Test {} ###\n".format(i+1))

        num_students = max(0, int(random.normalvariate(500, 50)))
        remaining_students = num_students
        while remaining_students > 0:
            # first, create a randomly sized classroom and check its structure
            classroom_size = max(0, int(random.normalvariate(30, 10)))
            classroom_size = min(remaining_students, classroom_size)
            teacher = Teacher(classroom_size)
            remaining_students -= classroom_size

            if verbose:
                print("Created classroom with {} students.".format(classroom_size))

            test_size(teacher, classroom_size)
            test_infected(teacher, False)

            # depending on a coin flip, infect the classroom, via either first
            #  infecting the teacher or a random student in the classroom and
            #  test that the classroom was properly infected
            if random.choice([True, False]):
                if classroom_size == 0 or random.choice([True, False]):
                    if verbose:
                        print("   Infecting via the teacher.")
                    teacher.infect()
                else:
                    if verbose:
                        print("   Infecting via a random student.")
                    teacher.get_random_student().infect()

                test_infected(teacher, True)

            # depending on a coin flip, disinfect the classroom (even if it has
            #  not been infected) again via either a random student or the
            #  teacher, and check that it was properly disinfected
            if random.choice([True, False]):
                if classroom_size == 0 or random.choice([True, False]):
                    if verbose:
                        print("   Disinfecting via the teacher.")
                    teacher.infect(infect = False)
                else:
                    if verbose:
                        print("   Disinfecting via a random student.")
                    teacher.get_random_student().infect(infect = False)

                test_infected(teacher, False)

    if verbose:
        print("\n")
    print("All tests passed.")

def usage():
    """Prints brief usage information on how to run tests."""
    print("Runs correctness tests.")
    print("   -h | --help    : print this help message")
    print("   -v | --verbose : print verbose output for each test (default false)")
    print("   -n TESTS       : run TESTS number of tests (default 100)")

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hvn:", ["help, verbose"])
    except getopt.GetoptError:
        usage()
        return

    verbose = False
    num_tests = 100
    for opt, arg in opts:
        if opt in ["-h", "help"]:
            usage()
            return
        elif opt in ["-v", "verbose"]:
            verbose = True
        elif opt in ["-n"]:
            num_tests = int(arg)

    test(verbose = verbose, num_tests = num_tests)

if __name__ == "__main__":
    main(sys.argv[1:])
