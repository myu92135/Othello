import math
def bol(t, *arg):
     for i in list(*arg):
        bunbo = math.e**(i/t)
        bunsi = sum([math.e**(j/t) for j in list(*arg)])
        print(bunbo/bunsi)

bol(1, [2, 4, 5, 1])