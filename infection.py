class Teacher:
    def __init__(self, num_students = 0):
        self._students = [Student for i in xrange(num_students)]
        self._infected = False;

    @property
    def num_students(self):
        return len(self._students)

    @property
    def num_users(self):
        return 1 + self.num_students

    @property
    def num_infected(self):
        return self.infected + sum(student.infected for student in students)

    @property
    def infected(self):
        return self._infected

    def infect(self, infect = True, spread = True):
        self._infected = infect
        if spread:
            for student in students:
                student.infect(infect)

    def __str__(self):
        return "[{}/{}]".format(self.num_infected(), self.num_users())

class Student:
    def __init__(self, teacher, spread = True):
        self._teacher = teacher
        self._infected = spread and teacher.infected

    @property
    def infected(self):
        return self._infected

    def infect(self, infect = True, spread = True):
        self._infected = infect
        if spread:
            self._teacher.infect(infect)


    