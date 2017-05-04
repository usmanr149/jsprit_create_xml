import pandas as pd
import datetime as dt
import sys
import random

import numpy as np

df_ = pd.read_csv('/home/analytics/PycharmProjects/jsprit_create_xml/72GM/Data/Equipment_Inventory - Sheet3.csv')

def create_xml_for_vehicle(start, end):
    
    df_vehicle_72GM = pd.read_csv('/home/analytics/PycharmProjects/jsprit_create_xml/72GM/Data/72GM_vehicles.csv')

    df_vehicle_72GM.drop_duplicates(inplace=True)
    df_vehicle_72GM['yard'] = df_vehicle_72GM['vehicle-id'].apply(lambda x: x.split("-")[0])
    #select the yard
    new_df_vehicle_72GM = df_vehicle_72GM[df_vehicle_72GM['yard'] == 'DON']
    #select the time wimdow
    new_df_vehicle_72GM = new_df_vehicle_72GM[(new_df_vehicle_72GM['start-time'] > start) & (new_df_vehicle_72GM['end-time'] < end)]
    print("Number of neighbourhood vehicle: {0}".format(len(new_df_vehicle_72GM[new_df_vehicle_72GM['skills'] == 'neighbourhood'])))
    print("Number of roadway vehicle: {0}".format(len(new_df_vehicle_72GM[new_df_vehicle_72GM['skills'] == 'roadway'])))
    new_df_vehicle_72GM.to_csv('72GM_test.csv')
    #
    #print(len(new_df_vehicle_72GM))
    #input("Press Enter ...")

    xml = ['<vehicles>']
    xml.append(new_df_vehicle_72GM.to_xml_vehicle())
    xml.append('</vehicles>')

    xml.append('<vehicleTypes>')
    xml.append('<type>')
    xml.append('<id>solomonType</id>')
    xml.append('<capacity>10000</capacity>')
    xml.append('<costs>')
    xml.append('<fixed>0.5</fixed>')
    xml.append('<distance>0</distance>')
    xml.append('<time>1</time>')
    xml.append('</costs>')
    xml.append('</type>')
    xml.append('</vehicleTypes>')

    return '\n'.join(xml)


def create_xml_for_turf():
    df = pd.read_csv('/home/analytics/PycharmProjects/jsprit_create_xml/72GM/DON/services_yard_DONNAN ARENA')
    df = df.rename(columns={'pk_site_id': 'raw-Id'})
    df['raw-Id'] = df['raw-Id'].apply(lambda x: int(x))

    df_72GM = pd.read_csv('/home/analytics/PycharmProjects/jsprit_create_xml/72GM/Data/ODL_Inputs_72GM.csv')
    df_72GM.drop_duplicates(subset=['Id'], inplace=True)
    df_72GM['raw-Id'] = df_72GM['Id'].apply(lambda x: int(float(x.split("_")[0])))

    df_72GM = df_72GM.merge(df[['raw-Id', 'yard']],
                            on='raw-Id', how='right')

    df_72GM.dropna(subset=['Id'], inplace=True)

    df_72GM['start-time'] = df_72GM['start-time'].apply(lambda x: fix_time(x))
    df_72GM['end-time'] = df_72GM['end-time'].apply(lambda x: fix_time(x))

    xml = ['<services>']
    xml.append(df_72GM.to_xml_turfs())
    xml.append('</services>')

    return '\n'.join(xml)

def fix_time(x):
    def time_to_hour(x):
        x = x.split(':')
        return float(x[0])+float(x[1])/60 + float(x[2])/3600
    x = str(x).split('d')
    time = x[1]
    return float(x[0])*24 + time_to_hour(time)

def to_xml_vehicle(df, filename=None, mode='w'):
    veh_depot = {}

    for index, row in df_.iterrows():
        veh_depot[row['vehicle_id']] = row['depot_name']

    def row_to_xml(row):
        xml = ["<vehicle>"]
        xml.append('<id>{0}</id>'.format(row['vehicle-id']))
        xml.append('<typeId>solomonType</typeId>'.format(row['vehicle-name']))
        xml.append('<startLocation>')
        xml.append('<id>{0}</id>'.format(veh_depot[row['vehicle-id'].split("_")[0]]))
        xml.append('<coord x="{0}" y="{1}"/>'.format(row['start-longitude'], row['start-latitude']))
        xml.append('</startLocation>')
        xml.append('<endLocation>')
        xml.append('<id>{0}</id>'.format(veh_depot[row['vehicle-id'].split("_")[0]]))
        xml.append('<coord x="{0}" y="{1}"/>'.format(row['start-longitude'], row['start-latitude']))
        xml.append('</endLocation>')
        xml.append('<timeSchedule>')
        xml.append('<start>{0}</start>'.format(row['start-time']))
        xml.append('<end>{0}</end>'.format(row['end-time']))
        xml.append('</timeSchedule>')
        xml.append('<skills>{0}</skills>'.format(row['skills']))
        xml.append('<returnToDepot>true</returnToDepot>')
        xml.append('</vehicle>')

        return '\n'.join(xml)
    res = '\n'.join(df.apply(row_to_xml, axis=1))
    #res = df.apply(row_to_xml, axis=1)

    #res = "\n".join(res)

    if filename is None:
        return res
    with open(filename, mode) as f:
        f.write(res)

def getUnassignedJobs(filename):

    uJobs = []

    tree = ET.parse(filename)
    root = tree.getroot()

    solutions = root.find('{http://www.w3schools.com}solutions')
    solution = solutions.findall('{http://www.w3schools.com}solution')[1]
    unassignedJobs = solution.findall('{http://www.w3schools.com}unassignedJobs')[0]

    for i in unassignedJobs.iter():
        zig = dict(i.attrib)
        try:
            uJobs.append(list(zig.values())[0])
        except IndexError:
            pass
    print(len(uJobs))
    return uJobs

def to_xml_turfs(df, filename=None, mode='w', start=0):
    print("Input: ", len(df))

    print(df[df['required-skills'] =='neighbourhood']['service-duration'].sum()*24)
    print(df[df['required-skills'] =='roadway']['service-duration'].sum()*24)
    def row_to_xml(row):
        xml = ["<service id='{0}' type='delivery'>".format(row['Id'])]
        xml.append('<locationId>{0}</locationId>'.format(str(row['raw-Id'])))
        xml.append('<coord x="{0}" y="{1}"/>'.format(row['longitude'], row['latitude']))
        xml.append('<capacity-demand>1</capacity-demand>')
        #xml.append('<priority>1</priority>'.format(row['priority']))
        xml.append('<duration>{0}</duration>'.format(row['service-duration']*24*0.85))
        xml.append('<timeWindows>')
        xml.append('<timeWindow>')
        if row['Level'] == 'B1':
            if row['Id'].split("_")[1] == "0" or row['Id'].split("_")[2] == "0":
                start_at = fix_time("0d 06:00:00")
                end_at = fix_time("12d 14:45:00")
            else:
                start_at = fix_time("13d 06:00:00")
                end_at = fix_time("20d 14:45:00")
            xml.append('<start>{0}</start>'.format(start_at))
            xml.append('<end>{0}</end>'.format(end_at))
        elif row['Level'] == 'A1' or row['Level'] == 'A2':
            if row['Id'].split("_")[1] == "0" or row['Id'].split("_")[2] == "0":
                start_at = fix_time("4d 06:00:00")
                end_at = fix_time("5d 14:45:00")
            elif row['Id'].split("_")[1] == "1" or row['Id'].split("_")[2] == "1":
                start_at = fix_time("11d 06:00:00")
                end_at = fix_time("12d 14:45:00")
            else:
                start_at = fix_time("18d 06:00:00")
                end_at = fix_time("19d 14:45:00")
            xml.append('<start>{0}</start>'.format(start_at))
            xml.append('<end>{0}</end>'.format(end_at))
        else:
            xml.append('<start>{0}</start>'.format(row['start-time']))
            xml.append('<end>{0}</end>'.format(row['end-time']))
        xml.append('</timeWindow>')
        xml.append('</timeWindows>')
        xml.append('<requiredSkills>{0}</requiredSkills>'.format(row['required-skills']))
        xml.append('</service>')

        return '\n'.join(xml)

    res = '\n'.join(df.apply(row_to_xml, axis=1))


    if filename is None:
        return res
    with open(filename, mode) as f:
        f.write(res)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        exit()
    pd.DataFrame.to_xml_turfs = to_xml_turfs
    pd.DataFrame.to_xml_vehicle = to_xml_vehicle
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<problem      xmlns = "http://www.w3schools.com"   xmlns:xsi = "http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation = "http://www.w3schools.com vrp_xml_schema.xsd" >')
    xml.append('<problemType>\n<fleetSize>FINITE</fleetSize>\n<fleetComposition>HOMOGENEOUS</fleetComposition>\n</problemType>')
    xml.append(create_xml_for_vehicle(int(sys.argv[1]), int(sys.argv[2])))
    xml.append(create_xml_for_turf())
    xml.append('</problem>')
    #print("\n".join(xml))
    with open('/home/analytics/PycharmProjects/jsprit_create_xml/72GM/DON/problem_setup.xml', 'w') as f:
        f.write("\n".join(xml))
