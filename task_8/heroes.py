from random import random


class Hero:
    def __init__(self, name, health, speed, attack, defense, agility, critical_chance):
        self.name = name
        self.health = health
        self.speed = speed
        self.attack = attack
        self.defense = defense
        self.agility = agility
        self.critical_chance = critical_chance

    def damage_apply(self, damage):
        self.health -= damage

    def critical_hit(self):
        return random() < self.critical_chance / 100

    def dodge(self):
        return random() < self.agility / 100
