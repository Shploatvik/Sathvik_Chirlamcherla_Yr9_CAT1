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
formula = input("What formula is being used? (eg sin(x), x**2, etc.) ").lower()
rectangles = int(input("How many rectangles do you want to use? "))
method = input("What method do you want to use? (left, right, midpoint) ").lower()
# x and y axis variables
x = np.linspace(lower_bound, upper_bound, 400)
y = get_function(formula)(x)

# rectangles
# compute left edges ONCE
width = (upper_bound - lower_bound) / rectangles
left_edges = np.linspace(lower_bound, upper_bound - width, rectangles)

# compute sample points (your existing logic)
if method == "left":
    sample_x = left_edges
elif method == "right":
    sample_x = left_edges + width
elif method == "midpoint":
    sample_x = left_edges + width/2
f = get_function(formula)
heights = f(sample_x)

# ⭐ DRAW rectangles from left_edges, not sample_x
for x_left, h in zip(left_edges, heights):
    plt.bar(x_left, h, width=width, align='edge',
            alpha=0.3, edgecolor='black')


final_estimate = np.sum(np.abs(heights * width))
print(final_estimate)

# final graphing
plt.plot(x, y, label=f"f(x) = {formula}")
plt.grid(True)
plt.legend()
plt.show()
