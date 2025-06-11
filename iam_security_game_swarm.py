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
pygame.display.set_caption("AWS IAM Security Adventure - Swarm Attack")

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
    def __init__(self, risk_text, player_pos):
        self.risk_text = risk_text
        
        # 文字列の長さに基づいて幅を計算
        font = get_japanese_font(12)
        text_surface = font.render(self.risk_text, True, STAR_WHITE)
        text_width = text_surface.get_width()
        self.width = max(text_width + 10, 60)
        self.height = 25
        
        # 画面の端からランダムに出現
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        
        if edge == 'top':
            self.x = random.randint(0, SCREEN_WIDTH - self.width)
            self.y = -self.height
        elif edge == 'bottom':
            self.x = random.randint(0, SCREEN_WIDTH - self.width)
            self.y = SCREEN_HEIGHT
        elif edge == 'left':
            self.x = -self.width
            self.y = random.randint(0, SCREEN_HEIGHT - self.height)
        else:  # right
            self.x = SCREEN_WIDTH
            self.y = random.randint(0, SCREEN_HEIGHT - self.height)
        
        # プレイヤーに向かう方向を計算
        player_x, player_y = player_pos
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # 正規化して速度を設定
        if distance > 0:
            speed = random.uniform(2, 5)
            self.vel_x = (dx / distance) * speed
            self.vel_y = (dy / distance) * speed
        else:
            self.vel_x = 0
            self.vel_y = 0
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = random.choice([PLASMA_RED, COSMIC_ORANGE, VOID_PURPLE, GALAXY_PINK])
        self.pulse = random.randint(0, 59)
        
        # 軌道の微調整
        self.wobble_angle = random.uniform(0, 2 * math.pi)
        self.wobble_speed = random.uniform(0.05, 0.15)
        self.wobble_strength = random.uniform(0.5, 2.0)
    
    def update(self, player_pos):
        # プレイヤーに向かって移動
        self.x += self.vel_x
        self.y += self.vel_y
        
        # 軽い軌道変化（ホーミング効果）
        player_x, player_y = player_pos
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # 軽いホーミング効果
            homing_strength = 0.02
            self.vel_x += (dx / distance) * homing_strength
            self.vel_y += (dy / distance) * homing_strength
        
        # 微細な軌道変化
        self.wobble_angle += self.wobble_speed
        wobble_x = math.sin(self.wobble_angle) * self.wobble_strength
        wobble_y = math.cos(self.wobble_angle) * self.wobble_strength
        
        self.x += wobble_x
        self.y += wobble_y
        
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.pulse = (self.pulse + 1) % 60
    
    def draw(self, screen):
        # パルス効果
        pulse_intensity = int(20 * math.sin(self.pulse * 0.2))
        main_color = tuple(max(0, min(255, c + pulse_intensity)) for c in self.color)
        
        # メインボディ
        pygame.draw.rect(screen, main_color, self.rect)
        pygame.draw.rect(screen, STAR_WHITE, self.rect, 1)
        
        # 危険マーク
        center_x = self.rect.centerx
        center_y = self.rect.centery
        
        # 小さな三角形の警告マーク
        size = 4
        triangle_points = [
            (center_x - size, center_y + size),
            (center_x + size, center_y + size),
            (center_x, center_y - size)
        ]
        pygame.draw.polygon(screen, SOLAR_YELLOW, triangle_points)
        
        # リスクテキスト
        font = get_japanese_font(10)
        text = font.render(self.risk_text, True, STAR_WHITE)
        text_rect = text.get_rect(center=(center_x, center_y + 12))
        screen.blit(text, text_rect)
    
    def is_off_screen(self):
        margin = 100
        return (self.x < -margin or self.x > SCREEN_WIDTH + margin or 
                self.y < -margin or self.y > SCREEN_HEIGHT + margin)

class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.width = 50
        self.height = 50
        self.speed = 7
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.shield_animation = 0
    
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
        
        self.x = max(25, min(self.x, SCREEN_WIDTH - self.width - 25))
        self.y = max(25, min(self.y, SCREEN_HEIGHT - self.height - 25))
        
        self.rect.x = self.x
        self.rect.y = self.y
        self.shield_animation = (self.shield_animation + 1) % 60
    
    def draw(self, screen):
        center_x = self.rect.centerx
        center_y = self.rect.centery
        
        # 外側のエネルギーシールド（アニメーション）
        shield_radius = 25 + int(5 * math.sin(self.shield_animation * 0.2))
        pygame.draw.circle(screen, CYBER_CYAN, (center_x, center_y), shield_radius, 2)
        
        # メインシールド
        pygame.draw.circle(screen, NEBULA_BLUE, (center_x, center_y), 20, 3)
        pygame.draw.circle(screen, LASER_GREEN, (center_x, center_y), 15)
        
        # 中央のコア
        pygame.draw.circle(screen, STAR_WHITE, (center_x, center_y), 8)
        
        # IAMテキスト
        font = get_japanese_font(16)
        text = font.render("IAM", True, SPACE_BLACK)
        text_rect = text.get_rect(center=(center_x, center_y))
        screen.blit(text, text_rect)
    
    def get_position(self):
        return (self.rect.centerx, self.rect.centery)

def spawn_swarm(player_pos, iam_risks, count=30):
    """大量の敵を一気に生成"""
    swarm = []
    for _ in range(count):
        risk = SecurityRisk(random.choice(iam_risks), player_pos)
        swarm.append(risk)
    return swarm

def main():
    player = Player()
    risks = []
    spawn_timer = 0
    score = 0
    wave = 1
    game_over = False
    
    # IAMリスク
    iam_risks = [
        "ルートアカウント使用", "弱いパスワード", "MFA未設定", "過度な権限付与",
        "権限昇格攻撃", "クロスアカウント侵害", "一時認証情報漏洩", "未使用ユーザー放置",
        "アクセスキー漏洩", "シークレット平文保存", "認証情報ハードコード", "ローテーション未実施",
        "ワイルドカード乱用", "リソース制限なし", "条件設定不備", "継承権限過多",
        "AssumeRole悪用", "フェデレーション攻撃", "サービスロール乗っ取り", "IAMロール連鎖攻撃"
    ]
    
    # 最初の大群を生成
    risks.extend(spawn_swarm(player.get_position(), iam_risks, 30))
    print(f"Wave {wave}: {len(risks)}体の敵を生成！")
    
    running = True
    while running and not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r and game_over:
                    # リスタート
                    risks.clear()
                    risks.extend(spawn_swarm(player.get_position(), iam_risks, 30))
                    score = 0
                    wave = 1
                    game_over = False
                    player.x = SCREEN_WIDTH // 2
                    player.y = SCREEN_HEIGHT // 2
        
        if not game_over:
            # 更新
            player.update()
            
            for risk in risks[:]:
                risk.update(player.get_position())
                if risk.is_off_screen():
                    risks.remove(risk)
                    score += 10
                elif player.rect.colliderect(risk.rect):
                    game_over = True
                    print(f"ゲームオーバー！ Wave {wave}, スコア: {score}")
            
            # 新しい波の生成
            if len(risks) < 5:  # 敵が少なくなったら新しい波
                wave += 1
                new_count = min(30 + wave * 5, 50)  # 徐々に増加、最大50体
                risks.extend(spawn_swarm(player.get_position(), iam_risks, new_count))
                print(f"Wave {wave}: {len(risks)}体の敵を生成！")
        
        # 描画
        screen.fill(SPACE_BLACK)
        
        # 星を描画
        for i in range(100):
            x = (i * 37) % SCREEN_WIDTH
            y = (i * 23) % SCREEN_HEIGHT
            brightness = 100 + (i * 7) % 155
            color = (brightness, brightness, brightness)
            pygame.draw.circle(screen, color, (x, y), 1)
        
        if not game_over:
            player.draw(screen)
        
        for risk in risks:
            risk.draw(screen)
        
        # UI表示
        font = get_japanese_font(24)
        score_text = font.render(f"スコア: {score}", True, CYBER_CYAN)
        wave_text = font.render(f"Wave: {wave}", True, LASER_GREEN)
        enemy_text = font.render(f"敵: {len(risks)}", True, PLASMA_RED)
        
        screen.blit(score_text, (10, 10))
        screen.blit(wave_text, (10, 40))
        screen.blit(enemy_text, (10, 70))
        
        if game_over:
            # ゲームオーバー画面
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(SPACE_BLACK)
            screen.blit(overlay, (0, 0))
            
            font_big = get_japanese_font(48)
            game_over_text = font_big.render("セキュリティ侵害！", True, PLASMA_RED)
            final_score = font.render(f"最終スコア: {score} (Wave {wave})", True, STAR_WHITE)
            restart_text = font.render("R でリスタート、ESC で終了", True, STAR_WHITE)
            
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 100))
            screen.blit(final_score, (SCREEN_WIDTH//2 - final_score.get_width()//2, SCREEN_HEIGHT//2 - 20))
            screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 20))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
