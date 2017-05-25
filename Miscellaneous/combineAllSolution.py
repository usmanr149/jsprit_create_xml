import pandas as pd

df = pd.read_csv('../72GM/ASY/ASY_solution.csv')

df = df.append(pd.read_csv('../72GM/DON/DON_solution.csv'))
df = df.append(pd.read_csv('../72GM/GBY/GBY_solution.csv'))
df = df.append(pd.read_csv('../72GM/MWD/MWD_neighbourhood_solution.csv'))
df = df.append(pd.read_csv('../72GM/MWD/MWD_roadway_solution.csv'))
df = df.append(pd.read_csv('../72GM/OKY/OKY_solution.csv'))
df = df.append(pd.read_csv('../72GM/RBV/RBV_solution.csv'))

df = df.append(pd.read_csv('../580D/GBY/GBY_solution.csv'))
df = df.append(pd.read_csv('../580D/MWD/MWD_neighbourhood_solution.csv'))
df = df.append(pd.read_csv('../580D/MWD/MWD_roadway_solution.csv'))
df = df.append(pd.read_csv('../580D/OKY/OKY_solution.csv'))
df = df.append(pd.read_csv('../580D/RBV/RBV_solution.csv'))

#df.to_csv('All_routes.csv', index=False)

#get all unassigned stops

df_turfs = pd.read_csv('../72GM/Data/ODL_Inputs_72GM.csv')
df_turfs = df_turfs.append(pd.read_csv('../580D/Data/ODL_Inputs_580D.csv'))

df_turfs_unassigned = df_turfs[~df_turfs["Id"].isin(df['job-Id'])]

df_turfs_unassigned.to_csv("Unassigned_turfs.csv")

#get all unassigned vehicles
veh_used = df['vehicle-Id'].unique()

df_veh = pd.read_csv("../72GM/Data/72GM_vehicles.csv")
df_veh = df_veh.append(pd.read_csv("../580D/Data/580D_vehicles.csv"))

df_veh_unused = df_veh[~df_veh['vehicle-id'].isin(veh_used)]

df_veh_unused.to_csv("Unused_vehicles.csv")