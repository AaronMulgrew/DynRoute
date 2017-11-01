from bs4 import BeautifulSoup

x = open('output.xml', 'r').read()

y=BeautifulSoup(x)


print y.prettify()

for vehicle in y.findAll('region'):
	print vehicle