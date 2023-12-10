def battle(hero1, hero2):
	while hero1.health > 0 and hero2.health > 0:
		if (hero1.speed > hero2.speed) or (hero1.speed == hero2.speed):
			attacker = hero1
			defender = hero2
		else:
			attacker = hero2
			defender = hero1

		damage_dealt = attacker.attack * (1 - (defender.defense/100))

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
	battle()
