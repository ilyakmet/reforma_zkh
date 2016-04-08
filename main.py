# -*- coding: utf-8 -*-




import urllib.request
from socket import timeout
from bs4 import BeautifulSoup
from datetime import datetime
import os.path 

#--------------------------------------
#enter filename here, example: test_row.txt
main_file_name = ''
#--------------------------------------

DIR = os.path.abspath(os.curdir) + '/'


def file_len(file):
	count = 0
	for i in file:
		count += 1
	return count

def get_html_test(url, timeout):
	response = urllib.request.urlopen(url, timeout=timeout)
	response = response.read()
	return response

def test_connection():
	try:
		id = [7960045, 8512100, 8512138, 6473675, 8489373, 7964305, 8512150, 6720076, 7964311, 7960239]
		print('start connection test', len(id))
		speed_count = 0
		for i in id:
			time = datetime.now()
			BeautifulSoup(get_html_test('https://www.reformagkh.ru/myhouse/profile/view/' + str(i), 8), "html.parser")
			speed = datetime.now() - time
			print(speed)
			speed_count += float(str(speed).split(':')[2])
		timeout = round(speed_count/len(id)) + 2
		print('mid speed:', timeout)
	except:
		print('connection lost, try again')
		timeout = -1	
	return timeout

def get_html(url, timeout):
	try:
		response = urllib.request.urlopen(url, timeout=timeout)
		response = response.read()
	except:
		response = '0'
	return response

def bsoup(id, timeout):
	try:
		soup = BeautifulSoup(get_html('https://www.reformagkh.ru/myhouse/profile/view/' + id, timeout), "html.parser")
	except(urllib.error.HTTPError, urllib.error.URLError):
		print('connection error')
		soup = 0
	except timeout:
		print('timeout')
		soup = 0
	except:
		print('soup error')
		soup = 0
	return soup

def get_geo(soup):
	try:
		if 'center' in soup.findAll('script')[11]:
			lat,lon = soup.findAll('script')[11].text.split('\n')[3].split('[')[1].split(']')[0].split(',')
		else:
			lat,lon = soup.findAll('script')[12].text.split('\n')[3].split('[')[1].split(']')[0].split(',')
	except:
		print('geo error')
		lat, lon = 'error', 'error'
	return lat, lon

def calc_tools(soup):
	try:
		calc_web = soup.find('div', id='tab1-subtab5').find_all('tbody')
		calc= []
		row = {}
		for i in calc_web[0:len(calc_web):2]:
			res = i.find('tr').text.strip('\n').split('\n')
			row[res[0]] = [x for x in res[1:]] 
		calc_names = ['Водоотведение', 'Газоснабжение', 'Электроснабжение', 'Горячее водоснабжение', 'Отопление', 'Холодное водоснабжение']
		for i in calc_names:
			if len(row[i]) == 1:
				if 'не' in row[i][0]:
					calc.append((0,0,0))
				else:
					calc.append((0,1,0))
			else:
				calc.append((1,1,row[i][2]))
	except:
		print('calc error')
		calc = [('error', 0, 0) for x  in range(0,6)]
	return calc

def get_id(i):
	try:
		id = i.split(',')[1].strip('\n')
	except:
		print('id error')
		id = 'error'
	return id

def main(name, timeout):
	try:
		print('FILE:'  + name)
		border = file_len(open(DIR + name, 'r'))
		f = open(DIR + name, 'r')
		f2 = open(DIR + 'reforma_final_with_geo_and_calc.txt', 'w')
		f2.write('houseid, lat, lon, water_remove, need, dateon, gaz, need, dateon, power, need, dateon, hot, need, dateon, heating, need, dateon, cold, need, dateon\n')
		count = 1
		for i in f:
			time = datetime.now()
			print(str(count) + '/' + str(border))
			id = get_id(i)
			soup = bsoup(id, timeout)
			lat, lon = get_geo(soup)
			f2.write(id + ',' + lat + ',' + lon )
			calc = calc_tools(soup)
			for i in calc:
				for j in i:
					f2.write(',' + str(j))
			f2.write('\n')
			count += 1
			speed = datetime.now() - time
			print('speed:', speed, 'wait:', round((float(str(speed).split(':')[2])*(border-count))/60/60, 2), 'h')	
	except:
		print('ERROR')
		f2.close()
	f2.close()
	print('COMPLETE!')




if __name__ == '__main__':
	test_connection = test_connection()
	if test_connection != -1:
		print('start main')
		main(main_file_name, test_connection)

