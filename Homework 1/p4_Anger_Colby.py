import math
import matplotlib.pyplot as plt


def plot_function(fun_str, domain, ns):
    xmin, xmax = domain
    step = (xmax - xmin) / (ns - 1)

    xs = []
    ys = []

    for i in range(ns):
        x = xmin + i * step
        y = eval(fun_str)
        xs.append(x)
        ys.append(y)

    print('{:>10s} {:>10s}'.format('x', 'y'))
    print('-' * 21)

    for i in range(ns):
        print('{:>10.4f} {:>+10.4f}'.format(xs[i], ys[i]))

    plt.figure()
    plt.plot(xs, ys, marker='o', markersize=3)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(fun_str)
    plt.grid(True)
    plt.show()


fun_str = input('Enter function with variable x: ')
ns = int(input('Enter number of samples: '))
xmin = float(input('Enter xmin: '))
xmax = float(input('Enter xmax: '))

plot_function(fun_str, (xmin, xmax), ns)
