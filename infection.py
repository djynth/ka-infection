class Teacher:
    def __init__(self, num_students = 0):
        self._students = [Student for i in xrange(num_students)]
        self._infected = False;

    def num_students(self):
        return len(self._students)

    @property
    def infected(self):
        return self._infected

    def infect(self, infect = True, spread = True):
        self._infected = infect
        if spread:
            for student in students:
                student.infect(infect)

class Student:
    def __init__(self, teacher, spread = True):
        self._teacher = teacher
        self._infected = spread if teacher.infected else False

    @property
    def infected(self):
        return self._infected

    def infect(self, infect = True, spread = True):
        self._infected = infect
        if spread:
            self._teacher.infect(infect)
    