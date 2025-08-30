"""
Snake Game with A* AI
"""

import pygame, sys, time, random, heapq
difficulty = 20

# Setting
frame_size_x = 600
frame_size_y = 400
cell_size = 20
cols = frame_size_x // cell_size
rows = frame_size_y // cell_size

# Init
check_errors = pygame.init()
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

game_window = pygame.display.set_mode((frame_size_x, frame_size_y))
pygame.display.set_caption('Snake Game With A* AI')
fps_controller = pygame.time.Clock()

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)

# Snake & Food      
snake = [(0, 0)]
random.seed(0)
food = (random.randint(0, cols - 1), random.randint(0, rows - 1))
score = 0
# A* Functions
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) #manhattan distance

def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < cols and 0 <= ny < rows:
            neighbors.append((nx, ny))
    return neighbors

def astar(start, goal, obstacles):
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start, []))
    visited = set()
    while open_set:
        _, cost, current, path = heapq.heappop(open_set)
        if current in visited:
            continue
        visited.add(current)
        path = path + [current]
        # with open("astar_log.txt", "a", encoding="utf-8") as f:
        #     f.write(f"\n--- A* Step ---\n")
        #     f.write(f"Current: {current}, Cost={cost}\n")
        #     f.write(f"Food: {food}\n")
        #     f.write(f"Open set: {open_set}\n")
        #     f.write(f"Visited: {visited}\n")
        #     f.write(f"Path so far: {path}\n")
        if current == goal:
            return path[1:]  # exclude current

        for neighbor in get_neighbors(current):
            if neighbor in visited or neighbor in obstacles:
                continue
            heapq.heappush(open_set, (cost + 1 + heuristic(neighbor, goal), cost + 1, neighbor, path))
    return []

def draw():
    game_window.fill(black)
    for x, y in snake:
        pygame.draw.rect(game_window, green, (x * cell_size, y * cell_size, cell_size, cell_size))
    pygame.draw.rect(game_window, white, (food[0] * cell_size, food[1] * cell_size, cell_size, cell_size))
    show_score(1, white, 'consolas', 20)
    pygame.display.update()

def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        # score_rect.midtop = (frame_size_x/10, 15)
        score_rect.topleft = (10,10)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)

def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/3)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()



# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    head = snake[0]
    path = astar(head, food, snake[1:])

    if not path:
        game_over()

    next_cell = path[0]
    new_head = next_cell

    # Collision check
    if new_head in snake or not (0 <= new_head[0] < cols) or not (0 <= new_head[1] < rows):
        game_over()

    snake.insert(0, new_head)

    if new_head == food:
        score += 1
        while True:
            new_food = (random.randint(0, cols - 1), random.randint(0, rows - 1))
            if new_food not in snake:
                food = new_food
                break
    else:
        snake.pop()

    draw()
    fps_controller.tick(difficulty)
