#A* và BFS ,nếu A* không tìm được đường đi tối ưu thì BFS sẽ hỗ trợ ( nhiều vật cản thay đổi theo thời gian.)
import pygame
import random
import heapq
from collections import deque

# Khởi tạo pygame
pygame.init()

# Màu sắc
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)  # Màu vật cản

# Kích thước cửa sổ game
width, height = 600, 400
snake_block = 10
snake_speed = 10

# Font chữ
font_style = pygame.font.SysFont("bahnschrift", 25)

# Tạo cửa sổ game
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game with A* and BFS")

# Hiển thị điểm số
def show_score(score):
    value = font_style.render(f"Score: {score}", True, white)
    screen.blit(value, [10, 10])

# Vẽ rắn
def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, green, [x[0], x[1], snake_block, snake_block])

# Hàm heuristic cho A*
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Thuật toán A* tìm đường
def astar_path(start, goal, snake_list, obstacles):
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
            if (0 <= neighbor[0] < width and 0 <= neighbor[1] < height and 
                neighbor not in snake_list and neighbor not in obstacles):
                
                temp_g_score = g_score[current] + 1
                if neighbor not in g_score or temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return []  # Không tìm thấy đường đi

# Thuật toán BFS để tìm đường bất kỳ
def bfs_find_path(start, snake_list, obstacles):
    queue = deque([start])
    visited = set()
    
    while queue:
        current = queue.popleft()
        for dx, dy in [(-snake_block, 0), (snake_block, 0), (0, -snake_block), (0, snake_block)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if (0 <= neighbor[0] < width and 0 <= neighbor[1] < height and 
                neighbor not in snake_list and neighbor not in obstacles and neighbor not in visited):
                return neighbor  # Trả về ô trống có thể đi
            queue.append(neighbor)
            visited.add(neighbor)
    
    return None

# Hàm tạo vật cản
def generate_obstacles(num, snake_list, food):
    obstacles = set()
    while len(obstacles) < num:
        obs = (random.randrange(0, width - snake_block, snake_block),
               random.randrange(0, height - snake_block, snake_block))
        if obs != food and obs not in snake_list:
            obstacles.add(obs)
    return list(obstacles)

# Vòng lặp chính
def game_loop():
    global snake_speed

    x, y = width // 2, height // 2
    snake_list = []
    snake_length = 1

    food = (random.randrange(0, width - snake_block, snake_block), 
            random.randrange(0, height - snake_block, snake_block))
    
    obstacles = generate_obstacles(20, snake_list, food)

    clock = pygame.time.Clock()

    while True:
        screen.fill(black)

        # Tìm đường bằng A*
        path = astar_path((x, y), food, snake_list, obstacles)

        if not path:
            # Nếu A* thất bại, thử BFS
            next_move = bfs_find_path((x, y), snake_list, obstacles)
            if not next_move:
                # Nếu BFS cũng thất bại, chọn hướng đi ngẫu nhiên an toàn
                next_move = random_safe_move(x, y, snake_list, obstacles)
        else:
            next_move = path[0]

        x, y = next_move

        # Vẽ thức ăn
        pygame.draw.rect(screen, red, [food[0], food[1], snake_block, snake_block])

        # Vẽ vật cản
        for ox, oy in obstacles:
            pygame.draw.rect(screen, blue, [ox, oy, snake_block, snake_block])

        # Cập nhật rắn
        snake_head = [x, y]
        snake_list.append(snake_head)
        
        if len(snake_list) > snake_length:
            del snake_list[0]

        draw_snake(snake_block, snake_list)
        show_score(snake_length - 1)

        pygame.display.update()

        # Khi rắn ăn thức ăn
        if (x, y) == food:
            food = (random.randrange(0, width - snake_block, snake_block), 
                    random.randrange(0, height - snake_block, snake_block))
            obstacles = generate_obstacles(100, snake_list, food)  # Tạo lại vật cản mới
            snake_length += 3  # Rắn dài thêm 3 khối
            
            # Tăng tốc độ rắn mỗi lần ăn
            if snake_length % 5 == 0:
                snake_speed += 1  

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Chạy game
game_loop()
