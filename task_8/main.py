from heroes import Hero
from battle import battle
import random


def main():
	pass


if __name__ == '__main__':
	Timirka = Hero('YuckTir', 100, 0, 0, 0, 0, 0)
	Tema = Hero('Director', 100, 70, 20, 40, 80, 40)
	Mitya = Hero('Timir', 100, 1, 2, 3, 4, 1)
	Ventil = Hero('Вентиль', 100, 35, 40, 60, 30, 70)
	Vodila = Hero('Ярик', 100, 90, 90, 100, 90, 80)

	wins = {'YuckTir': 0, 'Director': 0, 'Timir': 0, 'Вентиль': 0, 'Ярик': 0}

	for i in range(10000):
		heroes = [Timirka, Tema, Mitya, Ventil, Vodila]
		random.shuffle(heroes)
		hero1, hero2 = heroes[:2]

		winner = battle(hero1, hero2)

		wins[winner.name] += 1

	for name, count in wins.items():
		print(f'{name} - побед {count}')

	max_wins = max(wins.values())
	max_winners = [name for name, count in wins.items() if count == max_wins]

	print(f'Наибольшее количество побед - {max_winners}')
