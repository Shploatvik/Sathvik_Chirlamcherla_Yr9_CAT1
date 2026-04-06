import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
import numpy as np
import pygame

fig = plt.figure(figsize=(10, 6))

# PAGE 1 (bottom layer)
page1 = plt.axes([0,0,1,1])
page1.set_facecolor('lightgoldenrodyellow')

# PAGE 2 BACKGROUND (middle layer, full screen)
page2_bg = plt.axes([0,0,1,1])
page2_bg.set_facecolor("peachpuff")
page2_bg.set_visible(False)
page2_bg.set_xticks([])
page2_bg.set_yticks([])
page2_bg.set_frame_on(False)

# PAGE 2 GRAPH (top layer, normal subplot)
page2 = fig.add_subplot(111)
page2.set_visible(False)

# --- BACK BUTTON (store its axes so we can hide/show it) ---
back_ax = page2_bg.inset_axes([0.02, 0.9, 0.15, 0.07])
back_button = Button(back_ax, "Back")
back_ax.set_visible(False)   # hidden until page2 is shown

button_enabled = False


# ------------------------------------------------------------
# PAGE SWITCHING
# ------------------------------------------------------------
def show_page1(*args):
    page1.set_visible(True)
    graph_ax.set_visible(True)     # show Draw Graph button again
    page2.set_visible(False)
    page2_bg.set_visible(False)
    back_ax.set_visible(False)
    fig.canvas.draw_idle()

back_button.on_clicked(show_page1)


def show_page2(*args):
    if button_enabled:
        page1.set_visible(False)
        graph_ax.set_visible(False)   # hide Draw Graph button
        page2_bg.set_visible(True)
        page2.set_visible(True)
        back_ax.set_visible(True)

        lower = float(lower_box.text)
        upper = float(upper_box.text)
        rects = int(rects_box.text)
        formula = formula_box.text
        method = method_box.text.lower()
        f = get_function(formula)

        page2_setup(lower, upper, rects, formula, method, f)
        fig.canvas.draw_idle()

def show_pygame_rectangles(left_edges, heights, width, font_path=None):
    pygame.init()
    screen = pygame.display.set_mode((900, 600))
    pygame.display.set_caption("Rectangle Results")

    # Load custom font or fallback
    try:
        font = pygame.font.Font("Saira_Stencil/SairaStencil-VariableFont_wdth,wght.ttf", 20)
    except:
        font = pygame.font.SysFont("arial", 20)
    rectangles = len(left_edges)
    areas = np.abs(heights * width)

    # Layout
    PADDING = 40
    BAR_X = 80
    MAX_BAR_W = 740
    MIN_BAR_H = 28
    BAR_H = max(MIN_BAR_H, (600 - 2*PADDING) // rectangles)

    # Scrolling
    scroll_offset = 0
    max_scroll = max(0, rectangles * BAR_H - 520)

    # Width scaling
    max_height = max(abs(heights)) if max(abs(heights)) != 0 else 1

    running = True
    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Scroll wheel
            if event.type == pygame.MOUSEWHEEL:
                scroll_offset -= event.y * 30
                scroll_offset = max(-max_scroll, min(0, scroll_offset))

        screen.fill((245, 245, 245))

        title = font.render("Rectangle Results", True, (40, 40, 40))
        screen.blit(title, (BAR_X, 10))

        for i, (x_left, h, area) in enumerate(zip(left_edges, heights, areas)):
            y = PADDING + i * BAR_H + scroll_offset

            # Skip if off-screen
            if y < -50 or y > 650:
                continue

            # Width scaling based on |height|
            scaled_width = MAX_BAR_W * (abs(h) / max_height)

            # Base rectangle
            rect = pygame.Rect(BAR_X, y, scaled_width, BAR_H - 6)

            # Hover detection
            hovered = rect.collidepoint(mouse_x, mouse_y)

            # Colors
            base_color = (150, 190, 255) if h >= 0 else (255, 160, 160)
            hover_color = (120, 160, 230) if h >= 0 else (230, 120, 120)

            color = hover_color if hovered else base_color

            # Hover expansion
            draw_rect = rect.copy()
            if hovered:
                draw_rect.inflate_ip(10, 4)

            pygame.draw.rect(screen, color, draw_rect, border_radius=6)
            pygame.draw.rect(screen, (60, 60, 60), draw_rect, 1, border_radius=6)

            # Text (only if not too many)
            if rectangles <= 40:
                text_str = (
                    f"Rect {i+1} | x={x_left:.4f} | w={width:.4f} | "
                    f"h={h:.4f} | area={area:.4f}"
                )
                text = font.render(text_str, True, (20, 20, 20))
                screen.blit(text, (BAR_X + 10, y + (BAR_H - text.get_height())/2))

        pygame.display.flip()

    pygame.quit()

# ------------------------------------------------------------
# INPUT VALIDATION
# ------------------------------------------------------------
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

    lower = lower_box.text
    upper = upper_box.text
    rect  = rects_box.text
    formula = formula_box.text
    method  = method_box.text

    if valid_input(lower, upper, rect, formula, method):
        button_enabled = True
        graph.color = "palegreen"
        graph.hovercolor = "mediumseagreen"
    else:
        button_enabled = False
        graph.color = "lightcoral"
        graph.hovercolor = "indianred"

    fig.canvas.draw_idle()


# ------------------------------------------------------------
# SAFE FUNCTION BUILDER
# ------------------------------------------------------------
def get_function(formula):
    formula = formula.replace("^", "**")
    allowed = {
        "sin": np.sin,
        "cos": np.cos,
        "sqrt": np.sqrt,
    }
    def f(x):
        return eval(formula, {"__builtins__": {}}, {**allowed, "x": x})
    return f


# ------------------------------------------------------------
# PAGE 1 INPUTS
# ------------------------------------------------------------
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

# --- DRAW GRAPH BUTTON (store its axes so we can hide/show it) ---
graph_ax = page1.inset_axes([0.1, 0.05, 0.3, 0.1])
graph = Button(graph_ax, 'Draw Graph')
graph.on_clicked(show_page2)


# ------------------------------------------------------------
# PAGE 2 GRAPHING
# ------------------------------------------------------------
def page2_setup(lower_bound, upper_bound, rectangles, formula, method, f):
    page2.clear()

    width = (upper_bound - lower_bound) / rectangles
    left_edges = np.linspace(lower_bound, upper_bound - width, rectangles)
    page2.set_title(f"Estimated Area for - f(x) = {formula} & Method: {method.title()}")
    if method == "left":
        sample_x = left_edges
    elif method == "right":
        sample_x = left_edges + width
    elif method == "midpoint":
        sample_x = left_edges + width / 2

    heights = f(sample_x)

    print("\n--- Total Area ---- Method:", method.capitalize(), "--------")
    for i, (x_left, h) in enumerate(zip(left_edges, heights), start=1):
        area_i = abs(h * width)
        print(
            f"Rectangle {i}: width = {round(width, 4)}, "
            f"height = {round(h,4)}, area = {round(area_i,4)}"
        )

    final_area = np.sum(np.abs(heights * width))
    print(f'Total absolute area estimate: {final_area}')

    x = np.linspace(lower_bound, upper_bound, 400)
    y = f(x)
    
    page2.plot(x, y, label=f"f(x) = {formula}")
    page2.grid(True)

    for x_left, h in zip(left_edges, heights):
        page2.bar(x_left, h, width=width, align='edge',
                  alpha=0.3, edgecolor='black')

    page2.legend()
    show_pygame_rectangles(left_edges, heights, width)


plt.show()
