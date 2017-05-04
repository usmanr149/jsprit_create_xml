import numpy as np
import pandas as pd
import requests

import pprint
import sys

depots = pd.read_csv("data/southside_depots.csv")
depots.columns = ['depot_name','team_lead','latitude','longitude','start_time','id']
depots_mat = depots.as_matrix()

# vehicles_72GM = pd.read_csv("data/72GM_vehicles.csv")
vehicles_72GM = pd.read_csv("data/580D_vehicles.csv")

serv_dur = pd.read_csv("service_duration.csv")
yard_distances = pd.read_csv("distance_yard_services.csv")

services = pd.read_csv("data/turf_services.csv")
service_points = list(zip(services['latitude'],services['longitude'],services['pk_site_id']))

service_dict = {}
for x in service_points:
    service_dict[x[2]] = x

service_dur = dict(serv_dur.as_matrix())

num_vehicles = {'GBY':0,'RBV':0,'OKY':0,'ASY':0,'DON':0,'MWD':0}
labels = dict(enumerate(['GBY','RBV','OKY','ASY','DON','MWD']))

vehicle_yard = [id.split('-')[0] for id in list(vehicles_72GM['vehicle-id'])]
for x in vehicle_yard:
    num_vehicles[x]+=1

load_yard = {k:v*7.85 for k,v in num_vehicles.items()}
print(load_yard)

serv_cluster = {0:set(),1:set(),2:set(),3:set(),4:set(),5:set()}
serv_yard = {0:[],1:[],2:[],3:[],4:[],5:[]}
unassigned = []

yard_dist = yard_distances.as_matrix()
for s in yard_dist:
    sort_dist = sorted(enumerate(s[1:]), key=lambda tup: tup[1])
    yard = sort_dist[0]
    serv_yard[yard[0]].append((s[0],yard[1],sort_dist[1:]))


yard_order = [2,3,0,1,5,4]

finished = False
while not finished:
    for i in range(len(yard_order)):
        yard = yard_order[i]
        print("---- {} ----".format(yard))
        if len(serv_yard[yard])>0:
            # if yard==4:
                # pprint.pprint(serv_yard[yard])
            sorted_serv = sorted(serv_yard[yard], key=lambda tup: tup[1])
        else:
            continue
        for d in sorted_serv:
            if load_yard[labels[yard]]-service_dur[d[0]]>=0:
                load_yard[labels[yard]] -= service_dur[d[0]]
                serv_cluster[yard].add(d[0])
            else:
                # print("Site {} not assigned to yard {}".format(d[0],yard))
                # print(d)
                if len(d[2])>0:
                    next_yard = d[2][0]
                    # print("next yard to try: {}".format(next_yard))
                    # print(serv_yard[next_yard[0]])
                    serv_yard[next_yard[0]].append((d[0],d[2][0][1],d[2][1:]))
                else:
                    unassigned.append(d[0])
        serv_yard[yard] = []
    finished = sum([len(x) for x in serv_yard.values()])==0
                
# pprint.pprint(serv_cluster)
print(unassigned)
print(load_yard)

for y in range(6):
    fname="services_yard_{}.csv".format(depots_mat[y][0])
    with open(fname,"w") as fout:
        fout.write("pk_site_id,latitude,longitude,yard,distance\n")
        for s in serv_cluster[y]:
            info = service_dict[int(s)]
            fout.write("{},{},{},{}\n".format(int(s),info[0],info[1],0))
            # fout.write('\n')

fname="services_yard_all.csv"
with open(fname, "w") as fout:
    fout.write("pk_site_id,latitude,longitude,yard,distance\n")
    for y in range(6):
        for s in serv_cluster[y]:
            info = service_dict[int(s)]
            fout.write("{},{},{},{},{}\n".format(int(s),info[0],info[1],y,0))

print(unassigned)
