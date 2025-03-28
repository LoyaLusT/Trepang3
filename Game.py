import math, os, sys, pygame as pg
import random
from Data import *

#Канал 1 - Музыка меню, Канал 2 - Музыка игры, Канал 3 - Голос в миссиях, Канал 4 - Голос врагов
pg.mixer.Channel(1).play(pg.mixer.Sound('Trepang3/assets/sounds/music/57. Where to Next.mp3'),-1)
pg.mixer.Channel(1).set_volume(0.25)

bullets = []
level = 1

lvl1walls = []
if os.path.exists('Trepang3/leveldata/level1.txt'):
    row = 0
    column = 0
    file = open('Trepang3/leveldata/level1.txt', 'r')
    worldLines = file.readlines()
    for line in worldLines:
        x = list(line)
        column = 0
        for i in x:
            if i == '1':
                lvl1walls.append(pg.Rect(column * 20, row * 20,20,20))
            column += 1
        row += 1


class Game:
    def __init__(self):#Инициализация и вводные данные
        pg.init()
        self.screen = pg.display.set_mode(( ScreenWidht,ScreenHeight ),pg.FULLSCREEN)
        self.clock = pg.time.Clock()
        self.game_state = 'main_menu'
        self.last = pg.time.get_ticks()

        self.running = True
    def run(self):
        while self.running:
            self.update()
            self.draw()
            from Data import enemy_wave

            if self.game_state == 'main_menu':          #МЭЙН МЕНЮ
                for e in pg.event.get():
                    if e.type == pg.QUIT:
                        sys.exit()
                main_menu.draw()


                if NewGameButton.draw():
                    self.game_state = 'play'
                if ExitButton.draw():
                    self.running = False
                    self.close()
                if CombatSimulatorButton.draw(): #кнопка симулятора
                    pg.mixer.Channel(1).stop()
                    self.game_state = 'play'
                    pg.mixer.Channel(2).play(pg.mixer.Sound('Trepang3/assets/sounds/music/05. Broken Cuffs.mp3'),-1)
                    pg.mixer.Channel(2).set_volume(0.75)
                    pg.mixer.Channel(3).play(pg.mixer.Sound(crash_site_voicelines['intro']))
                    pg.mixer.Channel(3).set_volume(0.75)
                    if subtitles['crash_site']['intro1'].draw():
                        pass
                    lvl1enemies = [
                        
                        Enemy(30, 80, 85, 121, 30, 200, 'h', 'hazmat', 'shotgun', True),
                        Enemy(420, 50, 84, 120, 50, 400, 'v', 'hazmat', 'rifle', True),
                        Enemy(400, 550, 84, 120, 200, 300, 'h', 'hazmat', 'smg', True),
                        Enemy(900, 50, 84, 120, 300, 500, 'v', 'hazmat', 'pistol', True),
                        Enemy(100, 300, 84, 120, 100, 400, 'h', 'hazmat', 'pistol', True)
                    ]
                    remaining_enemies_get = len(lvl1enemies)

                BuildVersion.draw()

            elif self.game_state == 'play':             #ИГРА
                for e in pg.event.get():
                    if e.type == pg.QUIT:
                        sys.exit()
                    if e.type == pg.KEYDOWN:
                        if e.key == pg.K_w:
                            player.y_speed = -5
                        elif e.key == pg.K_a:
                            player.x_speed = -5
                        elif e.key == pg.K_s:
                            player.y_speed = 5
                        elif e.key == pg.K_d:
                            player.x_speed = 5
                        elif e.key == pg.K_ESCAPE:
                            self.game_state = 'pause_menu'
                            pg.mixer.Channel(2).pause()
                            pg.mixer.Channel(1).play(pg.mixer.Sound('Trepang3/assets/sounds/music/55. Pause That.mp3'),-1)
                            pg.mixer.Channel(1).set_volume(0.25)
                            pg.mixer.Channel(3).pause()
                            pg.mixer.Channel(4).pause()
                        elif e.key == pg.K_TAB:
                            self.game_state = 'shop'
                            pg.mixer.Channel(2).pause()
                            pg.mixer.Channel(1).set_volume(0.55)
                            pg.mixer.Channel(1).play(pg.mixer.Sound('Trepang3/assets/sounds/music/56. Load Up.mp3'),-1)
                            pg.mixer.Channel(3).pause()
                            pg.mixer.Channel(4).pause()

                        elif e.key == pg.K_r: #Перезарядка
                            if weapon['spas12']['holding']:
                                if weapon['spas12']['magazine'] > 0 and weapon['spas12']['magazine'] < 8:
                                    if player_inventory['spas12_bullet'] > 0:
                                        pg.mixer.Sound.play(Spas12_reload_single)
                                        while player_inventory['spas12_bullet'] > 0 and weapon['spas12']['magazine'] < 8:
                                            now = pg.time.get_ticks() #проверка кулдауна перезарядки
                                            if now - self.last >= weapon_cooldown['spas12']['reload_tactical']:     #Задержка 1 секунда
                                                self.last = now
                                                player_inventory['spas12_bullet'] -= 1
                                                weapon['spas12']['magazine'] += 1
                                        pg.mixer.Sound.stop(Spas12_reload_single)
                                        

                                elif weapon['spas12']['magazine'] == 0 and player_inventory['spas12_bullet'] > 0:
                                    pg.mixer.Sound.play(Spas12_reload_empty)
                                    while player_inventory['spas12_bullet'] > 0 and weapon['spas12']['magazine'] < 8:
                                        now = pg.time.get_ticks()
                                        if now - self.last >= weapon_cooldown['spas12']['reload_empty']:     #Задержка 1 секунда
                                            self.last = now
                                            player_inventory['spas12_bullet'] -= 1
                                            weapon['spas12']['magazine'] += 1
                                            #Задержка 1 секунда
                                    pg.mixer.Sound.stop(Spas12_reload_empty)
                            elif weapon['mk23']['holding']:
                                if weapon['mk23']['magazine'] > 0 and weapon['mk23']['magazine'] < 13:
                                    if player_inventory['mk23_bullet'] > 0:
                                        pg.mixer.Sound.play(Mk23_reload_tactical)
                                        pg.time.wait(int(weapon_cooldown['mk23']['reload_tactical']))
                                        bullets_to_reload = min(13 - weapon['mk23']['magazine'], player_inventory['mk23_bullet'])
                                        weapon['mk23']['magazine'] += bullets_to_reload
                                        player_inventory['mk23_bullet'] -= bullets_to_reload

                                elif weapon['mk23']['magazine'] == 0 and player_inventory['mk23_bullet'] > 0:
                                    pg.mixer.Sound.play(Mk23_reload)
                                    pg.time.wait(int(weapon_cooldown['mk23']['reload_empty']))
                                    bullets_to_reload = min(13, player_inventory['mk23_bullet'])
                                    weapon['mk23']['magazine'] = bullets_to_reload
                                    player_inventory['mk23_bullet'] -= bullets_to_reload

                    if e.type == pg.KEYUP:
                        if e.key == pg.K_w or e.key == pg.K_s:
                            player.y_speed = 0
                        elif e.key == pg.K_a or e.key == pg.K_d:
                            player.x_speed = 0


                    if e.type == pg.MOUSEBUTTONDOWN:
                        if e.button == 1:
                            now = pg.time.get_ticks()
                            if weapon['spas12']['holding']:
                                if weapon['spas12']['magazine'] > 0: #Стрельба
                                    if now - self.last >= weapon_cooldown['spas12']['shot']:
                                        self.last = now
                                        pg.mixer.Sound.play(Spas12_shot)
                                        x, y = e.pos
                                        bullet = Bullet(player.rect.centerx, player.rect.centery, 8, 16, 'Trepang3/assets/textures/sprites/bullet.png', e.pos)
                                        bullets.append(bullet)
                                        weapon['spas12']['magazine'] -= 1
                                else:
                                    if now - self.last >= weapon_cooldown['spas12']['shot']:
                                        self.last = now
                                        pg.mixer.Sound.play(Shot_empty)
                            elif weapon['mk23']['holding']:
                                if weapon['mk23']['magazine'] > 0:
                                    if now - self.last >= weapon_cooldown['mk23']['shot']:
                                        self.last = now
                                        pg.mixer.Sound.play(Mk23_shot)
                                        x, y = e.pos
                                        bullet = Bullet(player.rect.centerx, player.rect.centery, 8, 16, 'Trepang3/assets/textures/sprites/bullet.png', e.pos)
                                        bullets.append(bullet)
                                        weapon['mk23']['magazine'] -= 1
                                else:
                                    pg.mixer.Sound.play(Shot_empty)

                        elif e.button == 4 or e.button == 5:
                            if weapon['spas12']['holding']:
                                weapon['spas12']['holding'] = False
                                weapon['mk23']['holding'] = True
                                pg.time.wait(weapon_cooldown['mk23']['draw']) # Задержка перед переключением оружия
                            elif weapon['mk23']['holding']:
                                weapon['spas12']['holding'] = True
                                weapon['mk23']['holding'] = False
                                pg.mixer.Sound.play(Spas12_draw_sound)
                                pg.time.wait(weapon_cooldown['spas12']['draw']) # Задержка перед переключением оружия
                for bullet in bullets:
                    if bullet.rect.x > 1280 or bullet.rect.x <= -bullet.rect.width or bullet.rect.y >= 720 or bullet.rect.y <= -bullet.rect.height:
                        bullets.remove(bullet)
                    bullet.draw()
                    bullet.move() #рисовка пуль
                    


                if level == 1:
                    for enemy in lvl1enemies:
                        enemy.move()

                    for enemy in lvl1enemies:
                        enemy.draw()

                    for enemy in lvl1enemies:
                        enemy_dead = False
                        for bullet in bullets:
                            if bullet.collide(enemy):
                                bullets.remove(bullet)
                                if enemy.armor > 0:
                                    if weapon['spas12']['holding']:
                                        enemy.armor -= weapon['spas12']['damage']
                                        pg.mixer.Sound.play(Armor_hit)
                                    elif weapon['mk23']['holding']:
                                        enemy.armor -= weapon['mk23']['damage']
                                        pg.mixer.Sound.play(Armor_hit)
                                else:
                                    if weapon['spas12']['holding']:
                                        enemy.health -= weapon['spas12']['damage']
                                        if enemy.health > 0:
                                            pg.mixer.Sound.play(Melee_hit)
                                    elif weapon['mk23']['holding']:
                                        enemy.health -= weapon['mk23']['damage']
                                        if enemy.health > 0:
                                            pg.mixer.Sound.play(Melee_hit)
                                if enemy.health <= 0:
                                    enemy_dead = True
                                break
                        if enemy_dead:
                            randint = random.randint(0, 5)

                            lvl1enemies.remove(enemy)
                            pg.mixer.Sound.play(kill_confirmed_sound)
                            player_inventory['money'] += 100
                            remaining_enemies_get -= 1
                            if enemy_wave == 0 and remaining_enemies_get == 4:
                                pg.mixer.Channel(3).play(crash_site_voicelines['contact'])

                            if remaining_enemies_get == 0:
                                enemy_wave += 1
                                if enemy_wave == 1:
                                    pg.mixer.Channel(2).play(pg.mixer.Sound('Trepang3/assets/sounds/music/59. GACK/59. GACK(A).mp3'))
                                    pg.mixer.Channel(3).set_volume(0.75)
                                    pg.mixer.Channel(3).play(crash_site_voicelines['1st_wave_intro'])
                                    pg.mixer.Channel(3).set_volume(1.25)
                                    pg.mixer.Channel(3).queue(HVTs_voicelines['Wane_intro'])
                                    while pg.mixer.Channel(2).get_busy():
                                        self.update()
                                    if pg.mixer.Channel(2).get_busy() == False:
                                        pg.mixer.Channel(2).play(pg.mixer.Sound('Trepang3/assets/sounds/music/59. GACK/59. GACK(B).mp3'),-1)

                                        lvl1enemies = [
                                            Enemy(30, 80, 85, 121, 30, 200, 'h', 'hazmat', 'shotgun', False),
                                            Enemy(420, 50, 85, 121, 50, 400, 'v', 'hazmat', 'shotgun', False),
                                            Enemy(200, 200, 85, 121, 200, 300, 'h', 'hazmat', 'shield', False),
                                            Enemy(100, 300, 85, 121, 300, 400, 'v', 'hazmat', 'shield', False),
                                            Enemy(300, 500, 85, 121, 500, 300, 'h', 'hazmat', 'shield', False),
                                            Enemy(600, 100, 84, 120, 100, 200, 'h', 'hazmat', 'smg', False),
                                            Enemy(400, 600, 84, 120, 500, 100, 'v', 'hazmat', 'smg', False),
                                            Enemy(200, 400, 84, 120, 400, 100, 'v', 'hazmat', 'smg', False),
                                            Enemy(500, 300, 84, 120, 300, 500, 'h', 'hazmat', 'sniper', False),
                                            Enemy(400, 200, 84, 120, 200, 500, 'v', 'hazmat', 'sniper', False),
                                            Enemy(700, 400, 84, 120, 400, 200, 'v', 'hazmat', 'rifle', False),
                                            Enemy(100, 100, 84, 120, 100, 300, 'h', 'hazmat', 'rifle', False),
                                            Enemy(700, 600, 84, 120, 600, 400, 'v', 'hazmat', 'rifle', False),
                                            Enemy(100, 500, 84, 120, 500, 200, 'h', 'hazmat', 'rifle', False),
                                            Enemy(600, 500, 84, 120, 500, 300, 'h', 'hazmat', 'pistol', False),
                                            Enemy(600, 300, 84, 120, 300, 400, 'h', 'hazmat', 'pistol', False),
                                            Enemy(400, 500, 86, 122, 500, 400, 'h', 'heavy', 'shotgun', False),
                                            Enemy(200, 600, 86, 122, 500, 200, 'v', 'heavy', 'minigun', False),
                                            Enemy(100, 500, 84, 120, 200, 200, 'h', 'HVT', 'wane', False)
                                                    ]
                                        remaining_enemies_get = len(lvl1enemies)

                                    # wave_2_spawn_delay = 5
                                    # wave_2_spawn_event = pg.USEREVENT
                                    # pg.time.set_timer(wave_2_spawn_event, wave_2_spawn_delay)
                                    # for e in pg.event.get():
                                    #     if e.type == wave_2_spawn_event:

                                elif enemy_wave == 2:
                                    pg.mixer.Channel(2).play(pg.mixer.Sound('Trepang3/assets/sounds/music/59. GACK/59. GACK(F).MP3'))
                                    pg.mixer.Channel(3).play(pg.mixer.Sound('Trepang3/assets/sounds/voicelines/missions/crash_site/2nd_wave_intro.MP3'))
                                    while pg.mixer.Channel(2).get_busy():
                                        self.update()                            
                                    if pg.mixer.Channel(2).get_busy() == False:
                                        pg.mixer.Channel(2).play(pg.mixer.Sound('Trepang3/assets/sounds/music/59. GACK/59. GACK(B).mp3'),-1)

                                        lvl1enemies = [
                                            Enemy(30, 80, 84, 120, 30, 200, 'h', 'hazmat', 'shield', False),
                                            Enemy(420, 50, 84, 120, 50, 400, 'v', 'hazmat', 'rifle', False),
                                            Enemy(200, 200, 84, 120, 200, 300, 'h', 'hazmat', 'pistol', False),
                                            Enemy(100, 300, 84, 120, 300, 400, 'v', 'hazmat', 'smg', False),
                                            Enemy(300, 500, 84, 120, 500, 300, 'h', 'hazmat', 'rifle', False),
                                            # Enemy(600, 100, 84, 120, 'Trepang3/assets/textures/steve.png', 100, 200, 'h', 100, 100, 'hazmat', False),
                                            # Enemy(400, 600, 84, 120, 'Trepang3/assets/textures/steve.png', 600, 100, 'v', 100, 100, 'hazmat', False),
                                            # Enemy(200, 400, 84, 120, 'Trepang3/assets/textures/steve.png', 400, 100, 'v', 100, 100, 'hazmat', False),
                                            # Enemy(500, 300, 84, 120, 'Trepang3/assets/textures/steve.png', 300, 500, 'h', 100, 100, 'hazmat', False),
                                            # Enemy(700, 400, 84, 120, 'Trepang3/assets/textures/steve.png', 400, 200, 'v', 100, 100, 'hazmat', False),
                                            # Enemy(100, 100, 84, 120, 'Trepang3/assets/textures/steve.png', 100, 300, 'h', 100, 100, 'hazmat', False),
                                            # Enemy(700, 600, 84, 120, 'Trepang3/assets/textures/steve.png', 600, 400, 'v', 100, 100, 'hazmat', False),
                                            # Enemy(100, 500, 84, 120, 'Trepang3/assets/textures/steve.png', 500, 200, 'h', 100, 100, 'hazmat', False),
                                            # Enemy(600, 500, 84, 120, 'Trepang3/assets/textures/steve.png', 500, 300, 'h', 100, 100, 'hazmat', False),
                                            # Enemy(600, 300, 84, 120, 'Trepang3/assets/textures/steve.png', 300, 400, 'h', 100, 100, 'hazmat', False),
                                            # Enemy(400, 200, 84, 120, 'Trepang3/assets/textures/steve.png', 200, 300, 'h', 100, 100, 'hazmat', False),
                                            # Enemy(200, 400, 84, 120, 'Trepang3/assets/textures/steve.png', 400, 100, 'v', 100, 100, 'hazmat', False),
                                            # Enemy(500, 400, 84, 120, 'Trepang3/assets/textures/steve.png', 400, 200, 'v', 100, 100, 'hazmat', False),
                                            # Enemy(300, 300, 84, 120, 'Trepang3/assets/textures/steve.png', 300, 500, 'h', 100, 100, 'hazmat', False),
                                            # Enemy(100, 100, 84, 120, 'Trepang3/assets/textures/steve.png', 100, 300, 'h', 100, 100, 'hazmat', False),
                                            # Enemy(600, 600, 84, 120, 'Trepang3/assets/textures/steve.png', 600, 400, 'v', 100, 100, 'hazmat', False),
                                            # Enemy(400, 500, 84, 120, 'Trepang3/assets/textures/steve.png', 0.5, 500, 400, 'h', 100, 1000, 'heavy', False),
                                            # Enemy(200, 600, 84, 120, 'Trepang3/assets/textures/steve.png', 0.5, 600, 200, 'v', 100, 1000, 'heavy', False),
                                            # Enemy(500, 300, 84, 120, 'Trepang3/assets/textures/steve.png', 0.5, 300, 400, 'h', 100, 1000, 'heavy', False),
                                            # Enemy(300, 200, 84, 120, 'Trepang3/assets/textures/steve.png', 0.5, 200, 300, 'h', 100, 1000, 'heavy', False),
                                            # Enemy(600, 500, 84, 120, 'Trepang3/assets/textures/steve.png', 0.5, 500, 300, 'h', 100, 1000, 'heavy', False),
                                            # Enemy(100, 400, 84, 120, 'Trepang3/assets/textures/steve.png', 0.5, 400, 200, 'v', 100, 1000, 'heavy', False)
                                                    ]
                                        remaining_enemies_get = len(lvl1enemies)

                                elif enemy_wave == 3:
                                    pg.mixer.Channel(2).play(pg.mixer.Sound('Trepang3/assets/sounds/music/59. GACK/59. GACK(C).MP3'))
                                    pg.mixer.Channel(3).play(pg.mixer.Sound('Trepang3/assets/sounds/voicelines/missions/crash_site/3rd_wave_intro.MP3'))
                                    while pg.mixer.Channel(2).get_busy():
                                        pass
                                    if pg.mixer.Channel(2).get_busy() == False:
                                        pg.mixer.Channel(2).play(pg.mixer.Sound('Trepang3/assets/sounds/music/59. GACK/59. GACK(D).mp3'),-1)
                                                                                
                                        lvl1enemies = [
                                            Enemy(30, 80, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 30, 200, 'h', 100, 180, 'talon'),
                                            Enemy(420, 50, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 50, 400, 'v', 100, 180, 'talon'),
                                            Enemy(200, 200, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 200, 300, 'h', 100, 180, 'talon'),
                                            Enemy(100, 300, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 300, 400, 'v', 100, 180, 'talon'),
                                            Enemy(300, 500, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 500, 300, 'h', 100, 180, 'talon'),
                                            Enemy(600, 100, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 100, 200, 'h', 100, 180, 'talon'),
                                            # Enemy(400, 600, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 600, 100, 'v', 100, 180, 'talon'),
                                            # Enemy(200, 400, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 400, 100, 'v', 100, 180, 'talon'),
                                            # Enemy(500, 300, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 300, 500, 'h', 100, 180, 'talon'),
                                            # Enemy(700, 400, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 400, 200, 'v', 100, 180, 'talon'),
                                            # Enemy(100, 100, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 100, 300, 'h', 100, 180, 'talon'),
                                            # Enemy(700, 600, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 600, 400, 'v', 100, 180, 'talon'),
                                            # Enemy(100, 500, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 500, 200, 'h', 100, 180, 'talon'),
                                            # Enemy(600, 500, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 500, 300, 'h', 100, 180, 'talon'),
                                            # Enemy(600, 300, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 300, 400, 'h', 100, 180, 'talon'),
                                            # Enemy(400, 200, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 200, 300, 'h', 100, 180, 'talon'),
                                            # Enemy(200, 400, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 400, 100, 'v', 100, 180, 'talon'),
                                            # Enemy(500, 400, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 400, 200, 'v', 100, 180, 'talon'),
                                            # Enemy(300, 300, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 300, 500, 'h', 100, 180, 'talon'),
                                            # Enemy(100, 100, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 100, 300, 'h', 100, 180, 'talon'),
                                            # Enemy(600, 600, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 600, 400, 'v', 100, 180, 'talon'),
                                            # Enemy(400, 500, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 500, 400, 'h', 100, 180, 'talon'),
                                            # Enemy(200, 600, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 600, 200, 'v', 100, 180, 'talon'),
                                            # Enemy(500, 300, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 300, 400, 'h', 100, 180, 'talon'),
                                            # Enemy(300, 200, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 200, 300, 'h', 100, 180, 'talon'),
                                            # Enemy(600, 500, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 500, 300, 'h', 100, 180, 'talon'),
                                            # Enemy(100, 400, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 400, 200, 'v', 100, 180, 'talon'),
                                            # Enemy(700, 300, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 300, 500, 'h', 100, 180, 'talon'),
                                            # Enemy(500, 600, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 600, 400, 'v', 100, 180, 'talon'),
                                            # Enemy(100, 200, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 200, 300, 'h', 100, 180, 'talon'),
                                            # Enemy(600, 200, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 200, 500, 'h', 100, 180, 'talon'),
                                            # Enemy(400, 100, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 100, 300, 'h', 100, 180, 'talon'),
                                            # Enemy(200, 500, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 500, 200, 'v', 100, 180, 'talon'),
                                            # Enemy(500, 400, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 400, 100, 'v', 100, 180, 'talon'),
                                            # Enemy(300, 600, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 600, 400, 'v', 100, 180, 'talon'),
                                            # Enemy(100, 300, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 300, 500, 'h', 100, 180, 'talon'),
                                            # Enemy(600, 100, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 100, 400, 'v', 100, 180, 'talon'),
                                            # Enemy(400, 400, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 400, 100, 'v', 100, 180, 'talon'),
                                            # Enemy(200, 300, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 300, 500, 'h', 100, 180, 'talon'),
                                            # Enemy(500, 300, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 300, 400, 'h', 100, 180, 'talon'),
                                            # Enemy(300, 200, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 200, 300, 'h', 100, 180, 'talon'),
                                            # Enemy(600, 500, 84, 120, 'Trepang3/assets/textures/steve.png', 3, 500, 300, 'h', 100, 180, 'talon')
                                                    ]
                                        remaining_enemies_get = len(lvl1enemies)

                            elif remaining_enemies_get == 1:#Squad down voicelines
                                pg.mixer.Channel(4).set_volume(5)
                                if randint < 5 and enemy_wave < 3:
                                    if randint == 0:                                #MALLCOP VOICELINES
                                        pg.mixer.Channel(4).play(mallcop_voicelines['squad_down']['squad_down_1'])
                                    elif randint == 1:
                                        pg.mixer.Channel(4).play(mallcop_voicelines['squad_down']['squad_down_2'])
                                    elif randint == 2:
                                        pg.mixer.Channel(4).play(mallcop_voicelines['squad_down']['squad_down_3'])
                                    elif randint == 3:
                                        pg.mixer.Channel(4).play(mallcop_voicelines['squad_down']['squad_down_4'])
                                    elif randint == 4:
                                        pg.mixer.Channel(4).play(mallcop_voicelines['squad_down']['squad_down_5'])
                                    elif randint == 5:
                                        pg.mixer.Channel(4).play(mallcop_voicelines['squad_down']['squad_down_6'])

                                elif randint >= 5 and enemy_wave < 3 and enemy_wave > 0:
                                    if randint == 0:                                #HEAVY VOICELINES
                                        pg.mixer.Channel(4).play(heavy_voicelines['squad_down']['squad_down_1'])
                                    elif randint == 1:
                                        pg.mixer.Channel(4).play(heavy_voicelines['squad_down']['squad_down_2'])
                                    elif randint == 2:
                                        pg.mixer.Channel(4).play(heavy_voicelines['squad_down']['squad_down_3'])
                                    elif randint == 3:
                                        pg.mixer.Channel(4).play(heavy_voicelines['squad_down']['squad_down_4'])
                                    elif randint == 4:
                                        pg.mixer.Channel(4).play(heavy_voicelines['squad_down']['squad_down_5'])
                                    elif randint == 5:
                                        pg.mixer.Channel(4).play(heavy_voicelines['squad_down']['squad_down_6'])

                                elif enemy_wave == 3:
                                    if randint == 0:#TALON VOICELINES
                                        pg.mixer.Channel(4).play(talon_voicelines['squad_down']['squad_down_1'])
                                    elif randint == 1:
                                        pg.mixer.Channel(4).play(talon_voicelines['squad_down']['squad_down_2'])
                                    elif randint == 2:
                                        pg.mixer.Channel(4).play(talon_voicelines['squad_down']['squad_down_3'])
                                    elif randint == 3:
                                        pg.mixer.Channel(4).play(talon_voicelines['squad_down']['squad_down_4'])
                                    elif randint == 4:
                                        pg.mixer.Channel(4).play(talon_voicelines['squad_down']['squad_down_5'])
                                    elif randint == 5:
                                        pg.mixer.Channel(4).play(talon_voicelines['squad_down']['squad_down_6'])
                                    
                            elif remaining_enemies_get > 1:#Friendly down voicelines
                                pg.mixer.Channel(4).set_volume(5)
                                if randint < 5 and enemy_wave < 3:
                                    if randint == 0:#MALLCOP VOICELINES
                                        pg.mixer.Channel(4).play(mallcop_voicelines['friendly_down']['friendly_down_1'])
                                    elif randint == 1:
                                        pg.mixer.Channel(4).play(mallcop_voicelines['friendly_down']['friendly_down_2'])
                                    elif randint == 2:
                                        pg.mixer.Channel(4).play(mallcop_voicelines['friendly_down']['friendly_down_3'])
                                    elif randint == 3:
                                        pg.mixer.Channel(4).play(mallcop_voicelines['friendly_down']['friendly_down_4'])
                                    elif randint == 4:
                                        pg.mixer.Channel(4).play(mallcop_voicelines['friendly_down']['friendly_down_5'])
                                    elif randint == 5:
                                        pg.mixer.Channel(4).play(mallcop_voicelines['friendly_down']['friendly_down_6'])

                                elif randint >= 5 and enemy_wave < 3 and enemy_wave > 0:
                                    if randint == 0:#HEAVY VOICELINES
                                        pg.mixer.Channel(4).play(heavy_voicelines['friendly_down']['friendly_down_1'])
                                    elif randint == 1:
                                        pg.mixer.Channel(4).play(heavy_voicelines['friendly_down']['friendly_down_2'])
                                    elif randint == 2:
                                        pg.mixer.Channel(4).play(heavy_voicelines['friendly_down']['friendly_down_3'])
                                    elif randint == 3:
                                        pg.mixer.Channel(4).play(heavy_voicelines['friendly_down']['friendly_down_4'])
                                    elif randint == 4:
                                        pg.mixer.Channel(4).play(heavy_voicelines['friendly_down']['friendly_down_5'])
                                    elif randint == 5:
                                        pg.mixer.Channel(4).play(heavy_voicelines['friendly_down']['friendly_down_6'])

                                elif enemy_wave == 3:
                                    if randint == 0:#TALON VOICELINES
                                        pg.mixer.Channel(4).play(talon_voicelines['friendly_down']['friendly_down_1'])
                                    elif randint == 1:
                                        pg.mixer.Channel(4).play(talon_voicelines['friendly_down']['friendly_down_2'])
                                    elif randint == 2:
                                        pg.mixer.Channel(4).play(talon_voicelines['friendly_down']['friendly_down_3'])
                                    elif randint == 3:
                                        pg.mixer.Channel(4).play(talon_voicelines['friendly_down']['friendly_down_4'])
                                    elif randint == 4:
                                        pg.mixer.Channel(4).play(talon_voicelines['friendly_down']['friendly_down_5'])
                                    elif randint == 5:
                                        pg.mixer.Channel(4).play(talon_voicelines['friendly_down']['friendly_down_6'])
                            break
            
                for wall in lvl1walls:
                    if player.collide(wall):
                        player.rect.x -= player.x_speed
                        player.rect.y -= player.y_speed

                for wall in lvl1walls:
                    pg.draw.rect(screen, (220, 110, 55), wall)

                player.draw()
                player.move()

                Remaining_enemiesFont = Font(60, 500, True, 20, 'Arial', (240,240,240), f'Оставшиеся враги: {remaining_enemies_get}')
                Remained_enemies = Button(1075, 50, 200, 50, 150, 'Trepang3/assets/textures/air.png', Remaining_enemiesFont, False)  

                if weapon['spas12']['holding']:
                    AmmoBarFont.textSurf =  AmmoBarFont.textDef.render(f'{weapon["spas12"]["magazine"]} | {player_inventory["spas12_bullet"]}          {player_inventory["grenade"]}', True, (255,255,255))
                elif weapon['mk23']['holding']:
                    AmmoBarFont.textSurf =  AmmoBarFont.textDef.render(f'{weapon["mk23"]["magazine"]} | {player_inventory["mk23_bullet"]}          {player_inventory["grenade"]}', True, (255,255,255))
                AmmoBar.update_font(AmmoBarFont.textSurf)

                Remained_enemies.textSurf = Remaining_enemiesFont.textDef.render(f'Оставшиеся враги: {remaining_enemies_get}', True, (255,255,255))
                Remained_enemies.update_font(Remaining_enemiesFont.textSurf)

                MoneyFont.textSurf =  MoneyFont.textDef.render(f'${player_inventory["money"]}', True, (240,240,240))
                Money_counter.update_font(MoneyFont.textSurf)

                ShopMoneyFont.textSurf =  ShopMoneyFont.textDef.render(f'${player_inventory["money"]}', True, (240,240,240))
                Shop_money_counter.update_font(ShopMoneyFont.textSurf)

                if AmmoBar.draw():
                    pass
                if Money_counter.draw():
                    pass
                if Remained_enemies.draw():
                    pass


            elif self.game_state == 'pause_menu':
                enemy.draw()
                player.draw()
                for bullet in bullets:
                    bullet.draw()
                for wall in lvl1walls:
                    pg.draw.rect(screen, (255, 0, 0), wall)
                if PauseBackground.draw():
                    pass
                if ResumeButton.draw():
                    self.game_state = 'play'
                    pg.mixer.Channel(1).stop()
                    pg.mixer.Channel(2).unpause()
                    pg.mixer.Channel(3).unpause()
                    pg.mixer.Channel(4).unpause()
                if ExitButton.draw():
                    self.running = False
                    self.close()
                    sys.exit()
                if ToMenuButton.draw():
                    self.game_state = 'main_menu'
                    pg.mixer.Channel(1).stop()
                    pg.mixer.Channel(2).stop()
                    pg.mixer.Channel(3).stop()
                    pg.mixer.Channel(4).stop()
                    pg.mixer.Channel(1).play(pg.mixer.Sound('Trepang3/assets/sounds/music/57. Where to Next.mp3'),-1)
                    pg.mixer.Channel(1).set_volume(0.25)
                    reload_game()
                for e in pg.event.get():
                    if e.type == pg.KEYDOWN:
                        if e.key == pg.K_ESCAPE:
                            self.game_state = 'play'
                            pg.mixer.Channel(1).stop()
                            pg.mixer.Channel(2).unpause()
                            pg.mixer.Channel(3).unpause()
                            pg.mixer.Channel(4).unpause()
                    elif e.type == pg.MOUSEBUTTONDOWN:
                        x, y = e.pos
                        if 50 < x < 225 and 225 < y < 260:
                            self.game_state = 'play'
                            pg.mixer.music.unpause()
                        elif 50 < x < 360 and 525 < y < 550:
                            sys.exit()
                        elif 50 < x < 360 and 475 < y < 500:
                            self.game_state = 'main_menu'
                            pg.mixer.music.play(loops=-1)
            
            elif self.game_state == 'shop':   
                if level == 1:
                    for enemy in lvl1enemies:
                        enemy.draw()
                player.draw()
                for bullet in bullets:
                    bullet.draw()
                for wall in lvl1walls:
                    pg.draw.rect(screen, (220, 110, 55), wall)
                PauseBackground.draw()
                Shop_background.draw()
                Shop_money_counter.draw()

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.running = False
                        self.close()
                        sys.exit()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE or event.key == pg.K_TAB:
                            self.game_state = 'play'
                            pg.mixer.Channel(1).stop()
                            pg.mixer.Channel(2).unpause()
                            pg.mixer.Channel(3).unpause()
                            pg.mixer.Channel(4).unpause()
                        elif event.key == pg.K_SPACE:
                            player_inventory['spas12_bullet'] = 24
                            player_inventory['mk23_bullet'] = 100
                            player_inventory['money'] -= 750

    def update(self):      
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

        pg.display.update()
        self.clock.tick(FPS)

    def draw(self):
        self.screen.fill('lightblue')

    def close(self):
        pg.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()