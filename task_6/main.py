import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from PIL import Image


# Вот тут дату читаешь и в словарь пихаешь
def read_data(path):
	data = {}
	with open(path, 'r') as file:
		next(file)
		for line in file:
			line = line.strip().split('\t')
			position = int(line[1])
			nucleotides = {'A': int(line[2]), 'T': int(line[3]), 'G': int(line[4]), 'C': int(line[5])}
			coverage = int(line[6])
			data[position] = {'nucleotides': nucleotides, 'coverage': coverage}
	return data


# Вот тут из словаря последовательность делаешь
def rec_seq(data):
	max_position = max(data.keys())
	min_position = min(data.keys())

	rec_sequence = ''
	coverage_stats = []

	for pos in range(1, max_position + 1):
		if pos in data:
			coverage = data[pos]['coverage']
			nucleotides = data[pos]['nucleotides']

			if coverage >= 80:
				max_nucleotide = max(nucleotides, key=nucleotides.get)
				rec_sequence += max_nucleotide
				coverage_stats.append(coverage)
			else:
				rec_sequence += '-'
		else:
			rec_sequence += '-'

	return rec_sequence


# Г и Ц букавы считаешь
def gc_count(sequence):
	bykavi_count = len(sequence)
	gc_bykavok = sequence.count('G') + sequence.count('C')
	gc_sostav = (gc_bykavok / bykavi_count) * 100
	print(f'GC-состав - {gc_sostav}%')


# Брух плот строишь
def bruh_plot(sequence):
	counts = {
		'A': (sequence.count('A') / len(sequence)),
		'T': (sequence.count('T') / len(sequence)),
		'G': (sequence.count('G') / len(sequence)),
		'C': (sequence.count('C') / len(sequence))
	}

	nucleotides = list(counts.keys())
	values = list(counts.values())

	plt.bar(nucleotides, values, color=['blue', 'green', 'red', 'purple'])
	plt.xlabel('Nucleotides')
	plt.ylabel('Count')
	plt.title('Nucleotide Ratio')
	plt.show()


# А вот тут график покрытия строишь
def karnoval(data):
	img = Image.open('KDE.png')
	img.show()
	max_position = max(data.keys())
	positions = list(data.keys())
	coverages = [data[pos]['coverage'] for pos in positions]

	for pos in range(1, max_position):
		if pos not in data:
			positions.append(pos)
			coverages.append(0)

	df = pd.DataFrame({'Position': positions, 'Coverage': coverages})
	sb.kdeplot(data=df, x='Position', y='Coverage', fill=True)
	plt.xlabel('Position')
	plt.ylabel('Coverage')
	plt.title('Coverage Distribution (KDE)')


if __name__ == '__main__':
	seq_path = '6_coverage.txt'
	txt_data = read_data(seq_path)

	seq1 = rec_seq(txt_data)
	gc_count(seq1)
	bruh_plot(seq1)
	karnoval(txt_data)
