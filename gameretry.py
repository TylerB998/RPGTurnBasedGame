#Importing modules
import random
import pygame
import button


pygame.init()

#setting my framerate
clock = pygame.time.Clock()
fps = 60


#game window
bottom_panel = 290
screen_width = 1920
screen_height = 900 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')

#define game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
potion_effect = 15
clicked = False

#define fonts
font = pygame.font.SysFont('Times New Roman', 40)

#define colors
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0,0,255)

#load images
#background image
background_img = pygame.image.load('assets/Background/1.png').convert_alpha()
#panel image
panel_img = pygame.image.load('assets/Icons/panel.png').convert_alpha()
#potion image
potion_img = pygame.image.load('assets/Icons/potion.png').convert_alpha()
#sword mouse image
sword_img = pygame.image.load('assets/Icons/sword.png').convert_alpha()


#function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#function for drawing background
def draw_bg():
    screen.blit(background_img, (0, 0))

#function for drawing panel
def draw_panel():
    #draw panel rectangle
    screen.blit(panel_img, (0, screen_height - bottom_panel))
    #show MC stats
    draw_text(f'{mc.name} HP: {mc.hp}', font, blue, 100, screen_height - bottom_panel + 10)
    #show enemy name and health
    for count, i  in enumerate(goblin_list):
        draw_text(f'{i.name} HP: {i.hp}', font, green, 1300, (screen_height - bottom_panel + 10) + count * 60)

#fighter class
class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp 
        self.strength = strength
        self.start_potions = potions 
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0#0:idle, 1:attack, 2:hurt, 3:dead
        self.update_time = pygame.time.get_ticks()
        #load idle images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'assets/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1, img.get_height() * 1))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load attack images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'assets/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1, img.get_height() * 1))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    #update method
    def update(self):
        animation_cooldown = 45
    #handle animation
    #update image
        self.image = self.animation_list[self.action][self.frame_index]
    #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
           self.update_time = pygame.time.get_ticks()
           self.frame_index += 1
    #if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
           self.idle()
    #
    #idle method
    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        #deal damage to enemy
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        #check if target has died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
        damage_taken = DamageTaken(target.rect.centerx, target.rect.y, str(damage), red)
        damage_taken_group.add(damage_taken)
        #set variables to attack animation 
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect)

#healthbar class - Used for getting the health bar, and adjusting the hp from max_hp during battle
class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        #update with new health
        self.hp = hp
        #calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 200, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 200 * ratio, 20))

class DamageTaken(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        #move damage text up
        self.rect.y -= 1
        #delete previous damage text
        self.counter += 1
        if self.counter > 50:
            self.kill()

damage_taken_group = pygame.sprite.Group()

#The main character (mc) stats (x & y position, name, max_hp, strength, potions)
mc = Fighter(240, 500, 'MC', 40, 10, 3)
#The goblin enemy (goblin) stats (x & y position, name, max_hp, strength, potions)
goblin1 = Fighter(1300, 600, 'Goblin', 20, 6, 1)
goblin2 = Fighter(1700, 600, 'Goblin', 20, 6, 1)

goblin_list = []
goblin_list.append(goblin1)
goblin_list.append(goblin2)

mc_health_bar = HealthBar(100, screen_height - bottom_panel + 50, mc.hp, mc.max_hp)
goblin1_health_bar = HealthBar(1300, screen_height - bottom_panel + 50, goblin1.hp, goblin1.max_hp)
goblin2_health_bar = HealthBar(1300, screen_height - bottom_panel + 110, goblin2.hp, goblin2.max_hp)

#create buttons
potion_button = button.Button(screen, 100, screen_height - bottom_panel + 70, potion_img, 64, 64)

run = True

#main game while-loop
while run: 

    clock.tick(fps)
    #draw background
    draw_bg()
    #draw panel
    draw_panel()
    mc_health_bar.draw(mc.hp)
    goblin1_health_bar.draw(goblin1.hp)
    goblin2_health_bar.draw(goblin2.hp)

    #draw MC
    mc.update()
    mc.draw()
    for goblin in goblin_list:
        goblin.update()
        goblin.draw()

    #draw the damage taken text
    damage_taken_group.update()
    damage_taken_group.draw(screen)

    #control player actions
    #reset action variables
    attack = False
    potion = False
    target = None
    #getting the mouse cursor and turning it into a sword when I hover over the enemies
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, goblin in enumerate(goblin_list):
        if goblin.rect.collidepoint(pos):
            #hide mouse
            pygame.mouse.set_visible(False)
            #show sword in place of mouse cursor
            screen.blit(sword_img, pos)
            if clicked == True:
                attack = True
                target = goblin_list[count]
    #drawing the potion
    if potion_button.draw():
        potion = True
    #show number of potions remaining
    draw_text(str(mc.potions), font, red, 150, screen_height - bottom_panel + 70)

    #player action
    if mc.alive == True:
        if current_fighter == 1:
            action_cooldown += 1
            if action_cooldown >= action_wait_time:
                #look for player action
                #attack
                if attack == True and target != None:
                    mc.attack(target)
                    current_fighter += 1
                    action_cooldown = 0
                #potion
                if potion == True:
                    if mc.potions > 0:
                        #check if the potion will heal the player more then max hp
                        if mc.max_hp - mc.hp > potion_effect:
                          heal_amount = potion_effect
                        else:
                            heal_amount =   mc.max_hp - mc.hp
                        mc.hp += heal_amount
                        mc.potions -= 1
                        damage_taken = DamageTaken(mc.rect.centerx, mc.rect.y, str(heal_amount), green)
                        damage_taken_group.add(damage_taken)
                        current_fighter += 1
                        action_cooldown = 0

    #enemy action
    #count & enumerate is used to keep a count of all the goblins in the list. from 0(1) - infinite
    for count, goblin in enumerate(goblin_list):
        if current_fighter == 2 + count:
            if goblin.alive == True:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    #check if goblin needs to heal first
                    if (goblin.hp / goblin.max_hp) < 0.5 and goblin.potions > 0:
                        #check if the potion will heal the goblin more then max hp
                        if goblin.max_hp - goblin.hp > potion_effect:
                          heal_amount = potion_effect
                        else:
                            heal_amount =   goblin.max_hp - goblin.hp
                        goblin.hp += heal_amount
                        goblin.potions -= 1
                        damage_taken = DamageTaken(goblin.rect.centerx, goblin.rect.y, str(heal_amount), green)
                        damage_taken_group.add(damage_taken)
                        current_fighter += 1
                        action_cooldown = 0
                    #attack
                    else:
                        goblin.attack(mc)
                        current_fighter += 1
                        action_cooldown = 0
            else:
                current_fighter += 1
    
    #if all fighters have had a turn then reset the attack action for all fighters
    if current_fighter > total_fighters:
        current_fighter = 1


    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else: 
            click = False

    pygame.display.update()

pygame.quit()
