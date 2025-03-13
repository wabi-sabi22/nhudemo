import pygame
import random
from collections import deque

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
WIDTH, HEIGHT = 400, 400
CELL_SIZE = 20
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

# Màu sắc
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Hướng di chuyển
DIRECTIONS = {'UP': (0, -1), 'DOWN': (0, 1), 'LEFT': (-1, 0), 'RIGHT': (1, 0)}

def generate_food(snake):
    while True:
        food = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if food not in snake:
            return food

def bfs(snake, food):
    queue = deque([(snake[0], [])])  # (vị trí hiện tại, đường đi tới đó)
    visited = set()
    visited.add(snake[0])
    
    while queue:
        (x, y), path = queue.popleft()
        
        if (x, y) == food:
            return path  # Trả về đường đi ngắn nhất
        
        for direction, (dx, dy) in DIRECTIONS.items():
            nx, ny = x + dx, y + dy
            next_pos = (nx, ny)
            
            if (0 <= nx < COLS and 0 <= ny < ROWS and
                next_pos not in snake and next_pos not in visited):
                queue.append((next_pos, path + [direction]))
                visited.add(next_pos)
    return []  # Không tìm thấy đường đi

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake AI - BFS")
    clock = pygame.time.Clock()
    
    snake = [(COLS // 2, ROWS // 2)]
    food = generate_food(snake)
    direction = 'RIGHT'
    
    running = True
    while running:
        screen.fill(WHITE)
        
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Tìm đường đi bằng BFS
        path = bfs(snake, food)
        if path:
            direction = path[0]
        
        # Cập nhật vị trí rắn
        dx, dy = DIRECTIONS[direction]
        new_head = (snake[0][0] + dx, snake[0][1] + dy)
        
        if new_head == food:
            food = generate_food(snake)
        else:
            snake.pop()
        
        if new_head in snake or not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS):
            running = False  # Thua cuộc nếu đâm vào chính mình hoặc tường
        
        snake.insert(0, new_head)
        
        # Vẽ rắn
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Vẽ thức ăn
        pygame.draw.rect(screen, RED, (food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        pygame.display.flip()
        clock.tick(10)
    
    pygame.quit()

if __name__ == "__main__":
    main()