import numpy as np


# Сигмоида
def nonlin(x, deriv=False):
    if (deriv == True):
        return x * (1-x)
    return 1 / (1 + np.exp(-x))


# набор входных данных
"""
X = np.array([[1/60, 9/24],
              [1/60, 10/24],
              [1/60, 11/24],
              [1/60, 12/24]])
"""

"""X = np.array([[9/24],
              [10/24],
              [11/24],
              [12/24]])
# выходные данные
y = np.array([0,0,1,1]).T"""

# набор входных данных
X = np.array([[0, 0, 1],
              [0, 1, 1],
              [1, 0, 1],
              [1, 1, 1]])

# выходные данные
y = np.array([[0, 0, 1, 1]]).T

# сделаем случайные числа более определёнными
np.random.seed(2)

# инициализируем веса случайным образом со средним 0
syn0 = 2 * np.random.random((3, 1)) - 1
print("syn0")
print(syn0)

for iter in range(10000):
    # прямое распространение
    l0 = X
    print('dot')
    print(np.dot(l0, syn0))
    l1 = nonlin(np.dot(l0, syn0))
    print('l1')
    print(l1)

    # насколько мы ошиблись?
    l1_error = y - l1
    print('error')
    print(l1_error)

    # перемножим это с наклоном сигмоиды
    # на основе значений в l1
    l1_delta = l1_error * nonlin(l1, True)  # !!!

    # обновим веса
    syn0 += np.dot(l0.T, l1_delta)  # !!!

print("Выходные данные после тренировки:")
print(l1)