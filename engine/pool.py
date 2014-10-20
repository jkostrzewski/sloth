import threading
from page import Page
from http_client import get_hostname

class Pool():

	filewrite_buffer_size = 20
	def __init__(self, pages):
		self.pages = pages
		self.lock = threading.Lock()
		self.result_buffer_lock = threading.Lock()
		self.visited = {}
		self.saved = {}
		self.blacklist = get_blacklist()
		self.filewrite_buffer = []
	
	def get_page(self):
		page = False
		try:
			self.lock.acquire()
			if len(self.pages)>0:
				page = self.pages[0]
				del self.pages[0]
		finally:
			self.lock.release()
		return page
	
	def add_pages(self, page, pages_to_add):
		hostname = get_hostname(page.url)
		self.lock.acquire()
		for item in pages_to_add:
			if item.url in self.visited:
				continue
			else:
				if item.url.startswith('/'):
					item.url = hostname+item.url
				if hostname not in self.blacklist and page.depth>0:
					item.depth-=1
					self.pages.append(item)
				self.visited[page.url] = True
		self.lock.release()
		
	def save_result(self, result):
		self.result_buffer_lock.acquire() 
		if len(self.filewrite_buffer) <self.filewrite_buffer_size:
			if result not in self.saved:
				self.filewrite_buffer.append(result)
				self.saved[result] = True
		else:
			f = open('result.txt', 'a+')
			f.writelines(self.filewrite_buffer)
			f.close()
			self.filewrite_buffer = []
		self.result_buffer_lock.release() 
		
		
		
		
		
	
def get_blacklist():
	result = []
	for line in open('../config/blacklist.txt', 'r').readlines():
		result.append(line.strip('\n'))
	return result