import pygame
import numpy as np

def show_pygame_rectangles(left_edges, heights, width, font_path=None):
    pygame.init()
    screen = pygame.display.set_mode((900, 600))
    pygame.display.set_caption("Rectangle Results")

    # Load custom font or fallback
    if font_path:
        font = pygame.font.Font(font_path, 20)
    else:
        font = pygame.font.SysFont("arial", 20)

    rectangles = len(left_edges)
    areas = np.abs(heights * width)

    # Layout
    PADDING = 40
    BAR_X = 80
    BAR_W = 740
    BAR_H = max(20, (600 - 2*PADDING) // rectangles)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((245, 245, 245))

        title = font.render("Rectangle Results", True, (40, 40, 40))
        screen.blit(title, (BAR_X, 10))

        for i, (x_left, h, area) in enumerate(zip(left_edges, heights, areas)):
            y = PADDING + i * BAR_H

            rect = pygame.Rect(BAR_X, y, BAR_W, BAR_H - 6)

            # Clean single color
            color = (180, 200, 255)
            pygame.draw.rect(screen, color, rect, border_radius=4)
            pygame.draw.rect(screen, (60, 60, 60), rect, 1, border_radius=4)

            # Only print text if not too many rectangles
            if rectangles <= 25:
                text_str = (
                    f"Rect {i+1} | x={x_left:.4f} | w={width:.4f} | "
                    f"h={h:.4f} | area={area:.4f}"
                )
                text = font.render(text_str, True, (20, 20, 20))
                screen.blit(text, (BAR_X + 10, y + (BAR_H - text.get_height())/2))

        pygame.display.flip()

    pygame.quit()
