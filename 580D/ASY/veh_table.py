import pandas as pd

def create_xml_for_vehicle(start, end):
    df_eq = pd.read_csv('/home/usman/Downloads/Turf_Clusters/Equipment_Inventory - Sheet3.csv')
    replace_DOW = {'Monday - Friday': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                   'Monday - Sunday': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                   'Monday - Thursday': ['Monday', 'Tuesday', 'Wednesday', 'Thursday'],
                   'Friday - Monday': ['Friday', 'Saturday', 'Sunday', 'Monday'],
                   'Tuesday - Friday': ['Tuesday', 'Wednesday', 'Thursday', 'Friday']}

    df_eq['Days_of_Week'] = df_eq['Days_of_Week'].map(replace_DOW)

    new_df_eq = pd.DataFrame(columns=df_eq.columns)

    for i in range(len(df_eq)):
        for day in df_eq['Days_of_Week'][i]:
            new_df_eq = new_df_eq.append(df_eq.ix[i])
            new_df_eq.iloc[-1, new_df_eq.columns.get_loc('Days_of_Week')] = day

    df_vehicle_580D = pd.DataFrame(
        columns=["vehicle-name", "vehicle-id", "start-latitude", "start-longitude", "end-latitude",
                 "end-longitude", "start-time", "end-time", "capacity", "speed-multiplier", "cost-per-km",
                 "cost-per-hour", "waiting-cost-per-hour", "fixed-cost", "skills", "number-of-vehicles", 'day'])

    #day_Conversion = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 0}
    day_Conversion = {'Monday': 3, 'Tuesday': 4, 'Wednesday': 5, 'Thursday': 6, 'Friday': 0, 'Saturday': 1, 'Sunday': 2}
    new_df_eq.reset_index(inplace=True)
    for cycle in range(1, 4):
        weekend_neighb_1_2_Sat = 0
        zig = 0
        Fri_roadway = 0
        Mon_roadway = 0
        Mon_roadway_1 = 0
        Mon_roadway_2 = 0
        Sat_neighb = 0
        for i in new_df_eq.index:
            if new_df_eq.iloc[i]['equipment_type(5910 or 72inch)'] == "JD 1545 72\"":
                #default skill is neighbourhood
                skill = "neighbourhood"
                if cycle == 1:
                    if new_df_eq.iloc[i]["Days_of_Week"] == 'Sunday' or new_df_eq.iloc[i]["Days_of_Week"] == 'Saturday': 
                        skill = 'roadway'
                    elif new_df_eq.iloc[i]["Days_of_Week"] == 'Monday':
                        if Mon_roadway_2 > 2:
                            skill='roadway'
                        Mon_roadway_2+=1
                elif cycle == 2:
                    if new_df_eq.iloc[i]["Days_of_Week"] == 'Sunday' or new_df_eq.iloc[i]["Days_of_Week"] == 'Saturday': 
                        skill = 'roadway'
                    elif new_df_eq.iloc[i]["Days_of_Week"] == 'Monday':
                        if Mon_roadway_1 > -1:
                            skill='roadway'
                        Mon_roadway_1+=1
                elif cycle == 3:
                    if new_df_eq.iloc[i]["Days_of_Week"] == 'Saturday' or new_df_eq.iloc[i]["Days_of_Week"] == 'Sunday':
                        skill = "roadway"
                    elif new_df_eq.iloc[i]["Days_of_Week"] == 'Friday':
                        if Fri_roadway > 3:
                            skill = "neighbourhood"
                        else:
                            skill = 'roadway'
                        Fri_roadway+=1
                    elif new_df_eq.iloc[i]["Days_of_Week"] == 'Monday':
                        if Mon_roadway > 3:
                            skill='roadway'
                        Mon_roadway+=1  
                df_vehicle_580D = df_vehicle_580D.append(
                    pd.DataFrame(columns=df_vehicle_580D.columns, data=[[new_df_eq.iloc[i]["vehicle_name"],
                                                                         new_df_eq.iloc[i]["vehicle_id"] + "_" + str(
                                                                             cycle) + "_" + str(
                                                                             day_Conversion[new_df_eq.iloc[i]["Days_of_Week"]]),
                                                                         new_df_eq.iloc[i]["depot_latitude"],
                                                                         new_df_eq.iloc[i]["depot_latitude.1"],
                                                                         new_df_eq.iloc[i]["depot_latitude"],
                                                                         new_df_eq.iloc[i]["depot_latitude.1"],
                                                                         str(day_Conversion[
                                                                                 new_df_eq.iloc[i]["Days_of_Week"]] + 7 * (
                                                                             cycle - 1)) + "d 06:00:00",
                                                                         str(day_Conversion[
                                                                                 new_df_eq.iloc[i]["Days_of_Week"]] + 7 * (
                                                                             cycle - 1)) + "d 14:45:00",
                                                                         10000, 1, 0.001, 1, 0.5, 100,
                                                                         skill, 1, day_Conversion[
                                                                             new_df_eq.iloc[i]["Days_of_Week"]] + 7 * (
                                                                         cycle - 1)]]))
    df_vehicle_580D.drop_duplicates(inplace=True)
    new_df_vehicle_580D = df_vehicle_580D.copy()
    new_df_vehicle_580D['start-time'] = new_df_vehicle_580D['start-time'].apply(lambda x: fix_time(x))
    new_df_vehicle_580D['end-time'] = new_df_vehicle_580D['end-time'].apply(lambda x: fix_time(x))
    new_df_vehicle_580D = new_df_vehicle_580D[(new_df_vehicle_580D['start-time'] > start) & (new_df_vehicle_580D['end-time'] < end)]
    new_df_vehicle_580D.to_csv('/home/usman/Downloads/Turf_Clusters/580D/580D_vehicles.csv')

def fix_time(x):
    def time_to_hour(x):
        x = x.split(':')
        return float(x[0])+float(x[1])/60 + float(x[2])/3600
    x = str(x).split('d')
    time = x[1]
    return float(x[0])*24 + time_to_hour(time)

create_xml_for_vehicle(0, 504)