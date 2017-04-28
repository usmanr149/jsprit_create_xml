import pandas as pd
import xml.etree.ElementTree as ET
import lxml.etree as etree
import sys
import time

def getSolution(filename):

	df = pd.DataFrame(columns = ['vehicle-Id', 'activity', 'job-Id', 'arrTime', 'endTime'])

	tree = ET.parse(filename)
	root = tree.getroot()

	solutions = root.find('{http://www.w3schools.com}solutions')
	solution = solutions.findall('{http://www.w3schools.com}solution')[0]
	try:
		routes = solution.findall('{http://www.w3schools.com}routes')[0]
		route = routes.findall('{http://www.w3schools.com}route')

		for r in route:
			#print(r.find('{http://www.w3schools.com}vehicleId').text)
			df = df.append(pd.DataFrame(columns = df.columns, data = [[r.find('{http://www.w3schools.com}vehicleId').text, 
				'start', '', 
				'undef', 0]]))
			for details in r.findall('{http://www.w3schools.com}act'):
				df = df.append(pd.DataFrame(columns = df.columns, data = [[r.find('{http://www.w3schools.com}vehicleId').text, 
					'delivery', details.find('{http://www.w3schools.com}serviceId').text, 
					details.find('{http://www.w3schools.com}arrTime').text, 
					details.find('{http://www.w3schools.com}endTime').text]]))
			df = df.append(pd.DataFrame(columns = df.columns, data = [[r.find('{http://www.w3schools.com}vehicleId').text, 
				'end', '', 
				details.find('{http://www.w3schools.com}endTime').text, 'undef']]))
		return df
	except IndexError:
		return df

df = pd.DataFrame(columns = ['vehicle-Id', 'activity', 'job-Id', 'arrTime', 'endTime'])
for i in range(4):
	filename = '/home/usman/jsprit/jsprit-examples/output/usman_data_' + str(i) + '.xml'
	print(filename)
	df = df.append(getSolution(filename))

df.to_csv('72GM_solution.csv', index=False)