import pygame
from enum import Enum
import math
import random
from typing import List, Set

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
COLOR1 = (255, 255, 255)
SEACOLOR = (9, 182, 209)
FONT = 'contents/val.ttf'
placenum = 6
BOAT_lvl = 1

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
fishtypes = ['tuna', 'carp', 'barracuda', 'yellow_perch', 'buffalo', 'mackerel', 'rockfish', 'white_bass', 'white_crappie']


class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

def display_text(message, x, y, field_size):
        font_type = pygame.font.Font(FONT, field_size)
        text = font_type.render(message, True, COLOR1)
        screen.blit(text, (x, y))

def message(mes, x, y, size, start, time):
    timer = time + (start - pygame.time.get_ticks()) // 1000
    if timer > 0:
        display_text(mes, x, y, size)


class Object:
    def __init__(self, amount: int):
        self.amount = amount

    def display(self, surface: pygame.Surface, position: Coordinates, size):
        scaled_image = pygame.transform.scale(self.image, (size, size))
        surface.blit(scaled_image, (position.x, position.y+5))
        display_text(str(self.amount), position.x, position.y, 15)


class Money(Object):
    def __init__(self, amount: int):
        super().__init__(amount)
        self.image = pygame.image.load("contents/" + "money.png")


class Lure(Object):
    def __init__(self, amount: int, buff: float, time: int):
        super().__init__(amount)
        self.buff = buff
        self.image = pygame.image.load("contents/" + "lure.png")
        self.useTime = time
        self.price = 50

    def using(self):
        if self.amount > 0:
            timer = 6 + (self.useTime - pygame.time.get_ticks()) // 1000
            if timer == 0:
                self.useTime = pygame.time.get_ticks()
                self.amount -= 1
        if self.amount == 0 or timer < 0:
            timer = 0
            self.useTime = pygame.time.get_ticks()


class Bait(Object):
    def __init__(self, amount: int, buff: float):
        super().__init__(amount)
        self.buff = buff
        self.image = pygame.image.load("contents/" + "bait.png")
        self.price = 40


class Fish:
    def __init__(self, position: Coordinates, type: str, speed: float, price: int):
        self.position = position
        self.type = type
        self.speed = speed
        self.price = price
        self.image = pygame.image.load("contents/" + type+".png")
        self.angle = random.uniform(0, 2 * math.pi)

    def display(self, surface: pygame.Surface, position: Coordinates, size):
        scaled_image = pygame.transform.scale(self.image, (size, size/3*2))
        surface.blit(scaled_image, (position.x, position.y))


class Rod:
    def __init__(self, lvl: float, price: int):
        self.lvl = lvl
        self.price = price
        self.image = pygame.image.load("contents/" + "rod.png")

    def display_lvl(self, surface: pygame.Surface, position: Coordinates):
        scaled_image = pygame.transform.scale(self.image, (50, 50))
        surface.blit(scaled_image, (position.x, position.y - 5))
        display_text("rod lvl: " + str(int(math.log(self.lvl, 1.25)) + 1), position.x + 70, position.y + 10, 20)


class Inventory:
    def __init__(self, money: Object, lure: Lure, bait: Bait):
        self.contents = [money, lure, bait]
        self.fishlist = []
        self.is_open = False

    def add_fish(self, fish: Fish):
        self.fishlist.append(fish)

    def delete_fish(self, fish: Fish):
        if len(self.fishlist):
            self.fishlist.remove(fish)

    def add_content(self, i: int, am: int):
        self.contents[i].amount += am

    def delete_content(self, i: int, am: int):
        if len(self.contents):
            self.contents[i].amount -= am

    def display(self, rod, boat):
        if self.is_open:
            overlay = pygame.Surface((SCREEN_WIDTH - 180, SCREEN_HEIGHT - 180), pygame.SRCALPHA)
            overlay.fill((40, 40, 40, 220))
            screen.blit(overlay, (90, 100))
            display_text("Inventory", 550, 110, 40)
            # отображаем объекты
            position = Coordinates(120, 180)
            for obj in self.contents:
                overlay = pygame.Surface((100, 120), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 100))
                screen.blit(overlay, (position.x - 10, position.y - 10))
                obj.display(screen, position, 80)
                position.y += 135
            # все рыбы
            position = Coordinates(230, 180)
            for i, fish in enumerate(self.fishlist):
                overlay = pygame.Surface((110, 90), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 100))
                screen.blit(overlay, (position.x - 10, position.y - 10))
                fish.display(screen, position, 90)
                position.x += 120
                if position.x >= SCREEN_WIDTH - 200:
                    position.y += 100
                    position.x = 230
            #  уровень лодки
            position = Coordinates(120, 580)
            overlay = pygame.Surface((525, 60), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            screen.blit(overlay, (position.x - 10, position.y - 10))
            position.x += 160
            boat.display_lvl(screen, position)
            # уровень удочки
            position.x = 655
            overlay = pygame.Surface((525, 60), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            screen.blit(overlay, (position.x - 10, position.y - 10))
            position.x += 160
            rod.display_lvl(screen, position)


class SellFish:
    def __init__(self, position, height, width, i):
        self.position = position
        self.width = height
        self.height = width
        self.i = i

    def sell(self, inventory: Inventory):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (self.position.x - 10, self.position.y - 10))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if (self.position.x < mouse[0] < self.position.x + self.width) and (self.position.y < mouse[1] < self.position.y + self.height):
            # если навелись - показали цену
            display_text(str(inventory.fishlist[self.i].price), self.position.x + self.width - 50, self.position.y + self.height - 30, 20)
            # клик - покупка
            if (click[0] == 1):
                inventory.add_content(0, inventory.fishlist[self.i].price)
                inventory.delete_fish(inventory.fishlist[self.i])
                pygame.time.delay(100)


class BuyObj:
    def __init__(self, position, height, width, i):
        self.position = position
        self.width = height
        self.height = width
        self.obj = i

    def buy(self, inventory: Inventory):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (self.position.x - 10, self.position.y - 10))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if (self.position.x < mouse[0] < self.position.x + self.width) and (self.position.y < mouse[1] < self.position.y + self.height):
            # если навелись - показали цену
            display_text(str(inventory.contents[self.obj].price), self.position.x + self.width - 40, self.position.y + self.height - 40, 20)
            # клик - покупка
            if (click[0] == 1) and inventory.contents[0].amount >=  inventory.contents[self.obj].price:
                inventory.delete_content(0, inventory.contents[self.obj].price)
                inventory.add_content(self.obj, 1)
                pygame.time.delay(200)


class BuyUpdates:
    def __init__(self, position, height, width, obj):
        self.position = position
        self.width = height
        self.height = width
        self.obj = obj

    def buy(self, inventory: Inventory):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (self.position.x - 10, self.position.y - 10))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if (self.position.x < mouse[0] < self.position.x + self.width) and (self.position.y < mouse[1] < self.position.y + self.height):
            # если навелись - показали цену
            display_text(str(self.obj.price), self.position.x + self.width - 40, self.position.y + self.height - 30, 20)
            # клик - покупка
            if (click[0] == 1) and inventory.contents[0].amount >=  self.obj.price:
                inventory.delete_content(0, self.obj.price)
                self.obj.lvl += 0.25
                pygame.time.delay(100)


class Island:
    def __init__(self, position, type, size):
        self.position = position
        self.image = pygame.image.load("contents/" + "is"+str(type)+".png")
        self.size = size
        self.is_open = False

    def draw(self, surface: pygame.Surface):
        scaled_image = pygame.transform.scale(self.image, (self.size, self.size))
        surface.blit(scaled_image, (self.position.x, self.position.y))

    def display(self, screen: pygame.Surface, inventory, rod, boat):
        if self.is_open:
            overlay = pygame.Surface((SCREEN_WIDTH - 180, SCREEN_HEIGHT - 200), pygame.SRCALPHA)
            overlay.fill((27, 67, 20, 220))
            screen.blit(overlay, (90, 100))
            position = Coordinates(120, 230)
            display_text("Island", 580, 110, 40)
            if len(inventory.fishlist):
                display_text("click to sell", 580, 160, 20)
            else:
                display_text("you have no fish to sell", 500, 160, 20)
            # отображаем деньги в углу экрана
            position = Coordinates(1110, 120)
            obj = inventory.contents[0]
            obj.display(screen, position, 60)
            # рыбы
            position = Coordinates(170, 210)
            for i, fish in enumerate(inventory.fishlist):
                sellFish = SellFish(position, 110, 90, i)
                sellFish.sell(inventory)
                fish.display(screen, position, 90)
                position.x += 120
                if position.x >= SCREEN_WIDTH - 200:
                    position.y += 100
                    position.x = 170

def near_object(delta, object1, objects):
    for i, object in enumerate(objects):
        if object1.position.y - delta < object.position.y + object.size and object1.position.y + 64 >= object.position.y + object.size and \
        object1.position.x + 64 >= object.position.x and object1.position.x <= object.position.x + object.size or \
        object1.position.y + 64 + delta > object.position.y and object1.position.y - 64 <= object.position.y and \
        object1.position.x + 64 >= object.position.x and object1.position.x <= object.position.x + object.size or \
        object1.position.x - delta < object.position.x + object.size and object1.position.x + 64 >= object.position.x + object.size and \
        object1.position.y >= object.position.y and object1.position.y <= object.position.y + object.size or \
        object1.position.x + 64 + delta > object.position.x and object1.position.x - 64 <= object.position.x and \
        object1.position.y >= object.position.y and object1.position.y <= object.position.y + object.size or \
        object1.position.x + 64 >= object.position.x and object1.position.x <= object.position.x + object.size and \
        object1.position.y >= object.position.y and object1.position.y <= object.position.y + object.size:
            return i
    return -1


class Shop(Island):
    def __init__(self, position, type, size):
        super().__init__(position, type, size)

    def display(self, screen: pygame.Surface, inventory, rod, boat):
            if self.is_open:
                overlay = pygame.Surface((SCREEN_WIDTH - 180, SCREEN_HEIGHT - 150), pygame.SRCALPHA)
                overlay.fill((70, 34, 20, 220))
                screen.blit(overlay, (90, 100))
                position = Coordinates(120, 230)
                display_text("Shop", 580, 110, 40)
                display_text("click to buy", 100, 160, 20)
                if len(inventory.fishlist):
                    display_text("click to sell", 580, 160, 20)
                else:
                    display_text("you have no fish to sell", 500, 160, 20)
                display_text("click to update", 100, 610, 20)
                # отображаем деньги
                position = Coordinates(1110, 120)
                obj = inventory.contents[0]
                obj.display(screen, position, 60)
                # кнопки покупки наживки и прикормки
                position = Coordinates(120, 200)
                for i in range(1,3):
                    obj = inventory.contents[i]
                    buyObj = BuyObj(position, 100, 190, i)
                    buyObj.buy(inventory)
                    position.y += 40
                    obj.display(screen, position, 80)
                    position.y = 400
                # продажа рыбы
                position = Coordinates(230, 200)
                for i, fish in enumerate(inventory.fishlist):
                    sellFish = SellFish(position, 110, 90, i)
                    sellFish.sell(inventory)
                    fish.display(screen, position, 90)
                    position.x += 120
                    if position.x >= SCREEN_WIDTH - 200:
                        position.y += 100
                        position.x = 230
                # улучшить лодку
                position = Coordinates(300, 600)
                buyUpdates = BuyUpdates(position, 435, 60, boat)
                buyUpdates.buy(inventory)
                position.x += 100
                boat.display_lvl(screen, position)
                # улучшить удочку
                position.x = 745
                buyUpdates = BuyUpdates(position, 435, 60, rod)
                buyUpdates.buy(inventory)
                position.x += 100
                rod.display_lvl(screen, position)


class Boat:
    def __init__(self, position: Coordinates, lvl: float, price: int):
        self.position = position
        self.lvl = lvl
        self.price = price
        # в зависимости от направления меняем картинку чтобы лодка "поворачивалась"
        self.images = {
            Direction.UP: pygame.image.load("contents/" + "boat_up.png"),
            Direction.DOWN: pygame.image.load("contents/" + "boat_down.png"),
            Direction.LEFT: pygame.image.load("contents/" + "boat_left.png"),
            Direction.RIGHT: pygame.image.load("contents/" + "boat_right.png"),
        }
        self.current_direction = Direction.DOWN
        self.image = self.images[self.current_direction]

    def display_lvl(self, surface: pygame.Surface, position: Coordinates):
        scaled_image = pygame.transform.scale(self.images[Direction.RIGHT], (64, 40))
        surface.blit(scaled_image, (position.x, position.y))
        # уровень лодки на самом деле дробное число, но так как это степень 1.25 считаем логарифм + 1
        display_text("boat lvl: " + str(int(math.log(self.lvl, 1.25)) + 1), position.x + 80, position.y + 10, 20)

    def move(self, direction: Direction, delta, islands):
        s = 50
        if direction == Direction.UP:
            for island in islands:
                if self.position.y - self.lvl < island.position.y + island.size and self.position.y + s >= island.position.y + island.size and \
                self.position.x + s >= island.position.x and self.position.x <= island.position.x + island.size: # проверки на столкновение
                    return
            self.position.y = max(self.position.y - delta.y, 0) # двигаемся но не за экран
        if direction == Direction.DOWN:
            for island in islands:
                if self.position.y + s + self.lvl > island.position.y and self.position.y - s <= island.position.y and \
                self.position.x + s >= island.position.x and self.position.x <= island.position.x + island.size: # проверки на столкновение
                    return
            self.position.y = min(self.position.y + delta.y, SCREEN_HEIGHT - 64) # двигаемся но не за экран
        if direction == Direction.LEFT:
            for island in islands:
                if self.position.x - self.lvl < island.position.x + island.size and self.position.x + s >= island.position.x + island.size and \
                self.position.y >= island.position.y and self.position.y <= island.position.y + island.size: # проверки на столкновение
                    return
            self.position.x = max(self.position.x - delta.x, 0) # двигаемся но не за экран
        if direction == Direction.RIGHT:
            for island in islands:
                if self.position.x + s + self.lvl > island.position.x and self.position.x - s <= island.position.x and \
                self.position.y >= island.position.y and self.position.y <= island.position.y + island.size: # проверки на столкновение
                    return
            self.position.x = min(self.position.x + delta.x, SCREEN_WIDTH - 64) # двигаемся но не за экран
        # "поворачиваем" лодку (бедный Вилли как у него голова не закружилась)
        self.current_direction = direction
        self.image = self.images[self.current_direction]

    def display(self, surface: pygame.Surface):
        surface.blit(self.image, (self.position.x, self.position.y))  


class Minigame:
    def __init__(self, position: Coordinates):
        self.position = position
        # начинаем определять параметры рыбки, которая тут живет
        self.size = random.randint(30, 50) # размер
        type = fishtypes[random.randint(0, len(fishtypes) - 1)] # тип только на картинку влияет 
        speed = random.randint(100, 15000) / 100 # скорость от 1 до 150 вообще любая дробная
        self.fishsize = random.randint(60, 250) # размер от 60 до 250 любой не дробный
        self.fishtime = int((1 / self.fishsize * 10000) // 6) # считаем время обратным скорости (формула выведена экспериментальным путем)
        price = int(speed + self.fishtime) // 2 # цена = сложность(скорость) поимки рыбы и затраченное на эти страдания время
        self.fish = Fish(Coordinates((SCREEN_WIDTH - self.fishsize) / 2, (SCREEN_HEIGHT - self.fishsize) / 2), type, speed, price) # вот и рыба
        self.is_open = False # изначально ничего не ловим 
        self.start = pygame.time.get_ticks() # опрелили уже старт миниигры чтобы было (чтобы отрицательных чисел потом в таймере не появлялось)
        # print(self.fish.type, "  speed",self.fish.speed,"  fishsize", self.fishsize,"  fishtime", self.fishtime,"  price", self.fish.price) 
        # если раскомментировать предыдущую строчку можно включить читы и подсматрить, что там за рыба такая у нас сейчас ловится

    def draw(self, surface: pygame.Surface):
        # красиво отображаем пузырики по четности-нечетности текущего времени
        scaled_image = pygame.transform.scale(pygame.image.load("contents/" + "fishplace" + str((pygame.time.get_ticks()//300)%2 + 1) + ".png"), (self.size, self.size))
        surface.blit(scaled_image, (self.position.x, self.position.y))

    def move_fish(self):
        # сложный и непонятный алгоритм рандомного движения, который я боюсь менять
        target_x = self.fish.position.x + self.fish.speed * math.cos(self.fish.angle) * (pygame.time.get_ticks() - self.start) / 1000
        target_y = self.fish.position.y + self.fish.speed * math.sin(self.fish.angle) * (pygame.time.get_ticks() - self.start) / 1000
        target_x = max(0, min(SCREEN_WIDTH - self.fishsize, target_x))
        target_y = max(0, min(SCREEN_HEIGHT - self.fishsize, target_y))
        angle_to_target = math.atan2(target_y - self.fish.position.y, target_x - self.fish.position.x)
        self.fish.angle += (angle_to_target - self.fish.angle) / 10
        self.fish.position.x += self.fish.speed * math.cos(self.fish.angle) / 60
        self.fish.position.y += self.fish.speed * math.sin(self.fish.angle) / 60

    def minigame(self, inventory: Inventory, rod: Rod):
        # определяем кучу счетчиков
        self.start = pygame.time.get_ticks() # просто время начала миниигры
        goal = self.fishtime / 1.2 / rod.lvl # сколько нам надо времени ловить рыбу (тип float)
        start2 = self.start - 3000 # определили заранее чтобы не отображалось сообщение (нужно при попытке закрыть миниигру)
        start3 = 0 # это будет время когда мы начали рыбу ловить
        timer1 = self.fishtime # столько времени ещё будет длиться миниигра (до проигрыша)
        timer3 = int(goal) # столько времени надо ловить время но целочисленное чтобы красиво отобразилось для пользователя
        win = False
        if inventory.contents[2].amount > 0 and self.is_open: # если есть наживки - используем
                self.fishsize *= inventory.contents[2].buff
                inventory.contents[2].amount -= 1
        while self.is_open:
            self.move_fish()
            screen.fill(SEACOLOR)
            self.fish.display(screen, self.fish.position, self.fishsize)
            timer1 = int(self.fishtime + (self.start - pygame.time.get_ticks()) // 1000)  # столько времени ещё будет длиться миниигра
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if (self.fish.position.x < mouse[0] < self.fish.position.x + self.fishsize) and (self.fish.position.y < mouse[1] < self.fish.position.y + self.fishsize * 2/3) and (click[0] == 1):
                if start3 == 0: # если мы ещё не начали ловить рыбу до этого то начали сейчас
                    start3 = pygame.time.get_ticks()
                timer3 = int(goal + (start3 - pygame.time.get_ticks()) // 1000)# столько ещё времени надо ловить
            if start3 != 0 and click[0] == 0: # если ловить уже начали но перестали
                start3 = 0 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start2 = pygame.time.get_ticks() # если попытались выйти, то на 3 секунды...
            message("You can't leave at minigame", 940, 10, 20, start2, 3) # выводим сообщение
            display_text(str(timer3) + " / " + str(timer1), 10, 10, 30) # выводим таймеры чтобы понимать сколько осталось страдать
            if timer1 <= 0 or timer3 - timer1 > 2: # если время на миниигру закончилось или если уже точно выиграть не успеешь (экономия времени)
                win = False # проиграли
                self.is_open = False # закрыли
            if timer3 <= 0: # если всё время что надо ловить мы ловили рыбу а не мух
                win = True # победили
                self.is_open = False
            pygame.display.update()
        self.start = pygame.time.get_ticks() # обновляем время чтобы вывести сообщения о результатах этой схватки с рыбой
        if win:
            inventory.add_fish(self.fish)
        while int(3 + (self.start - pygame.time.get_ticks()) // 1000):
            overlay = pygame.Surface((SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50), pygame.SRCALPHA) # прямоугольник для красоты
            overlay.fill((40, 40, 40, 1))
            screen.blit(overlay, (25, 25))
            if win:
                display_text(self.fish.type.replace('_', ' '), (SCREEN_WIDTH - len(self.fish.type*50))//2, 250, 80)
                display_text("is caught", 460, 350, 70)
            else:
                display_text("The fish escaped", 300, 300, 70)
            pygame.display.update()

def main():
    # все определяем:
    islands = [Shop(Coordinates(500, 200), 0, 250), Island(Coordinates(0, 0), 1, 170), Island(Coordinates(850, 80), 2, 200),
            Island(Coordinates(1000, 420), 3, 180), Island(Coordinates(110, 500), 4, 210)]
    boat = Boat(Coordinates(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 200), BOAT_lvl, 90)
    rod = Rod(BOAT_lvl, 90) 
    start_time = pygame.time.get_ticks()
    money = Money(100)
    lure = Lure(2, 2, start_time)
    bait = Bait(10, 1.5)
    inventory = Inventory(money=money, lure=lure, bait=bait)
    is_open = False
    fishplaces = []
    running = True
    while running:
        placenum1 = placenum * lure.buff if lure.amount > 0 else placenum # количество рыбных мест зависит от прикормки
        while len(fishplaces) < placenum1:
            fishplace = Minigame(Coordinates(random.randint(0, SCREEN_WIDTH - 60), random.randint(0, SCREEN_HEIGHT - 60)))
            if near_object(10, fishplace, islands) == -1 and near_object(2, fishplace, fishplaces) == -1:
                fishplaces.append(fishplace) # набираем подходящие места
        while len(fishplaces) > placenum1:
            fishplaces.pop() # убираем если действие прикормки закончилось
        near_island = near_object(boat.lvl, boat, islands)
        near_fishplace = near_object(boat.lvl, boat, fishplaces) # -1 если нет подблизости ничего
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN: # если нажали Е
                if event.key == pygame.K_e:
                    if is_open: # если уже что=то открыли, то все закрываем
                        inventory.is_open = False
                        for i in range(len(islands)):
                            islands[i].is_open = False
                        is_open = False
                    else:
                        is_open = True
                        if near_fishplace != -1: # рыба в приоритете
                            fishplaces[near_fishplace].is_open = True
                        elif near_island != -1:
                            islands[near_island].is_open = True
                        else:
                            inventory.is_open = True
        if not(is_open): # если ничего не открыли, можно дышать и двигаться
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                boat.move(Direction.UP, Coordinates(0, boat.lvl), islands)
            if keys[pygame.K_s]:
                boat.move(Direction.DOWN, Coordinates(0, boat.lvl), islands)
            if keys[pygame.K_a]:
                boat.move(Direction.LEFT, Coordinates(boat.lvl, 0), islands)
            if keys[pygame.K_d]:
                boat.move(Direction.RIGHT, Coordinates(boat.lvl, 0), islands)
            lure.using()
        # рисуем
        screen.fill(SEACOLOR)
        for fishplace in fishplaces:
            fishplace.draw(screen)
        boat.display(screen)
        for island in islands:
            island.draw(screen)
        if near_fishplace != -1: # если рядом с рыбным местом 
            if is_open and fishplaces[near_fishplace].is_open and not(inventory.is_open):
                fishplaces[near_fishplace].minigame(inventory, rod)
                fishplaces.remove(fishplaces[near_fishplace])
                is_open = False
            else: # если ещё не нажали Е то предлагаем это сделать
                display_text("Press E for fishing", 500, 680, 30)
        elif near_island != -1:
            if is_open and islands[near_island].is_open and not(inventory.is_open):
                display_text("Press E to close", 500, 680, 30)
            else:
                display_text("Press E to use", 500, 680, 30)
            islands[near_island].display(screen, inventory, rod, boat) # отображаем интерфейс того острова с которым мы рядом (и что что они все одинаковые?)
        inventory.display(rod, boat) # внутри функции display есть проверка открыт инвентарь или нет
        pygame.display.update()
    pygame.quit()
main()