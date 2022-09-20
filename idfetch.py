from config import FILE

def fetchid():

	opened = open(FILE, "rt")
	return opened.readline()