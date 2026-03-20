import numpy as np # numpy is needed to calculate huge functions and also knows how to do sine, cos and more
import matplotlib.pyplot as plt  # you need thos to graph all the functions and to also draw the rectangles and more
# this imports numpy as np and also imports matplotlib as plt 

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
#it tells Python which names the user is allowed to use (x, sin, cos, etc.), and then eval uses those allowed names to turn the user’s text into real math that NumPy can compute.
# -----------------------------
# USER INPUTS
# -----------------------------
func_str = input("Enter a function in terms of x (e.g., x**2 or x**3 + 2): ")
a = float(input("Enter the lower bound: "))
b = float(input("Enter the upper bound: "))
n = int(input("Enter the number of rectangles: "))
method = input("Choose method (left, right, midpoint): ").strip().lower()
# it basically asks the user all the vallues that we need to get the rectanfles, the graph and also which rectangle way to use to calculatea the area.
# -----------------------------
# COMPUTATION
# -----------------------------
width = (b - a) / n
# this is needed tp ensure the width of all the rectangles are the same and also is needed to calculate the area of each rectangle
if method == "left":
    x_samples = np.linspace(a, b - width, n)
    # gets the x values at the left of each rectangle eg if you have 5 rectangles it would look like this
    # |---|---|---|---|---|
    # L   L   L   L   L   
    # if you took another L youo would jst be adding an extra rectangle
elif method == "right":
    x_samples = np.linspace(a + width, b, n)
    #eg
    # |---|---|---|---|---|
    #     R   R   R   R   R
    #it measures the point where the right corner of the rectangle touches the curve 
elif method == "midpoint":
    x_samples = np.linspace(a + width/2, b - width/2, n)
    #eg
    # |---|---|---|---|---|
    #   M   M   M   M   M
    #it measures the point where the middle of the rectangle touches the curve
    # also if you didn't undertand yet, x_samples is a list
else:
    raise ValueError("Invalid method. Choose left, right, or midpoint.")
# x_samples represents the x values where you haave to find the height of the curve, as this is the place where the rectangles touches the point
heights = f(func_str, x_samples)
#it finds the height using the function from the start that the user gave and also the llist of x values from the x_samples
heights = np.abs(heights)
# it finds the absolute value of the heights because if you have a negative height it would just subtract from the total area instead of adding to it, so we need to make sure all the heights are positive to get the correct total area
areas = heights * width
# the area of the rectangles is recorded into areas
total_area = np.sum(areas)
# finally the total area is found by adding the areas of all the rectangles together. 

print("\n--- Rectangle Areas ---")
# just printing the heading
for i in range(n):
    print(f"Rectangle {i+1}: height = {heights[i]:.5f}, area = {areas[i]:.5f}")
# it loops the same number as the number of rectangles and prints the area and height of each rectangle

print(f"\nEstimated total area using {method} rectangles: {total_area:.5f}\n")
# prints the total area of all the rectangles combined

# -----------------------------
# GRAPHING
# -----------------------------
x_curve = np.linspace(a, b, 400)
# it makes 400 points between a and b 
y_curve = f(func_str, x_curve)
#this finds the associated y values for each of the x values


plt.figure(figsize=(10, 6))  
# Create a new graph window and set its size (10 inches wide, 6 inches tall)

plt.plot(x_curve, y_curve, label=f"f(x) = {func_str}", color="blue")
# Draw the smooth function curve using the x and y values we calculated earlier


# -----------------------------
# Draw rectangles
# -----------------------------
for i in range(n):
    # Work out where the LEFT EDGE of this rectangle should be
    if method == "left":
        x0 = x_samples[i]                 # left method: sample IS the left edge
    elif method == "right":
        x0 = x_samples[i] - width         # right method: sample is the RIGHT edge, so move left by width
    else:  # midpoint
        x0 = x_samples[i] - width/2       # midpoint method: sample is the middle, so move left by half width

    # The x‑coordinates of the rectangle corners (left bottom, left top, right top, right bottom)
    rect_x = [x0, x0, x0 + width, x0 + width]

    # The y‑coordinates of the rectangle corners (from 0 up to the height, then back to 0)
    rect_y = [0, heights[i], heights[i], 0]

    plt.fill(rect_x, rect_y, edgecolor="black", alpha=0.3)
    # Draw the rectangle with a black outline and a transparent fill


# -----------------------------
# Graph labels and display
# -----------------------------
plt.title(f"Area Approximation Using {method.capitalize()} Rectangles")
# Set the title of the graph

plt.xlabel("x")
# Label the x‑axis

plt.ylabel("f(x)")
# Label the y‑axis

plt.grid(True)
# Turn on grid lines to make the graph easier to read

plt.legend()
# Show the label for the function curve

plt.show()
# Display the final graph window
