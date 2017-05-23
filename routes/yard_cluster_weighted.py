import numpy as np
import pandas as pd
import requests

depots = pd.read_csv("data/southside_depots.csv")
depots.columns = ['depot_name','team_lead','latitude','longitude','start_time','id']
depots_mat = depots.as_matrix()
yard_distances = pd.read_csv("distance_yard_services.csv")
vehicles_72GM = pd.read_csv("data/72GM_vehicles.csv")
serv_dur = pd.read_csv("service_duration.csv")

services = pd.read_csv("data/turf_services.csv")
service_points = list(zip(services['latitude'],services['longitude'],services['pk_site_id']))

services = services.set_index('pk_site_id')

df_services = pd.read_csv('data/Input_72GM.csv')

df_services['raw-Id'] = df_services['Id'].apply(lambda x: int(float(x.split("_")[0])))

serv_dur = df_services.groupby('raw-Id')['service-duration'].sum()

df_services = df_services.drop_duplicates('raw-Id').set_index('raw-Id')

service_dict = {}
for x in service_points:
    service_dict[x[2]] = x

#service_dur = dict(serv_dur.as_matrix())

num_vehicles = {'GBY':0,'RBV':0,'OKY':0,'ASY':0,'DON':0,'MWD':0}
labels = ['RBV', 'MWD', 'GBY','OKY', 'ASY', 'DON']

vehicle_yard = [id.split('-')[0] for id in list(vehicles_72GM['vehicle-id'])]
for x in vehicle_yard:
    num_vehicles[x]+=1

load_yard = {k:v*7.65 for k,v in num_vehicles.items()}
load_yard['GBY'] = load_yard['GBY']*7.6/7.75
load_yard['DON'] = load_yard['DON']*1.1

print(load_yard)

# serv_yard = {0:[],1:[],2:[],3:[],4:[],5:[]}
serv_yard = {'GBY':set(),'RBV':set(),'OKY':set(),'ASY':set(),'DON':set(),'MWD':set()}
unassigned = []

#iterate over the depots
solution = []

yard_distances = yard_distances.drop_duplicates()
yard_distances['MWD'] = yard_distances['MWD']*0.8
yard_distances = yard_distances.set_index('id')


#for depot in labels.values():

yard_distance_hold = []

yard_ind = 0

print(load_yard)

yard_distances = yard_distances.merge(services[['latitude', 'longitude']], how='left', right_index=True, left_index=True)

"""
#check for the one that are farthest from every yard but nearest to you
for depot in labels:
    yard_distance_hold = []
    yard_distances = yard_distances.sort(depot, ascending=False)

    time_allocated = 0.8*load_yard[depot]
    time_taken = 0

    for index, row in yard_distances.iloc[:int(len(yard_distances)*1)].iterrows():
        pk_site_id = int(index)
        if row[labels].idxmin() == depot and load_yard[depot] - serv_dur.ix[pk_site_id]>0 and time_taken < time_allocated:
            load_yard[depot] = load_yard[depot] - serv_dur.ix[pk_site_id]
            time_taken+=serv_dur.ix[pk_site_id]
            distance = 0
            latitude = df_services.ix[pk_site_id]['latitude']
            longitude = df_services.ix[pk_site_id]['longitude']
            yard_distance_hold.append(pk_site_id)
            # pk_site_id,latitude,longitude,yard,distance
            solution.append((pk_site_id, latitude, longitude, depot, distance))

    yard_distances = yard_distances.drop(yard_distance_hold)

print(len(yard_distances))
"""

"""
#check for the one that are farthest from every yard but second nearest to you nearest
for depot in labels:
    yard_distance_hold = []
    yard_distances = yard_distances.sort(depot, ascending=False)

    time_allocated = 1*load_yard[depot]
    time_taken = 0

    for index, row in yard_distances.iterrows():
        pk_site_id = int(index)
        if row[labels].drop(row[labels].idxmin()).idxmin() == depot and load_yard[depot] - serv_dur.ix[pk_site_id]>0 and row[depot] < 15000 and time_taken < time_allocated:
            load_yard[depot] = load_yard[depot] - serv_dur.ix[pk_site_id]
            time_taken+=serv_dur.ix[pk_site_id]
            distance = 0
            latitude = df_services.ix[pk_site_id]['latitude']
            longitude = df_services.ix[pk_site_id]['longitude']
            yard_distance_hold.append(pk_site_id)
            # pk_site_id,latitude,longitude,yard,distance
            solution.append((pk_site_id, latitude, longitude, depot, distance))

    yard_distances = yard_distances.drop(yard_distance_hold)

print(len(yard_distances))
print(load_yard)
"""

#empty out goldbar
yard_distance_hold = []
depot = "GBY"
yard_distances = yard_distances.sort(depot)
for index, row in yard_distances.iterrows():
    pk_site_id = int(index)

    if load_yard[depot] - serv_dur.ix[pk_site_id] > 0 and row[depot] < 10000:
        load_yard[depot] = load_yard[depot] - serv_dur.ix[pk_site_id]
        distance = 0
        latitude = df_services.ix[pk_site_id]['latitude']
        longitude = df_services.ix[pk_site_id]['longitude']
        yard_distance_hold.append(pk_site_id)
        # pk_site_id,latitude,longitude,yard,distance
        solution.append((pk_site_id, latitude, longitude, depot, distance))

yard_distances = yard_distances.drop(yard_distance_hold)

#empty out RBV
yard_distance_hold = []
depot = "RBV"
yard_distances = yard_distances.sort(depot)
for index, row in yard_distances.iterrows():
    pk_site_id = int(index)

    if load_yard[depot] - serv_dur.ix[pk_site_id] > 0:
        if row['longitude'] > -113.6474 and row['longitude'] < -113.5533 and row['latitude'] < 53.5040 and row['latitude'] > 53.4490:
            load_yard[depot] = load_yard[depot] - serv_dur.ix[pk_site_id]
            distance = 0
            latitude = df_services.ix[pk_site_id]['latitude']
            longitude = df_services.ix[pk_site_id]['longitude']
            yard_distance_hold.append(pk_site_id)
            # pk_site_id,latitude,longitude,yard,distance
            solution.append((pk_site_id, latitude, longitude, depot, distance))

yard_distances = yard_distances.drop(yard_distance_hold)

#empty out DON
yard_distance_hold = []
depot = "DON"
yard_distances = yard_distances.sort(depot)
for index, row in yard_distances.iterrows():
    pk_site_id = int(index)

    if load_yard[depot] - serv_dur.ix[pk_site_id] > 0 and row[depot] < 12000:
            load_yard[depot] = load_yard[depot] - serv_dur.ix[pk_site_id]
            distance = 0
            latitude = df_services.ix[pk_site_id]['latitude']
            longitude = df_services.ix[pk_site_id]['longitude']
            yard_distance_hold.append(pk_site_id)
            # pk_site_id,latitude,longitude,yard,distance
            solution.append((pk_site_id, latitude, longitude, depot, distance))

yard_distances = yard_distances.drop(yard_distance_hold)

#empty out OKY
yard_distance_hold = []
depot = "OKY"
yard_distances = yard_distances.sort(depot)
for index, row in yard_distances.iterrows():
    pk_site_id = int(index)

    if load_yard[depot] - serv_dur.ix[pk_site_id] > 0 and row[depot] < 10000:
            load_yard[depot] = load_yard[depot] - serv_dur.ix[pk_site_id]
            distance = 0
            latitude = df_services.ix[pk_site_id]['latitude']
            longitude = df_services.ix[pk_site_id]['longitude']
            yard_distance_hold.append(pk_site_id)
            # pk_site_id,latitude,longitude,yard,distance
            solution.append((pk_site_id, latitude, longitude, depot, distance))

yard_distances = yard_distances.drop(yard_distance_hold)

#empty out RBV
yard_distance_hold = []
depot = "RBV"
yard_distances = yard_distances.sort(depot)
for index, row in yard_distances.iterrows():
    pk_site_id = int(index)

    if load_yard[depot] - serv_dur.ix[pk_site_id] > 0 and row[depot] < 12000:
            load_yard[depot] = load_yard[depot] - serv_dur.ix[pk_site_id]
            distance = 0
            latitude = df_services.ix[pk_site_id]['latitude']
            longitude = df_services.ix[pk_site_id]['longitude']
            yard_distance_hold.append(pk_site_id)
            # pk_site_id,latitude,longitude,yard,distance
            solution.append((pk_site_id, latitude, longitude, depot, distance))

yard_distances = yard_distances.drop(yard_distance_hold)


#check for the nearest
for depot in labels:
    yard_distance_hold = []
    yard_distances = yard_distances.sort(depot)
    for index, row in yard_distances.iterrows():
        pk_site_id = int(index)

        if row[labels].idxmin() == depot and load_yard[depot] - serv_dur.ix[pk_site_id]>0:
            load_yard[depot] = load_yard[depot] - serv_dur.ix[pk_site_id]
            distance = 0
            latitude = df_services.ix[pk_site_id]['latitude']
            longitude = df_services.ix[pk_site_id]['longitude']
            yard_distance_hold.append(pk_site_id)
            # pk_site_id,latitude,longitude,yard,distance
            solution.append((pk_site_id, latitude, longitude, depot, distance))

    yard_distances = yard_distances.drop(yard_distance_hold)

    #print(yard_distances.index)

print(load_yard)
print(len(yard_distances))


#check for the second nearest
for depot in labels:
    yard_distance_hold = []
    yard_distances = yard_distances.sort(depot)
    for index, row in yard_distances.iterrows():

        pk_site_id = int(index)

        if row[labels].drop(row[labels].idxmin()).idxmin() == depot and load_yard[depot] - serv_dur.ix[pk_site_id]>0 and row[depot] < 14000:
            load_yard[depot] = load_yard[depot] - serv_dur.ix[pk_site_id]
            distance = 0
            latitude = df_services.ix[pk_site_id]['latitude']
            longitude = df_services.ix[pk_site_id]['longitude']
            yard_distance_hold.append(pk_site_id)
            # pk_site_id,latitude,longitude,yard,distance
            solution.append((pk_site_id, latitude, longitude, depot, distance))

    yard_distances = yard_distances.drop(yard_distance_hold)

    #print(yard_distances.index)

print(load_yard)
print(len(yard_distances))


#check for the third nearest
for depot in labels:
    yard_distance_hold = []
    yard_distances = yard_distances.sort(depot)
    for index, row in yard_distances.iterrows():

        pk_site_id = int(index)
        i=0
        while i < 2:
            row = row[labels].drop(row[labels].idxmin())
            i+=1

        if row[labels].idxmin() == depot and load_yard[depot] - serv_dur.ix[pk_site_id]>0 and row[depot] < 12000:
            load_yard[depot] = load_yard[depot] - serv_dur.ix[pk_site_id]
            distance = 0
            latitude = df_services.ix[pk_site_id]['latitude']
            longitude = df_services.ix[pk_site_id]['longitude']
            yard_distance_hold.append(pk_site_id)
            # pk_site_id,latitude,longitude,yard,distance
            solution.append((pk_site_id, latitude, longitude, depot, distance))

    yard_distances = yard_distances.drop(yard_distance_hold)

    #print(yard_distances.index)

    print(load_yard)

print(len(yard_distances))

"""
#check for the fourth nearest
for depot in labels:
    yard_distance_hold = []
    yard_distances = yard_distances.sort(depot)
    for index, row in yard_distances.iterrows():

        pk_site_id = int(index)

        i = 0
        while i < 3:
            row = row[labels].drop(row[labels].idxmin())
            i += 1

        if row[labels].idxmin() == depot and load_yard[depot] - serv_dur.ix[pk_site_id]>0 and row[depot] < 10000:
            load_yard[depot] = load_yard[depot] - serv_dur.ix[pk_site_id]
            distance = 0
            latitude = df_services.ix[pk_site_id]['latitude']
            longitude = df_services.ix[pk_site_id]['longitude']
            yard_distance_hold.append(pk_site_id)
            # pk_site_id,latitude,longitude,yard,distance
            solution.append((pk_site_id, latitude, longitude, depot, distance))

    yard_distances = yard_distances.drop(yard_distance_hold)

    #print(yard_distances.index)

    print(load_yard)

print(len(yard_distances))

#check for the fifth nearest
for depot in labels:
    yard_distance_hold = []
    yard_distances = yard_distances.sort(depot)
    for index, row in yard_distances.iterrows():

        pk_site_id = int(index)
        i=0
        while i < 4:
            row = row[labels].drop(row[labels].idxmin())
            i += 1


        if row[labels].idxmin() == depot and load_yard[depot] - serv_dur.ix[pk_site_id]>0 and row[depot] < 10000:
            load_yard[depot] = load_yard[depot] - serv_dur.ix[pk_site_id]
            distance = 0
            latitude = df_services.ix[pk_site_id]['latitude']
            longitude = df_services.ix[pk_site_id]['longitude']
            yard_distance_hold.append(pk_site_id)
            # pk_site_id,latitude,longitude,yard,distance
            solution.append((pk_site_id, latitude, longitude, depot, distance))

    yard_distances = yard_distances.drop(yard_distance_hold)

    #print(yard_distances.index)

    print(load_yard)

print(len(yard_distances))

#check for the sixth nearest
for depot in labels:
    yard_distance_hold = []
    yard_distances = yard_distances.sort(depot)
    for index, row in yard_distances.iterrows():

        pk_site_id = int(index)
        i=0
        while i < 5:
            row = row[labels].drop(row[labels].idxmin())
            i += 1

        if row[labels].idxmin() == depot and load_yard[depot] - serv_dur.ix[pk_site_id]>0 and row[depot] < 10000:
            load_yard[depot] = load_yard[depot] - serv_dur.ix[pk_site_id]
            distance = 0
            latitude = df_services.ix[pk_site_id]['latitude']
            longitude = df_services.ix[pk_site_id]['longitude']
            yard_distance_hold.append(pk_site_id)
            # pk_site_id,latitude,longitude,yard,distance
            solution.append((pk_site_id, latitude, longitude, depot, distance))

    yard_distances = yard_distances.drop(yard_distance_hold)

    #print(yard_distances.index)

    print(load_yard)

print(yard_distances)

#print(yard_distances.index)
"""
print(load_yard)

print(yard_distances)

#assign the leftover
yard_distance_hold = []
for index, row in yard_distances.iterrows():
    #yard_distances = yard_distances.sort(labels[yard_ind], ascending=True)
    #goto the next nearest if can't be assigned to neasrest
    depot = row[labels].idxmin()
    pk_site_id = int(index)


    load_yard[depot] = load_yard[depot] - serv_dur.ix[pk_site_id]
    print("service_time = {0}".format(serv_dur.ix[pk_site_id]))
    distance = 0
    latitude = df_services.ix[pk_site_id]['latitude']
    longitude = df_services.ix[pk_site_id]['longitude']
    yard_distance_hold.append(pk_site_id)
    # pk_site_id,latitude,longitude,yard,distance
    solution.append((pk_site_id, latitude, longitude, 'unassigned', distance))

yard_distances = yard_distances.drop(yard_distance_hold)

print(load_yard)
print(len(yard_distances))

fname="services_yard_all.csv"
with open(fname, "w") as fout:
    fout.write("pk_site_id,latitude,longitude,yard,distance\n")
    for s in solution:
        # print(int(s),service_dict[int(s)])
        fout.write("{0},{1},{2},{3},{4}\n".format(s[0],s[1],s[2],s[3],s[4]))
        # fout.write('\n')

fname = 'services_yard_Ambleside Yard'
with open(fname, "w") as fout:
    fout.write("pk_site_id,latitude,longitude,yard,distance\n")
    for s in solution:
        if s[3] == 'ASY':
            # print(int(s),service_dict[int(s)])
            fout.write("{0},{1},{2},{3},{4}\n".format(s[0],s[1],s[2],s[3],s[4]))

fname = 'services_yard_DONNA Arena'
with open(fname, "w") as fout:
    fout.write("pk_site_id,latitude,longitude,yard,distance\n")
    for s in solution:
        if s[3] == 'DON':
            # print(int(s),service_dict[int(s)])
            fout.write("{0},{1},{2},{3},{4}\n".format(s[0],s[1],s[2],s[3],s[4]))

fname = 'services_yard_Gold Bar Yard'
with open(fname, "w") as fout:
    fout.write("pk_site_id,latitude,longitude,yard,distance\n")
    for s in solution:
        if s[3] == 'GBY':
            # print(int(s),service_dict[int(s)])
            fout.write("{0},{1},{2},{3},{4}\n".format(s[0],s[1],s[2],s[3],s[4]))

fname = 'services_yard_MILLWOODS'
with open(fname, "w") as fout:
    fout.write("pk_site_id,latitude,longitude,yard,distance\n")
    for s in solution:
        if s[3] == 'MWD':
            # print(int(s),service_dict[int(s)])
            fout.write("{0},{1},{2},{3},{4}\n".format(s[0],s[1],s[2],s[3],s[4]))

fname = "services_yard_O'Keefe Yard"
with open(fname, "w") as fout:
    fout.write("pk_site_id,latitude,longitude,yard,distance\n")
    for s in solution:
        if s[3] == 'OKY':
            # print(int(s),service_dict[int(s)])
            fout.write("{0},{1},{2},{3},{4}\n".format(s[0],s[1],s[2],s[3],s[4]))

fname = 'services_yard_Rainbow Valley Yard'
with open(fname, "w") as fout:
    fout.write("pk_site_id,latitude,longitude,yard,distance\n")
    for s in solution:
        if s[3] == 'RBV':
            # print(int(s),service_dict[int(s)])
            fout.write("{0},{1},{2},{3},{4}\n".format(s[0],s[1],s[2],s[3],s[4]))

"""
yard_distance_hold = []
for index, row in yard_distances.iterrows():
    #yard_distances = yard_distances.sort(labels[yard_ind], ascending=True)
    #goto the next nearest if can't be assigned to neasrest
    while load_yard[row[labels].idxmin()] - serv_dur.ix[int(index)]<0:
        row = row[labels].drop(row[labels].idxmin())

    depot = row[labels].idxmin()
    pk_site_id = int(index)


    if load_yard[depot] - serv_dur.ix[pk_site_id]>0:
        load_yard[depot] = load_yard[depot] - serv_dur.ix[pk_site_id]
        distance = 0
        latitude = df_services.ix[pk_site_id]['latitude']
        longitude = df_services.ix[pk_site_id]['longitude']
        yard_distance_hold.append(pk_site_id)
        # pk_site_id,latitude,longitude,yard,distance
        solution.append((pk_site_id, latitude, longitude, depot, distance))

yard_distances = yard_distances.drop(yard_distance_hold)
print(len(yard_distances))
"""