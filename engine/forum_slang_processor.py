from http_client import *
import db_manager
from BeautifulSoup import BeautifulSoup
import re
from page import Page

def process_response(robot, page, page_response):
		pages = []
		text = ''
		content = BeautifulSoup(page_response.text).find('div', attrs={'class': 'topic__content'})
		if content is not None:
			text = content.text
		anchors = BeautifulSoup(page_response.text).findAll('a')
		for anchor in anchors:
					if  anchor.has_key('href'):
						href = anchor['href']
						if is_same_host(page.url, href) is True:
							pages.append(Page(href, page.depth, {'action':'default'}))

		open('C:\cygwin64\home\Kuba\working_dir\kobiety.txt', 'a+').write(text)
						
				
		return [], pages