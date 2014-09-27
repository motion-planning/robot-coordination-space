# Truck
test = ''

for x in range(-75, -50):
    test += str(2) + ' '
    test += str(x) + ' '
    test += str(25) + ' '
    test += str(0) + ' '

for x in range(-50, 51):
    test += str(2) + ' '
    test += str(x) + ' '
    test += str(25 - (2500 - x ** 2) ** 0.5) + ' '
    test += str(0) + ' '

for x in range(51, 75):
    test += str(2) + ' '
    test += str(x) + ' '
    test += str(25) + ' '
    test += str(0) + ' '
print test

# Crane
test = ''

for x in range(-75, -50):
    test += str(3) + ' '
    test += str(x) + ' '
    test += str(-25) + ' '
    test += str(0) + ' '

for x in range(-50, 51):
    test += str(3) + ' '
    test += str(x) + ' '
    test += str((2500 - x ** 2) ** 0.5 - 25) + ' '
    test += str(0) + ' '

for x in range(51, 75):
    test += str(3) + ' '
    test += str(x) + ' '
    test += str(-25) + ' '
    test += str(0) + ' '
print test

# Human
test = ''

for x in range(-50, 0):
    test += str(1) + ' '
    test += str(x) + ' '
    test += str(x - 50) + ' '
    test += str(0) + ' '

for y in range(-50, 51):
    test += str(1) + ' '
    test += str(0) + ' '
    test += str(y) + ' '
    test += str(0) + ' '

for x in range(1, 50):
    test += str(1) + ' '
    test += str(x) + ' '
    test += str(x + 50) + ' '
    test += str(0) + ' '
print test
