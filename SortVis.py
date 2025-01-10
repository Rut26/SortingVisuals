import pygame
import random
import math

pygame.init()

class DrawInformation:
    BLACK = 21, 21, 21
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    DARK_BLUE = 100, 148, 170
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (28, 12, 13),
        (60, 22, 24),
        (89, 33, 36)
    ]

    FONT = pygame.font.SysFont('BebasNeue-Regular', 12) 
    LARGE_FONT = pygame.font.SysFont('AREEIRO DEMO', 30)

    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Visual Sorting Algos")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.DARK_BLUE)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    controls = [
        "R - Reset", "SPACE - Start Sorting", "A - Ascending",
        "D - Descending", "I - Insertion Sort", "B - Bubble Sort",
        "M - Merge Sort"
    ]

    y_offset = 45
    for control in controls:
        text = draw_info.FONT.render(control, 1, draw_info.RED)
        draw_info.window.blit(text, (10, y_offset))
        y_offset += 30

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD,
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]
        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
        
        number_text = draw_info.FONT.render(str(val), 1, draw_info.BLACK)
        draw_info.window.blit(number_text, (x + draw_info.block_width / 2 - number_text.get_width() / 2, y - number_text.get_height()))

    if clear_bg:
        pygame.display.update()

def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst

def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True
                pygame.time.delay(30) 

    return lst

def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True
            pygame.time.delay(30)  

    return lst

def merge_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def merge(left, right):
        result = []
        left_index, right_index = 0, 0
        while left_index < len(left) and right_index < len(right):
            if (left[left_index] <= right[right_index] and ascending) or (left[left_index] >= right[right_index] and not ascending):
                result.append(left[left_index])
                left_index += 1
            else:
                result.append(right[right_index])
                right_index += 1

        result.extend(left[left_index:])
        result.extend(right[right_index:])
        return result

    def merge_sort_recursive(sub_lst, start, end):
        if end - start <= 1:
            return sub_lst[start:end]

        middle = (start + end) // 2
        left = yield from merge_sort_recursive(sub_lst, start, middle)
        right = yield from merge_sort_recursive(sub_lst, middle, end)

        sorted_lst = merge(left, right)
        for i in range(len(sorted_lst)):
            sub_lst[start + i] = sorted_lst[i]
            draw_list(draw_info, {start + i: draw_info.GREEN}, True)
            yield True
        return sub_lst[start:end]

    yield from merge_sort_recursive(lst, 0, len(lst))
    return lst

def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm = merge_sort
                sorting_algo_name = "Merge Sort"

    pygame.quit()

if __name__ == "__main__":
    main()
