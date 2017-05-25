#load the 72GM solution and fix the dates for the 192" machines

import pandas as pd

#filename ithe path to the file with the 72GM solutions
#you will need to append all the solution tables for all the different yard to get the complete table
def matchDates(filename, df_580D):
    def getID(x):
        if len(x.split("_")) > 3:
            return x.split("_")[0] + "_" + x.split("_")[2]
        else:
            return x.split("_")[0] + "_" + x.split("_")[1]

    df_72GM_solution = pd.read_csv(filename)

    df_72GM_solution = df_72GM_solution.dropna(subset=['job-Id'])

    df_72GM_solution['raw-id'] = df_72GM_solution['job-Id'].apply(lambda x: getID(x))

    df_580D['raw-id'] = df_580D['Id'].apply(lambda x: getID(x))
    df_72GM_solution['day'] = df_72GM_solution['arrTime'].apply(lambda x: int(float(x) / 24))

    df_580D = df_580D.merge(df_72GM_solution[['raw-id', 'day']], on='raw-id', how='left')

    df_580D['start-time'] = df_580D.apply(lambda row: str(row['day']) + "d 06:00:00" if pd.notnull(row['day']) else row['start-time'], axis=1)
    df_580D['end-time'] = df_580D.apply(lambda row: str(row['day']) + "d 14:45:00" if pd.notnull(row['day']) else row['end-time'], axis=1)
    df_580D['priority'] = df_580D.apply(lambda row: 1 if pd.notnull(row['day']) else row['priority'], axis=1)

    return df_580D


if __name__ == "__main__":

    filename = '../72GM/Data/72GM_solution_all_yards.csv'

    df = pd.read_csv('../72GM/ASY/ASY_solution.csv')

    df = df.append(pd.read_csv('../72GM/DON/DON_solution.csv'))
    df = df.append(pd.read_csv('../72GM/GBY/GBY_solution.csv'))
    df = df.append(pd.read_csv('../72GM/MWD/MWD_neighbourhood_solution.csv'))
    df = df.append(pd.read_csv('../72GM/MWD/MWD_roadway_solution.csv'))
    df = df.append(pd.read_csv('../72GM/OKY/OKY_solution.csv'))
    df = df.append(pd.read_csv('../72GM/RBV/RBV_solution.csv'))

    print(len(df))

    df.to_csv(filename)

    df_580D = pd.read_csv('Data/ODL_Inputs_580D.csv')
    print(len(df_580D))

    #update the 580D Inputs
    #df_580D = matchDates(filename, df_580D)

    df_580D.drop_duplicates(subset=['Id'], inplace=True)

    df_580D.to_csv('Data/ODL_Inputs_580D.csv', index=False)
    print(len(df_580D))