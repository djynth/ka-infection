#!/usr/bin/env python3

import getopt
import sys
import random
from infection import *

def bruteforce(classrooms, target):
    """Attempts to find a subset of classrooms to infect such that the number
       of infected users equals the target via a brute force algorithm.

    Returns a list of classrooms meeting the criteria if one could be found, or
     None otherwise.

    @param classrooms : the classrooms among which to choose
    @param target : the target number of students to infect
    """

    # it is impossible to get a negative target, so we can cut off this branch
    if target < 0:
        return None

    # the base case: no classrooms remain, either we have succeeded and the
    #  target is to add no more users, or we have failed and it is nonzero
    if not classrooms:
        return [] if target == 0 else None

    teacher = classrooms.pop()

    # we consider the two possibilites for this classroom: either include it in
    #  the final set of infected classrooms, or do not
    # if it is included, the target is decreased by the number of users in the
    #  classroom; otherwise the target remains the same
    # note that these two options could be run in parallel (but are not here)
    included = bruteforce(classrooms, target - teacher.num_users)
    if included != None:
        included.append(teacher)
        return included

    not_included = bruteforce(classrooms, target)
    if not_included != None:
        return not_included

    return None

def close_enough(classrooms, target, delta = 1.0):
    """A simple approximation algorithm designed to select a subset of the given
       classrooms whose users sum to approximately the given target.

    Our strategy is to add random classrooms to the selected set until we get
     "close enough" to the target.
    This strategy is nice in a few ways:
    * the algorithm is very simple and clean
    * most classrooms chosen are random - this means that users are roughly
      equally likely to get early access to new features
    * it runs in (expected) polynomial time, and if the distribution of
      classroom size is reasonable, it runs very quickly

    @param classrooms : the classrooms among which to choose
    @param target : the target number of students to infect
    @param delta : how close to the target is sufficient, linear scaling with
                   0.0 for exact and 1.0 for within the average classroom size,
                   default 1.0
    """

    if len(classrooms) == 0:
        return []

    avg_size = sum(c.num_users for c in classrooms)/len(classrooms)
    selected = []
    total = 0

    # keep track of the number of loops since the last classroom was selected,
    #  as a means to break if getting close enough to the target is hard
    last_addition = 0

    while abs(total - target) > delta * avg_size:
        if not classrooms:
            return None

        # pick a random classroom
        selection = classrooms.pop(random.randint(0, len(classrooms)-1))
        size = selection.num_users

        # check whether adding this classroom to the selected set will get the
        #  total closer to the target
        if abs(total - target) < abs(total - (target + size)):
            # if so, add it in and continue
            selected.append(selection)
            total += size
            last_addition = 0
        else:
            # otherwise, don't add it and make sure we haven't been looping too
            #  much
            classrooms.append(selection)
            last_addition += 1
            if last_addition > len(classrooms):
                return None

    return selected

def usage():
    print(("Runs randomized tests for the Limited Infection scenario and "
           "evaluates how successfully and accurately solutions can be found."))
    print( "   -h | --help    : print this help message")
    print( "   -v | --verbose : print verbose output for each test")
    print( "   -b | --bf      : use the brute force algorithm")
    print( "   -n TESTS       : run TESTS number of tests (default 50)")
    print(("   -d DELTA       : the required accuracy delta (see "
           "'close_enough') (default 1.0)"))

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hvbn:d:",
            ["help", "verbose", "bruteforce"])
    except getopt.GetoptError:
        usage()
        return

    verbose = False
    bf = False
    num_tests = 50
    delta = 1.0
    for opt, arg in opts:
        if opt in ["-h", "help"]:
            usage()
            return
        elif opt in ["-v", "verbose"]:
            verbose = True
        elif opt in ["-b", "bruteforce"]:
            bf = True
        elif opt in ["-n"]:
            num_tests = int(arg)
        elif opt in ["-d"]:
            delta = float(arg)

    print("Running {} Limited Infeciton tests...".format(num_tests))

    successes = 0
    accuracies = []
    for i in range(num_tests):
        if verbose:
            print("\n### Limited Infection Test {} ###\n".format(i+1))

        num_students = max(0, int(random.normalvariate(10000, 2500)))
        remaining_students = num_students
        classrooms = []
        while remaining_students > 0:
            classroom_size = max(0, int(random.normalvariate(40, 5)))
            classroom_size = min(remaining_students, classroom_size)
            teacher = Teacher(classroom_size)
            remaining_students -= classroom_size
            classrooms.append(teacher)

        if verbose:
            print("Created {} classrooms with a total of {} users."
                .format(len(classrooms), num_students))

        # aim for 5-20% of the userbase to be infected
        target = int(random.uniform(0.05, 0.20) * num_students)
        if verbose:
            print("Target is {} users, {:.2%} of the userbase."
                .format(target, float(target) / num_students))

        if bf:
            solution = bruteforce(list(classrooms), target)
        else:
            solution = close_enough(list(classrooms), target, delta)

        if solution != None:
            successes += 1
            num_infected = sum(c.num_users for c in solution)
            accuracy = float(abs(num_infected - target)) / target
            accuracies.append(accuracy)

            if verbose:
                print(("Adequate solution found with {} users infected, within "
                       "{:.2%} of the target.").format(num_infected, accuracy))
        else:
            if verbose:
                print("No Adequate solution found.")

    if verbose:
        print("\n")
    print("Success rate: {:.2%}".format(float(successes) / num_tests))
    print("Average accuracy on success: {:.2%}"
        .format(sum(accuracies) / successes))

if __name__ == "__main__":
    main(sys.argv[1:])
