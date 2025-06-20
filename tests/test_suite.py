#-------------------- Imports --------------------

import types

#-------------------- Testing Suite --------------------

class TestClass1():
    """
    Random Docstring created for testing purposes.
    """
    name: str
    age: int
    grades: list[int]
    is_active: bool

    def __init__(self, name: str, age: int, grades: list[int], is_active: bool):
        self.name = name
        self.age = age
        self.grades = grades
        self.is_active = is_active

    def get_average(self):
        return round(sum(self.grades) / len(self.grades), 2)
    
class TestClass2():
    """
    Random Docstring created for testing purposes.
    """
    __slots__ = ("name", "age", "grades", "is_active")

    def __init__(self, name: str, age: int, grades: list[int], is_active: bool):
        self.name = name
        self.age = age
        self.grades = grades
        self.is_active = is_active

    def get_average(self):
        return round(sum(self.grades) / len(self.grades), 2)
        
tc1 = TestClass1(
    name="Renoir Dessendre",
    age=50,
    grades= [50, 60, 70, 80, 90],
    is_active=True
)

tc2 = TestClass2(
    name="Verso Dessendre",
    age=31,
    grades= [60, 65, 75, 55, 60],
    is_active=False
)



print(TestClass1.__mro__)