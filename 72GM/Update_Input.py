import pandas as pd
import numpy as np
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

def getUnassignedJobs(filename):

	uJobs = []

	tree = ET.parse(filename)
	root = tree.getroot()

	solutions = root.find('{http://www.w3schools.com}solutions')
	solution = solutions.findall('{http://www.w3schools.com}solution')[1]
	try:
		unassignedJobs = solution.findall('{http://www.w3schools.com}unassignedJobs')[0]
	except IndexError:
		return ["nothing_here_folks"]

	for i in unassignedJobs.iter():
		zig = dict(i.attrib)
		try:
			uJobs.append(list(zig.values())[0])
		except IndexError:
			pass
	print(len(uJobs))
	return uJobs

def updateInputFile(filename, df_solution, unassignedJobs, d): #an argument specifying the day should be passed

	df = pd.read_csv(filename)
	
	###This gives the the list of unassigned jobs for the particular day
	df_updates = df[df['Id'].isin(unassignedJobs)]
	
	##Get the assigned jobs as well
	df_assigned = df[~df['Id'].isin(unassignedJobs)]

	unassignedJobs = [raw_id.split("_")[0] for raw_id in unassignedJobs]
	assignedJobs = np.array(df_solution['job-Id'])
	assignedJobs = [raw_id.split("_")[0] for raw_id in assignedJobs]
	#print(assignedJobs)

	df_updates['raw_id'] = df_updates['Id'].apply(lambda x: x.split("_")[0])
	
	df_solution = df_solution[df_solution['activity'] == 'delivery']
	df_solution['raw_id'] = df_solution['job-Id'].apply(lambda x: x.split("_")[0])
	df_solution['Day'] = df_solution['arrTime'].apply(lambda x: int(float(x)/24))
	df_updates = df_updates.merge(df_solution[['raw_id', 'Day']], on='raw_id', how='left')

	for i in df_updates.index:
		if df_updates.ix[i]['raw_id'] in assignedJobs:
			#if B1 service level, do it within the next 
			if df_updates.ix[i]['Level'] == 'B1' and df_updates.ix[i]['required-skills'] == 'neighbourhood':
				#look at the board
				if df_updates.ix[i]['Day'] == 0:
					df_updates.set_value(i, 'start-time', str(10) + "d 06:00:00")
					df_updates.set_value(i, 'end-time', str(13) + "d 14:45:00")
				if df_updates.ix[i]['Day'] == 1:
					df_updates.set_value(i, 'start-time', str(10) + "d 06:00:00")
					df_updates.set_value(i, 'end-time', str(13) + "d 14:45:00")
				if df_updates.ix[i]['Day'] == 2:
					df_updates.set_value(i, 'start-time', str(11) + "d 06:00:00")
					df_updates.set_value(i, 'end-time', str(14) + "d 14:45:00")
				if df_updates.ix[i]['Day'] == 3:
					df_updates.set_value(i, 'start-time', str(12) + "d 06:00:00")
					df_updates.set_value(i, 'end-time', str(15) + "d 14:45:00")
				if df_updates.ix[i]['Day'] == 4:
					df_updates.set_value(i, 'start-time', str(13) + "d 06:00:00")
					df_updates.set_value(i, 'end-time', str(16) + "d 14:45:00")
				if df_updates.ix[i]['Day'] == 5:
					df_updates.set_value(i, 'start-time', str(14) + "d 06:00:00")
					df_updates.set_value(i, 'end-time', str(17) + "d 14:45:00")
				if df_updates.ix[i]['Day'] == 6:
					df_updates.set_value(i, 'start-time', str(15) + "d 06:00:00")
					df_updates.set_value(i, 'end-time', str(18) + "d 14:45:00")
				if df_updates.ix[i]['Day'] == 7:
					df_updates.set_value(i, 'start-time', str(16) + "d 06:00:00")
					df_updates.set_value(i, 'end-time', str(19) + "d 14:45:00")
				if df_updates.ix[i]['Day'] == 8:
					df_updates.set_value(i, 'start-time', str(17) + "d 06:00:00")
					df_updates.set_value(i, 'end-time', str(20) + "d 14:45:00")
				if df_updates.ix[i]['Day'] == 9:
					df_updates.set_value(i, 'start-time', str(18) + "d 06:00:00")
					df_updates.set_value(i, 'end-time', str(20) + "d 14:45:00")
				#if df_updates.ix[i]['Day'] == 10:
				#	df_updates.set_value(i, 'start-time', str(15) + "d 06:00:00")
				#	df_updates.set_value(i, 'end-time', str(20) + "d 14:45:00")
				if df_updates.ix[i]['end-time'] == '20d 14:45:00':
					if 11-df_updates.ix[i]['Day'] > 10 and 11-df_updates.ix[i]['Day'] < 1: 
						df_updates.set_value(i, 'priority', (11 - df_updates.ix[i]['Day']))
					else:
						df_updates.set_value(i, 'priority', 1)

	return df_updates

if __name__ == '__main__':
	
	day = int(sys.argv[1])

	filename = '/home/usman/jsprit/jsprit-examples/output/usman_data_.xml'

	unassignedJobs = getUnassignedJobs(filename)
	
	df_solution = getSolution(filename)

	df = updateInputFile('/home/usman/PycharmProjects/jsprit_create_xml/72GM/ODL_Inputs_hold_test.csv',
		df_solution, unassignedJobs, day)
	
	df.drop('Day', axis=1, inplace=True)
	df.drop_duplicates(inplace=True)
	#df.drop_duplicates(subset=['Id'], inplace=True)
	df.to_csv('/home/usman/PycharmProjects/jsprit_create_xml/72GM/ODL_Inputs_hold_test.csv', index = False)