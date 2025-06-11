import pygame
import random
import sys
import os
import math

# 初期化
pygame.init()

# 日本語フォント設定
def get_japanese_font(size):
    """日本語対応フォントを取得"""
    font_paths = [
        "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",  # macOS
        "/System/Library/Fonts/Hiragino Sans GB.ttc",  # macOS alternative
        "/System/Library/Fonts/Arial Unicode MS.ttf",  # macOS
        "C:/Windows/Fonts/msgothic.ttc",  # Windows
        "C:/Windows/Fonts/meiryo.ttc",  # Windows
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return pygame.font.Font(font_path, size)
            except:
                continue
    
    # フォールバック：システムデフォルト
    return pygame.font.Font(None, size)

# 画面設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AWS IAM Security Adventure")

# 色定義（宇宙テーマ）
SPACE_BLACK = (10, 10, 25)
STAR_WHITE = (255, 255, 255)
NEBULA_BLUE = (30, 144, 255)
PLASMA_RED = (255, 69, 0)
LASER_GREEN = (0, 255, 127)
COSMIC_ORANGE = (255, 140, 0)
SOLAR_YELLOW = (255, 215, 0)
VOID_PURPLE = (138, 43, 226)
CYBER_CYAN = (0, 255, 255)
ASTEROID_GRAY = (105, 105, 105)
DEEP_SPACE = (25, 25, 112)
GALAXY_PINK = (255, 20, 147)

# フレームレート
clock = pygame.time.Clock()
FPS = 60

class SecurityRisk:
    def __init__(self, risk_text):
        self.risk_text = risk_text
        self.width = 120
        self.height = 35
        
        # シンプルな4方向からの出現
        direction = random.choice(['right', 'left', 'top', 'bottom'])
        
        if direction == 'right':
            self.x = SCREEN_WIDTH
            self.y = random.randint(0, SCREEN_HEIGHT - self.height)
            self.vel_x = -3
            self.vel_y = 0
        elif direction == 'left':
            self.x = -self.width
            self.y = random.randint(0, SCREEN_HEIGHT - self.height)
            self.vel_x = 3
            self.vel_y = 0
        elif direction == 'top':
            self.x = random.randint(0, SCREEN_WIDTH - self.width)
            self.y = -self.height
            self.vel_x = 0
            self.vel_y = 3
        else:  # bottom
            self.x = random.randint(0, SCREEN_WIDTH - self.width)
            self.y = SCREEN_HEIGHT
            self.vel_x = 0
            self.vel_y = -3
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = PLASMA_RED
    
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, STAR_WHITE, self.rect, 2)
        
        font = get_japanese_font(14)
        text = font.render(self.risk_text, True, STAR_WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
    
    def is_off_screen(self):
        return (self.x < -200 or self.x > SCREEN_WIDTH + 200 or 
                self.y < -200 or self.y > SCREEN_HEIGHT + 200)

class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.width = 50
        self.height = 50
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
        
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))
        
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, screen):
        pygame.draw.circle(screen, LASER_GREEN, self.rect.center, 25)
        pygame.draw.circle(screen, STAR_WHITE, self.rect.center, 15)
        
        font = get_japanese_font(16)
        text = font.render("IAM", True, SPACE_BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

def main():
    player = Player()
    risks = []
    spawn_timer = 0
    score = 0
    
    # IAMリスク
    iam_risks = ["ルートアカウント使用", "弱いパスワード", "MFA未設定", "過度な権限付与"]
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # 敵の生成
        spawn_timer += 1
        if spawn_timer >= 60:  # 1秒ごと
            risks.append(SecurityRisk(random.choice(iam_risks)))
            spawn_timer = 0
            print(f"敵を生成しました。現在の敵数: {len(risks)}")
        
        # 更新
        player.update()
        
        for risk in risks[:]:
            risk.update()
            if risk.is_off_screen():
                risks.remove(risk)
                score += 10
            elif player.rect.colliderect(risk.rect):
                print("ゲームオーバー！")
                running = False
        
        # 描画
        screen.fill(SPACE_BLACK)
        
        # 星を描画
        for i in range(50):
            x = (i * 37) % SCREEN_WIDTH
            y = (i * 23) % SCREEN_HEIGHT
            pygame.draw.circle(screen, STAR_WHITE, (x, y), 1)
        
        player.draw(screen)
        
        for risk in risks:
            risk.draw(screen)
        
        # スコア表示
        font = get_japanese_font(24)
        score_text = font.render(f"スコア: {score}", True, STAR_WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
