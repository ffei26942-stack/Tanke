import pygame
import sys
import math
import random

# 初始化 Pygame
pygame.init()

# 屏幕设置
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("坦克大战 - 简易版")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (30, 144, 255)
RED = (220, 20, 60)
GREEN = (50, 205, 50)
GRAY = (100, 100, 100)

# 玩家坦克类
class PlayerTank:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.speed = 3
        self.angle = 0  # 坦克朝向角度（弧度）
        self.health = 100

    def draw(self, screen):
        # 绘制车身（矩形）
        body = pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)
        pygame.draw.rect(screen, BLUE, body)
        pygame.draw.rect(screen, (0, 0, 139), body, 2)

        # 绘制炮管（从中心向前延伸）
        end_x = self.x + math.cos(self.angle) * 30
        end_y = self.y + math.sin(self.angle) * 30
        pygame.draw.line(screen, (0, 0, 139), (self.x, self.y), (end_x, end_y), 6)

    def move(self, dx, dy):
        self.x = max(self.width//2, min(WIDTH - self.width//2, self.x + dx * self.speed))
        self.y = max(self.height//2, min(HEIGHT - self.height//2, self.y + dy * self.speed))

    def rotate_left(self):
        self.angle -= 0.1

    def rotate_right(self):
        self.angle += 0.1

# 敌方坦克类
class EnemyTank:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.speed = 1.2
        self.health = 100
        self.move_timer = 0

    def draw(self, screen):
        body = pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)
        pygame.draw.rect(screen, RED, body)
        pygame.draw.rect(screen, (139, 0, 0), body, 2)

    def update(self):
        self.move_timer += 1
        if self.move_timer % 90 == 0:
            # 随机改变方向
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])
            self.x = max(self.width//2, min(WIDTH - self.width//2, self.x + dx * self.speed))
            self.y = max(self.height//2, min(HEIGHT - self.height//2, self.y + dy * self.speed))

# 子弹类
class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 7
        self.radius = 4
        self.lifetime = 60  # 子弹存活帧数

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.lifetime -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), self.radius)

    def is_alive(self):
        return self.lifetime > 0 and 0 <= self.x <= WIDTH and 0 <= self.y <= HEIGHT

# 检测碰撞
def check_collision(bullet, enemy):
    dist = math.hypot(bullet.x - enemy.x, bullet.y - enemy.y)
    return dist < (bullet.radius + enemy.width//2)

# 主游戏循环
def main():
    player = PlayerTank(WIDTH // 2, HEIGHT - 100)
    enemy = EnemyTank(WIDTH // 2, 100)
    bullets = []
    score = 0
    game_over = False
    clock_tick = 60

    while True:
        dt = clock.tick(clock_tick)
        screen.fill(BLACK)

        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    # 发射子弹
                    bullets.append(Bullet(player.x, player.y, player.angle))
                if event.key == pygame.K_r and game_over:
                    # 重开
                    main()

        if not game_over:
            # 键盘控制
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_LEFT]:
                player.rotate_left()
            if keys[pygame.K_RIGHT]:
                player.rotate_right()
            if keys[pygame.K_UP]:
                dx = math.cos(player.angle)
                dy = math.sin(player.angle)
            if keys[pygame.K_DOWN]:
                dx = -math.cos(player.angle)
                dy = -math.sin(player.angle)
            player.move(dx, dy)

            # 更新敌人
            enemy.update()

            # 更新并绘制子弹
            for bullet in bullets[:]:
                bullet.update()
                if not bullet.is_alive():
                    bullets.remove(bullet)
                elif check_collision(bullet, enemy):
                    score += 10
                    enemy = EnemyTank(random.randint(100, WIDTH-100), random.randint(50, 150))
                    bullets.remove(bullet)

        # 绘制
        player.draw(screen)
        enemy.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        # 绘制UI
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (20, 20))

        if game_over:
            over_text = font.render("GAME OVER! Press R to Restart", True, RED)
            screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2))

        pygame.display.flip()

if __name__ == "__main__":
    main()