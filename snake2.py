# A* 
import pygame
import random
import heapq

# Khởi tạo pygame
pygame.init()

# Định nghĩa màu sắc
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)

# Kích thước cửa sổ game
width = 600
height = 400

# Kích thước khối rắn
snake_block = 10
snake_speed = 10  # Tốc độ ban đầu

# Font chữ
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 20)

# Tạo cửa sổ game
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game with A* Pathfinding")

# Hiển thị điểm số
def show_score(score):
    value = score_font.render(f"Score: {score}", True, white)
    screen.blit(value, [10, 10])

# Vẽ rắn
def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, green, [x[0], x[1], snake_block, snake_block])

# Hàm heuristic cho A*
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Thuật toán A* tìm đường
def astar_path(start, goal, snake_list):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]
        
        for dx, dy in [(-snake_block, 0), (snake_block, 0), (0, -snake_block), (0, snake_block)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < width and 0 <= neighbor[1] < height and neighbor not in snake_list:
                temp_g_score = g_score[current] + 1
                if neighbor not in g_score or temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return []

# Vòng lặp chính
def game_loop():
    global snake_speed  

    x, y = width // 2, height // 2
    
    snake_list = []
    snake_length = 1
    
    food_positions = [(random.randrange(0, width - snake_block, snake_block),
                       random.randrange(0, height - snake_block, snake_block)) for _ in range(3)]
    
    clock = pygame.time.Clock()
    
    while True:
        food_x, food_y = min(food_positions, key=lambda food: heuristic((x, y), food))
        path = astar_path((x, y), (food_x, food_y), snake_list)
        if path:
            x, y = path[0]
        
        # 🚀 Rắn đi xuyên tường
        x = (x + width) % width
        y = (y + height) % height
        
        screen.fill(black)
        
        # Vẽ thức ăn
        for fx, fy in food_positions:
            pygame.draw.rect(screen, red, [fx, fy, snake_block, snake_block])
        
        snake_head = [x, y]
        snake_list.append(snake_head)
        
        if len(snake_list) > snake_length:
            del snake_list[0]
        
        # 🚀 Khi rắn ăn chính nó, chỉ mất 3 ô thay vì thua
        for segment in snake_list[:-1]:
            if segment == snake_head:
                snake_length = max(1, snake_length - 1)  
        
        draw_snake(snake_block, snake_list)
        show_score(snake_length - 1)
        
        pygame.display.update()
        
        # Khi rắn ăn thức ăn
        if (x, y) in food_positions:
            food_positions.remove((x, y))
            food_positions.append((random.randrange(0, width - snake_block, snake_block),
                                   random.randrange(0, height - snake_block, snake_block)))
            snake_length += 3  # 🎯 Mỗi lần ăn, rắn dài thêm 3 khối
            
            # Tăng tốc độ rắn mỗi lần ăn
            if snake_length % 5 == 0:
                snake_speed += 1  

        clock.tick(snake_speed)
    
    pygame.quit()
    quit()

# Chạy game
game_loop()
