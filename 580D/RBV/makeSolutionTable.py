import pandas as pd
import xml.etree.ElementTree as ET
import numpy as np
#import lxml.etree as etree
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


def getUnassigned(filename):

    df = pd.read_csv('../Data/ODL_Inputs_580D.csv')

    unassignedJobs = getUnassignedJobs(filename)
    df_solution = getSolution(filename)

    ###This gives the the list of unassigned jobs for the particular day
    df_updates = df[df['Id'].isin(unassignedJobs)]

    ##Get the assigned jobs as well
    df_assigned = df[~df['Id'].isin(unassignedJobs)]

    unassignedJobs = [raw_id.split("_")[0] for raw_id in unassignedJobs]
    assignedJobs = np.array(df_solution['job-Id'])
    assignedJobs = [raw_id.split("_")[0] for raw_id in assignedJobs]

    df_updates['raw_id'] = df_updates['Id'].apply(lambda x: x.split("_")[0])

    df_solution = df_solution[df_solution['activity'] == 'delivery']
    df_solution['raw_id'] = df_solution['job-Id'].apply(lambda x: x.split("_")[0])
    df_solution['Day'] = df_solution['arrTime'].apply(lambda x: int(float(x) / 24))
    df_updates = df_updates.merge(df_solution[['raw_id', 'Day']], on='raw_id', how='left')

    df_updates = df_updates.drop_duplicates(subset=['Id'])

    return df_updates

if __name__ == "__main__":

    filename = 'RBV_solution.xml'

    df = getSolution(filename)
    #write the solution table to disk
    df.to_csv('RBV_solution.csv', index=False)

    print(getUnassigned(filename))

    #unassigned vehicle
    veh_used = df['vehicle-Id'].unique()
    #print(veh_used)
    df_veh = pd.read_csv('../Data/580D_vehicles.csv')

    #get raw-id
    df_veh['raw_v-id'] = df_veh['vehicle-id'].apply(lambda x: x.split("-")[0])

    df_veh = df_veh[df_veh['raw_v-id'] == "RBV"]

    print(df_veh[~df_veh['vehicle-id'].isin(veh_used)]['vehicle-id'])

'''
df = pd.DataFrame(columns = ['vehicle-Id', 'activity', 'job-Id', 'arrTime', 'endTime'])

filename = '/home/usman/jsprit/jsprit-examples/output/clusterd_MWD_72GM.xml'
print(filename)
df = df.append(getSolution(filename))

df.to_csv('MWD_72GM_solution.csv', index=False)

'''