import pandas as pd
import sys
from make_xml import *

def create_xml_for_turf(df):
    #df.drop_duplicates(subset=['Id'], inplace=True)
    
    df['service-duration'] = 24 * df['service-duration']

    xml = ['<services>']
    xml.append(df.to_xml_turfs())
    xml.append('</services>')

    return '\n'.join(xml)

def fix_time(x):
    def time_to_hour(x):
        x = x.split(':')
        return float(x[0])+float(x[1])/60 + float(x[2])/3600
    x = str(x).split('d')
    time = x[1]
    return float(x[0])*24 + time_to_hour(time)

def getPriority1(df, start, end):
	df['start-time'] = df['start-time'].apply(lambda x: fix_time(x))
	df['end-time'] = df['end-time'].apply(lambda x: fix_time(x))

	df = df[(df['start-time'] > start) & (df['end-time'] < end)]

	#print(df)
	#input("press enter ...")

	return df


if __name__ == '__main__':
	if len(sys.argv) < 3:
		exit()
	pd.DataFrame.to_xml_turfs = to_xml_turfs
	pd.DataFrame.to_xml_vehicle = to_xml_vehicle

	df = pd.read_csv('ODL_Inputs_hold_test.csv')
	df = getPriority1(df, int(sys.argv[1]), int(sys.argv[2]))

	xml = ['<?xml version="1.0" encoding="UTF-8"?>']
	xml.append('<problem      xmlns = "http://www.w3schools.com"   xmlns:xsi = "http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation = "http://www.w3schools.com vrp_xml_schema.xsd" >')
	xml.append('<problemType>\n<fleetSize>FINITE</fleetSize>\n<fleetComposition>HOMOGENEOUS</fleetComposition>\n</problemType>')
	xml.append(create_xml_for_vehicle(int(sys.argv[1]), int(sys.argv[2])))
	xml.append(create_xml_for_turf(df))
	xml.append('</problem>')
    #print("\n".join(xml))
	with open('/home/usman/Downloads/Turf_Clusters/72GM/problem_setup.xml', 'w') as f:
		f.write("\n".join(xml))