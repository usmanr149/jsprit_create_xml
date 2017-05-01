import numpy as np
import pandas as pd
import requests

import pprint
import sys

url = "http://coevtubbi4:5000/route/v1/driving/{},{};{},{}?steps=false"

# services = pd.read_csv("data/turf_services.csv")
depots = pd.read_csv("data/southside_depots.csv")
depots.columns = ['depot_name','team_lead','latitude','longitude','start_time','id']
depots_mat = depots.as_matrix()
depot_points = list(zip(depots['latitude'],depots['longitude'],depots['id']))

services = pd.read_csv("data/Input_72GM.csv")
#service_points = list(zip(services['latitude'],services['longitude'],services['pk_site_id']))
service_points = list(zip(services['latitude'],services['longitude'],services['Id'],services['service-duration']))
services_mat = services.as_matrix()
service_dict = {}
for d in services_mat:
    service_dict[d[4]]=d


def road_distance(p1,p2):
    r = requests.get(url.format(p1[1],p1[0],p2[1],p2[0]))
    # print(r.url)
    res = r.json()
    route_info = res['routes'][0]
    # pprint.pprint(route_info['distance'])
    return route_info['distance']


def close_yard(p,depot_points):
    min_dis = 10000000
    yard = -1
    for idx,d in enumerate(depot_points):
        # print(s,'--',d)
        dis = road_distance(s,d)
        if dis < min_dis:
            min_dis = dis
            yard = idx
    return yard,min_dis


def distance_to_yard(p,depot_points):
    dist = [p[2].split('_')[0]]
    for idx,d in enumerate(depot_points):
        dis = road_distance(s,d)
        dist.append(dis)
    return dist


service_dur = {}
yard_serv_dist = []
for s in service_points:
    print(s)
    yard_serv_dist.append(distance_to_yard(s,depot_points))
    id = s[2].split('_')[0]
    service_dur.setdefault(id,s[3])

yard_serv= pd.DataFrame(yard_serv_dist,columns=['id','GBY','RBV','OKY','ASY','DON','MWD'])
yard_serv.to_csv("distance_yard_services.csv",index=False)

print(service_dur)
serv_dur = pd.DataFrame([[k,v] for k,v in service_dur.items()],columns=['id','duration'])
serv_dur.to_csv("service_duration.csv",index=False)


sys.exit()

serv_yard = {0:[],1:[],2:[],3:[],4:[],5:[]}


print("pk_site_id,latitude,longitude,yard,distance")
for s in service_points[:10]:
    print(s)
    yard,distance = close_yard(s,depot_points)
#    serv_yard[yard].append(service_dict[s[2]])
    serv_yard[yard].append("{},{},{},{},{}\n".format(s[2],s[0],s[1],yard,distance))
    print("{},{},{},{},{}".format(s[2],s[0],s[1],yard,distance))

for y in serv_yard:
    name = "service_yard_{}.csv".format(depots_mat[y][0])
    with open(name,'w') as f:
        f.write("pk_site_id,latitude,longitude,yard,distance\n")
        for s in serv_yard[y]:
            f.write(s)
