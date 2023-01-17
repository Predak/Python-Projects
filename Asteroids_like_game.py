# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 1
level = 1
highscore = 0
time = 0
image_thrust = 0
upper = 1
lower = -1
speed_amount = .33
turn_speed = .1
cannon_speed = 6
fire_distance = 45
rock_range = upper - lower
difficulty = 1000
missile_pos = [WIDTH * 3, HEIGHT * 3]
missile_vel = [0, 0]
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# ship explosion
ship_explode_info = ImageInfo([45, 45], [90, 90], 35, 24, True)
ss_info = ImageInfo([50, 50], [100, 100], 35, 30, True) 
ss = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/explosion.hasgraphics.png")
ship_explode = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5, 5], [10, 10], 3, 15)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")
soundtrack.set_volume(.6)
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    global turn_speed
    
    def __init__(self, pos, vel, angle, image, info):
        global image_thrust
        
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = 0
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if self.thrust:
            image_thrust = 90
    
    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos
    
    def get_velocity(self):
        return self.vel
    
    def get_angle(self):
        return self.angle

    def add_vel(self):
        self.angle_vel += turn_speed
        
    def minus_vel(self):
        self.angle_vel -= turn_speed
        
    def start(self):
        global ship_thrust_sound
        
        self.thrust = True
        ship_thrust_sound.play()
        
    def stop(self):      
        global ship_thrust_sound
        
        self.thrust = False
        ship_thrust_sound.rewind()
        
    def shoot(self):
        global a_missile, missile_group, cannon_speed, fire_distance
        
        speed = cannon_speed
        cannon_dist = fire_distance
        
        pos = [self.pos[0] + cannon_dist * angle_to_vector(self.angle)[0], self.pos[1] + cannon_dist * angle_to_vector(self.angle)[1]]
        vel_init = [speed * angle_to_vector(self.angle)[0], speed * angle_to_vector(self.angle)[1]] 
        vel = [vel_init[0] + self.vel[0], vel_init[1] + self.vel[1]]
        
        a_missile = Sprite(pos, vel, 0, 0, missile_image, missile_info, missile_sound)
        
        missile_group.add(a_missile)
        
    def draw(self,canvas):
        global image_thrust
        if self.animated:
            EXPLOSION_DIM = [9, 9]
            explosion_index = [self.age % EXPLOSION_DIM[0] // 1, (self.age // EXPLOSION_DIM[0]) % EXPLOSION_DIM[1]]
            canvas.draw_image(self.image, [self.image_center[0] + explosion_index[0] * self.image_size[0], self.image_center[1] + explosion_index[1] * self.image_size[1]], self.image_size, self.pos, self.image_size)
        else:
            canvas.draw_image(self.image, (self.image_center[0] + image_thrust, self.image_center[1]), self.image_size, self.pos, self.image_size, self.angle) 
            
    def update(self):
        global image_thrust
        
        forward = angle_to_vector(self.angle)
        friction = .06
        image_thrust = 0
        
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        if not(self.thrust):
            self.vel[0] += -friction * self.vel[0]
            self.vel[1] += -friction * self.vel[1] 
            
        if self.thrust:
            image_thrust = 90
            
            self.vel[0] += ((forward[0] * 1) - (self.vel[0] * friction))
            self.vel[1] += ((forward[1] * 1) - (self.vel[1] * friction))
            
        # ship exploding
        self.age += .5
        if self.age > self.lifespan:
            return True
        else:
            return False

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = .5
        if sound:
            sound.rewind()
            sound.play()
            
    def get_radius(self):
        return self.radius
    
    def get_velocity(self):
        return self.vel
    
    def get_position(self):
        return self.pos
    
    def collide(self, other_sprite):
        if dist(self.pos, other_sprite.get_position()) <= self.radius + other_sprite.get_radius():
            return True
        else:
            return False
    
    def rock_ship_collide(self, other_sprite):
        if dist(self.pos, other_sprite.get_position()) <= self.radius * 2 + other_sprite.get_radius():
            return True
        else:
            return False
        
    def draw(self, canvas):
        if self.animated:
            current_image_center = (self.age % 24) // 1
            canvas.draw_image(self.image, [self.image_center[0] + current_image_center * self.image_size[0], self.image_center[1]], self.image_size, self.pos, self.image_size)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
          
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]    
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        self.age += .5
        if self.age > self.lifespan:
            return True
        else:
            return False
        

# key handlers, mouse handlers, and helper functions    
def keydown(key):
    DOWN = {"up": my_ship.start, "left": my_ship.minus_vel, "right": my_ship.add_vel, "space": my_ship.shoot}
    
    if started:
        for i in DOWN:
            if key == simplegui.KEY_MAP[i]:
                DOWN[i]()
            
def keyup(key):
    UP = {"up": my_ship.stop, "left": my_ship.add_vel, "right": my_ship.minus_vel}
    
    if started:      
        for i in UP:
            if key == simplegui.KEY_MAP[i]:
                UP[i]()
        
def click(pos):
    global started, my_ship, score, lives, level
    
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
        score = 0
        lives = 5
        level = 1
        soundtrack.play()
        started = True
        
    # drawing helper function
def process_sprite_group(group, canvas):
    global lives, score
    
    for i in set(group):
        i.draw(canvas)
        i.update()
        if i.update():
            group.discard(i)
        if group_collide(rock_group, my_ship):
            lives -= 1
            if lives == 0:
                ship_explosion.add(Ship(my_ship.get_position(), my_ship.get_velocity(), my_ship.get_angle(), ss, ss_info))
 
def high_score(x):
    global highscore
    
    if x > highscore:
        highscore = x
    
    # group collision helpers
def group_collide(group, sprite):
    global explosion_group
    
    for i in set(group):
        if i.collide(sprite):
            group.discard(i)
        if i.collide(sprite):
            explosion_group.add(Sprite(i.get_position(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound))
            return True
    
def group_group_collide(group1, group2):
    global score
    
    for i in set(group1):
        if group_collide(group2, i):
            group1.discard(i)
            score += 100
            return True
        
    # restart and level difficulty helpers        
def restart(group):
    global missile_group, started, rock_group, difficulty, upper, lower, rock_range
    
    for i in set(group):
        if i.update():
            started = False
            missile_group = set([])
            rock_group = set([])
            score = 0
            lives = 5
            level = 1
            difficulty = 1000
            upper = 1
            lower = -1
            rock_range = upper - lower
            soundtrack.rewind()
            ship_thrust_sound.rewind()
        
def level_increase(x):
    global upper, lower, difficulty, speed_amount, rock_range, level
    
    if int(x)  == int(difficulty):
        difficulty += 1000
        level += 1
        upper += speed_amount
        lower -= speed_amount
        rock_range = upper - lower
             
# draw handlers 
def draw(canvas):
    global time, lives, score
    
    # restart
    restart(ship_explosion)
    
    # level increase every 1000 points
    level_increase(score)
    
    # high score
    high_score(score)
    
    # animiate background
    time += 1
    center = debris_info.get_center()
    wtime = (time / 4) % WIDTH
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw and update ship
    if started and lives > 0:
        my_ship.draw(canvas)
        my_ship.update()
    process_sprite_group(ship_explosion, canvas)
    
    # score and time       
    canvas.draw_text('Lives', [30, 50], 30, 'White')
    canvas.draw_text(str(lives), [30, 70], 20, 'White')
    canvas.draw_text('Score', [700, 50], 30, 'White')
    canvas.draw_text(str(score), [700, 70], 20, 'White')
    canvas.draw_text('Level', [700, 90], 20, 'White')
    canvas.draw_text(str(level), [700, 110], 20, 'White')
    canvas.draw_text('High Score', [330, 50], 30, 'Blue')
    canvas.draw_text(str(highscore), [330, 70], 20, 'Blue')

    # missiles
    process_sprite_group(missile_group, canvas)
    group_group_collide(rock_group, missile_group)
    group_group_collide(missile_group, rock_group)

    # rocks
    process_sprite_group(rock_group, canvas)
    process_sprite_group(explosion_group, canvas)
    group_collide(rock_group, my_ship)
        
    # splash
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, my_ship
    if started:
        a_rock = Sprite([random.randrange(WIDTH), random.randrange(HEIGHT)], [(random.random() * rock_range + lower), 
                       (random.random() * rock_range + lower)], 0, random.choice([-.03, .03]), asteroid_image, asteroid_info)
   
    # spawn rock when game starts and not in ships position
        if len(rock_group) < 12 and not a_rock.rock_ship_collide(my_ship):
            rock_group.add(a_rock)
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])
ship_explosion = set([])
                                   
# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1500.0, rock_spawner)

# start
timer.start()
frame.start()