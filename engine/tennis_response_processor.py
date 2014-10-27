from http_client import *
import db_manager
from BeautifulSoup import BeautifulSoup
import re
from page import Page

allPlayers = 0
def process_response(robot, page, page_response):
		global allPlayers
		out_urls = []
		soup = BeautifulSoup(page_response.text)
		pages = []
		anchors = soup.findAll('a')
		if 'action' not in page.args:
			for a in anchors:
				if a.has_key('href'):
					href = a['href']
					if re.compile('\./\?country=[\w\?=&]+').match(href):
						pages.append(Page('/list-players'+href.strip('.'), page.depth-1, {'action':'find_players'}))
		else:
			if page.args['action'] == 'find_players':
				name_ths = soup.findAll('th', {'class':'t-name'})
				for name_th in name_ths:
					for a in name_th.findAll('a'):
						href = a['href']
						if re.compile('/player/[\w]+').match(a['href']):
							#print a
							allPlayers+=1
				for anchor in anchors:
					if anchor.has_key('href'):
						href = anchor['href']
						#print 'testing', href
						if re.compile('\?page=[0-9]+&country=[\w]+&order=[\w]+').match(href+'\n'):
							pages.append(Page('/list-players/'+href.strip('.'), page.depth-1, {'action':'find_players'}))
						
		print allPlayers
		return [], pages