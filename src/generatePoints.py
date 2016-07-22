import matplotlib.pyplot as plt

test = ''
xs = []
ys = []

for x in xrange(45, 50):
    test += str(1) + ' '
    test += str(x) + ' '
    xs.append(x)
    test += str(x - 20) + ' '
    ys.append(x - 20)
    test += str(0) + ' '
    test += str(0) + ' '
    test += str(0) + ' '
    test += str(0) + ' '

for y in xrange(30, 80):
    test += str(1) + ' '
    test += str(50) + ' '
    xs.append(50)
    test += str(y) + ' '
    ys.append(y)
    test += str(0) + ' '
    test += str(0) + ' '
    test += str(0) + ' '
    test += str(0) + ' '

for x in xrange(50, 55):
    test += str(1) + ' '
    test += str(x) + ' '
    xs.append(x)
    test += str(x + 30) + ' '
    ys.append(x + 30)
    test += str(0) + ' '
    test += str(0) + ' '
    test += str(0) + ' '
    test += str(0) + ' '

print test

plt.plot(xs, ys, color='red')
plt.show()
