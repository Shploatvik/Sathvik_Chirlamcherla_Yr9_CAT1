import matplotlib.pyplot as plt
import numpy as np

# ------------------------------------------------------------
# Function builder: safely turns a string like "sin(x+1)" into
# a real Python function f(x). It restricts what can be used
# inside eval() so the user cannot run dangerous code. It also
# replaces ^ with ** so users can type math naturally.
# ------------------------------------------------------------
def get_function(formula):
    formula = formula.replace("^", "**")
    # Allowed functions
    allowed = {
        "sin": np.sin,
        "cos": np.cos,
        "sqrt": np.sqrt,
    }

    # Build the function safely
    def f(x):
        return eval(formula, {"__builtins__": {}}, {**allowed, "x": x})
    return f
# ------------------------------------------------------------
# INPUT VALIDATION SECTION
# This part ensures the user cannot break the program by typing
# invalid numbers, reversed bounds, missing x in the formula,
# or an invalid method name. Each check gives a clear message.
# ------------------------------------------------------------
try:
    lower_bound = float(input("Enter the lower bound of x: "))
    upper_bound = float(input("Enter the upper bound of x: "))
    if upper_bound <= lower_bound:
        raise ValueError("Upper bound must be greater than lower bound.")
    
    formula = input("Enter the formula (must contain x): ").lower()
    if "x" not in formula:
        raise ValueError("The formula must contain the variable x.")

    rectangles = int(input("How many rectangles? "))
    if rectangles <= 0:
        raise ValueError("Number of rectangles must be positive.")
    
    method = input("Method (left, right, midpoint): ").lower()
    if method not in ["left", "right", "midpoint"]:
        raise ValueError("Method must be left, right, or midpoint.")

except ValueError as e:
    print("Input error:", e)
    exit()
# ------------------------------------------------------------
# FUNCTION EVALUATION
# We now convert the formula string into a real function f(x).
# If the formula is invalid (like "sin(x+"), eval will throw an
# error here, which we catch and report cleanly.
# ------------------------------------------------------------
try:
    f = get_function(formula)
    # Test the function once to ensure it's valid
    f(0)
except Exception:
    print("Your formula is invalid. Please check your syntax.")
    exit()
# ------------------------------------------------------------
# RECTANGLE SETUP
# width: the width of each rectangle
# left_edges: where each rectangle STARTS on the x-axis
# sample_x: where we evaluate the function for height
# ------------------------------------------------------------
width = (upper_bound - lower_bound) / rectangles
left_edges = np.linspace(lower_bound, upper_bound - width, rectangles)

if method == "left":
    sample_x = left_edges
elif method == "right":
    sample_x = left_edges + width
elif method == "midpoint":
    sample_x = left_edges + width / 2

heights = f(sample_x)
# ------------------------------------------------------------
# PRINT PER-RECTANGLE AREA
# This loop prints a clean summary of each rectangle, including
# its x-range, height, and absolute area contribution.
# ------------------------------------------------------------
print("\n--- Total Area ---")
for i, (x_left, h) in enumerate(zip(left_edges, heights), start=1):
    area_i = abs(h * width)
    print(
        f"Rectangle {i}: from x={x_left:.4f} to x={x_left+width:.4f}, "
        f"height={h:.4f}, area={area_i:.4f}"
    )
# ------------------------------------------------------------
# TOTAL AREA
# We compute the absolute area (as you wanted) by summing the
# absolute value of each rectangle's area.
# ------------------------------------------------------------
final_area = np.sum(np.abs(heights * width))
print(f'Total absolute area estimate: {final_area}')
# ------------------------------------------------------------
# GRAPHING
# We draw the function smoothly, then draw each rectangle from
# its left edge with the correct height. align='edge' ensures
# the bars start exactly at the left edge instead of being
# centered, which is crucial for correct Riemann rectangles.
# ------------------------------------------------------------
x = np.linspace(lower_bound, upper_bound, 400)
y = f(x)
plt.plot(x, y, label=f"f(x) = {formula}")
plt.grid(True)
for x_left, h in zip(left_edges, heights):
    plt.bar(x_left, h, width=width, align='edge',alpha=0.3, edgecolor='black', color='orange')
plt.legend()
plt.show()
