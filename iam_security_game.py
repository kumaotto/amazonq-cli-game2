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

# ゲーム状態
MENU = 0
STAGE_SELECT = 1
LEVEL_SELECT = 2
PLAYING = 3
GAME_OVER = 4

# ステージ設定（宇宙テーマ）
STAGES = {
    1: {
        "name": "IAM基本設定",
        "description": "基本的なIAM設定ミス",
        "background_color": SPACE_BLACK,
        "star_color": NEBULA_BLUE,
        "risks": ["ルートアカウント使用", "弱いパスワード", "MFA未設定", "過度な権限付与"]
    },
    2: {
        "name": "アクセス管理",
        "description": "アクセス制御の脅威",
        "background_color": SPACE_BLACK,
        "star_color": COSMIC_ORANGE,
        "risks": ["権限昇格攻撃", "クロスアカウント侵害", "一時認証情報漏洩", "未使用ユーザー放置"]
    },
    3: {
        "name": "認証情報漏洩",
        "description": "認証情報の不適切な管理",
        "background_color": SPACE_BLACK,
        "star_color": PLASMA_RED,
        "risks": ["アクセスキー漏洩", "シークレット平文保存", "認証情報ハードコード", "ローテーション未実施"]
    },
    4: {
        "name": "ポリシー設定ミス",
        "description": "IAMポリシーの設定不備",
        "background_color": SPACE_BLACK,
        "star_color": VOID_PURPLE,
        "risks": ["ワイルドカード乱用", "リソース制限なし", "条件設定不備", "継承権限過多"]
    },
    5: {
        "name": "高度なIAM攻撃",
        "description": "巧妙なIAM攻撃手法",
        "background_color": SPACE_BLACK,
        "star_color": GALAXY_PINK,
        "risks": ["AssumeRole悪用", "フェデレーション攻撃", "サービスロール乗っ取り", "IAMロール連鎖攻撃"]
    }
}

# 難易度設定（より明確な差をつける）
DIFFICULTY_LEVELS = {
    "簡単": {
        "speed_multiplier": 0.5, 
        "spawn_rate": 2.5, 
        "burst_rate": 3.0,
        "description": "初心者向け - ゆっくりとした動きで少ない敵"
    },
    "普通": {
        "speed_multiplier": 1.0, 
        "spawn_rate": 1.5, 
        "burst_rate": 2.0,
        "description": "標準的な難易度 - バランスの取れた挑戦"
    },
    "難しい": {
        "speed_multiplier": 1.8, 
        "spawn_rate": 0.8, 
        "burst_rate": 1.2,
        "description": "上級者向け - 速い敵と頻繁な攻撃"
    },
    "エキスパート": {
        "speed_multiplier": 2.5, 
        "spawn_rate": 0.4, 
        "burst_rate": 0.6,
        "description": "最高難易度 - 超高速で大量の敵"
    }
}

class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 4  # 中央寄りに配置
        self.y = SCREEN_HEIGHT // 2
        self.width = 50
        self.height = 50
        self.speed = 6
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.shield_animation = 0
        # 慣性システム
        self.vel_x = 0
        self.vel_y = 0
        self.acceleration = 0.8
        self.friction = 0.85
        self.max_speed = 8
    
    def update(self):
        keys = pygame.key.get_pressed()
        
        # 加速度ベースの移動制御
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x -= self.acceleration
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x += self.acceleration
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel_y -= self.acceleration
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel_y += self.acceleration
        
        # 最大速度制限
        self.vel_x = max(-self.max_speed, min(self.max_speed, self.vel_x))
        self.vel_y = max(-self.max_speed, min(self.max_speed, self.vel_y))
        
        # 摩擦による減速
        if not (keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.vel_x *= self.friction
        if not (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_DOWN] or keys[pygame.K_s]):
            self.vel_y *= self.friction
        
        # 位置更新
        self.x += self.vel_x
        self.y += self.vel_y
        
        # 画面境界チェック
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))
        
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # シールドアニメーション
        self.shield_animation = (self.shield_animation + 1) % 60
    
    def draw(self, screen):
        # 宇宙船風のIAMシールド
        center_x = self.rect.centerx
        center_y = self.rect.centery
        
        # 外側のエネルギーシールド（アニメーション）
        shield_radius = 25 + int(5 * math.sin(self.shield_animation * 0.2))
        pygame.draw.circle(screen, CYBER_CYAN, (center_x, center_y), shield_radius, 2)
        
        # 移動方向インジケーター
        if abs(self.vel_x) > 1 or abs(self.vel_y) > 1:
            trail_x = center_x - int(self.vel_x * 3)
            trail_y = center_y - int(self.vel_y * 3)
            pygame.draw.line(screen, LASER_GREEN, (center_x, center_y), (trail_x, trail_y), 3)
        
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

class SecurityRisk:
    def __init__(self, stage_risks, difficulty_multiplier, player_pos, difficulty_level="普通"):
        self.risk_text = random.choice(stage_risks)
        self.difficulty_level = difficulty_level
        
        # 文字列の長さに基づいて幅を計算
        font = get_japanese_font(14)
        text_surface = font.render(self.risk_text, True, STAR_WHITE)
        text_width = text_surface.get_width()
        
        self.width = max(text_width + 20, 80)
        self.height = 35
        
        # 画面の外周からランダムに出現（円形配置）
        angle = random.uniform(0, 2 * math.pi)
        spawn_distance = 400  # 画面中心からの距離
        
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        
        # 出現位置を円形に配置
        self.x = center_x + math.cos(angle) * spawn_distance
        self.y = center_y + math.sin(angle) * spawn_distance
        
        # プレイヤーに向かう方向ベクトルを計算
        player_x, player_y = player_pos
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # 速度設定（難易度に応じて基本速度を調整）
        if difficulty_level == "簡単":
            base_speed = random.uniform(1.5, 3.0)
        elif difficulty_level == "普通":
            base_speed = random.uniform(2.5, 4.5)
        elif difficulty_level == "難しい":
            base_speed = random.uniform(4.0, 6.5)
        elif difficulty_level == "エキスパート":
            base_speed = random.uniform(6.0, 9.0)
        else:
            base_speed = random.uniform(2, 5)
        
        self.speed = base_speed * difficulty_multiplier
        
        if distance > 0:
            # 正規化して方向を決定
            self.vel_x = (dx / distance) * self.speed
            self.vel_y = (dy / distance) * self.speed
        else:
            self.vel_x = 0
            self.vel_y = 0
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # 宇宙風の色とエフェクト
        risk_colors = [PLASMA_RED, COSMIC_ORANGE, VOID_PURPLE, GALAXY_PINK]
        self.color = random.choice(risk_colors)
        self.color = tuple(max(0, min(255, c)) for c in self.color[:3])
        self.pulse_animation = random.randint(0, 59)
        self.trail_particles = []
        
        # ランダムな軌道変化パラメータ（難易度に応じて調整）
        self.orbit_angle = random.uniform(0, 2 * math.pi)
        
        if difficulty_level == "簡単":
            self.orbit_speed = random.uniform(0.01, 0.03)
            self.orbit_radius = random.uniform(5, 15)
            self.homing_strength = random.uniform(0.005, 0.015)
        elif difficulty_level == "普通":
            self.orbit_speed = random.uniform(0.03, 0.06)
            self.orbit_radius = random.uniform(15, 30)
            self.homing_strength = random.uniform(0.01, 0.025)
        elif difficulty_level == "難しい":
            self.orbit_speed = random.uniform(0.06, 0.10)
            self.orbit_radius = random.uniform(25, 45)
            self.homing_strength = random.uniform(0.02, 0.04)
        elif difficulty_level == "エキスパート":
            self.orbit_speed = random.uniform(0.08, 0.15)
            self.orbit_radius = random.uniform(35, 60)
            self.homing_strength = random.uniform(0.03, 0.06)
        else:
            self.orbit_speed = random.uniform(0.03, 0.08)
            self.orbit_radius = random.uniform(15, 40)
            self.homing_strength = random.uniform(0.01, 0.03)
        
        # 攻撃パターン（難易度に応じて複雑さを調整）
        if difficulty_level == "簡単":
            self.attack_pattern = random.choice(['direct', 'direct', 'curve'])  # 簡単なパターンが多い
        elif difficulty_level == "普通":
            self.attack_pattern = random.choice(['direct', 'spiral', 'curve'])
        elif difficulty_level == "難しい":
            self.attack_pattern = random.choice(['direct', 'spiral', 'zigzag', 'curve'])
        elif difficulty_level == "エキスパート":
            self.attack_pattern = random.choice(['spiral', 'zigzag', 'curve', 'spiral'])  # 複雑なパターンが多い
        else:
            self.attack_pattern = random.choice(['direct', 'spiral', 'zigzag', 'curve'])
        
        self.pattern_timer = 0
    
    def update(self, player_pos):
        player_x, player_y = player_pos
        
        # 攻撃パターンに基づく移動
        if self.attack_pattern == 'direct':
            # 直接攻撃 + 軽いホーミング
            dx = player_x - self.x
            dy = player_y - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0:
                self.vel_x += (dx / distance) * self.homing_strength
                self.vel_y += (dy / distance) * self.homing_strength
        
        elif self.attack_pattern == 'spiral':
            # スパイラル攻撃
            self.orbit_angle += self.orbit_speed
            spiral_x = math.cos(self.orbit_angle) * self.orbit_radius * 0.1
            spiral_y = math.sin(self.orbit_angle) * self.orbit_radius * 0.1
            
            # プレイヤー方向 + スパイラル
            dx = player_x - self.x
            dy = player_y - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0:
                self.vel_x = (dx / distance) * self.speed * 0.7 + spiral_x
                self.vel_y = (dy / distance) * self.speed * 0.7 + spiral_y
        
        elif self.attack_pattern == 'zigzag':
            # ジグザグ攻撃
            self.pattern_timer += 1
            zigzag_strength = 3
            
            if self.pattern_timer % 30 < 15:
                perpendicular_x = -self.vel_y / (math.sqrt(self.vel_x**2 + self.vel_y**2) + 0.001)
                perpendicular_y = self.vel_x / (math.sqrt(self.vel_x**2 + self.vel_y**2) + 0.001)
            else:
                perpendicular_x = self.vel_y / (math.sqrt(self.vel_x**2 + self.vel_y**2) + 0.001)
                perpendicular_y = -self.vel_x / (math.sqrt(self.vel_x**2 + self.vel_y**2) + 0.001)
            
            self.vel_x += perpendicular_x * zigzag_strength
            self.vel_y += perpendicular_y * zigzag_strength
        
        elif self.attack_pattern == 'curve':
            # カーブ攻撃
            self.orbit_angle += self.orbit_speed
            curve_strength = 2
            
            curve_x = math.sin(self.orbit_angle) * curve_strength
            curve_y = math.cos(self.orbit_angle) * curve_strength
            
            self.vel_x += curve_x
            self.vel_y += curve_y
        
        # 基本移動
        self.x += self.vel_x
        self.y += self.vel_y
        
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.pulse_animation = (self.pulse_animation + 1) % 60
        
        # パーティクルトレイル効果
        if random.random() < 0.4:
            particle = {
                'x': self.rect.centerx,
                'y': self.rect.centery,
                'life': 15,
                'color': self.color,
                'vel_x': -self.vel_x * 0.2 + random.uniform(-1, 1),
                'vel_y': -self.vel_y * 0.2 + random.uniform(-1, 1)
            }
            self.trail_particles.append(particle)
        
        # パーティクル更新
        for particle in self.trail_particles[:]:
            particle['life'] -= 1
            particle['x'] += particle['vel_x']
            particle['y'] += particle['vel_y']
            particle['vel_x'] *= 0.9
            particle['vel_y'] *= 0.9
            if particle['life'] <= 0:
                self.trail_particles.remove(particle)
    
    def draw(self, screen):
        # パーティクルトレイル描画
        for particle in self.trail_particles:
            if particle['life'] > 0:
                safe_color = tuple(max(0, min(255, c)) for c in particle['color'][:3])
                alpha_factor = particle['life'] / 15
                faded_color = tuple(int(c * alpha_factor) for c in safe_color)
                pygame.draw.circle(screen, faded_color, (int(particle['x']), int(particle['y'])), 2)
        
        # メインの脅威オブジェクト（宇宙船風）
        pulse_intensity = max(-50, min(50, int(20 * math.sin(self.pulse_animation * 0.2))))
        
        # 外側のエネルギーフィールド
        pygame.draw.rect(screen, self.color, 
                        (self.rect.x - 2, self.rect.y - 2, self.rect.width + 4, self.rect.height + 4))
        
        # メインボディ
        main_color = tuple(max(0, min(255, c + pulse_intensity)) for c in self.color)
        pygame.draw.rect(screen, main_color, self.rect)
        pygame.draw.rect(screen, STAR_WHITE, self.rect, 2)
        
        # 危険マーク
        center_x = self.rect.centerx
        center_y = self.rect.centery
        
        # 三角形の警告マーク
        triangle_points = [
            (center_x - 8, center_y + 6),
            (center_x + 8, center_y + 6),
            (center_x, center_y - 6)
        ]
        pygame.draw.polygon(screen, SOLAR_YELLOW, triangle_points)
        pygame.draw.polygon(screen, PLASMA_RED, triangle_points, 2)
        
        # 感嘆符
        font_small = get_japanese_font(12)
        exclamation = font_small.render("!", True, SPACE_BLACK)
        exclamation_rect = exclamation.get_rect(center=(center_x, center_y))
        screen.blit(exclamation, exclamation_rect)
        
        # リスクテキスト（下部に表示）
        font = get_japanese_font(12)
        text = font.render(self.risk_text, True, STAR_WHITE)
        text_rect = text.get_rect(center=(center_x, self.rect.bottom + 10))
        
        # テキスト背景
        bg_rect = pygame.Rect(text_rect.x - 5, text_rect.y - 2, text_rect.width + 10, text_rect.height + 4)
        pygame.draw.rect(screen, SPACE_BLACK, bg_rect)
        pygame.draw.rect(screen, self.color, bg_rect, 1)
        
        screen.blit(text, text_rect)
    
    def is_off_screen(self):
        margin = 150
        return (self.x < -margin or 
                self.x > SCREEN_WIDTH + margin or 
                self.y < -margin or 
                self.y > SCREEN_HEIGHT + margin)

class Goal:
    def __init__(self):
        self.x = SCREEN_WIDTH - 80
        self.y = SCREEN_HEIGHT // 2 - 40
        self.width = 80
        self.height = 80
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.glow_animation = 0
    
    def update(self):
        self.glow_animation = (self.glow_animation + 1) % 120
    
    def draw(self, screen):
        # 宇宙ステーション風のセキュアクラウド
        center_x = self.rect.centerx
        center_y = self.rect.centery
        
        # 外側のエネルギーリング（アニメーション）
        glow_radius = 45 + int(10 * math.sin(self.glow_animation * 0.1))
        for i in range(3):
            radius = glow_radius - i * 5
            alpha = 100 - i * 30
            pygame.draw.circle(screen, LASER_GREEN, (center_x, center_y), radius, 2)
        
        # メインステーション
        pygame.draw.circle(screen, DEEP_SPACE, (center_x, center_y), 35)
        pygame.draw.circle(screen, LASER_GREEN, (center_x, center_y), 35, 3)
        
        # 内側のコア
        pygame.draw.circle(screen, CYBER_CYAN, (center_x, center_y), 25)
        pygame.draw.circle(screen, STAR_WHITE, (center_x, center_y), 15)
        
        # セキュアクラウドテキスト
        font = get_japanese_font(12)
        text1 = font.render("セキュア", True, SPACE_BLACK)
        text2 = font.render("クラウド", True, SPACE_BLACK)
        
        text1_rect = text1.get_rect(center=(center_x, center_y - 8))
        text2_rect = text2.get_rect(center=(center_x, center_y + 8))
        
        screen.blit(text1, text1_rect)
        screen.blit(text2, text2_rect)

class Game:
    def __init__(self):
        self.state = MENU
        self.player = Player()
        self.security_risks = []
        self.goal = Goal()
        self.score = 0
        self.game_over = False
        self.won = False
        self.spawn_timer = 0
        self.spawn_delay = 40  # より頻繁に出現
        self.burst_timer = 0
        self.burst_delay = 180  # 3秒ごとに大量出現
        self.current_stage = 1
        self.current_difficulty = "普通"
        self.selected_menu_item = 0
        self.selected_stage = 1
        self.selected_difficulty = 0
        self.difficulty_keys = list(DIFFICULTY_LEVELS.keys())
    
    def spawn_security_risk(self):
        stage_data = STAGES[self.current_stage]
        difficulty_data = DIFFICULTY_LEVELS[self.current_difficulty]
        new_risk = SecurityRisk(stage_data["risks"], difficulty_data["speed_multiplier"], self.player.get_position(), self.current_difficulty)
        self.security_risks.append(new_risk)
    
    def spawn_burst_attack(self, count=5):
        """複数の敵を一度に生成"""
        stage_data = STAGES[self.current_stage]
        difficulty_data = DIFFICULTY_LEVELS[self.current_difficulty]
        
        for _ in range(count):
            new_risk = SecurityRisk(stage_data["risks"], difficulty_data["speed_multiplier"], self.player.get_position(), self.current_difficulty)
            self.security_risks.append(new_risk)
    
    def update(self):
        if self.state == PLAYING:
            self.update_game()
    
    def update_game(self):
        if self.game_over:
            return
        
        # プレイヤー更新
        self.player.update()
        
        # ゴール更新
        self.goal.update()
        
        # セキュリティリスク生成（通常）
        self.spawn_timer += 1
        difficulty_data = DIFFICULTY_LEVELS[self.current_difficulty]
        adjusted_spawn_delay = int(self.spawn_delay * difficulty_data["spawn_rate"])
        
        if self.spawn_timer >= adjusted_spawn_delay:
            self.spawn_security_risk()
            self.spawn_timer = 0
            # 難易度に応じた難易度上昇速度
            difficulty_reduction = 1
            if self.current_difficulty == "簡単":
                difficulty_reduction = 0.5
            elif self.current_difficulty == "普通":
                difficulty_reduction = 1
            elif self.current_difficulty == "難しい":
                difficulty_reduction = 1.5
            elif self.current_difficulty == "エキスパート":
                difficulty_reduction = 2
            
            if self.spawn_delay > 15:
                self.spawn_delay -= difficulty_reduction
        
        # バースト攻撃（大量出現）
        self.burst_timer += 1
        adjusted_burst_delay = int(self.burst_delay * difficulty_data["burst_rate"])
        
        if self.burst_timer >= adjusted_burst_delay:
            # 難易度に応じたバースト数
            if self.current_difficulty == "簡単":
                burst_count = random.randint(2, 4)
            elif self.current_difficulty == "普通":
                burst_count = random.randint(3, 6)
            elif self.current_difficulty == "難しい":
                burst_count = random.randint(5, 10)
            elif self.current_difficulty == "エキスパート":
                burst_count = random.randint(8, 15)
            
            self.spawn_burst_attack(burst_count)
            self.burst_timer = 0
            
            # バースト間隔も徐々に短く（難易度に応じて）
            burst_reduction = 5
            if self.current_difficulty == "簡単":
                burst_reduction = 2
            elif self.current_difficulty == "普通":
                burst_reduction = 3
            elif self.current_difficulty == "難しい":
                burst_reduction = 5
            elif self.current_difficulty == "エキスパート":
                burst_reduction = 8
            
            if self.burst_delay > 60:
                self.burst_delay -= burst_reduction
        
        # セキュリティリスク更新
        for risk in self.security_risks[:]:
            risk.update(self.player.get_position())
            if risk.is_off_screen():
                self.security_risks.remove(risk)
                self.score += 15  # より高いスコア
        
        # 衝突判定
        for risk in self.security_risks:
            if self.player.rect.colliderect(risk.rect):
                self.game_over = True
                self.state = GAME_OVER
                return
        
        # ゴール判定
        if self.player.rect.colliderect(self.goal.rect):
            self.won = True
            self.game_over = True
            self.state = GAME_OVER
    
    def handle_menu_input(self, key):
        if self.state == MENU:
            if key == pygame.K_UP:
                self.selected_menu_item = (self.selected_menu_item - 1) % 3
            elif key == pygame.K_DOWN:
                self.selected_menu_item = (self.selected_menu_item + 1) % 3
            elif key == pygame.K_RETURN:
                if self.selected_menu_item == 0:  # ゲーム開始
                    self.state = STAGE_SELECT
                elif self.selected_menu_item == 1:  # 説明
                    pass  # 説明画面（今回は省略）
                elif self.selected_menu_item == 2:  # 終了
                    return False
        
        elif self.state == STAGE_SELECT:
            if key == pygame.K_LEFT:
                self.selected_stage = max(1, self.selected_stage - 1)
            elif key == pygame.K_RIGHT:
                self.selected_stage = min(len(STAGES), self.selected_stage + 1)
            elif key == pygame.K_RETURN:
                self.current_stage = self.selected_stage
                self.state = LEVEL_SELECT
            elif key == pygame.K_ESCAPE:
                self.state = MENU
        
        elif self.state == LEVEL_SELECT:
            if key == pygame.K_UP:
                self.selected_difficulty = (self.selected_difficulty - 1) % len(self.difficulty_keys)
            elif key == pygame.K_DOWN:
                self.selected_difficulty = (self.selected_difficulty + 1) % len(self.difficulty_keys)
            elif key == pygame.K_RETURN:
                self.current_difficulty = self.difficulty_keys[self.selected_difficulty]
                self.start_game()
            elif key == pygame.K_ESCAPE:
                self.state = STAGE_SELECT
        
        elif self.state == GAME_OVER:
            if key == pygame.K_r:
                self.reset_game()
            elif key == pygame.K_ESCAPE:
                self.state = MENU
        
        return True
    
    def start_game(self):
        self.state = PLAYING
        self.reset_game()
        
        # 難易度に応じてプレイヤーの速度を調整
        if self.current_difficulty == "簡単":
            self.player.max_speed = 6
            self.player.acceleration = 0.6
        elif self.current_difficulty == "普通":
            self.player.max_speed = 8
            self.player.acceleration = 0.8
        elif self.current_difficulty == "難しい":
            self.player.max_speed = 10
            self.player.acceleration = 1.0
        elif self.current_difficulty == "エキスパート":
            self.player.max_speed = 12
            self.player.acceleration = 1.2
    
    def reset_game(self):
        self.player = Player()
        self.security_risks = []
        self.goal = Goal()
        self.score = 0
        self.game_over = False
        self.won = False
        self.spawn_timer = 0
        self.spawn_delay = 40  # より頻繁に出現
        self.burst_timer = 0
        self.burst_delay = 180  # 3秒ごとに大量出現
    
    def draw_menu(self, screen):
        # 宇宙背景
        screen.fill(SPACE_BLACK)
        self.draw_stars(screen)
        
        # タイトル（宇宙風エフェクト）
        font_title = get_japanese_font(48)
        title = font_title.render("AWS IAM セキュリティ", True, CYBER_CYAN)
        title2 = font_title.render("アドベンチャー", True, LASER_GREEN)
        
        # タイトルにグロー効果
        for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
            glow_title = font_title.render("AWS IAM セキュリティ", True, NEBULA_BLUE)
            screen.blit(glow_title, (SCREEN_WIDTH//2 - title.get_width()//2 + offset[0], 100 + offset[1]))
        
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        screen.blit(title2, (SCREEN_WIDTH//2 - title2.get_width()//2, 160))
        
        # メニュー項目
        font_menu = get_japanese_font(36)
        menu_items = ["ゲーム開始", "説明", "終了"]
        
        for i, item in enumerate(menu_items):
            color = CYBER_CYAN if i == self.selected_menu_item else STAR_WHITE
            text = font_menu.render(item, True, color)
            y = 300 + i * 60
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, y))
            
            if i == self.selected_menu_item:
                # 選択項目にエネルギーフィールド
                pygame.draw.rect(screen, CYBER_CYAN, 
                               (SCREEN_WIDTH//2 - text.get_width()//2 - 15, y - 8, 
                                text.get_width() + 30, text.get_height() + 16), 2)
    
    def draw_stars(self, screen):
        """背景の星を描画"""
        import random
        random.seed(42)  # 固定シードで一貫した星配置
        for _ in range(100):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            brightness = random.randint(100, 255)
            color = (brightness, brightness, brightness)
            pygame.draw.circle(screen, color, (x, y), 1)
    
    def draw_stage_select(self, screen):
        screen.fill(SPACE_BLACK)
        self.draw_stars(screen)
        
        # タイトル
        font_title = get_japanese_font(36)
        title = font_title.render("ステージ選択", True, CYBER_CYAN)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        # ステージ情報
        stage_data = STAGES[self.selected_stage]
        font_stage = get_japanese_font(28)
        font_desc = get_japanese_font(20)
        
        stage_name = font_stage.render(f"ステージ {self.selected_stage}: {stage_data['name']}", True, STAR_WHITE)
        stage_desc = font_desc.render(stage_data['description'], True, ASTEROID_GRAY)
        
        screen.blit(stage_name, (SCREEN_WIDTH//2 - stage_name.get_width()//2, 150))
        screen.blit(stage_desc, (SCREEN_WIDTH//2 - stage_desc.get_width()//2, 190))
        
        # セキュリティリスク一覧
        font_risks = get_japanese_font(16)
        risks_title = font_risks.render("このステージのセキュリティリスク:", True, STAR_WHITE)
        screen.blit(risks_title, (SCREEN_WIDTH//2 - risks_title.get_width()//2, 230))
        
        for i, risk in enumerate(stage_data['risks']):
            risk_text = font_risks.render(f"• {risk}", True, PLASMA_RED)
            screen.blit(risk_text, (SCREEN_WIDTH//2 - 100, 260 + i * 25))
        
        # ナビゲーション
        nav_text = font_desc.render("← → でステージ選択、ENTER で続行、ESC で戻る", True, STAR_WHITE)
        screen.blit(nav_text, (SCREEN_WIDTH//2 - nav_text.get_width()//2, 500))
        
        # ステージインジケーター（宇宙風）
        for i in range(1, len(STAGES) + 1):
            color = stage_data['star_color'] if i == self.selected_stage else ASTEROID_GRAY
            center_x = 200 + i * 80
            center_y = 400
            
            # 外側のリング
            pygame.draw.circle(screen, color, (center_x, center_y), 25, 3)
            if i == self.selected_stage:
                pygame.draw.circle(screen, color, (center_x, center_y), 30, 2)
            
            # 内側の数字
            stage_num = font_risks.render(str(i), True, STAR_WHITE)
            screen.blit(stage_num, (center_x - stage_num.get_width()//2, center_y - stage_num.get_height()//2))
    
    def draw_level_select(self, screen):
        screen.fill(SPACE_BLACK)
        self.draw_stars(screen)
        
        # タイトル
        font_title = get_japanese_font(36)
        title = font_title.render("難易度選択", True, CYBER_CYAN)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        # 難易度一覧
        font_level = get_japanese_font(28)
        font_desc = get_japanese_font(20)
        
        for i, (level, data) in enumerate(DIFFICULTY_LEVELS.items()):
            color = LASER_GREEN if i == self.selected_difficulty else STAR_WHITE
            level_text = font_level.render(level, True, color)
            desc_text = font_desc.render(data['description'], True, ASTEROID_GRAY)
            
            y = 150 + i * 80
            screen.blit(level_text, (SCREEN_WIDTH//2 - level_text.get_width()//2, y))
            screen.blit(desc_text, (SCREEN_WIDTH//2 - desc_text.get_width()//2, y + 30))
            
            if i == self.selected_difficulty:
                # エネルギーフィールド
                pygame.draw.rect(screen, LASER_GREEN, 
                               (SCREEN_WIDTH//2 - 160, y - 15, 320, 70), 2)
                # 内側のグロー
                pygame.draw.rect(screen, CYBER_CYAN, 
                               (SCREEN_WIDTH//2 - 155, y - 10, 310, 60), 1)
        
        # ナビゲーション
        nav_text = font_desc.render("↑ ↓ で難易度選択、ENTER でゲーム開始、ESC で戻る", True, STAR_WHITE)
        screen.blit(nav_text, (SCREEN_WIDTH//2 - nav_text.get_width()//2, 500))
    
    def draw_game(self, screen):
        # 宇宙背景
        stage_data = STAGES[self.current_stage]
        screen.fill(stage_data['background_color'])
        self.draw_stars(screen)
        
        # 宇宙グリッド（エネルギーフィールド）
        grid_color = (*stage_data['star_color'][:3], 50)
        for x in range(0, SCREEN_WIDTH, 100):
            pygame.draw.line(screen, stage_data['star_color'], (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 100):
            pygame.draw.line(screen, stage_data['star_color'], (0, y), (SCREEN_WIDTH, y), 1)
        
        # ゲームオブジェクト描画
        self.player.draw(screen)
        self.goal.draw(screen)
        
        for risk in self.security_risks:
            risk.draw(screen)
        
        # UI描画（宇宙風）
        font = get_japanese_font(28)
        score_text = font.render(f"スコア: {self.score}", True, CYBER_CYAN)
        
        # スコア背景
        score_bg = pygame.Rect(5, 5, score_text.get_width() + 10, score_text.get_height() + 10)
        pygame.draw.rect(screen, SPACE_BLACK, score_bg)
        pygame.draw.rect(screen, CYBER_CYAN, score_bg, 2)
        screen.blit(score_text, (10, 10))
        
        # ステージ情報
        font_small = get_japanese_font(20)
        stage_info = font_small.render(f"ステージ {self.current_stage}: {stage_data['name']} | {self.current_difficulty}", True, STAR_WHITE)
        
        info_bg = pygame.Rect(5, 45, stage_info.get_width() + 10, stage_info.get_height() + 10)
        pygame.draw.rect(screen, SPACE_BLACK, info_bg)
        pygame.draw.rect(screen, stage_data['star_color'], info_bg, 1)
        screen.blit(stage_info, (10, 50))
        
        # 指示テキスト
        instruction = font_small.render("矢印キーまたはWASDで移動。セキュリティリスクを避けよう！", True, STAR_WHITE)
        
        inst_bg = pygame.Rect(5, SCREEN_HEIGHT - 35, instruction.get_width() + 10, instruction.get_height() + 10)
        pygame.draw.rect(screen, SPACE_BLACK, inst_bg)
        pygame.draw.rect(screen, LASER_GREEN, inst_bg, 1)
        screen.blit(instruction, (10, SCREEN_HEIGHT - 30))
    
    def draw_game_over(self, screen):
        # ゲーム画面を薄暗く
        self.draw_game(screen)
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(SPACE_BLACK)
        screen.blit(overlay, (0, 0))
        
        font_big = get_japanese_font(48)
        font = get_japanese_font(28)
        
        if self.won:
            text = font_big.render("セキュリティ確保完了！", True, LASER_GREEN)
            sub_text = font.render("AWS環境が保護されました！", True, CYBER_CYAN)
            
            # 勝利エフェクト
            for i in range(5):
                pygame.draw.circle(screen, LASER_GREEN, 
                                 (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100), 50 + i*10, 2)
        else:
            text = font_big.render("セキュリティ侵害！", True, PLASMA_RED)
            sub_text = font.render("IAMが危険にさらされました！", True, COSMIC_ORANGE)
            
            # 危険エフェクト
            for i in range(3):
                pygame.draw.rect(screen, PLASMA_RED, 
                               (SCREEN_WIDTH//2 - 200 - i*20, SCREEN_HEIGHT//2 - 150 - i*10, 
                                400 + i*40, 200 + i*20), 3)
        
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        sub_rect = sub_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        
        # テキスト背景
        text_bg = pygame.Rect(text_rect.x - 10, text_rect.y - 10, 
                             text_rect.width + 20, text_rect.height + 20)
        pygame.draw.rect(screen, SPACE_BLACK, text_bg)
        pygame.draw.rect(screen, CYBER_CYAN, text_bg, 2)
        
        screen.blit(text, text_rect)
        screen.blit(sub_text, sub_rect)
        
        restart_text = font.render("R でリスタート、ESC でメニューに戻る", True, STAR_WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        
        restart_bg = pygame.Rect(restart_rect.x - 10, restart_rect.y - 5,
                               restart_rect.width + 20, restart_rect.height + 10)
        pygame.draw.rect(screen, SPACE_BLACK, restart_bg)
        pygame.draw.rect(screen, STAR_WHITE, restart_bg, 1)
        
        screen.blit(restart_text, restart_rect)
    
    def draw(self, screen):
        if self.state == MENU:
            self.draw_menu(screen)
        elif self.state == STAGE_SELECT:
            self.draw_stage_select(screen)
        elif self.state == LEVEL_SELECT:
            self.draw_level_select(screen)
        elif self.state == PLAYING:
            self.draw_game(screen)
        elif self.state == GAME_OVER:
            self.draw_game_over(screen)

def main():
    game = Game()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and game.state == PLAYING:
                    game.state = MENU
                else:
                    if not game.handle_menu_input(event.key):
                        running = False
        
        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
