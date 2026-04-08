import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
import numpy as np
import pygame
#stting the size of the window and creating the different layers for the pages.
fig = plt.figure(figsize=(10, 6))

# PAGE 1 (bottom layer)
page1 = plt.axes([0,0,1,1])
page1.set_facecolor('lightgoldenrodyellow')
# PAGE 2 BACKGROUND (middle layer, full screen)
page2_bg = plt.axes([0,0,1,1]) # full screen background for page 2
page2_bg.set_visible(False) #makes it invisible until we switch to page 2
page2_bg.set_xticks([])
page2_bg.set_yticks([])
page2_bg.set_frame_on(False)

# PAGE 2 GRAPH (top layer, normal subplot)
page2 = fig.add_subplot(111)
page2.set_visible(False)

# --- BACK BUTTON (store its axes so we can hide/show it) ---
back_ax = page2_bg.inset_axes([0.02, 0.9, 0.15, 0.07]) #sets the axis of the back button
back_button = Button(back_ax, "Back") #makes a button and adds text
back_ax.set_visible(False)   # hidden until page2 is shown

button_enabled = False # the global button state variable is triggered as false until all the inputs are valid

#this definition shows the first page. 
def show_page1(*args): 
    page1.set_visible(True)# the first poage is visible
    graph_ax.set_visible(True)     # show Draw Graph button again
    page2.set_visible(False) # hide the graph
    page2_bg.set_visible(False) # hide the background
    back_ax.set_visible(False) # hide the back button
    fig.canvas.draw_idle()

back_button.on_clicked(show_page1) # this sets the function for what happens if the button is presssed. Here its it shows page 1

def show_page2(*args):
    if button_enabled:
        page1.set_visible(False) # hide page 1
        graph_ax.set_visible(False)   # hide Draw Graph button
        page2_bg.set_visible(True) # the background is shown
        page2.set_visible(True) # the graph is shown
        back_ax.set_visible(True) # the back button is shown

        lower = float(lower_box.text) # the lower bound is taken from the text box and converted to a float
        upper = float(upper_box.text) # the upper bound is taken from the text box and converted to a float
        rects = int(rects_box.text) # the number of rectangles is coverted to an int from the text box
        formula = formula_box.text # then the formula
        method = method_box.text.lower() # then the method 
        f = get_function(formula) # we define f here - using the get function formula to convert the formula in the textbox to real maths. 

        page2_setup(lower, upper, rects, formula, method, f) # it sets up page 2 with all the inputs from page one
        fig.canvas.draw_idle()
#pygame visualisation of rectangles based on the height of the rectangles.
def show_pygame_rectangles(left_edges, heights, width, font_path=None):
    pygame.init() # starts pygame
    screen = pygame.display.set_mode((900, 600)) # sets the size of the window
    pygame.display.set_caption("Rectangle Results") # we give it a title to the window

    # Load custom font or fallback
    try:
        font = pygame.font.Font("Saira_Stencil/SairaStencil-VariableFont_wdth,wght.ttf", 20) # i downloaded this
    except:
        font = pygame.font.SysFont("arial", 20)
    rectangles = len(left_edges) # the number of rectangles is the length of the left edges array
    areas = np.abs(heights * width) # this is the absolute area of each rectangle, which is the height times the width. 

    # Layout
    PADDING = 40 
    BAR_X = 80
    MAX_BAR_W = 740
    MIN_BAR_H = 28
    BAR_H = max(MIN_BAR_H, (600 - 2*PADDING) // rectangles)

    # Scrolling
    scroll_offset = 0 # this alllows for scrolling if there are too many rectangles to fit on the screen
    max_scroll = max(0, rectangles * BAR_H - 520) # this sets the maximum amount of scrolling from 0 to rectangle * bar height minus 520 

    # Width scaling
    max_height = max(abs(heights)) if max(abs(heights)) != 0 else 1 # it scales the width of the rectangle based on the maximum height in teh graph.
    #in a way, this becomes a less clear visualisation of the actual graph, but has all the areas asnd stuff in each rectangle.
    running = True
    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()# this gets teh position of the mouse while we are using the pygame window.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # if the user clicks the X button on the window, it will quit the program and it wont runn anymore

            # Scroll wheel
            if event.type == pygame.MOUSEWHEEL:
                scroll_offset -= event.y * 30#it just takes the scroll motion and multplies it by 30 pixels and subtracts from the scroll offset.
                scroll_offset = max(-max_scroll, min(0, scroll_offset))# makes sure the scroll stays within teh bounds of max and 0

        screen.fill((245, 245, 245)) #its the colour og the screen

        title = font.render("Rectangle Results", True, (40, 40, 40))# its the titke of the page
        screen.blit(title, (BAR_X, 10)) 

        for i, (x_left, h, area) in enumerate(zip(left_edges, heights, areas)):
            y = PADDING + i * BAR_H + scroll_offset # it just pairs the lenghts, areas and heights of hte rectangles together. 

            # Skip if off-screen
            if y < -50 or y > 650:
                continue# if teh vertical postoition is off screen it just skips it. 

            # Width scaling based on |height|
            scaled_width = MAX_BAR_W * (abs(h) / max_height) # it scales the width of the rectangle based on the maximum height in teh graph.

            # Base rectangle
            rect = pygame.Rect(BAR_X, y, scaled_width, BAR_H - 6)

            # Hover detection
            hovered = rect.collidepoint(mouse_x, mouse_y)

            # Colors
            base_color = (150, 190, 255) if h >= 0 else (255, 160, 160)
            hover_color = (120, 160, 230) if h >= 0 else (230, 120, 120) # these are some colours which are used

            color = hover_color if hovered else base_color # changes colour if a mouse hovers over teh rectangle. 

            # Hover expansion
            draw_rect = rect.copy()
            if hovered:
                draw_rect.inflate_ip(10, 4) # it maeks the rectangle bigger if you hover over it. 

            pygame.draw.rect(screen, color, draw_rect, border_radius=6)
            pygame.draw.rect(screen, (60, 60, 60), draw_rect, 1, border_radius=6)

            # Text (only if not too many)
            if rectangles <= 40: # if the number of rectangles is more than 40 it wont work because the text will be too small and it will just be a mess, so it only shows the text if there are 40 or less rectangles.
                text_str = (
                    f"Rect {i+1} | x={x_left:.4f} to {x_left + width:.4f} | w={width:.4f} | "
                    f"h={h:.4f} | area={area:.4f}"
                ) # it writes teh area, height, width and x values of each rectangle in the graph depending on the recangle number. 
                text = font.render(text_str, True, (20, 20, 20))
                screen.blit(text, (BAR_X + 10, y + (BAR_H - text.get_height())/2))

        pygame.display.flip()

    pygame.quit() # its the end of the loop

# ------------------------------------------------------------
# INPUT VALIDATION
# ------------------------------------------------------------
def is_float(s):
    try:
        float(s)
        return True
    except:
        return False # this is to detect if a number is a float or not - uses try to detect and return false or true

def is_int(s):
    try:
        int(s)
        return True
    except:
        return False # this is to detect if a number is an integer or not - uses try to detect and return false or true

def valid_input(lower, upper, rect, formula, method):
    if not is_float(lower):
        return False # if its not a flowat it returns false
    if not is_float(upper):
        return False # if it is not a float it also returns false
    if float(upper) <= float(lower):
        return False # if the upper bound is less than or equal to the lower bound, then it is said to be false
    if not is_int(rect):
        return False # if the amount of rectangles are not an integer then it is false
    if int(rect) <= 0:
        return False # if the number of rectangles is not positive, its false
    if "x" not in formula:
        return False # if the formula doesn't contain x then it is false
    if method.lower() not in ["left", "l", "right", 'r',"midpoint",'m']:
        return False # if teh method id not one of these options then it is false
    return True

def validate_inputs(*args):
    global button_enabled

    lower = lower_box.text
    upper = upper_box.text
    rect  = rects_box.text
    formula = formula_box.text
    method  = method_box.text # just assigns all of these variables to teh input
    message = ""
    if not is_float(lower):
        message = "Lower bound must be a number."  # these lines all set the message to be the first detected error
    elif not is_float(upper):
        message = "Upper bound must be a number."
    elif float(upper) <= float(lower):  # this will then determine if the button allows you to move the the next screen or not
        message = "Upper bound must be greater than lower bound."
    elif not is_int(rect):
        message = "Number of rectangles must be an integer." # when all of these errors in inout are fixed
    elif int(rect) <= 0:
        message = "Number of rectangles must be positive."
    elif "x" not in formula:                      # then the graph can be drawn
        message = "Formula must contain the variable 'x'."
    elif method.lower() not in ["left", "right", "midpoint"]:
        message = "Method must be one of: left, right, midpoint."

    if message == "": # if the message is empty, then there are no errors, and the button allows you to go to page 2
        button_enabled = True
        graph.color = "palegreen" #. turns green
        graph.hovercolor = "mediumseagreen" # if hovered on then it turns this colur
        error_text.set_text("") # if there are no errors then there is no error message
    else: # however if the messafe is anything else ... 
        button_enabled = False # button is not enabled
        graph.color = "lightcoral" # this is the colour of the button
        graph.hovercolor = "indianred" #when hovered on it turns induan red
        error_text.set_text(message) #it sends the message to teh error text box on page 1
    fig.canvas.draw_idle()
# this builds safe functions from the formula inoput
def get_function(formula):
    formula = formula.replace("^", "**") # replaces ^ with ** which is num py math for to teh power of.
    allowed = {
        "sin": np.sin,
        "cos": np.cos,
        "sqrt": np.sqrt,
    } # these are the only allowed numpy functions
    def f(x):
        return eval(formula, {"__builtins__": {}}, {**allowed, "x": x}) # this disables all the builtin functins to make sure my computer doesnt get cooked.
    return f # it returns the function f which is the formula that the user inputted, but now its a real function that can be used to calculate the heights of the rectangles and stuff.

# PAGE 1 INPUTS

lower_bound_val = page1.inset_axes([0.5, 0.8, 0.3, 0.1])
lower_box = TextBox(lower_bound_val, "Lower bound:")
lower_box.on_text_change(validate_inputs) #this is the text box to input lower bound

upper_bound_val = page1.inset_axes([0.5, 0.65, 0.3, 0.1])
upper_box = TextBox(upper_bound_val, "Upper bound:")
upper_box.on_text_change(validate_inputs) #this is the text box to input upper bound

rectangle_amt = page1.inset_axes([0.5, 0.5, 0.3, 0.1])
rects_box = TextBox(rectangle_amt, "Rectangles:")
rects_box.on_text_change(validate_inputs) #this is the text box to input number of rectangles

formula_input = page1.inset_axes([0.5, 0.35, 0.3, 0.1])
formula_box = TextBox(formula_input, "Formula: (use 'x' as variable, e.g. 'x^2 + 3')")
formula_box.on_text_change(validate_inputs) #this is the text box to input the formula

ax_method = page1.inset_axes([0.5, 0.2, 0.3, 0.1])
method_box = TextBox(ax_method, "Method: (left, right, midpoint)")
method_box.on_text_change(validate_inputs)  #this is the text box to input the method

# --- DRAW GRAPH BUTTON (store its axes so we can hide/show it) ---
graph_ax = page1.inset_axes([0.5, 0.05, 0.3, 0.1]) # makes the axes of teh button and sets its position and size
graph = Button(graph_ax, 'Draw Graph') #the text on teh button
graph.on_clicked(show_page2) # this sets what will happen when the button is clicked - show page 2

error_ax = page1.inset_axes([0.2, 0.05, 0.5, 0.1])
error_ax.set_xticks([])
error_ax.set_yticks([])
error_ax.set_frame_on(False) # this is the text box for error messages on page 1 - it just sets up the axes and stuff

error_text = error_ax.text(0.02, 0.5, "", fontsize=12, color="red", va="center") # this sets the font colour, alignment, size and position.
# PAGE 2 GRAPHING
def page2_setup(lower_bound, upper_bound, rectangles, formula, method, f): #this sets up the page 2 based on the inputs. 
    page2.clear() # clears anything from page 2 so that it can be redrawn with the new inputs
    page2_bg.set_facecolor("peachpuff") 
    width = (upper_bound - lower_bound) / rectangles # this is the width of each rectangle, total width / rectangles. 
    left_edges = np.linspace(lower_bound, upper_bound - width, rectangles) # this is the x value of the left edge of each rectangle, which is an array of values from lower bound to upper bound minus width, with the number of rectangles.
    page2.set_title(f"Estimated Area for - f(x) = {formula} & Method: {method.title()}") # sets teh title of the graph based on the formula and teh method
    if method == "left" or method == "l": # if the method is left, then the x value used to calculate the height of the rectangle is the left edge of the rectangle
        sample_x = left_edges
    elif method == "right": # if teh method is right, it uses the right edge of hte rectangle to calculate the height - left + width
        sample_x = left_edges + width
    elif method == "midpoint": # if the method is midpoint, it uses the middle of the rectangle to caluclate the height which is left +1/2width
        sample_x = left_edges + width / 2

    heights = f(sample_x) # this calculates the heights of the rectangles by plugging in the sample x values into the function f, which is the formula that the user inputted.

    print("\n--- Total Area ---- Method:", method.capitalize(), "--------") # it prints the method and the area of the rectagles and is the title in output. 
    for i, (x_left, h) in enumerate(zip(left_edges, heights), start=1): # it basically starts from 1 and joins up the heights and left edges togethr
        area_i = abs(h * width) # those two are used to calculate the area of each rectangle.
        print(
            f"Rectangle {i}: width = {round(width, 4)}, " 
            f"height = {round(h,4)}, area = {round(area_i,4)}" # this prints the width, height, and areas of each rectangle rounde to 4 dec.
        ) #it then lists everything out inthe output of teh thingy. 

    final_area = np.sum(np.abs(heights * width)) # this calculates the total area by summing up the absolute values of the individual areas.
    print(f'Total absolute area estimate: {final_area}') # it finally prints the positive total area out.

    x = np.linspace(lower_bound, upper_bound, 400) # it basically makes the borders of the graph the lower and upper bounds, and it makes 400 points in between to make a smooth graph of the function.
    y = f(x) # the y axis is the function values at the x values.
    
    page2.plot(x, y, label=f"f(x) = {formula}") # it plots the graph of the function on page 2
    page2.grid(True) # it adds a grid to the graph to make it easier to see the values and stuff

    for x_left, h in zip(left_edges, heights):
        page2.bar(x_left, h, width=width, align='edge',
                  alpha=0.3, edgecolor='black') # it draws all the erctangles on the graph based ont he left edge, height anf stuff

    page2.legend() # it adds a legend to the graph to show the formula
    show_pygame_rectangles(left_edges, heights, width) # it shows the pygame visualisation of the rectangles based on the heights and stuff

plt.show() # shows the whole thing. 
