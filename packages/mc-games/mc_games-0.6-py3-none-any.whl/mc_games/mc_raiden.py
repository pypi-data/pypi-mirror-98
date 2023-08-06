import sys
from random import *

from pgzero import music
from pgzero.actor import Actor
from pgzero.runner import prepare_mod, set_my_root, run_mod

WIDTH = 512
HEIGHT = 768
TITLE = '飞机大战'
# PATH = "./"
# os.path.abspath(os.path.join("./", ".."))

mod = sys.modules['mc_games.mc_raiden']

if not getattr(sys, '_pgzrun', None):
    if not getattr(mod, '__file__', None):
        raise ImportError(
            "You are running from an interactive interpreter.\n"
            "'import pgzrun' only works when you are running a Python file."
        )
    prepare_mod(mod)


def go():
    """Run the __main__ module as a Pygame Zero script."""
    mymod = sys.modules['mc_games.mc_raiden']
    set_my_root(getattr(mymod, 'PATH', ''))
    print(getattr(mymod, 'PATH', ''))

    if getattr(sys, '_pgzrun', None):
        return
    run_mod(mod)


bg1 = Actor('bg', topleft=(0, 0))
bg2 = Actor('bg', topleft=(0, -768))

map_speed = 1

player = None
bullets_lst = []
bullets2_lst = []

e1_act = None
e1_blood = None
e1_blood_size = 2
e1_status = None
e1_score = 100
e1_size = 100
e1_speed = 500

e2_act = None
e2_blood = None
e2_blood_size = 4
e2_status = None
e2_fired = None
e2_score = 200
e2_size = 100
e2_speed = 700

score = 0
game_status = 0

attack = "F"

up = "UP"
down = "DOWN"
left = "LEFT"
right = "RIGHT"


def draw():
    global game_status
    bg1.draw()
    bg2.draw()

    if game_status == 0:
        if e1_act is not None:
            for i in range(e1_size):
                if e1_status[i] < 2:
                    if e1_status[i] == 1:
                        if e1_act[i].image != 'boom-7':
                            e1_act[i].image = 'boom-' + str(int(e1_act[i].image[5:]) + 1)
                        else:
                            e1_status[i] = 2
                    e1_act[i].draw()

        for b in bullets_lst:
            b.draw()
        if e2_act is not None:
            for i in range(e2_size):
                if e2_status[i] < 2:
                    if e2_status[i] == 1:
                        if e2_act[i].image != 'boom-7':
                            e2_act[i].image = 'boom-' + str(int(e2_act[i].image[5:]) + 1)
                        else:
                            e2_status[i] = 2
                    e2_act[i].draw()

            for b in bullets2_lst:
                b.draw()

    if game_status < 2:
        if player is not None:
            if game_status == 1:
                if player.image != 'boom-7':
                    player.image = 'boom-' + str(int(player.image[5:]) + 1)
                else:
                    game_status = 2
            player.draw()
            screen.draw.text('%08d' % score, topright=(500, 10), color=(255, 255, 255), fontsize=30)



def update():
    global score, game_status, map_speed, e1_score, e2_score
    bg1.y += map_speed
    bg2.y += map_speed

    if bg1.topleft[1] > 768:
        bg1.y = bg2.y - 768
    if bg2.topleft[1] > 768:
        bg2.y = bg1.y - 768
    if game_status == 0:
        if e1_act is not None:
            for i in range(e1_size):
                e1_act[i].y += map_speed + 2
                if e1_act[i].y > 800:
                    e1_act[i].y = e1_act[i - 1].y - e1_speed
                    e1_act[i].image = 'e1'
                    e1_blood[i] = e1_blood_size
                    e1_status[i] = 0
        if e2_act is not None:
            for i in range(e2_size):
                e2_act[i].y += map_speed + 2
                if e2_act[i].y > 800:
                    e2_act[i].y = e2_act[i - 1].y - e2_speed
                    e2_act[i].image = 'e2'
                    e2_blood[i] = e2_blood_size
                    e2_status[i] = 0
                    e2_fired[i] = 0
                elif e2_act[i].y > 200 and e2_fired[i] == 0:
                    bullets2_lst.append(Actor('bullet-2', center=(e2_act[i].x, e2_act[i].y + 30)))
                    e2_fired[i] = 1

        for b in bullets_lst:
            b.y -= 10
            b_status = 0
            if b.y < -100:
                bullets_lst.remove(b)
                continue

            if e1_act is not None:
                for i in range(e1_size):
                    if e1_act[i].colliderect(b) and e1_status[i] == 0 and b.y > 0:
                        if e1_blood[i] > 1:
                            e1_act[i].y -= 3
                            e1_blood[i] -= 1
                        else:
                            sounds.boom.play()
                            e1_act[i].image = 'boom-1'
                            e1_status[i] = 1
                            score += e1_score
                        bullets_lst.remove(b)
                        b_status = 1
                        continue
            if b_status == 0:
                if e2_act is not None:
                    for i in range(e2_size):
                        if e2_act[i].colliderect(b) and e2_status[i] == 0 and b.y > 0:
                            if e2_blood[i] > 1:
                                e2_act[i].y -= 3
                                e2_blood[i] -= 1
                            else:
                                sounds.boom.play()
                                e2_act[i].image = 'boom-1'
                                e2_status[i] = 1
                                score += e2_score
                            bullets_lst.remove(b)
                            continue
        if e2_act is not None:
            for b in bullets2_lst:
                b.y += map_speed + 5
                if b.y > 800:
                    bullets2_lst.remove(b)
                    continue
                if player is not None:
                    if b.colliderect(player):
                        sounds.boom.play()
                        player.image = 'boom-1'
                        game_status = 1

        if player is not None:
            keys = {
                "A": keyboard.A,
                "B": keyboard.B,
                "C": keyboard.C,
                "D": keyboard.D,
                "E": keyboard.E,
                "F": keyboard.F,
                "G": keyboard.G,
                "H": keyboard.H,
                "I": keyboard.I,
                "J": keyboard.J,
                "K": keyboard.K,
                "L": keyboard.L,
                "M": keyboard.M,
                "N": keyboard.N,
                "O": keyboard.O,
                "P": keyboard.P,
                "Q": keyboard.Q,
                "R": keyboard.R,
                "S": keyboard.S,
                "T": keyboard.T,
                "U": keyboard.U,
                "V": keyboard.V,
                "W": keyboard.W,
                "X": keyboard.X,
                "Y": keyboard.Y,
                "Z": keyboard.Z,
                "UP": keyboard.up,
                "DOWN": keyboard.down,
                "LEFT": keyboard.left,
                "RIGHT": keyboard.right,
            }

            if keys[left] and player.x > player.width // 2:
                player.x -= map_speed + 4
            if keys[right] and player.x < WIDTH - player.width // 2:
                player.x += map_speed + 4
            if keys[up] and player.y > player.height // 2:
                player.y -= map_speed + 4
            if keys[down] and player.y < HEIGHT - player.height // 2:
                player.y += map_speed + 4


def on_key_down(key):
    if player is not None:
        keys = {
            "A": key.A,
            "B": key.B,
            "C": key.C,
            "D": key.D,
            "E": key.E,
            "F": key.F,
            "G": key.G,
            "H": key.H,
            "I": key.I,
            "J": key.J,
            "K": key.K,
            "L": key.L,
            "M": key.M,
            "N": key.N,
            "O": key.O,
            "P": key.P,
            "Q": key.Q,
            "R": key.R,
            "S": key.S,
            "T": key.T,
            "U": key.U,
            "V": key.V,
            "W": key.W,
            "X": key.X,
            "Y": key.Y,
            "Z": key.Z,
        }

        if key == keys[attack] and game_status == 0:
            bullets_lst.append(Actor('bullet-1', center=(player.x, player.y - 30)))


# 设置地图
def init_map(grade):
    global bg1
    global bg2
    if 0 < grade < 6 and isinstance(grade, int):
        bg1 = Actor('bg' + str(grade), topleft=(0, 0))
        bg2 = Actor('bg' + str(grade), topleft=(0, -768))
    else:
        bg1 = Actor('bg' + str(1), topleft=(0, 0))
        bg2 = Actor('bg' + str(1), topleft=(0, -768))
    music.play('bgm')


# 地图速度
def set_speed(speed):
    global map_speed
    if 0 < speed < 6 and isinstance(speed, int):
        map_speed = speed
    else:
        map_speed = 1


# 位置
def set_position(x, y):
    global player
    global bullets_lst
    if 20 < x < 490 and 20 < y < 740 and isinstance(x, int) and isinstance(y, int):
        player = Actor('p1', center=(x, y))
        bullets_lst = []
    else:
        player = Actor('p1', center=(WIDTH // 2, 700))


# 敌方的生命
def set_enemy1_life(blood):
    global e1_act
    global e1_blood
    global e1_blood_size
    global e1_status
    if 0 < blood < 5 and isinstance(blood, int):
        e1_blood_size = blood

    e1_act = [Actor('e1', center=(randint(50, 460), -100 - i * e1_speed)) for i in range(e1_size)]
    e1_blood = [e1_blood_size] * e1_size
    e1_status = [0] * e1_size


def set_enemy2_life(blood):
    global e2_act
    global e2_blood
    global e2_blood_size
    global e2_status
    global e2_fired
    global bullets2_lst
    if 2 < blood < 7 and isinstance(blood, int):
        e2_blood_size = blood
    e2_act = [Actor('e2', center=(randint(50, 460), -600 - i * e2_speed)) for i in range(e2_size)]
    e2_blood = [e2_blood_size] * e2_size
    e2_status = [0] * e2_size
    e2_fired = [0] * e2_size
    bullets2_lst = []


# 敌方的刷新
def set_enemy1_speed(speed):
    global e1_speed
    # if 0 < speed < 6 and isinstance(speed, int):
    if 100 <= speed <= 770 and isinstance(speed, int):
        e1_speed = 800 - speed


def set_enemy2_speed(speed):
    global e2_speed
    # if 0 < speed < 6 and isinstance(speed, int):
    if 100 <= speed <= 770 and isinstance(speed, int):
        e2_speed = 800 - speed


# 敌方的分数
def set_enemy1_score(score):
    global e1_score
    if 100 <= score <= 1000 and isinstance(score, int):
        e1_score = score


def set_enemy2_score(score):
    global e2_score
    if 200 <= score <= 1000 and isinstance(score, int):
        e2_score = score


# 设置方向键
def set_play_control(up_key, down_key, left_key, right_key):
    global up, down, left, right
    if player is not None:
        if isinstance(up_key, str) and isinstance(down_key, str) and isinstance(left_key, str) and isinstance(right_key,
                                                                                                              str):
            up = up_key.upper()
            down = down_key.upper()
            left = left_key.upper()
            right = right_key.upper()


# 设置攻击键
def set_play_attack(attack_key):
    global attack
    if player is not None:
        if isinstance(attack_key,
                      str) and attack_key != up and attack_key != down and attack_key != left and attack_key != right:
            attack = attack_key.upper()
