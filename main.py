import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
import numpy as np

fig = plt.figure(figsize=(10, 6))

page1 = plt.axes([0,0,1,1])
page1.set_facecolor('lightgoldenrodyellow')
 # Start with page2 hidden
page2 = fig.add_subplot(111)
page2.set_visible(False) 
page2_bg = plt.axes([0, 0, 1, 1])
page2_bg.set_facecolor("peachpuff")
page2_bg.set_visible(False)
page2 = fig.add_subplot(111)
page2.set_visible(False) 
page2_bg.set_xticks([])
page2_bg.set_yticks([])

button_enabled = False
# functions to switch between pages
def show_page1():
    page1.set_visible(True)
    page2.set_visible(False)
    page2_bg.set_visible(False)
    fig.canvas.draw_idle()

back_ax = page2_bg.inset_axes([0.02, 0.9, 0.15, 0.07])
back_button = Button(back_ax, "Back")
back_button.on_clicked(lambda *args: show_page1())

def show_page2(*args):
    if button_enabled:
        page1.set_visible(False)
        page2_bg.set_visible(True)
        page2.set_visible(True)
        
        lower = float(lower_box.text)
        upper = float(upper_box.text)
        rects = int(rects_box.text)
        formula = formula_box.text
        method = method_box.text.lower()
        f = get_function(formula)
        page2_setup(lower, upper, rects, formula, method,f)
        fig.canvas.draw_idle()

# the def functions to validate all the input
def is_float(s):
    try:
        float(s)
        return True
    except:
        return False
def is_int(s):
    try:
        int(s)
        return True
    except:
        return False

def valid_input(lower, upper, rect, formula, method):
    if not is_float(lower):
        return False
    if not is_float(upper):
        return False
    if float(upper) <= float(lower):
        return False
    if not is_int(rect):
        return False
    if int(rect) <= 0:
        return False
    if "x" not in formula:
        return False
    if method.lower() not in ["left", "right", "midpoint"]:
        return False
    return True

def validate_inputs(*args):
    global button_enabled

    # 1. Read all textbox values
    lower = lower_box.text
    upper = upper_box.text
    rect  = rects_box.text
    formula = formula_box.text
    method  = method_box.text

    # 2. Check if valid
    if valid_input(lower, upper, rect, formula, method):
        button_enabled = True
        graph.color = "palegreen"
        graph.hovercolor = "mediumseagreen"
    else:
        button_enabled = False
        graph.color = "lightcoral"
        graph.hovercolor = "indianred"

    # 3. Redraw UI
    fig.canvas.draw_idle()

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

# page one inputs
lower_bound_val = page1.inset_axes([0.1, 0.8, 0.3, 0.1])
lower_box = TextBox(lower_bound_val, "Lower bound:")
lower_box.on_text_change(validate_inputs)

upper_bound_val = page1.inset_axes([0.1, 0.65, 0.3, 0.1])
upper_box = TextBox(upper_bound_val, "Upper bound:")
upper_box.on_text_change(validate_inputs)

rectangle_amt = page1.inset_axes([0.1, 0.5, 0.3, 0.1])
rects_box = TextBox(rectangle_amt, "Rectangles:")
rects_box.on_text_change(validate_inputs)

formula_input = page1.inset_axes([0.1, 0.35, 0.3, 0.1])
formula_box = TextBox(formula_input, "Formula:")
formula_box.on_text_change(validate_inputs)

ax_method = page1.inset_axes([0.1, 0.2, 0.3, 0.1])
method_box = TextBox(ax_method, "Method:")
method_box.on_text_change(validate_inputs)

graph=Button(page1.inset_axes([0.1, 0.05, 0.3, 0.1]), 'Draw Graph')
graph.on_clicked(show_page2)  # Placeholder for actual graphing function
# ------------------------------------------------------------
# RECTANGLE SETUP
# width: the width of each rectangle
# left_edges: where each rectangle STARTS on the x-axis
# sample_x: where we evaluate the function for height
# ------------------------------------------------------------
def page2_setup(lower_bound, upper_bound, rectangles, formula, method,f):
    page2.clear()
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
            f"Rectangle {i}: width = {round(width, 4)}, "
            f"height = {round(h,4)}, area = {round(area_i,4)}"
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
    page2.plot(x, y, label=f"f(x) = {formula}")
    page2.grid(True)
    for x_left, h in zip(left_edges, heights):
        page2.bar(x_left, h, width=width, align='edge',alpha=0.3, edgecolor='black')
    page2.legend()
plt.show()