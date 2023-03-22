



















#子类
class Person(object):
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender


#父类
class Student(Person):
    def __init__(self, name, gender, score):
        super(Student, self).__init__(name, gender)
        self.score = score


















