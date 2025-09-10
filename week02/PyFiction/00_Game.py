import pygame, random, sys, os, math, time

# ---- Config ----
TILE_SIZE = 30
GRID_W, GRID_H = 36, 18
STATUS_BAR_HEIGHT = 26
WIDTH, HEIGHT = GRID_W * TILE_SIZE, GRID_H * TILE_SIZE + STATUS_BAR_HEIGHT
SPRITE_PATH = "./mantis.png"
SPRITE_SCALE = 0.8
# ----------------

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("第一章：活路，螳螂VII 的屋頂跳躍")

# use fonts with Unicode support
try:
    font = pygame.font.SysFont("Noto Sans CJK TC", 24)
    small_font = pygame.font.SysFont("Noto Sans CJK TC", 16, bold=True)
    big_font = pygame.font.SysFont("Noto Sans CJK TC", 48, bold=True)
except:
    font = pygame.font.Font(None, 24)
    small_font = pygame.font.Font(None, 16)
    big_font = pygame.font.Font(None, 48)

WHITE = (255,255,255)
GRAY = (200,200,200)
BLACK = (0,0,0)
WHITE_TEXT = (255,255,255)
YELLOW_TEXT = (255,255,180)
BAR_BG = (220,220,220)
EXIT_GREEN = (50, 220, 50)
RED = (220,50,50)

# ---------------- Player Class ----------------
class Player:
    def __init__(self, x, y, hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.sprite = self.load_sprite(SPRITE_PATH, SPRITE_SCALE)

    def load_sprite(self, path, scale=0.9):
        if not os.path.exists(path):
            return None
        img = pygame.image.load(path).convert_alpha()
        side = int(TILE_SIZE * scale)
        return pygame.transform.smoothscale(img, (side, side))

    def move(self, dx, dy, city, exit_pos):
        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < GRID_W and 0 <= ny < GRID_H and city[ny][nx] > 0:
            ch, th = city[self.y][self.x], city[ny][nx]
            msg = "移動成功拿～麼會跳！"
            if th < ch - 5:
                self.hp -= 3
                msg = "兩棟樓高差距太大！重落地 -3 HP"
            self.x, self.y = nx, ny
            if (self.x, self.y) == exit_pos:
                return "🎉 成功逃到城鎮的邊緣！活下來啦！！", True
            return msg, False
        else:
            return "⚠️ 不能跳到那裡！", False

    def draw(self):
        rect = pygame.Rect(self.x*TILE_SIZE, self.y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        if self.sprite:
            px = rect.centerx - self.sprite.get_width()//2
            py = rect.centery - self.sprite.get_height()//2
            screen.blit(self.sprite, (px,py))
        else:
            pygame.draw.circle(screen, (50,100,255), rect.center, TILE_SIZE//3)

# ---------------- City Generation ----------------
city = [[random.randint(1,20) if random.random()<0.6 else 0 for _ in range(GRID_W)] for _ in range(GRID_H)]

player = Player(0, GRID_H-1, hp=87)

# ensure start and exit
if city[player.y][player.x] == 0:
    city[player.y][player.x] = random.randint(4,8)
exit_x, exit_y = GRID_W-1, 0
if city[exit_y][exit_x] == 0:
    city[exit_y][exit_x] = random.randint(5,9)

# carve guaranteed path
cx, cy = player.x, player.y
while cx < exit_x:
    cx += 1
    if city[cy][cx] == 0:
        city[cy][cx] = random.randint(3,8)
while cy > exit_y:
    cy -= 1
    if city[cy][exit_x] == 0:
        city[cy][exit_x] = random.randint(3,8)

exit_pos = (exit_x, exit_y)

# ---------------- Controls ----------------
directions = {
    pygame.K_KP8:(0,-1), pygame.K_KP2:(0,1),
    pygame.K_KP4:(-1,0), pygame.K_KP6:(1,0),
    pygame.K_KP7:(-1,-1), pygame.K_KP9:(1,-1),
    pygame.K_KP1:(-1,1), pygame.K_KP3:(1,1)
}

# ---------------- Drawing ----------------
def building_color_and_text(height):
    if height <= 5:
        return (180,180,180), BLACK
    elif height <= 12:
        return (120,120,120), WHITE_TEXT
    else:
        return (60,80,120), YELLOW_TEXT

def draw_city(frame_count):
    for y in range(GRID_H):
        for x in range(GRID_W):
            h = city[y][x]
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if h > 0:
                if (x,y) == exit_pos:
                    pulse = (math.sin(frame_count*0.1)+1)/2
                    g = int(150 + 100*pulse)
                    exit_color = (50,g,50)
                    pygame.draw.rect(screen, exit_color, rect)
                    num_text = small_font.render("E", True, BLACK)
                else:
                    color, text_color = building_color_and_text(h)
                    pygame.draw.rect(screen, color, rect)
                    num_text = small_font.render(str(h), True, text_color)
                tx = rect.right - num_text.get_width() - 2
                ty = rect.top + 2
                screen.blit(num_text, (tx,ty))
            else:
                pygame.draw.rect(screen, GRAY, rect, 1)

def draw_status_bar(message):
    bar_rect = pygame.Rect(0, GRID_H*TILE_SIZE, WIDTH, STATUS_BAR_HEIGHT)
    pygame.draw.rect(screen, BAR_BG, bar_rect)
    current_h = city[player.y][player.x]
    status_text = f"機體完整度: {player.hp}  當前樓層: {current_h}   {message}"
    text_surface = font.render(status_text, True, BLACK)
    screen.blit(text_surface, (10, GRID_H*TILE_SIZE + (STATUS_BAR_HEIGHT-text_surface.get_height())//2))

def show_center_message(message, duration=2, fade=True):
    start_time = time.time()
    alpha_surface = pygame.Surface((WIDTH, HEIGHT))
    alpha_surface.fill(WHITE)

    while time.time() - start_time < duration:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()

        screen.fill(WHITE)
        draw_city(int((time.time()-start_time)*30))
        player.draw()
        draw_status_bar("")
        # render big red text
        text_surface = big_font.render(message, True, RED)
        tx = (WIDTH - text_surface.get_width())//2
        ty = (HEIGHT - STATUS_BAR_HEIGHT - text_surface.get_height())//2
        screen.blit(text_surface, (tx,ty))

        if fade:
            elapsed = time.time()-start_time
            fade_ratio = elapsed/duration
            fade_alpha = int(255 * fade_ratio)
            if fade_alpha > 0:
                alpha_surface.set_alpha(fade_alpha)
                screen.blit(alpha_surface, (0,0))

        pygame.display.flip()
        pygame.time.delay(30)

# ---------------- Game Loop ----------------
running = True
clock = pygame.time.Clock()
frame_count = 0
status_message = "逃命開始！"
game_over = False

# --- Start message (red, big, fade out) ---
show_center_message("你是全村的希望！", duration=2, fade=True)

while running:
    clock.tick(30)
    frame_count += 1

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        elif e.type == pygame.KEYDOWN:
            if e.key in directions and not game_over:
                dx,dy = directions[e.key]
                status_message, win = player.move(dx,dy,city,exit_pos)
                if win:
                    game_over = True

    if player.hp <= 0 and not game_over:
        status_message = "⚠️ 螳螂VII 摔毁了！"
        game_over = True

    screen.fill(WHITE)
    draw_city(frame_count)
    player.draw()
    draw_status_bar(status_message)
    pygame.display.flip()

    # --- Game over handling ---
    if game_over:
        show_center_message("全村沒希望！", duration=3, fade=False)
        pygame.quit()
        sys.exit()
