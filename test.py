import sys

newest = sys.argv[1]

with open(newest, 'r') as f:
	firstline = f.readline()
	print(firstline)

	


