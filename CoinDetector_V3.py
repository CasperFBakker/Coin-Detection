# import pygame module
import  pygame
import numpy as np
pygame.init()
import pygame.locals
import os

pygame.font.init()

class ImageHander:

    def __init__(self, foldername):
        self.foldername = foldername
        self.image_names = os.listdir(self.foldername)
        self.number_of_images = len(self.image_names)
        self.n = -1 

    def get_previous_image(self):
        self.n -= 1
        self.n = self.n % self.number_of_images
        return self.give_image()

    def get_next_image(self):
        self.n += 1
        self.n = self.n % self.number_of_images
        return self.give_image()

    def give_image(self):
        filename = os.path.join(self.foldername, self.image_names[self.n])
        return Image(filename)


class Image:

    def __init__(self, filename, s=2):
        self.image = pygame.image.load(filename)
        self.filename = filename.split('/')[-1]
        
        self.size_og = self.image.get_size()
        #self.size = self.image.get_size() 
        self.size = (self.size_og[0] // s, self.size_og[1] // s)
        self.image = pygame.transform.scale(self.image, self.size)

    def get(self):
        return self.image


class Circle:

    def __init__(self, pos, radius, color=pygame.Color(128, 0, 0)):
        self.pos = pos
        self.radius = radius
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.radius, width=2)
    

class Coin(Circle):

    def __init__(self, pos, radius, coin_type):
        super().__init__(pos, radius)
        self.coin_type = coin_type

    def scale(self, image_size):
            if self.radius == 0:
                return 0, 0, 0
            dia_coin_pix = self.radius * 2 
            coin_dia_mm = self.coin_type
            size_pixel = coin_dia_mm / dia_coin_pix # pixel size in mm
            height, width = image_size
            height *= size_pixel
            width *= size_pixel

            return height, width, size_pixel

font = pygame.font.SysFont("Roboto", 30)

screen_display = pygame.display

    
window = True
pressed = False


circles = []

clock = pygame.time.Clock()
FPS = 60
foldername = "/home/casper/Documents/Aardwetenschappen/MSc Thesis/PHZD Test/Top_C/" # os.path.join(os.getcwd(), 'Data')
money = '1_Euro'
img_handler = ImageHander(foldername)
img = img_handler.get_next_image()
width, height = img.size
coin_bank = {"2_Euro": 25.75, "1_Euro": 23.25, "50_Cent": 24.25,
            "20_Cent": 22.25, "10_Cent": 19.75, "5_Cent": 21.25}
surface = screen_display.set_mode(img.size)

while window:
    #surface.fill(white)
    surface.blit(img.get(), (0, 0))

    
    msg = font.render(f'Image size: {img.size_og}', False, pygame.Color(255, 255, 255))
    surface.blit(msg, (10,10))

    x, y = pygame.mouse.get_pos()
    pygame.draw.line(surface, pygame.Color(69, 69, 69), [x, 0], [x, height])
    pygame.draw.line(surface, pygame.Color(69, 69, 69), [width, y], [0, y])


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            window = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_z] and keys[pygame.K_LCTRL]:
            circles.pop()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not pressed:
                xi, yi = pygame.mouse.get_pos()
                circles.append(Coin(0, 0, coin_bank[money]))
                pressed = True

        if event.type == pygame.MOUSEBUTTONUP:
            pressed = False

        if keys[pygame.K_LEFT]:
            img = img_handler.get_previous_image()
            width, height = img.size
            surface = pygame.display.set_mode((width, height))
            circles = []
        if keys[pygame.K_RIGHT]:
            img = img_handler.get_next_image()
            width, height = img.size
            surface = pygame.display.set_mode((width, height))
            circles = []
    if pressed:
        xf, yf = pygame.mouse.get_pos()
        middle = [xi + (xf-xi) // 2, yi + (yf-yi) // 2]
        r_ = abs((xf-xi)//2)
        circles[-1].radius = r_
        circles[-1].pos = middle

    if circles:
        msg = font.render(f'Image: {img.filename}', False, pygame.Color(255, 255, 255))
        surface.blit(msg, (10,50))
        
        w, h, pixelsize = circles[-1].scale(img.size_og) 

        msg = font.render(f'{round(w,2)} mm x {round(h,2)} mm', False, pygame.Color(255, 255, 255))
        msg = font.render(f'Pixel size: {pixelsize}', False, pygame.Color(255, 255, 255))
        surface.blit(msg, (10,75))
        
    for circle in circles:
        circle.draw(surface)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()

# need img.size (unscaled )