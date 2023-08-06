from numpy import diagonal
from numpy import zeros
from sympy import simplify
from sympy import symbols


def coefficients(x, y):
    assert len(x) == len(y), "arguments must have the same size"
    size = len(x)
    result = zeros((size, size))
    result[:, 0] = y
    for column in range(1, size):
        result[column:, column] = (
            (result[column:, column-1] - result[column-1:-1, column-1])
            / (x[column:] - x[:-column])
        )
    return diagonal(result)


def expression(a, x):
    assert len(a) == len(x), "arguments must have the same size"
    size = len(a)

    x_ = symbols('x')
    xs = [1 for i in range(size)]
    result = [a[0] for i in range(size)]
    for i, x_i in enumerate(x[:-1], start=1):
        xs[i] = xs[i-1] * (x_ - x_i)
        result[i] = a[i] * xs[i]

    return simplify(sum(result))


def polynomial(x, y):
    a = coefficients(x, y)
    return expression(a, x)
