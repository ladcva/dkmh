# class Dog:
#     def __init__(self) -> None:
#         self.bark()

# def make_class(x):
#     class Dog:
#         def __init__(self, name) -> None:
#             self.name = name
        
#         def print_value(self):
#             print(x)

#     return Dog

# cls = make_class(10)
# d = cls("Duc")
# print(d.name)

# for i in range(10):
#     def show():
#         print(i*2)

# show()

# import inspect

# def func(x):
#     if x == 1:
#         def rv():
#             print('X is equal to 1 !')
#     else:
#         def rv():
#             print('X is not 1 !')

#     return rv

# new_func = func(2)
# print(inspect.getsource(new_func))

import inspect
from queue import Queue

print(inspect.getsource(Queue))