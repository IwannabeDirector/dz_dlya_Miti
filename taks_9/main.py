import requests
from bs4 import BeautifulSoup
import pandas as pd


def parsing_gene(gene_number, taxa):
	gene_url = f"https://www.kegg.jp/entry/{taxa}:{gene_number}"
	gene_info = {
		'Нуклеиновая последовательность': '',
		'Аминокислотная последовательность': '',
		'Позиция в геноме': ''
	}

	phenotypes_dictionary = {}

	gene_page = requests.get(gene_url)
	html_code = gene_page.text
	soup = BeautifulSoup(html_code, 'html.parser')

	kekes_list = []
	network_section = soup.find('th', string='Network')
	if network_section:
		disease = network_section.find_next('div', class_='cel')
		if disease:
			for link in disease:
				kekes_list.append(link)
				for i in range(0, len(kekes_list), 3):
					key = kekes_list[i].text
					value = kekes_list[i + 1].strip() if i + 1 < len(kekes_list) else None
					phenotypes_dictionary[key] = value

	list_for_nt = []
	nucleotide_section = soup.find(lambda tag: tag.name == 'th' and 'NT seq' in tag.text)
	if nucleotide_section:
		nt_sequence_tag = nucleotide_section.find_next('td')
		if nt_sequence_tag:
			nt_sequence = nt_sequence_tag.get_text(strip=True)
			list_for_nt = nt_sequence.split()[3:4]
			string_for_nt = ''.join(list_for_nt)
			string_for_nt = string_for_nt[12:]
			gene_info['Нуклеиновая последовательность'] = string_for_nt

	list_for_aa = []
	aminoacid_section = soup.find(lambda tag: tag.name == 'th' and 'AA seq' in tag.text)
	if aminoacid_section:
		aa_seq_tag = aminoacid_section.find_next('td')
		if aa_seq_tag:
			aa_sequence = aa_seq_tag.get_text(strip=True)
			list_for_aa = aa_sequence.split()[3:4]
			string_for_aa = ''.join(list_for_aa)
			string_for_aa = string_for_aa[6:]
			gene_info['Аминокислотная последовательность'] = string_for_aa

	list_for_position = []
	position_section = soup.find(lambda tag: tag.name == 'th' and 'Position' in tag.text)
	if position_section:
		position_tag = position_section.find_next('td')
		if position_tag:
			position = position_tag.get_text(strip=True)
			position_string = ''.join(position)
			elements = position_string.split(':')
			chromosome = 'chr' + elements[0]
			position = elements[1].split('..')
			start_position = position[0]
			end_position = position[1].split('G')[0]

			formatted_position = f'{chromosome}:{start_position}-{end_position}'
			gene_info['Позиция в геноме'] = formatted_position

	return phenotypes_dictionary, gene_info


def parsing_ortho(gene_number, taxa):
	orth_url = f"https://www.kegg.jp/ssdb-bin/ssdb_best?org_gene={taxa}:{gene_number}"
	orth_page = requests.get(orth_url)
	html = orth_page.text

	identificator = []
	SW_score_list = []
	identity_list = []

	soup = BeautifulSoup(html, 'html.parser')
	table_rows = soup.find_all('input', {'type': 'checkbox', 'name': 'ckid'})
	for element in table_rows:
		value = element.get('value')
		identificator.append(value)

	pre_tags = soup.find_all('pre')
	for pre_tag in pre_tags:
		lines = pre_tag.text.split('\n')
		for line in lines[2:-1]:
			line = line.strip().split()
			SW_score_list.append(line[-8])
			identity_list.append(line[-4])

	data = {
		'Col1': identificator,
		'Col2': SW_score_list,
		'Col3': identity_list
	}
	df = pd.DataFrame(data)

	orholog_counts = [10, 100, 200, 500]
	cor = []
	for count in orholog_counts:
		ids = df['Col1'].head(count).unique()

		subset = df[df['Col1'].isin(ids)]

		correlations = subset[['Col2', 'Col3']].corr(method='pearson').iloc[0, 1]
		cor.append(correlations)

	return cor


if __name__ == "__main__":
	taxa = 'hsa'
	gene_number = '7314'

	phenotypes, gene_info = parsing_gene(gene_number, taxa)
	print(f'Вот такую вот жижу напарсил: \nФенотипы{phenotypes}\n')
	for key, value in gene_info.items():
		print(f'{key}: {value}\n')

	cor = parsing_ortho(gene_number, taxa)
	for i, corr in enumerate(cor, start=1):
		print(f"N = {corr}")
