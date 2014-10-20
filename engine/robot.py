import time
import threading
from http_client import *
from db_manager import *
from tennis_response_processor import process_response


class Robot(threading.Thread):
	pool = False
	visited = {}
	end_search = False
	data_patterns = []
	session = False
	def __init__(self, pool, patterns):
		threading.Thread.__init__(self)
		self.pool = pool
		self.patterns = patterns
		end_search = False
		
		self.db_initialize()
		
	
	def check_sleep(self):
		if self.pool == [] or not self.pool:
			print 'waiting...'
			time.sleep(1);
			return True
		return False
	
	
	def run(self):
		while not self.end_search:
			if self.check_sleep():
				continue
				
			page = self.pool.get_page()
			if page is False:
				continue
			page_response=get_page(page.url)
			
			if not page_response:
				continue
			print page.url, page.depth

			data, anchors = process_response(self, page, page_response)
			self.pool.add_pages(page, anchors)

	def check_if_visited(self, page):
		del self.pool[0]
		if page.url in self.visited:
				return True
		else:
			self.visited[page.url] = True
	
	def kill(self):
		self.end_search = True
		
	def db_initialize(self):
		engine = create_engine('mysql://re-spider:mike1234@192.168.1.110:3306/re-spider?charset=utf8', echo=False)
		Session = sessionmaker(bind=engine)
		self.session = Session()
