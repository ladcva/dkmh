# # import inspect

# # x = [1, 2,3]
# # y = [4, 5]

# # print(x + y)

# class Person:
#     def __init__(self, name) -> None:
#         self.name = name

#     def __repr__(self) -> str:
#         return f"Person({self.name})"

#     def __mul__(self, x):
#         if type(x) is not int:
#             raise Exception("Invalid arguements, must be int")

#         self.name = self.name * x

#     def __call__(self, y):
#         print("Called this function", y)

#     def __len__(self):
#         return len(self.name)

# p = Person('Duc')
# p(4)
# print(p.__len__())

from queue import Queue
import inspect


class Queue(q):
    def __repr__(self) -> str:
        return f"Queue()"

    def __setattr__(self, __name: str, __value: Any) -> None:
        return super().__setattr__(__name, __value)
