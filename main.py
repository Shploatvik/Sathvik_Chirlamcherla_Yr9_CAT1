import matplotlib.pyplot as plt
import numpy as np

# all the formulas allowed
def get_function(formula):
    formula= formula.replace('^', '**')
    expressions = { 
        'sin': np.sin,
        'cos': np.cos,
        'sqrt': np.sqrt,
    }
    def f(x):
        return eval(formula, {"__builtins__": {}}, {**expressions, "x": x})
    return f

# input variables
lower_bound = int(input('What is the lower bound of x? '))
upper_bound = int(input('What is the upper bound of x? '))
formula = input("What formula is being used? (eg sin(x), x**2, etc.)")
rectangles = int(input("How many rectangles do you want to use? "))
method = input("What method do you want to use? (left, right, midpoint)")
# x and y axis variables
x = np.linspace(lower_bound, upper_bound, 400)
y = get_function(formula)(x)

# final graphing
plt.plot(x, y, label=f"f(x) = {formula}")
plt.grid(True)
plt.legend()
plt.show()
