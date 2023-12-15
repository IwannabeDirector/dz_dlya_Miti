from heroes import Hero
from random import random


def battle(hero1, hero2):
	while hero1.health > 0 and hero2.health > 0:
		if (hero1.speed > hero2.speed) or (hero1.speed == hero2.speed):
			attacker = hero1
			defender = hero2
		else:
			attacker = hero2
			defender = hero1

		damage_dealt = attacker.attack * (1 - (defender.defense/100))

		if random() < 0.1:
			print('Славянский зажим яйцами!')
			defender.damage_apply(100)

		elif random() < 0.2:
			print('Атака ящеров!!')
			attacker.damage_apply(100)

		elif random() < 0.1:
			print('Выпьем воды Байкальской братья! За победу')
			attacker.attack += 1

		if not defender.dodge():
			if attacker.critical_hit():
				damage_dealt *= 2

			defender.damage_apply(damage_dealt)

		hero1, hero2 = hero2, hero1

	if hero1.health <= 0:
		return hero2
	else:
		return hero1


if __name__ == '__main__':
	biba = Hero('Biba', 100, 50, 100, 25, 50, 10)
	boba = Hero('Boba', 100, 100, 50, 25, 50, 10)
	battle(biba, boba)
