from libgravatar import Gravatar

g = Gravatar('ladcva@gmail.com')
g.get_image()
print(g.get_image())

square = lambda x, y: 2*x + 5*y - 12
print(square(14, 11))