import math, pygame as pg
import random

pg.init()

FPS = 60
ScreenHeight = 1280
ScreenWidht = 720
screen = pg.display.set_mode((ScreenWidht,ScreenHeight),pg.FULLSCREEN)
surf = pg.Surface((1000, 300))
enemy_wave = 0


player_inventory = {
    'spas12_bullet': 24,
    'mk23_bullet': 100,
    'armor' : 100,
    'health' : 100,
    'grenade': 5,
    'money' : 0}
    # Add more items here

weapon = {
    'spas12' : {
        'magazine' : 8,
        'damage' : 180,
        'holding' : True
                }, 
    'mk23' : {
        'magazine' : 13,
          'damage' : 35,
          'holding' : False
                }
        }

weapon_cooldown = {
    'spas12' :  {
        'shot' : 650,
        'reload_tactical' : 1000,
        'reload_empty' : 900,
        'draw' : 900
                },
    'mk23' : {
        'shot' : 125,
        'reload_tactical' : 1000,
        'reload_empty' : 1900,
        'draw' : 500
                }
                   }

def reload_game():
    # Reset player inventory
    player_inventory['spas12_bullet'] = 24
    player_inventory['mk23_bullet'] = 78
    player_inventory['armor'] = 100
    player_inventory['health'] = 100
    player_inventory['grenade'] = 5

    # Reset weapon
    weapon['spas12']['holding'] = True
    weapon['mk23']['holding'] = False
    weapon['spas12']['magazine'] = 8
    weapon['mk23']['magazine'] = 13


class Font:
    def __init__(self, x, y, AntiAlaising, size, family, color, text):
        self.x = x
        self.y = y
        self.textDef = pg.font.SysFont(family, size)
        self.textSurf = self.textDef.render(text, AntiAlaising, color)


class Button(Font):
    def __init__(self, x, y, w, h, transparency, img_path, font, clickable):
        self.rect = pg.Rect(x, y, w, h)
        self.orig_img = pg.image.load(img_path)
        self.img = pg.transform.scale(self.orig_img, (w, h))
        self.clicked = False
        self.transparency = self.img.set_alpha(transparency)
        self.clickable = clickable

        if font is not None:
            self.textSurf = font.textSurf
            self.font = font
        else:
            self.textSurf = None
            self.font = None

    def draw(self):
        screen.blit(self.img, self.rect)

        if self.textSurf is not None:
            text_rect = self.textSurf.get_rect(center=self.rect.center)  # Центровка текста на кнопку
            screen.blit(self.textSurf, text_rect)

        action = False
        pos = pg.mouse.get_pos()            #Установка нажатия мыши
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
                if self.clickable == True:
                    pg.mixer.Sound.play(button_press_sound)

        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action
    
    def update_font(self, new_text):
        self.textSurf = new_text
                  

class Sprite:
    def __init__(self, x, y, w, h, transparency, img_path, e_key_interactive):
        self.rect = pg.Rect(x, y, w, h)
        self.orig_img = pg.image.load(img_path)
        self.img = pg.transform.scale(self.orig_img, (w, h))
        self.x_speed = 0
        self.y_speed = 0
        self.transparency = self.img.set_alpha(transparency)
        self.e_key_interactive = e_key_interactive

    def move(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        

    def draw(self):
        screen.blit(self.img, self.rect)

    def collide(self, obj):
        return self.rect.colliderect(obj)            
    

class Menu:
    def __init__(self, x, y, w, h, img_path):
        self.rect = pg.Rect(x, y, w, h)
        self.orig_img = pg.image.load(img_path)
        self.img = pg.transform.scale(self.orig_img, (w, h))

    def draw(self):
        screen.blit(self.img, self.rect)


class Enemy:
    def __init__(self, x, y, w, h, p1, p2, orient, type, weapon, story):
        self.type = type
        self.weapon = weapon
        randint_1 = random.randint(1, 3)

        # Наложение тексутрки на врагов
        if self.type == 'hazmat': 
            if self.weapon == 'pistol':
                img_path = 'Trepang3/assets/textures/sprites/enemies/hazmat_harry/hazmat_pistol_1.png'
                self.armor = 0
                if not story:
                    self.speed = 2
                else:
                    self.speed = 0

            elif self.weapon =='shotgun':
                img_path = 'Trepang3/assets/textures/sprites/enemies/hazmat_harry/hazmat_shotgun_1.png'
                self.armor = 100
                if not story:
                    self.speed = 2
                else:
                    self.speed = 0

            elif self.weapon == 'rifle':
                if randint_1 == 1:
                    img_path = 'Trepang3/assets/textures/sprites/enemies/hazmat_harry/hazmat_rifle_1.png'
                elif randint_1 == 2:
                    img_path = 'Trepang3/assets/textures/sprites/enemies/hazmat_harry/hazmat_rifle_2.png'
                elif randint_1 == 3:
                    img_path = 'Trepang3/assets/textures/sprites/enemies/hazmat_harry/hazmat_rifle_3.png'
                self.armor = 100
                if not story:
                    self.speed = 2
                else:
                    self.speed = 0

            elif self.weapon == 'smg':
                img_path = 'Trepang3/assets/textures/sprites/enemies/hazmat_harry/hazmat_smg_1.png'
                self.armor = 50
                if not story:
                    self.speed = 2
                else:
                    self.speed = 0

            elif self.weapon == 'sniper':
                img_path = 'Trepang3/assets/textures/sprites/enemies/hazmat_harry/hazmat_sniper_1.png'
                self.armor = 0
                if not story:
                    self.speed = 2
                else:
                    self.speed = 0

            elif self.weapon == 'woodchipper_sniper':
                img_path = 'Trepang3/assets/textures/sprites/enemies/hazmat_harry/hazmat_sniper_2.png'
                self.armor = 100
                if not story:
                    self.speed = 2
                else:
                    self.speed = 0

            elif self.weapon == 'shield':
                img_path = 'Trepang3/assets/textures/sprites/enemies/hazmat_harry/hazmat_shield_1.png'
                self.armor = 500
                if not story:
                    self.speed = 2
                else:
                    self.speed = 0

            self.health = 100

        elif self.type == 'heavy':
            if self.weapon == 'shotgun':
                img_path = 'Trepang3/assets/textures/sprites/enemies/heavy/heavy_shotgun_1.png'
                self.armor = 1000
                self.speed = 0.7
            elif self.weapon == 'minigun':
                img_path = 'Trepang3/assets/textures/sprites/enemies/heavy/heavy_minigun_1.png'
                self.armor = 1000
                self.speed = 0.7

            self.health = 100

        elif self.type == 'talon':
            pass

        elif self.type =='HVT':
            if self.weapon == 'wane':
                img_path = 'Trepang3/assets/textures/sprites/enemies/HVT/wane.png'
                self.armor = 0
                self.speed = 0.7
                self.health = 100


        self.rect = pg.Rect(x, y, w, h)
        self.img = pg.transform.scale(pg.image.load(img_path), (w, h))
        self.p1 = p1
        self.p2 = p2
        self.orient = orient
                    

    def move(self):
        if self.orient == 'h':
            self.rect.x += self.speed
            if self.rect.x >= self.p2 or self.rect.x <= self.p1:
                self.speed *= -1
        else:
            self.rect.y += self.speed
            if self.rect.y >= self.p2 or self.rect.y <= self.p1:
                self.speed *= -1

    def draw(self):
        screen.blit(self.img, (self.rect.x, self.rect.y))

    def voice(self):
        if self.type == 'mallcop':
            voiceline_folder = 'Foundation/assets/sounds/voicelines/enemies/mallcop/'
        elif self.type == 'heavy':
            voiceline_folder = 'Foundation/assets/sounds/voicelines/enemies/heavy/'
        elif self.type == 'talon':
            voiceline_folder = 'Foundation/assets/sounds/voicelines/enemies/talon/'


    
#Я не знаю, как это работает, но оно работает    
class Bullet:                                       
    def __init__(self, x, y, w, h, img_path, mouse):
        self.rect = pg.Rect(x, y, w, h)
        self.img_orig = pg.image.load(img_path) #текстурка
        self.img = pg.transform.scale(self.img_orig, (w, h))
        self.x_speed = 0
        self.y_speed = 0
        self.default_speed = 75                 #скорость пули, за остальное не шарю 
        self.mouse = mouse
        self.float_x = x
        self.float_y = y
        self.set_speed(mouse)
    
    def set_speed(self, to_point):
        x_from, y_from = self.rect.centerx, self.rect.centery
        x_to , y_to = to_point
        dx = x_to - x_from
        dy = y_to - y_from
        x_speed = round(abs((self.default_speed * dx) / math.sqrt(dx**2 + dy**2)), 3)
        y_speed = round(abs((x_speed * dy) / dx), 3)
        if x_to < x_from:
            x_speed *= -1
        if y_to < y_from:
            y_speed *= -1

        self.x_speed = x_speed
        self.y_speed = y_speed
        self.rotate_to_point(self.mouse)

    def rotate_to_point(self, mouse):
        dx, dy = mouse[0] - self.rect.centerx, mouse[1] - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx)) - 90
        self.img = pg.transform.rotate(self.img, angle)
        self.rect = self.img.get_rect(center=self.rect.center)
        self.float_x = self.rect.x
        self.float_y = self.rect.y

    def move(self):
        self.float_x += self.x_speed
        self.float_y += self.y_speed
        self.rect.x = round(self.float_x)
        self.rect.y = round(self.float_y)

    def draw(self):
        screen.blit(self.img, self.rect)

    def collide(self, obj):
        return self.rect.colliderect(obj)

#Объекты в мире
#ammunition_shop = Sprite(100, 100, 64, 64, 255, 'Trepang3/assets/textures/steve.png', True)

#Gui
main_menu = Menu(0, 0, 1280, 720, 'Trepang3/assets/textures/background/main_menu.png')
pause_menu = Menu(0, 0, 1280, 720, 'Trepang3/assets/textures/gui/pause_menu.png')

player = Sprite(1050, 525, 32, 64, 255, 'Trepang3/assets/textures/steve.png', False)
wall = Sprite(100, 100, 64, 64, 255, 'Trepang3/assets/textures/steve.png', False)

font_big = pg.font.SysFont('Arial Black', 25)
font_small = pg.font.SysFont('Arial Black', 20)


#Звуки
Spas12_shot = pg.mixer.Sound('Trepang3/assets/sounds/weapon/spas12/Spas12_shot.MP3')
Spas12_shot.set_volume(0.25)
Spas12_reload_single = pg.mixer.Sound('Trepang3/assets/sounds/weapon/spas12/Spas12_reload.MP3')
Spas12_reload_single.set_volume(0.25)
Spas12_reload_empty = pg.mixer.Sound('Trepang3/assets/sounds/weapon/spas12/Spas12_reload_empty.MP3')
Spas12_reload_single.set_volume(0.25)
Spas12_draw_sound = pg.mixer.Sound('Trepang3/assets/sounds/weapon/spas12/Spas12_draw.MP3')

Mk23_reload_tactical = pg.mixer.Sound('Trepang3/assets/sounds/weapon/mk23_pistol/mk23_reload_tactical.MP3')
Mk23_reload = pg.mixer.Sound('Trepang3/assets/sounds/weapon/mk23_pistol/mk23_reload.MP3')
Mk23_shot = pg.mixer.Sound('Trepang3/assets/sounds/weapon/mk23_pistol/mk23_shot.MP3')
Mk23_shot.set_volume(0.25)

Shot_empty = pg.mixer.Sound('Trepang3/assets/sounds/weapon/Trigger_empty.MP3')

Armor_hit = pg.mixer.Sound('Trepang3/assets/sounds/weapon/Armor_hit.MP3')
Bullet_hit = pg.mixer.Sound('Trepang3/assets/sounds/weapon/Bullet_hit.MP3')
Melee_hit = pg.mixer.Sound('Trepang3/assets/sounds/weapon/Melee_hit_sound.MP3')

kill_confirmed_sound = pg.mixer.Sound('Trepang3/assets/sounds/interface/kill_confirmation.MP3')
kill_confirmed_sound.set_volume(0.5)

button_press_sound = pg.mixer.Sound('Trepang3/assets/sounds/interface/button_press_sound.MP3')
button_press_sound.set_volume(10)


# Текст
BuildVersionFont = Font(5, 700, True, 15, 'Arial', (255, 255, 255), 'Build: InDev Closed Alpha v0.5 / 24.3.2025 20:17 Moscow')
ExitFont = Font(925, 500, True, 30, 'Arial', (240, 240, 240), 'На рабочий стол')
ToMenuFont = Font(925, 425, True, 30, 'Arial', (240, 240, 240), 'Выйти')
NewGameFont = Font(925, 425, True, 30, 'Arial', (240, 240, 240), 'Кампания (В разработке)')
CombatSimulatorFont = Font(925, 350, True, 30, 'Arial', (240, 240, 240), 'Место крушения')
ResumeFont = Font(60, 385, True, 30, 'Arial', (240, 240, 240), 'Продолжить')
AmmoBarFont = Font(60, 500, True, 30, 'Arial', (240, 240, 240), f'{weapon["spas12"]["magazine"]} | {player_inventory["spas12_bullet"]}          {player_inventory["grenade"]}')
MoneyFont = Font(60, 500, True, 20, 'Arial', (240, 240, 240), f'${player_inventory["money"]}')
ShopMoneyFont = Font(60, 500, True, 35, 'Arial', (240, 240, 240), f'${player_inventory["money"]}')
Press_e_to_amunition_shopFont = Font(60, 500, True, 30, 'Arial', (240, 240, 240), f'Припасы')


# Кнопки меню
BuildVersion = Button(110, 700, 100, 13, 150, 'Trepang3/assets/textures/air.png', BuildVersionFont, False)
ResumeButton = Button(5, 235, 400, 50, 150, 'Trepang3/assets/textures/gui/empty_button.png', ResumeFont, True)
NewGameButton = Button(5, 235, 400, 50, 150, 'Trepang3/assets/textures/gui/empty_button.png', NewGameFont, True)
ExitButton = Button(5, 330, 400, 50, 150, 'Trepang3/assets/textures/gui/empty_button.png', ExitFont, True)
ToMenuButton = Button(5, 282, 400, 50, 150, 'Trepang3/assets/textures/gui/empty_button.png', ToMenuFont, True)
CombatSimulatorButton = Button(5, 282, 400, 50, 150, 'Trepang3/assets/textures/gui/empty_button.png',CombatSimulatorFont, True)
PauseBackground = Button(0, -50, 1280, 900, 100, 'Trepang3/assets/textures/gui/empty_button.png', None, False)
AmmoBar = Button(1075, 625, 200, 50, 150, 'Trepang3/assets/textures/gui/empty_button.png', AmmoBarFont, False)
Money_counter = Button(1075, 75, 200, 50, 150, 'Trepang3/assets/textures/air.png', MoneyFont, False)
Shop_background = Button(200, 60, 900, 600, 243, 'Trepang3/assets/textures/gui/e_key_button.png', None, False)
Shop_money_counter = Button(250, 100, 100, 50, 255, 'Trepang3/assets/textures/air.png', ShopMoneyFont, False)



subtitles_font = {
    'crash_site' : {
        'intro1' : Font(400,400, True, 25, 'Arial', (255,255,255), 'ОТРЯД ХИМЗАЩИТЫ: Сэр, мы просканировали груз, радиационного заражения нет. Всё готово к забору.'),
        'intro2' : Font(0,0, True, 25, 'Arial', (255,255,255), 'ОТРЯД ХИМЗАЩИТЫ: Принято... Так точно... Да, сэр... Так точно, сэр... Приято, конец связи.'),
        'intro3' : Font(0,0, True, 25, 'Arial', (255,255,255), 'ОТРЯД ХИМЗАЩИТЫ: Думал он никогда не заткнётся...'),
        'intro4' : Font(0,0, True, 25, 'Arial', (255,255,255), 'ОТРЯД ХИМЗАЩИТЫ: Ладно, народ, мы почти закончили.')
    }
}

subtitles = {
    'crash_site' : {
            'intro1' : Button(400, 400, 200, 50, 150, 'Trepang3/assets/textures/air.png', subtitles_font['crash_site']['intro1'], False),
            'intro2' : Button(400, 400, 200, 50, 150, 'Trepang3/assets/textures/air.png', subtitles_font['crash_site']['intro2'], False),
            'intro3' : Button(400, 400, 200, 50, 150, 'Trepang3/assets/textures/air.png', subtitles_font['crash_site']['intro3'], False),
            'intro4' : Button(400, 400, 200, 50, 150, 'Trepang3/assets/textures/air.png', subtitles_font['crash_site']['intro4'], False)
    }
}


mallcop_voicelines = {
    'squad_down' : {
        'squad_down_1' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/mallcop/squad_down_1.MP3'),
        'squad_down_2' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/mallcop/squad_down_2.MP3'),
        'squad_down_3' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/mallcop/squad_down_3.MP3'),
        'squad_down_4' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/mallcop/squad_down_4.MP3'),
        'squad_down_5' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/mallcop/squad_down_5.MP3'),
        'squad_down_6' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/mallcop/squad_down_6.MP3')
    },
    'friendly_down' : {
        'friendly_down_1' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/mallcop/friendly_down_1.MP3'),
        'friendly_down_2' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/mallcop/friendly_down_2.MP3'),
        'friendly_down_3' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/mallcop/friendly_down_3.MP3'),
        'friendly_down_4' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/mallcop/friendly_down_4.MP3'),
        'friendly_down_5' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/mallcop/friendly_down_5.MP3'),
        'friendly_down_6' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/mallcop/friendly_down_6.MP3')
    }
}

heavy_voicelines = {
    'squad_down' : {
        'squad_down_1' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/heavy/squad_down_1.MP3'),
        'squad_down_2' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/heavy/squad_down_2.MP3'),
        'squad_down_3' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/heavy/squad_down_3.MP3'),
        'squad_down_4' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/heavy/squad_down_4.MP3'),
        'squad_down_5' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/heavy/squad_down_5.MP3'),
        'squad_down_6' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/heavy/squad_down_6.MP3')
    },
    'friendly_down' : {
        'friendly_down_1' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/heavy/friendly_down_1.MP3'),
        'friendly_down_2' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/heavy/friendly_down_2.MP3'),
        'friendly_down_3' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/heavy/friendly_down_3.MP3'),
        'friendly_down_4' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/heavy/friendly_down_4.MP3'),
        'friendly_down_5' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/heavy/friendly_down_5.MP3'),
        'friendly_down_6' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/heavy/friendly_down_6.MP3')
    }
}

talon_voicelines = {
    'squad_down' : {
        'squad_down_1' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/talon/squad_down_1.MP3'),
        'squad_down_2' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/talon/squad_down_2.MP3'),
        'squad_down_3' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/talon/squad_down_3.MP3'),
        'squad_down_4' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/talon/squad_down_4.MP3'),
        'squad_down_5' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/talon/squad_down_5.MP3'),
        'squad_down_6' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/talon/squad_down_6.MP3')
    },
    'friendly_down' : {
        'friendly_down_1' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/talon/friendly_down_1.MP3'),
        'friendly_down_2' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/talon/friendly_down_2.MP3'),
        'friendly_down_3' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/talon/friendly_down_3.MP3'),
        'friendly_down_4' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/talon/friendly_down_4.MP3'),
        'friendly_down_5' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/talon/friendly_down_5.MP3'),
        'friendly_down_6' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/enemies/talon/friendly_down_6.MP3')
    }
}

crash_site_voicelines = {
    'intro' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/missions/crash_site/intro.MP3'),
    'contact' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/missions/crash_site/1st_contact.MP3'),
    '1st_wave_intro' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/missions/crash_site/1st_wave_intro.MP3')
}

HVTs_voicelines = {
    'Wane_intro' : pg.mixer.Sound('Trepang3/assets/sounds/voicelines/HVTs/HVT_wane_intro.MP3')
}