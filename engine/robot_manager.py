import sys
import robot
from pool import Pool
from page import Page

def get_lines_from_file(path):
	tab = [line.strip('\n').split('\t') for line in open(path, 'r').readlines()]
	for i in tab:
		if i[0].startswith('#'):
			del i
	return tab

def main():
	reload(sys)
	sys.setdefaultencoding('utf-8')
	
	patterns = get_lines_from_file('../config/data_patterns.txt')
	start_pages_data = get_lines_from_file('../config/start_pages.txt')	
	
	pages = [Page(page_data[0], int(page_data[1])) for page_data in start_pages_data]
	pool = Pool(pages)
	
	for r in range(100):
		robo = robot.Robot(pool, patterns)
		try:
			robo.start()
		except:
			print ki
			robo.kill()
if __name__ == '__main__':
	main()