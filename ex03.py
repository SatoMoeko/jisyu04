import pyxel
import random
import time

WINDOW_H = 256
WINDOW_W = 256
GEM_H = 25
GEM_W = 25
BALL_H=5
BALL_W=5
ENEMY_H = 20
ENEMY_W = 20
ENEMY2_H = 55
ENEMY2_W = 256
ARROW_H=17
ARROW_W=17


class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class gem:
    def __init__(self, img_id):
        self.pos = Vec2(120, 200)
        self.vec = 0
        self.img_gem = img_id

    def update(self, x, y, dx):
        self.pos.x = x
        self.pos.y = y
        self.vec = dx

class Ball:
    def __init__(self):
        self.pos = Vec2(0, 0)
        self.vec = 0
        self.size = 2
        self.speed = 3
        self.color = 10 # 0~15

    def update(self, x, y, dx,size,color):
        self.pos.x = x
        self.pos.y = y
        self.vec = dx
        self.size = size
        self.color = color

class Enemy:
    def __init__(self, img_id):
        self.pos = Vec2(0, 0)
        self.vec = 0
        self.speed = 0.01
        self.img_enemy = img_id

    def update(self, x, y, dx):
        self.pos.x = x
        self.pos.y = y
        self.vec = dx

class Enemy2: #かけら
    def __init__(self):
        self.pos = Vec2(0, 0)
        self.vec = 0
        self.size = 1
        self.speed = 2
        self.color = pyxel.frame_count % 16

    def update(self, x, y, dx, size, color):
        self.pos.x = x
        self.pos.y = y
        self.vec = dx
        self.size = size
        self.color = color

class Arrow:
    def __init__(self,img_id):
        self.pos = Vec2(0, 0)
        self.vec = 0
        self.speed = 3
        self.img_arrow = img_id

    def update(self, x, y, dx):
        self.pos.x = x
        self.pos.y = y
        self.vec = dx

class App:
    def __init__(self):

        self.IMG_ID0 = 0
        self.IMG_ID1 = 1
        self.IMG_ID2 = 2

        pyxel.init(WINDOW_W, WINDOW_H, title="Land of lustrous fanGame")
        pyxel.load("assets/my_resource.pyxres") #画像

        # make instance
        self.mgem = gem(self.IMG_ID1)
        self.Balls = []
        self.Enemies = []
        self.Enemy2s = []
        self.Arrows = []

        # flag
        self.GameOver_flag = 0
        self.Start = False
        self.delE = (0,0)
        # Score
        self.Piece = 0
        self.Score = 0
        self.Hisc=0
        # 体力
        self.hp = 1000
        # 雲
        self.far_cloud=[(10,200),(30,128),(128,180),(70,30),(250,250)]
        self.near_cloud=[(50,230),(200,110)]


        pyxel.run(self.update, self.draw)

    def update(self):
        #閉じる
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        #====== ctrl start ======
        if pyxel.btn(pyxel.KEY_SPACE):
            self.Start = True
        if self.GameOver_flag ==1 and pyxel.btn(pyxel.KEY_SPACE):
            self.reset()
        if not self.Start:
            return      

        # ====== ctrl gem ======
        dx = pyxel.mouse_x - self.mgem.pos.x  # x軸方向の移動量(マウス座標 - cat座標)
        dy = pyxel.mouse_y - self.mgem.pos.y  # y軸方向の移動量(マウス座標 - cat座標)
        if dx != 0:
            self.mgem.update(pyxel.mouse_x, pyxel.mouse_y, dx) # 座標と向きを更新
        elif dy != 0:
            self.mgem.update(pyxel.mouse_x, pyxel.mouse_y, self.mgem.vec) # 座標のみ更新（真上or真下に移動）

        # ====== ctrl enemy ======
        if pyxel.frame_count % 30 == 1:
            # 画面の右端から
            new_enemy = Enemy(self.IMG_ID2)
            new_enemy.update(random.randint(WINDOW_W, WINDOW_W+5), random.randint(0, WINDOW_H+5), -self.mgem.vec)
            self.Enemies.append(new_enemy)
            # 画面の左端から
            new_enemy = Enemy(self.IMG_ID2)
            new_enemy.update(random.randint(-5, 0), random.randint(0, WINDOW_H+5), -self.mgem.vec)
            self.Enemies.append(new_enemy)

        enemy_count = len(self.Enemies)
        for i in range(enemy_count):
            # P制御
            ex = (self.mgem.pos.x - self.Enemies[i].pos.x)
            ey = (self.mgem.pos.y - self.Enemies[i].pos.y)
            Kp = self.Enemies[i].speed
            if ex != 0 or ey != 0:
                self.Enemies[i].update(self.Enemies[i].pos.x + ex * Kp, 
                                        self.Enemies[i].pos.y + ey * Kp, 
                                        self.mgem.vec)
            # 当たり判定(敵キャラとgem)
            if ((self.mgem.pos.x < self.Enemies[i].pos.x + ENEMY_W)
                 and (self.Enemies[i].pos.x + ENEMY_W < self.mgem.pos.x + GEM_W)
                 and (self.mgem.pos.y < self.Enemies[i].pos.y + ENEMY_H)
                 and (self.Enemies[i].pos.y + ENEMY_H < self.mgem.pos.y + GEM_H)
                or (self.mgem.pos.x < self.Enemies[i].pos.x)
                 and (self.Enemies[i].pos.x < self.mgem.pos.x + GEM_W)
                 and (self.mgem.pos.y < self.Enemies[i].pos.y + ENEMY_H)
                 and (self.Enemies[i].pos.y + ENEMY_H < self.mgem.pos.y + GEM_H)
                or (self.mgem.pos.x < self.Enemies[i].pos.x + ENEMY_W)
                 and (self.Enemies[i].pos.x + ENEMY_W < self.mgem.pos.x + GEM_W)
                 and (self.mgem.pos.y < self.Enemies[i].pos.y)
                 and (self.Enemies[i].pos.y < self.mgem.pos.y + GEM_H)
                or (self.mgem.pos.x < self.Enemies[i].pos.x)
                 and (self.Enemies[i].pos.x < self.mgem.pos.x + GEM_W)
                 and (self.mgem.pos.y < self.Enemies[i].pos.y)
                 and (self.Enemies[i].pos.y < self.mgem.pos.y + GEM_H)):
                # 体力とスコア
                if not self.GameOver_flag:
                    pyxel.play(0,1,loop=False)
                    del self.Enemies[i] 
                    enemy_count -= 1
                    self.hp -= 50
                    if self.hp <= 0:
                        self.GameOver_flag = 1
                break

        # ====== ctrl enemy2（かけら） =====
        if pyxel.frame_count % 18 == 1:
            new_enemy2 = Enemy2()
            new_enemy2.update(126, 16, 0, new_enemy2.size, new_enemy2.color)
            self.Enemy2s.append(new_enemy2)

            new_enemy2 = Enemy2()
            new_enemy2.update(127, 16, 0, new_enemy2.size, new_enemy2.color)
            self.Enemy2s.append(new_enemy2)

            new_enemy2 = Enemy2()
            new_enemy2.update(129, 16, 0, new_enemy2.size, new_enemy2.color)
            self.Enemy2s.append(new_enemy2)

            new_enemy2 = Enemy2()
            new_enemy2.update(130, 16, 0, new_enemy2.size, new_enemy2.color)
            self.Enemy2s.append(new_enemy2)

        enemy2_count = len(self.Enemy2s)
        for i in range(enemy2_count):
            if 0 < self.Enemy2s[i].pos.y and self.Enemy2s[i].pos.y < WINDOW_H: #画面内なら
                # Enemy2 update
                if i % 2 == 0:
                    if self.Enemy2s[i].pos.x >128:
                        self.Enemy2s[i].update(self.Enemy2s[i].pos.x+self.Enemy2s[i].speed, self.Enemy2s[i].pos.y+self.Enemy2s[i].speed, self.Enemy2s[i].vec, self.Enemy2s[i].size, self.Enemy2s[i].color)
                    else:
                        self.Enemy2s[i].update(self.Enemy2s[i].pos.x-self.Enemy2s[i].speed, self.Enemy2s[i].pos.y+self.Enemy2s[i].speed, self.Enemy2s[i].vec, self.Enemy2s[i].size, self.Enemy2s[i].color)
                else:
                    if self.Enemy2s[i].pos.x >128:
                        self.Enemy2s[i].update(self.Enemy2s[i].pos.x+self.Enemy2s[i].speed/3, self.Enemy2s[i].pos.y+self.Enemy2s[i].speed, self.Enemy2s[i].vec, self.Enemy2s[i].size, self.Enemy2s[i].color)
                    else:
                        self.Enemy2s[i].update(self.Enemy2s[i].pos.x-self.Enemy2s[i].speed/3, self.Enemy2s[i].pos.y+self.Enemy2s[i].speed, self.Enemy2s[i].vec, self.Enemy2s[i].size, self.Enemy2s[i].color)
                        
                # 当たり判定(gemとe2)
                if ((self.mgem.pos.x < self.Enemy2s[i].pos.x) 
                    and (self.Enemy2s[i].pos.x < self.mgem.pos.x + GEM_W)  
                    and (self.mgem.pos.y < self.Enemy2s[i].pos.y) 
                    and (self.Enemy2s[i].pos.y < self.mgem.pos.y + GEM_H)):
                    # あたったら
                    if not self.GameOver_flag:
                        pyxel.play(0,0,loop=False)
                        del self.Enemy2s[i] 
                        enemy2_count -= 1 
                        self.Piece += 1
                        self.Score += 100
                        self.hp -=5
                        if self.hp <= 0:
                            self.GameOver_flag = 1
                            pyxel.play(0,2,loop=False)
                    break
            else: #画面外にいったら
                del self.Enemy2s[i] 
                enemy2_count -= 1 
                break
        
        # ====== ctrl arrow =====
        if pyxel.frame_count % 150 == 0:
            new_arrow = Arrow(self.IMG_ID0)
            new_arrow.update(126, 16, 0)
            self.Arrows.append(new_arrow)
        if pyxel.frame_count % 180 == 0:
            new_arrow = Arrow(self.IMG_ID0)
            new_arrow.update(129, 16, 0)
            self.Arrows.append(new_arrow)
        if pyxel.frame_count % 270 == 0:
            new_arrow = Arrow(self.IMG_ID0)
            new_arrow.update(127, 16, 0)
            self.Arrows.append(new_arrow)
        if pyxel.frame_count % 240 == 0:
            new_arrow = Arrow(self.IMG_ID0)
            new_arrow.update(130, 16, 0)
            self.Arrows.append(new_arrow)

        arrow_count = len(self.Arrows)
        for i in range(arrow_count):
            if 0 < self.Arrows[i].pos.y and self.Arrows[i].pos.y < WINDOW_H: #画面内なら
                # arrow update
                if i % 2 == 0:
                    if self.Arrows[i].pos.x >128:
                        self.Arrows[i].update(self.Arrows[i].pos.x+self.Arrows[i].speed, self.Arrows[i].pos.y+self.Arrows[i].speed, self.Arrows[i].vec)
                    else:
                        self.Arrows[i].update(self.Arrows[i].pos.x-self.Arrows[i].speed, self.Arrows[i].pos.y+self.Arrows[i].speed, self.Arrows[i].vec)
                else:
                    if self.Arrows[i].pos.x >128:
                        self.Arrows[i].update(self.Arrows[i].pos.x+self.Arrows[i].speed/3, self.Arrows[i].pos.y+self.Arrows[i].speed, self.Arrows[i].vec)
                    else:
                        self.Arrows[i].update(self.Arrows[i].pos.x-self.Arrows[i].speed/3, self.Arrows[i].pos.y+self.Arrows[i].speed, self.Arrows[i].vec)
                        
                # 当たり判定(gemとarrow)
                if ((self.mgem.pos.x < self.Arrows[i].pos.x) 
                    and (self.Arrows[i].pos.x < self.mgem.pos.x + GEM_W)  
                    and (self.mgem.pos.y < self.Arrows[i].pos.y) 
                    and (self.Arrows[i].pos.y < self.mgem.pos.y + GEM_H)):
                    # あたったら
                    if not self.GameOver_flag:
                        time.sleep(1)
                        self.GameOver_flag = 1
                        pyxel.play(0,2,loop=False)
                    break
            else: #画面外にいったら
                del self.Arrows[i] 
                arrow_count -= 1 
                break


        # ====== ctrl Ball ======
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            new_ball = Ball()
            pyxel.play(0,3,loop=False)
            if self.mgem.vec > 0:
                new_ball.update(self.mgem.pos.x + GEM_W/2 + 6, 
                                self.mgem.pos.y + GEM_H/2, 
                                self.mgem.vec, new_ball.size, new_ball.color)
            else:
                new_ball.update(self.mgem.pos.x + GEM_W/2 - 6, 
                                self.mgem.pos.y + GEM_H/2, 
                                self.mgem.vec, new_ball.size, new_ball.color)
            self.Balls.append(new_ball)

        ball_count = len(self.Balls)
        for i in range(ball_count):
            if 0 < self.Balls[i].pos.x and self.Balls[i].pos.x < WINDOW_W:
                # Ball update
                if self.Balls[i].vec > 0:
                    self.Balls[i].update(self.Balls[i].pos.x + self.Balls[i].speed, 
                                        self.Balls[i].pos.y, 
                                        self.Balls[i].vec, self.Balls[i].size, self.Balls[i].color)
                else:
                    self.Balls[i].update(self.Balls[i].pos.x - self.Balls[i].speed, 
                                        self.Balls[i].pos.y, 
                                        self.Balls[i].vec, self.Balls[i].size, self.Balls[i].color)
                # 当たり判定(敵キャラとボール)
                enemy_count = len(self.Enemies)
                for j in range(enemy_count):
                    if ((self.Enemies[j].pos.x < self.Balls[i].pos.x)
                        and (self.Balls[i].pos.x < self.Enemies[j].pos.x + ENEMY_W) 
                        and (self.Enemies[j].pos.y < self.Balls[i].pos.y) 
                        and (self.Balls[i].pos.y < self.Enemies[j].pos.y + ENEMY_H)):
                        # 消滅(敵インスタンス破棄)
                        self.delE=(self.Enemies[j].pos.x,self.Enemies[j].pos.y)
                        del self.Enemies[j]
                        if not self.GameOver_flag:
                            pyxel.play(0,4,loop=False)
                            self.Score += 500
                        break
            else:
                del self.Balls[i]
                ball_count -= 1
                break

    def draw(self):
        pyxel.cls(0)

        # ====== draw background ======
        pyxel.bltm(0, 0, 0, 0, 0, 256, 256, 0)

        # ====== draw far cloud ======
        offset = (pyxel.frame_count//10) % 160
        for i in range(2):
            for x,y in self.far_cloud:
                pyxel.blt(x+i*160-offset,y,0,33,2,33,11,6)

        # ====== draw hp ======
        if self.GameOver_flag == 0:
            score_x = 2
            score_y = WINDOW_H-8
            score = "HP:" + str(self.hp)
            pyxel.text(score_x, score_y, score, 1)

        # ======= draw gem ========
        if self.GameOver_flag == 0:
            if self.mgem.vec > 0:
                pyxel.blt(self.mgem.pos.x, self.mgem.pos.y, 0, 7, 64, GEM_W, GEM_H, 6)
            else:
                pyxel.blt(self.mgem.pos.x, self.mgem.pos.y, 0, 0, 32, GEM_W, GEM_H, 6)
        if self.GameOver_flag == 1:
            pyxel.blt(self.mgem.pos.x, self.mgem.pos.y, 0, 96, 18, 20, 13, 6)

        # ====== draw Balls ======
        for ball in self.Balls:
            pyxel.blt(ball.pos.x, ball.pos.y, 0, 39, 64, BALL_W, BALL_H, 6)

        # ====== draw enemy ======
        if self.GameOver_flag == 0:
            for enemy in self.Enemies:
                pyxel.blt(enemy.pos.x, enemy.pos.y, 0, 32, 33, ENEMY_W, ENEMY_H, 6)
                
        if self.delE !=(0,0):
            x,y=self.delE
            pyxel.blt(x, y, 0, 128, 9, 19, 23, 6)
            self.delE=(0,0)
                
        # ====== draw enemy2 ======
        if self.GameOver_flag == 0:
            for enemy2 in self.Enemy2s:
                pyxel.circ(enemy2.pos.x, enemy2.pos.y, enemy2.size, enemy2.color)

        # ====== draw arrow ======
        if self.GameOver_flag == 0:
            for arrow in self.Arrows:
                if arrow.pos.x > 128:
                    pyxel.blt(arrow.pos.x, arrow.pos.y, 0, 71,23, ARROW_W, ARROW_H, 6) 
                else:
                    pyxel.blt(arrow.pos.x, arrow.pos.y, 0, 72,47, ARROW_W, ARROW_H, 6) 

        # ====== draw background (かざり)======       
        pyxel.blt(0, 0, 1, 0, 152, 256, 70, 6)

        # ====== draw score ======
        if self.GameOver_flag == 0:
            score_x = 40
            score_y = WINDOW_H-8
            score = "SCORE:" + str(self.Score)
            piece= "PIECE:" + str(self.Piece)
            highScore = "HIGH SCORE:"+str(self.Hisc)
            pyxel.text(score_x, score_y, score, 1)
            pyxel.text(score_x+50, score_y, piece, 1)
            pyxel.text(2, 2, highScore, 1)

        # ====== draw topEnemy ======
        pyxel.blt(20, 3, 0, 20, 99, 216, 55, 6)
        

        # ====== draw near cloud ======
        offset = (pyxel.frame_count//8) % 160
        for i in range(2):
            for x,y in self.near_cloud:
                pyxel.blt(x+i*160-offset,y,0,1,16,53,15,6)

        # ====== draw start ======
        if self.Start == False and self.GameOver_flag==0:
            pyxel.text(100, 160, "PUSH SPACE START", pyxel.frame_count % 10)
            pyxel.text(80, 80, "Land of lustrous fanGame", 12)
            pyxel.text(102, 170, "ALT:how to play", 1)
            #ALTで遊び方をみる
            if pyxel.btn(pyxel.KEY_ALT):
                pyxel.blt(0, 50, 1, 0, 0, 256, 151, 6) 

        # ====== draw game over ======
        if self.GameOver_flag == 1:
            pyxel.sounds[2].speed = 10
            if self.Score>self.Hisc:
                self.Hisc=self.Score
            piece= "PIECE:" + str(self.Piece)
            score = "SCORE:" + str(self.Score)
            highScore = "HIGH SCORE:"+str(self.Hisc)
            pyxel.text(115, 110, piece, 1)
            pyxel.text(110, 120, score, 1)
            pyxel.text(100, 130, highScore, 1)

            MESSAGE=\
"""
    GAME OVER
PUSH SPACE RESTART
"""
            pyxel.text(self.mgem.pos.x-22, self.mgem.pos.y-20, MESSAGE, pyxel.frame_count % 16)
            return
        
    def reset(self):
        self.Arrows = []
        self.Enemies = []
        # flag
        self.GameOver_flag = 0
        self.Start = False
        # Score
        self.Score = 0
        self.Piece = 0
        # 体力
        self.hp = 1000


App()