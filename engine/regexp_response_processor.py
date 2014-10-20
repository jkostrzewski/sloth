from http_client import *
import db_manager

def process_response(robot, page, page_response):
		for pattern in robot.patterns:
			data_pattern = re.compile(pattern[0], re.UNICODE)
			found_list = [found[0] for found in data_pattern.findall(page_response.text, re.UNICODE)]
			data = list(set(found_list))
			for data_entry in data:
				if pattern[1] == 'image':
					data_entry = normalize_url(get_hostname(page.url), data_entry)
				print data_entry.encode('utf-8'), pattern[1]
				robot.pool.save_result(data_entry.decode('utf-8') + '\n')
				db_manager.save_result(robot.session, data_entry, page.url, pattern[1])
		
		hrefs = re.findall('href="(https?://[\w\./?=+&-^ ]+[^.png^.pdf^.jpg^.css])"', page_response.text)
		relatives = re.findall('href="(/.+^ )"', page_response.text)
		return data, hrefs+relatives