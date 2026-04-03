import matplotlib.pyplot as plt
import numpy as np


# Simple get_function: returns a callable f(x) built from the user's expression string.
# This accepts basic arithmetic, the power operator ** (or ^ which will be converted),
# and the functions sin/cos/tan.
def get_function(expr: str):
    # This is the function header that defines a function named `get_function`.
    # `def` tells Python we are creating a function. `get_function` is the name you call.
    # `(expr: str)` names the single parameter `expr` and includes a type hint `: str`
    # which says "expr is expected to be a string" (type hints are for humans/tools only).
    # The colon `:` starts the indented function body that follows.
    
    s = expr.replace('^', '**').strip()
    # This line creates a new local variable `s`. It takes the input string `expr`,
    # calls the string method `.replace('^', '**')` which returns a new string where
    # every caret character `^` is replaced by Python's exponent operator `**`.
    # That makes `x^2` behave like `x**2`. After replacing, `.strip()` removes leading
    # and trailing whitespace so stray spaces won't cause syntax problems.
    # The resulting sanitized expression is stored in `s`.
    
    env = {'sin': np.sin, 'cos': np.cos, 'tan': np.tan, 'np': np}
    # This line builds a dictionary called `env` that maps short names to the real
    # NumPy functions/modules you want available inside the expression.
    # The key `'sin'` maps to the actual function `np.sin`, so when the evaluated
    # code calls `sin(x)` it will run `np.sin(x)`. Including `'np': np` lets users
    # optionally write `np.sin(x)` if they prefer. This `env` will be passed to
    # `eval(...)` so these names resolve correctly inside the created lambda.
    
    try:
        # Begin a try block: we attempt to build the lambda and return it.
        # If anything goes wrong (syntax error, unknown name, etc.) the except
        # block below will catch the exception so we can raise a clearer error.
        
        return eval('lambda x: ' + s, {}, env)
        # This is the core: we build a string that looks like a Python lambda,
        # for example 'lambda x: sin(x) + x**2'. `eval(...)` executes that string
        # as Python code and returns the resulting function object.
        # The first argument to eval is the expression string to evaluate.
        # The second argument here is a globals dictionary (`{}`) — emptyBUT  in this
        # minimal version. The third argument is `env`, the locals mapping used
        # during evaluation so names like `sin` resolve to `np.sin`.
        # The function returned by eval accepts a parameter `x`. When you later
        # call `f = get_function(...); y = f(x_array)`, NumPy will compute the
        # expression elementwise on the array.
        
    except Exception as e:
        # If any error occurs inside the try block (for example the user typed
        # `x**` or `sin(` with a syntax error, or used a name not present in `env`),
        # execution jumps here. `Exception as e` captures the error object so we can
        # include its message in the new error we raise next.
        
        raise ValueError(f'Invalid expression: {e}')
        # Re-raise the problem as a `ValueError` with a friendly message. This
        # gives the calling code (your program) a clear signal that the input
        # expression couldn't be turned into a working function, and it shows
        # the original error text inside the message so you can debug input mistakes.


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

    fig = plt.figure(figsize=(9, 5))
    plt.plot(x, y, label=f"f(x) = {func_str}")
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
