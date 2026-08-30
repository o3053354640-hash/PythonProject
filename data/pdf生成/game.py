import pygame
import sys
import random
import os


class MTRRunnerGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

        # 視窗與基本設定
        self.WIDTH = 960
        self.HEIGHT = 540
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("MTR Runner - 香港地鐵跑酷 (碰撞結束版)")

        self.clock = pygame.time.Clock()
        self.running = True

        # 遊戲狀態
        self.game_state = 'playing'  # 'playing' 或 'game_over'
        self.high_score = 0

        # 音效（同前版）
        self.sounds_dir = "sounds/"
        self.train_horn = None
        self.train_loop = None
        try:
            self.train_horn = pygame.mixer.Sound(self.sounds_dir + "train_horn.mp3")
            self.train_loop = pygame.mixer.Sound(self.sounds_dir + "train_loop.wav")
            self.train_loop.set_volume(0.4)
            self.train_horn.set_volume(0.6)
        except:
            pass  # 無音效不 crash

        if self.train_loop:
            self.train_loop.play(-1)

        # 顏色
        self.MTR_DARK_BLUE = (0, 51, 102)
        self.WHITE = (255, 255, 255)
        self.GOLD = (255, 215, 0)
        self.ORANGE = (255, 140, 0)
        self.GRAY_TRACK = (80, 80, 80)
        self.LIGHT_GRAY = (200, 200, 200)
        self.RED = (255, 50, 50)

        # 運行地鐵顏色
        self.train_colors = [
            (230, 30, 30), (0, 125, 197), (0, 168, 89),
            (247, 148, 29), (159, 42, 125)
        ]

        # 字型
        self.font_large = pygame.font.Font(None, 60)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

        self.reset_game()

    def reset_game(self):
        """重置遊戲（重新開始）"""
        self.lanes = [240, 480, 720]
        self.current_lane = 1
        self.player_target_x = self.lanes[self.current_lane]
        self.player_width = 60
        self.player_height = 90
        self.player_x = self.player_target_x
        self.player_y = self.HEIGHT - 150
        self.player_vel_y = 0
        self.gravity = 980
        self.jump_power = -420
        self.is_jumping = False
        self.lane_switch_speed = 800
        self.player_rect = pygame.Rect(
            self.player_x - self.player_width // 2, self.player_y,
            self.player_width, self.player_height
        )
        self.score = 0
        self.trains = []
        self.train_spawn_timer = 0
        self.train_spawn_interval = 120
        self.game_state = 'playing'

        self.title_surface = self.font_large.render("MTR Runner", True, self.WHITE)
        self.title_rect = self.title_surface.get_rect(center=(self.WIDTH // 2, 80))

    def spawn_train(self):
        lane_idx = random.randint(0, 2)
        lane_x = self.lanes[lane_idx]
        color = random.choice(self.train_colors)

        train = {
            'x': self.WIDTH + 100,
            'y': self.HEIGHT - 160,
            'lane_x': lane_x,
            'width': 120,
            'height': 70,
            'length': 300,
            'speed': 400 + (self.score // 1000) * 20,
            'color': color,
            'rect': None  # 稍後計算碰撞矩形
        }
        self.trains.append(train)

        if self.train_horn:
            self.train_horn.play()

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if self.game_state == 'playing':
            # 正常遊戲輸入
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.current_lane > 0:
                self.current_lane -= 1
                self.player_target_x = self.lanes[self.current_lane]
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.current_lane < 2:
                self.current_lane += 1
                self.player_target_x = self.lanes[self.current_lane]
            if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and not self.is_jumping:
                self.player_vel_y = self.jump_power
                self.is_jumping = True
        elif self.game_state == 'game_over':
            # Game Over 輸入
            if keys[pygame.K_SPACE]:
                self.reset_game()
            if keys[pygame.K_ESCAPE]:
                self.running = False

    def check_collision(self):
        """檢查玩家與地鐵碰撞"""
        for train in self.trains:
            # 計算地鐵碰撞矩形（整個車身範圍）
            train_rect = pygame.Rect(
                train['x'], train['y'],
                train['length'], train['height']
            )
            if self.player_rect.colliderect(train_rect):
                return True
        return False

    def update(self, dt):
        if self.game_state != 'playing':
            return

        # 生成地鐵
        self.train_spawn_timer += 1
        if self.train_spawn_timer >= self.train_spawn_interval:
            self.spawn_train()
            self.train_spawn_timer = 0
            if self.score > 5000:
                self.train_spawn_interval = max(60, self.train_spawn_interval - 1)

        # 玩家移動
        self.player_x += (self.player_target_x - self.player_x) * self.lane_switch_speed * dt
        self.player_vel_y += self.gravity * dt
        self.player_y += self.player_vel_y * dt
        ground_y = self.HEIGHT - 150
        if self.player_y >= ground_y:
            self.player_y = ground_y
            self.player_vel_y = 0
            self.is_jumping = False
        self.player_rect.topleft = (self.player_x - self.player_width // 2, self.player_y)

        # 更新地鐵
        for train in self.trains[:]:
            train['x'] -= train['speed'] * dt
            if train['x'] + train['length'] < 0:
                self.trains.remove(train)

        # 碰撞檢測
        if self.check_collision():
            self.game_state = 'game_over'
            if self.score > self.high_score:
                self.high_score = self.score

        self.score += 1

    def draw_train(self, train):
        x, y, width, height, length, color = train['x'], train['y'], train['width'], train['height'], train['length'], \
        train['color']
        # 車頭
        pygame.draw.rect(self.screen, color, (x, y, width, height), border_radius=15)
        pygame.draw.circle(self.screen, self.WHITE, (int(x + 15), int(y + height // 2)), 8)
        pygame.draw.circle(self.screen, (255, 255, 200), (int(x + 15), int(y + height // 2)), 6)
        # 車身
        for i in range(1, int(length / width)):
            car_x = x + i * width
            pygame.draw.rect(self.screen, color, (car_x, y, width, height), border_radius=10)
            window_y = y + 15
            for w in range(3):
                pygame.draw.rect(self.screen, (255, 255, 150), (car_x + 10 + w * 30, window_y, 20, 25))
        # 車尾
        tail_x = x + length - 20
        pygame.draw.circle(self.screen, (255, 50, 50), (int(tail_x), int(y + height // 2)), 10)

    def draw(self):
        if self.game_state == 'playing':
            self.screen.fill(self.MTR_DARK_BLUE)
            ground_y = self.HEIGHT - 150

            # 軌道
            for i, lane_x in enumerate(self.lanes):
                pygame.draw.line(self.screen, self.GRAY_TRACK, (lane_x, ground_y - 20), (lane_x, self.HEIGHT), 6)
                for offset in range(-200, self.HEIGHT, 40):
                    pygame.draw.line(self.screen, self.GRAY_TRACK, (lane_x - 15, ground_y + offset),
                                     (lane_x + 15, ground_y + offset), 4)
                colors = [(220, 0, 0), (0, 120, 190), (0, 168, 89)]
                pygame.draw.rect(self.screen, colors[i], (lane_x - 25, 20, 50, 40), border_radius=8)

            # 地鐵
            for train in self.trains:
                self.draw_train(train)

            # 地面線
            pygame.draw.line(self.screen, self.LIGHT_GRAY, (0, ground_y + self.player_height),
                             (self.WIDTH, ground_y + self.player_height), 8)

            # UI
            self.screen.blit(self.title_surface, self.title_rect)
            score_text = self.font_medium.render("Score: " + str(self.score // 10), True, self.GOLD)
            score_rect = score_text.get_rect(topleft=(20, 20))
            self.screen.blit(score_text, score_rect)

            # 玩家
            pygame.draw.rect(self.screen, self.ORANGE, self.player_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), self.player_rect, 3)

        elif self.game_state == 'game_over':
            # Game Over 畫面（全黑背景）
            self.screen.fill((20, 20, 20))

            # 標題
            game_over_surf = self.font_large.render("GAME OVER", True, self.RED)
            game_over_rect = game_over_surf.get_rect(center=(self.WIDTH // 2, 150))
            self.screen.blit(game_over_surf, game_over_rect)

            # 分數
            final_score_surf = self.font_medium.render("Final Score: " + str(self.score // 10), True, self.WHITE)
            final_score_rect = final_score_surf.get_rect(center=(self.WIDTH // 2, 220))
            self.screen.blit(final_score_surf, final_score_rect)

            high_score_surf = self.font_medium.render("High Score: " + str(self.high_score // 10), True, self.GOLD)
            high_score_rect = high_score_surf.get_rect(center=(self.WIDTH // 2, 260))
            self.screen.blit(high_score_surf, high_score_rect)

            # 提示
            restart_surf = self.font_small.render("Press SPACE to Restart / ESC to Quit", True, self.WHITE)
            restart_rect = restart_surf.get_rect(center=(self.WIDTH // 2, 350))
            self.screen.blit(restart_surf, restart_rect)

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.handle_input()
            self.update(dt)
            self.draw()

        if self.train_loop:
            self.train_loop.stop()
        pygame.quit()
        sys.exit()
if __name__ == "__main__":
    game = MTRRunnerGame()
    game.run()