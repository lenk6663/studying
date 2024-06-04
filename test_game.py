import unittest
import pygame
import math
import random
import time
from typing import List, Set
from game import *

class TestGame(unittest.TestCase):
    def setUp(self):
        # Инициализация игры:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.islands = [Shop(Coordinates(500, 200), 0, 250),
                       Island(Coordinates(0, 0), 1, 170),
                       Island(Coordinates(850, 80), 2, 200),
                       Island(Coordinates(1000, 420), 3, 180),
                       Island(Coordinates(110, 500), 4, 210)]
        self.boat = Boat(Coordinates(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 200), BOAT_lvl, 90)
        self.rod = Rod(BOAT_lvl, 90)
        self.money = Money(100)
        self.lure = Lure(2, 2, pygame.time.get_ticks())
        self.bait = Bait(10, 1.5)
        self.inventory = Inventory(money=self.money, lure=self.lure, bait=self.bait)
        self.is_open = False
        self.fishplaces = []

    def test_display_text(self):
        # Тест отображения текста
        self.assertTrue(display_text("TEST", 100, 100, 20))

    def test_message(self):
        # Тест отображения временного сообщения
        self.assertTrue(message("TEST", 100, 100, 20, pygame.time.get_ticks(), 2))

    def test_message(self):
        # Тест отображения временного сообщения с истекшим временем
        self.assertFalse(message("TEST", 100, 100, 20, pygame.time.get_ticks(), 0))

    def test_money_display(self):
        # Тест отображения денег
        money = Money(100)
        position = Coordinates(100, 100)
        size = 10
        money.display(self.screen, position, size)
        self.assertTrue(pygame.image.load("contents/money.png"))

    def test_lure_display(self):
        # Тест отображения приманки
        lure = Lure(2, 2, pygame.time.get_ticks())
        position = Coordinates(100, 100)
        size = 10
        lure.display(self.screen, position, size)
        self.assertTrue(pygame.image.load("contents/lure.png"))

    def test_lure_using(self):
        # Тест использования приманки
        lure = Lure(2, 2, pygame.time.get_ticks())
        lure.using(pygame.time.get_ticks() + 5000)
        self.assertTrue(lure.amount == 1)

    def test_bait_display(self):
        # Тест отображения наживки
        bait = Bait(10, 1.5)
        position = Coordinates(100, 100)
        size = 10
        bait.display(self.screen, position, size)
        self.assertTrue(pygame.image.load("contents/bait.png"))

    def test_fish_display(self):
        # Тест отображения рыбы
        fish = Fish(Coordinates(100, 100), "tuna", 1.0, 100)
        position = Coordinates(100, 100)
        size = 10
        fish.display(self.screen, position, size)
        self.assertTrue(pygame.image.load("contents/tuna.png"))

    def test_rod_display_lvl(self):
        # Тест отображения уровня удочки
        rod = Rod(1.0, 100)
        position = Coordinates(100, 100)
        rod.display_lvl(self.screen, position)
        self.assertTrue(pygame.image.load("contents/rod.png"))

    def test_inventory_display(self):
        # Тест отображения инвентаря
        self.inventory.is_open = True
        rod = Rod(1.0, 100)
        boat = Boat(Coordinates(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 200), BOAT_lvl, 90)
        self.assertTrue(self.inventory.display(rod, boat))

    def test_inventory_add_fish(self):
        # Тест добавления рыбы в инвентарь
        fish = Fish(Coordinates(100, 100), "tuna", 1.0, 100)
        self.inventory.add_fish(fish)
        self.assertTrue(self.inventory.fishlist[0] == fish)

    def test_inventory_delete_fish(self):
        # Тест удаления рыбы из инвентаря
        fish = Fish(Coordinates(100, 100), "tuna", 1.0, 100)
        self.inventory.add_fish(fish)
        self.inventory.delete_fish(fish)
        self.assertTrue(len(self.inventory.fishlist) == 0)

    def test_inventory_add_content(self):
        # Тест добавления предмета в инвентарь
        self.inventory.contents[1].amount = 0 
        self.inventory.add_content(1, 2)
        self.assertTrue(self.inventory.contents[1].amount == 2)

    def test_inventory_delete_content(self):
        # Тест удаления предмета из инвентаря
        self.inventory.contents[0].amount = 3
        self.inventory.delete_content(0, 2)
        self.assertTrue(self.inventory.contents[0].amount == 1)

    def test_sellfish_sell(self):
        # Тест продажи рыбы
        fish = Fish(Coordinates(100, 100),"tuna", 1.0, 100)
        self.inventory.add_fish(fish)
        sellfish = SellFish(Coordinates(100, 100), 10, 10, 0)
        self.assertTrue(sellfish.sell(self.inventory, [105, 105], [1]))

    def test_buyobj_buy(self):
        # Тест покупки предмета
        self.inventory.contents[0].amount = 100
        buyobj = BuyObj(Coordinates(100, 100), 10, 10, 1)
        self.assertTrue(buyobj.buy(self.inventory, [105, 105], [1]))

    def test_buyupdates_buy(self):
        # Тест покупки обновления
        buyupdates = BuyUpdates(Coordinates(100, 100), 10, 10, self.rod)
        self.inventory.contents[0].amount = 500
        self.assertTrue(buyupdates.buy(self.inventory, [105, 105], [1]))

    def test_island_draw(self):
        # Тест отрисовки острова
        island = Island(Coordinates(100, 100), 1, 200)
        island.draw(self.screen)
        self