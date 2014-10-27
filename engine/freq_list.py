def process(lines):
	list = [word for word in [line for line in lines]]
	print list

if __name__ == '__main__':
	text = open('result.txt', 'r').readlines()
	process(text)