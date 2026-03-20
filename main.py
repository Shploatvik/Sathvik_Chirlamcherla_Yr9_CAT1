import numpy as np
import matplotlib.pyplot as plt

# Safely evaluate user-entered function
def f(func_str, x):
    allowed = {
        "x": x,
        "np": np,
        "sin": np.sin,
        "cos": np.cos,
        "tan": np.tan,
        "exp": np.exp,
        "sqrt": np.sqrt,
        "log": np.log
    }
    return eval(func_str, {"__builtins__": {}}, allowed)

# -----------------------------
# USER INPUTS
# -----------------------------
func_str = input("Enter a function in terms of x (e.g., x**2 or x**3 + 2): ")
a = float(input("Enter the lower bound: "))
b = float(input("Enter the upper bound: "))
n = int(input("Enter the number of rectangles: "))
method = input("Choose method (left, right, midpoint): ").strip().lower()

# -----------------------------
# COMPUTATION
# -----------------------------
width = (b - a) / n

if method == "left":
    x_samples = np.linspace(a, b - width, n)
elif method == "right":
    x_samples = np.linspace(a + width, b, n)
elif method == "midpoint":
    x_samples = np.linspace(a + width/2, b - width/2, n)
else:
    raise ValueError("Invalid method. Choose left, right, or midpoint.")

heights = f(func_str, x_samples)
areas = heights * width
total_area = np.sum(areas)

print("\n--- Rectangle Areas ---")
for i in range(n):
    print(f"Rectangle {i+1}: height = {heights[i]:.5f}, area = {areas[i]:.5f}")

print(f"\nEstimated total area using {method} rectangles: {total_area:.5f}\n")

# -----------------------------
# GRAPHING
# -----------------------------
x_curve = np.linspace(a, b, 400)
y_curve = f(func_str, x_curve)

plt.figure(figsize=(10, 6))
plt.plot(x_curve, y_curve, label=f"f(x) = {func_str}", color="blue")

# Draw rectangles
for i in range(n):
    # Determine left edge of rectangle
    if method == "left":
        x0 = x_samples[i]
    elif method == "right":
        x0 = x_samples[i] - width
    else:  # midpoint
        x0 = x_samples[i] - width/2

    rect_x = [x0, x0, x0 + width, x0 + width]
    rect_y = [0, heights[i], heights[i], 0]

    plt.fill(rect_x, rect_y, edgecolor="black", alpha=0.3)

plt.title(f"Area Approximation Using {method.capitalize()} Rectangles")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.grid(True)
plt.legend()
plt.show()
