#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request, time, os
from bs4 import *
from urllib.parse import urljoin


def check_filename(filename):
	check = './lubimyczytac_recenzje/' + filename + '.txt'
	it = 0
	while os.path.isfile(check):
		it += 1
		check = './lubimyczytac_recenzje/' + str(it) + '-' + filename + '.txt'
	return check


def converting(page):
	text, scores = list(), list()
	try:
		page_source = urllib.request.urlopen(page).read()
	except urllib.request.HTTPError:
		print(f'HTTP Error 403: Forbidden - Couldn\'t open {page}')

	soup = BeautifulSoup(page_source, "html.parser")

	for div in soup.find_all('div', {'class': 'row comment pt-2 pb-2'}):
		for span in div.find_all('span', {'class': 'big-number'}):
			p = div.find('p', {'class': 'p-expanded js-expanded mb-0'})
			if p is not None:
				scores.append(''.join(span).strip())

				text.append(''.join(p.get_text()).strip())

	for t,s in zip(text, scores):
		key_words = page.rsplit('/',2)[-2:]
		title = '_'.join(key_words)
		filename =  check_filename(title.title() + '_' + s)
		
		with open(filename, 'w+', encoding='utf-8') as file:
			file.write(t)
		file.close()


def crawling(source_page):
	page = source_page
	it = 0

	for i in range(1, 119):
		if i == 1:
			page = source_page
		else:
			page = source_page + '/' + str(i)
		print(page)

		try:
			data = urllib.request.urlopen(page)
		except ValueError:
			print(f'Couldn\'t open {page}')
			continue

		soup = BeautifulSoup(data.read(), "html.parser")

		for link in soup.findAll('a', {'class' : 'authorAllBooks__singleTextTitle float-left'}):
			url = urljoin(page, link['href'])
			url = url.split('#')[0]
			converting(url)

		time.sleep(2)


crawling('https://lubimyczytac.pl/katalog')
