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

    def get_student(self, id = 0):
        """Gets the student in this classroom with the given ID, ranging from 0
           to num_students-1

        @param id : the ID of student
        """
        return self._students[id]

    def get_random_student(self):
        """Gets a random student in this classroom."""
        if self.num_students == 0:
            return None
        return random.choice(self._students)
        return self.get_student(random.randint(0, self.num_students-1))

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
