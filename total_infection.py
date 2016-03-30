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
    for i in range(teacher.num_students):
        assert teacher.get_student(i) != None

def test_infected(teacher, infected = True):
    """Tests whether the infection status of the classroom is accurate.

    @param teacher : the classroom to check
    @param infected : whether the classroom ought to be infected, default True
    """
    assert teacher.infected == infected
    assert teacher.num_infected == (teacher.num_users if infected else 0)
    for i in range(teacher.num_students):
        assert teacher.get_student(i).infected == infected

def test_total_infection(verbose, num_tests):
    """Runs randomized correctness tests for the Total Infection scenario.

    For each test, we create a number of separate classrooms, where both the 
     total number of students among all classrooms and the number of students
     in each classroom are chosen randomly.
    Then we infect and immediately disinfect some of the classrooms, both via
     spreading the infection from the teacher or a random student in the
     classroom.
    Finally, we go through all the classrooms one-by-one and infect them all.
    At each point, we run correctness checks that all students are properly
     infected/disinfected, and that the infection does not spread between
     classrooms.

    Aborts on error, or prints a success message if all tests were passed."""

    print("Running {} Total Infeciton tests...".format(num_tests))

    for i in range(num_tests):
        if verbose:
            print("\n### Total Infection Test {} ###\n".format(i+1))

        num_students = max(0, int(random.normalvariate(500, 50)))
        remaining_students = num_students
        classrooms = []
        num_classrooms = 0
        while remaining_students > 0:
            # first, create a randomly sized classroom and check its structure
            classroom_size = max(0, int(random.normalvariate(30, 10)))
            classroom_size = min(remaining_students, classroom_size)
            teacher = Teacher(classroom_size)
            remaining_students -= classroom_size
            classrooms.append(teacher)
            num_classrooms += 1

            if verbose:
                print("Created classroom with {} students."
                    .format(classroom_size))

            test_size(teacher, classroom_size)
            test_infected(teacher, False)

            # depending on a coin flip, infect the classroom, via either first
            #  infecting the teacher or a random student in the classroom and
            #  test that the classroom was properly infected and then disinfect
            #  in the same manner
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
            print("\nCreated {} classrooms, infecting one-by-one..."
                .format(num_classrooms))

        # now, infect all the students in all the classrooms, one by one
        #  (checking along the way that the infection was done correctly and did
        #  not spread between classrooms)
        for i in range(num_classrooms):

            teacher = classrooms[i]
            if teacher.num_students == 0 or random.choice([True, False]):
                if verbose:
                    print("   Infecting classroom {} via the teacher."
                        .format(i + 1))
                teacher.infect()
            else:
                teacher.get_random_student().infect()
                if verbose:
                    print("   Infecting classroom {} via a random student."
                        .format(i + 1))

            test_infected(teacher, True)
            # test that classrooms 0 up to and including i are still infected
            for j in range(i + 1):
                test_infected(classrooms[i], True)

            # test that classrooms beyond i are not infected
            for j in range(num_classrooms - i - 1):
                test_infected(classrooms[i + j + 1], False)

    if verbose:
        print("\n")
    print("All tests passed.")

def usage():
    print("Runs randomized correctness tests for the Total Infection scenario.")
    print("   -h | --help    : print this help message")
    print("   -v | --verbose : print verbose output for each test")
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

    test_total_infection(verbose = verbose, num_tests = num_tests)

if __name__ == "__main__":
    main(sys.argv[1:])
