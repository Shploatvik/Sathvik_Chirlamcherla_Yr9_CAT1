import pygame
import numpy as np

# ---------- CONFIG ----------
WIDTH, HEIGHT = 900, 600
BG_COLOR = (235, 235, 240)
PLOT_BG = (245, 245, 250)
AXIS_COLOR = (120, 120, 130)
RECT_COLOR = (180, 210, 240)
RECT_BORDER = (120, 150, 190)
TEXT_COLOR = (40, 40, 50)
ERROR_COLOR = (180, 80, 80)

PLOT_MARGIN = 80

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Riemann Sums - Pygame")
font = pygame.font.SysFont(None, 20)
big_font = pygame.font.SysFont(None, 26)
clock = pygame.time.Clock()


# ---------- SAFE FUNCTION BUILDER ----------
def get_function(formula):
    formula = formula.replace("^", "**")
    allowed = {
        "sin": np.sin,
        "cos": np.cos,
        "tan": np.tan,
        "sqrt": np.sqrt,
        "log": np.log,
        "exp": np.exp,
        "pi": np.pi,
        "e": np.e,
        "abs": np.abs
    }

    def f(x):
        return eval(formula, {"__builtins__": {}}, {**allowed, "x": x})

    return f


# ---------- UI ELEMENTS ----------
class TextBox:
    def __init__(self, x, y, w, h, text="", numeric=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = (220, 220, 230)
        self.color_active = (200, 200, 220)
        self.color = self.color_inactive
        self.text = text
        self.txt_surface = font.render(text, True, TEXT_COLOR)
        self.active = False
        self.numeric = numeric

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.color = self.color_inactive
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                ch = event.unicode
                if self.numeric:
                    if ch in "0123456789.-":
                        self.text += ch
                else:
                    self.text += ch
            self.txt_surface = font.render(self.text, True, TEXT_COLOR)

    def draw(self, surf):
        surf.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(surf, self.color, self.rect, 2)

    def get_value(self):
        return self.text


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, surf):
        pygame.draw.rect(surf, (210, 210, 225), self.rect)
        pygame.draw.rect(surf, (160, 160, 180), self.rect, 2)
        txt = font.render(self.text, True, TEXT_COLOR)
        surf.blit(txt, (self.rect.centerx - txt.get_width() // 2,
                        self.rect.centery - txt.get_height() // 2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# ---------- SETUP INPUTS ----------
lower_box = TextBox(80, 20, 80, 28, "-2", numeric=True)
upper_box = TextBox(240, 20, 80, 28, "2", numeric=True)
rects_box = TextBox(400, 20, 80, 28, "8", numeric=True)
formula_box = TextBox(80, 60, 400, 28, "sin(x+1)", numeric=False)

draw_button = Button(520, 20, 100, 30, "Draw")

error_message = ""
rectangles_data = []  # list of dicts: {screen_rect, area, show_area}
current_bounds = None  # (lower, upper, min_y, max_y)


# ---------- HELPER: MAP TO SCREEN ----------
def world_to_screen(x, y, lower, upper, min_y, max_y):
    plot_left = PLOT_MARGIN
    plot_right = WIDTH - PLOT_MARGIN
    plot_top = PLOT_MARGIN
    plot_bottom = HEIGHT - PLOT_MARGIN

    if upper == lower:
        sx = (plot_left + plot_right) / 2
    else:
        sx = plot_left + (x - lower) / (upper - lower) * (plot_right - plot_left)

    if max_y == min_y:
        sy = (plot_top + plot_bottom) / 2
    else:
        sy = plot_bottom - (y - min_y) / (max_y - min_y) * (plot_bottom - plot_top)

    return int(sx), int(sy)


# ---------- MAIN LOOP ----------
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        lower_box.handle_event(event)
        upper_box.handle_event(event)
        rects_box.handle_event(event)
        formula_box.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if draw_button.is_clicked(event.pos):
                error_message = ""
                rectangles_data = []
                current_bounds = None

                # Parse inputs
                try:
                    lower = float(lower_box.get_value())
                    upper = float(upper_box.get_value())
                    n_rects = int(rects_box.get_value())
                    formula = formula_box.get_value().strip().lower()
                    if upper <= lower:
                        raise ValueError("Upper bound must be greater than lower bound.")
                    if n_rects <= 0:
                        raise ValueError("Rectangles must be positive.")
                    if "x" not in formula:
                        raise ValueError("Formula must contain x.")
                    f = get_function(formula)
                    # test
                    f(0)
                except Exception as e:
                    error_message = f"Error: {e}"
                    continue

                # Compute data
                try:
                    width = (upper - lower) / n_rects
                    left_edges = np.linspace(lower, upper - width, n_rects)
                    sample_x = left_edges + width / 2  # midpoint
                    heights = f(sample_x)

                    # y-range for plotting
                    xs_dense = np.linspace(lower, upper, 400)
                    ys_dense = f(xs_dense)
                    all_y = np.concatenate([ys_dense, heights])
                    min_y = float(np.min(all_y))
                    max_y = float(np.max(all_y))
                    if min_y == max_y:
                        min_y -= 1
                        max_y += 1

                    current_bounds = (lower, upper, min_y, max_y)

                    rectangles_data = []
                    for x_left, h in zip(left_edges, heights):
                        area = abs(h * width)
                        # screen rect
                        x0, y0 = world_to_screen(x_left, 0, lower, upper, min_y, max_y)
                        x1, y1 = world_to_screen(x_left + width, h, lower, upper, min_y, max_y)
                        rect_left = min(x0, x1)
                        rect_right = max(x0, x1)
                        rect_top = min(y0, y1)
                        rect_bottom = max(y0, y1)
                        screen_rect = pygame.Rect(rect_left, rect_top,
                                                  rect_right - rect_left,
                                                  rect_bottom - rect_top)
                        rectangles_data.append({
                            "rect": screen_rect,
                            "area": area,
                            "height": h,
                            "show_area": False
                        })
                except Exception as e:
                    error_message = f"Error while computing: {e}"
                    rectangles_data = []
                    current_bounds = None

            else:
                # Click on rectangles to toggle area display
                for r in rectangles_data:
                    if r["rect"].collidepoint(event.pos):
                        r["show_area"] = not r["show_area"]

    # ---------- DRAW ----------
    screen.fill(BG_COLOR)

    # Input labels
    screen.blit(font.render("Lower:", True, TEXT_COLOR), (30, 25))
    screen.blit(font.render("Upper:", True, TEXT_COLOR), (190, 25))
    screen.blit(font.render("Rectangles:", True, TEXT_COLOR), (320, 25))
    screen.blit(font.render("Formula:", True, TEXT_COLOR), (20, 65))

    lower_box.draw(screen)
    upper_box.draw(screen)
    rects_box.draw(screen)
    formula_box.draw(screen)
    draw_button.draw(screen)

    # Error message
    if error_message:
        err_surf = font.render(error_message, True, ERROR_COLOR)
        screen.blit(err_surf, (PLOT_MARGIN, HEIGHT - 30))

    # Plot area background
    plot_rect = pygame.Rect(PLOT_MARGIN, PLOT_MARGIN,
                            WIDTH - 2 * PLOT_MARGIN,
                            HEIGHT - 2 * PLOT_MARGIN)
    pygame.draw.rect(screen, PLOT_BG, plot_rect)
    pygame.draw.rect(screen, (210, 210, 220), plot_rect, 1)

    # Draw graph and rectangles if we have data
    if current_bounds is not None:
        lower, upper, min_y, max_y = current_bounds

        # Axes (x=0 and y=0 if in range)
        if lower <= 0 <= upper:
            x0, y0 = world_to_screen(0, min_y, lower, upper, min_y, max_y)
            x1, y1 = world_to_screen(0, max_y, lower, upper, min_y, max_y)
            pygame.draw.line(screen, AXIS_COLOR, (x0, y0), (x1, y1), 1)
        if min_y <= 0 <= max_y:
            x0, y0 = world_to_screen(lower, 0, lower, upper, min_y, max_y)
            x1, y1 = world_to_screen(upper, 0, lower, upper, min_y, max_y)
            pygame.draw.line(screen, AXIS_COLOR, (x0, y0), (x1, y1), 1)

        # Function curve
        xs_dense = np.linspace(lower, upper, 400)
        ys_dense = get_function(formula_box.get_value().strip().lower())(xs_dense)
        points = [world_to_screen(x, y, lower, upper, min_y, max_y)
                  for x, y in zip(xs_dense, ys_dense)]
        if len(points) > 1:
            pygame.draw.lines(screen, (100, 130, 180), False, points, 2)

        # Rectangles
        for r in rectangles_data:
            pygame.draw.rect(screen, RECT_COLOR, r["rect"])
            pygame.draw.rect(screen, RECT_BORDER, r["rect"], 1)
            if r["show_area"]:
                area_text = f"{r['area']:.3f}"
                txt = font.render(area_text, True, TEXT_COLOR)
                tx = r["rect"].centerx - txt.get_width() // 2
                ty = r["rect"].centery - txt.get_height() // 2
                screen.blit(txt, (tx, ty))

        # Total area
        total_area = sum(r["area"] for r in rectangles_data)
        ta_text = big_font.render(f"Total |area| ≈ {total_area:.5f}", True, TEXT_COLOR)
        screen.blit(ta_text, (PLOT_MARGIN, HEIGHT - 55))

    pygame.display.flip()

pygame.quit()
