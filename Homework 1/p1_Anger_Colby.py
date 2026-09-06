import math
import matplotlib.pyplot as plt


def build_domain(a, b, c, disc):
    if disc >= 0:
        sqrt_disc = math.sqrt(disc)
        x1 = (-b - sqrt_disc) / (2 * a)
        x2 = (-b + sqrt_disc) / (2 * a)
        left_root = min(x1, x2)
        right_root = max(x1, x2)
        width = right_root - left_root

        if width == 0:
            margin = 2.0
        else:
            margin = width

        xmin = left_root - margin
        xmax = right_root + margin
    else:
        xopt = -b / (2 * a)
        xmin = xopt - 5.0
        xmax = xopt + 5.0

    return xmin, xmax


def plot_quadratic(a, b, c, xmin, xmax):
    n = 150
    step = (xmax - xmin) / (n - 1)

    xs = []
    ys = []

    for i in range(n):
        x = xmin + i * step
        y = a * x ** 2 + b * x + c
        xs.append(x)
        ys.append(y)

    plt.figure()
    plt.plot(xs, ys, marker='o', markersize=2)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'y = {a}x^2 + {b}x + {c}')
    plt.grid(True)
    plt.show()


while True:
    a_text = input('Enter a: ')
    if a_text == '':
        break

    b_text = input('Enter b: ')
    c_text = input('Enter c: ')

    a = float(a_text)
    b = float(b_text)
    c = float(c_text)

    disc = b ** 2 - 4 * a * c

    if disc < 0:
        print('no real solutions')
    elif disc == 0:
        x1 = -b / (2 * a)
        print(f'one solution: {x1:.5f}')
    else:
        sqrt_disc = math.sqrt(disc)
        x1 = (-b - sqrt_disc) / (2 * a)
        x2 = (-b + sqrt_disc) / (2 * a)
        print(f'two solutions: x1={x1:.5f} x2={x2:.5f}')

    xmin, xmax = build_domain(a, b, c, disc)
    plot_quadratic(a, b, c, xmin, xmax)
