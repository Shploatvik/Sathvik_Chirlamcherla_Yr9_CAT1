import matplotlib.pyplot as plt
import numpy as np


def get_function(expr: str):
    s = expr.replace('^', '**').strip()
    env = {'sin': np.sin, 'cos': np.cos, 'tan': np.tan, 'np': np}
    try:
        # Put allowed names into the globals mapping used by eval so
        # the created lambda's globals contain sin/cos/tan when it's called.
        g = {"__builtins__": {}}
        g.update(env)
        return eval('lambda x: ' + s, g)
    except Exception as e:
        raise ValueError(f'Invalid expression: {e}')
def main():
    try:
        lower_bound = float(input('What is the lower bound? '))
        upper_bound = float(input('What is the upper bound? '))
        func_str = input('Enter a function in terms of x (e.g. x**2 or sin(x) ): ')
    except Exception as e:
        print('Invalid input:', e)
        return

    if lower_bound >= upper_bound:
        print('Lower bound must be less than upper bound.')
        return

    x = np.linspace(lower_bound, upper_bound, 400)

    try:
        f = get_function(func_str)
        y = f(x)
    except Exception as e:
        print('Error evaluating expression:', e)
        return
    plt.figure(figsize=(9, 5))
    plt.plot(x, y, label=f"f(x) = {func_str}")
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
