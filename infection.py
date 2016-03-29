#!/usr/bin/env python3

import random

class Teacher:
    """Holds a typical classroom with a single Teacher and many Students."""

    def __init__(self, num_students = 0):
        """Creates a new, uninfected classroom.

        @param num_students : the number of students in the classroom, default 0
        """
        self._infected = False;
        self._students = [Student(self) for i in range(num_students)]

    @property
    def num_students(self):
        """The number of students in this classroom (not including the 
           teacher)."""
        return len(self._students)

    @property
    def num_users(self):
        """The number of total users in this classroom (including the 
           teacher)."""
        return 1 + self.num_students

    @property
    def num_infected(self):
        """The number of infected users in this classroom (including the
           teacher)."""
        return self.infected + sum(student.infected for student in self._students)

    @property
    def infected(self):
        """Whether the teacher of this classroom has been infected.

        Typically, but not always, students will be infected when the teacher
            is.
        """
        return self._infected

    def infect(self, infect = True, spread = True):
        """Infects (or uninfects) this classroom.

        @param infect : whether to toggle the infection on or off, default True
        @param spread : whether to spread the infection to all the students in
                        the classroom, default True
        """
        self._infected = infect
        if spread:
            for student in self._students:
                student.infect(infect, False)

    def __str__(self):
        return "[{}/{}]".format(self.num_infected, self.num_users)

class Student:
    def __init__(self, teacher, spread = True):
        """Creates a new student in the given classroom.

        @param teacher : the Teacher of this student
        @param spread : whether to automatically infect this student if the
                        teacher is infected, default True
        """
        self._teacher = teacher
        self._infected = spread and teacher.infected

    @property
    def infected(self):
        """Whether this student is infected."""
        return self._infected

    def infect(self, infect = True, spread = True):
        """Infects this student, typically spreading the infection to its
           classroom.

        @param infect : whether the toggle the infection on or off, default True
        @param spread : whether to spread the infection to all the the rest of
                        the classroom, default True
        """
        self._infected = infect
        if spread:
            self._teacher.infect(infect, True)

def test(verbose = False):
    """Runs correctness tests, first pre-defined then randomized scenarios.

    Aborts on error, or prints a success message if all tests were passed."""

    t1 = Teacher(1)
    t2 = Teacher(30)
    t3 = Teacher(7)

    assert t1.num_students == 1  and t1.num_users == 2
    assert t2.num_students == 30 and t2.num_users == 31
    assert t3.num_students == 7  and t3.num_users == 8
    assert t1.infected == False and t1.num_infected == 0
    assert t2.infected == False and t2.num_infected == 0
    assert t3.infected == False and t3.num_infected == 0

    t1.infect(infect = True)
    t1.infect(infect = False)
    t2.infect()
    t3.infect(spread = False)

    assert t1.infected == False and t1.num_infected == 0
    assert t2.infected == True  and t2.num_infected == 31
    assert t3.infected == True  and t3.num_infected == 1

    NUM_TESTS = 3

    classrooms = []
    for i in range(NUM_TESTS):
        if verbose:
            print("\n### Randomized Test {} ###\n".format(i+1))

        num_students = max(0, int(random.normalvariate(500, 50)))
        remaining_students = num_students
        while remaining_students > 0:
            classroom_size = max(0, int(random.normalvariate(30, 10)))
            classroom_size = min(remaining_students, classroom_size)
            teacher = Teacher(classroom_size)
            remaining_students -= classroom_size

            assert teacher.num_students == classroom_size
            assert teacher.num_users == 1 + classroom_size
            assert teacher.infected == False
            assert teacher.num_infected == 0

            if verbose:
                print("Created classroom with {} students.".format(classroom_size))

    if verbose:
        print("\n")
    print("All tests passed.")

if __name__ == "__main__":
    test(verbose = True)
    