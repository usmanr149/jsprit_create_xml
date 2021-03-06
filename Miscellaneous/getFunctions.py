import pandas as pd

def getServiceTime(df):
    serviceTime = 0

    for index, row in df.iterrows():
        if row['activity'] == 'delivery':
            serviceTime+= float(row['endTime']) - float(row['arrTime'])

    return serviceTime

def getTravelTime(df):
    travelTime = 0

    index = df.index

    for i in range(len(index)):
        if df['activity'].ix[i] != 'end':
            if df['activity'].ix[i] == 'start':
                startTime = int(float(df['arrTime'].ix[index[i+1]])/24.)*24 + 6
                travelTime += float(df['arrTime'].ix[index[i+1]]) - startTime
            else:
                travelTime += float(df['arrTime'].ix[index[i+1]]) - float(df['endTime'].ix[index[i]])

    return travelTime

def getHectaresCut(df):
    df_turfs = pd.read_csv('../580D/Data/ODL_Inputs_580D.csv')

    df = df.dropna()
    df = df.rename(columns={'job-Id': 'Id'})
    df = df.merge(df_turfs[['Id', 'service-duration']], on='Id', how='left')

    df['service_area'] = df['service-duration'].apply(lambda x: float(x)*2)

    return df['service_area'].sum()

if __name__ == '__main__':

    filename = '../580D/OKY/OKY_solution.csv'

    df = pd.read_csv(filename)
    serviceTime = getServiceTime(df)
    travelTime = getTravelTime(df)
    hectaresCut = getHectaresCut(df)

    print('Service Time = ', serviceTime)
    print('Travel Time = ', travelTime)
    print('Hectares Cut = ', hectaresCut)

    print("Productivity Rate = ", hectaresCut/serviceTime)