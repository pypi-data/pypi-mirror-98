import click
import sys
import json

RED = '\033[91m'
BLUE = '\033[34m'
END = '\033[0m'

found_at = []


def __search(search_term, item, parent):
	if isinstance(item, dict):
		for key in item.keys():
			search(search_term, item[key], parent + [key])
	elif isinstance(item, list):
		for i, list_item in enumerate(item):
			search(search_term, list_item, parent + [i])
	else:
		item = str(item)
		if search_term.lower() in item.lower():
			item = item.replace(search_term, f'{RED}{search_term}{END}')
			found_at.append(parent + [f'value: {item}'])


@click.command()
@click.argument('file_name')
@click.argument('search_term')
def main(file_name, search_term):
	with open(file_name, 'r') as file:
		content = json.loads(file.read())
		__search(search_term, content, [])
		if found_at:
			print(f'{BLUE}### SEARCH RESULTS ###{END}')
			for result in found_at:
				for item in result:
					if 'value: ' in str(item):
						print(item.replace('\n', ' '))
					else:
						print(item, end=' -> ')
			print(f'Found {len(found_at)} matches...')
		else:
			print('Nothing found...')
