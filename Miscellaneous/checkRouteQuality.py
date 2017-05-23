import pandas as pd

#Check that the B1 turfs are serviced 8 to 12 days apart
def checkB1Diff(df):
    try:
        if (float(df['arrTime'].iloc[1]) - float(df['arrTime'].iloc[0]))/24 < 8 or (float(df['arrTime'].iloc[1]) - float(df['arrTime'].iloc[0]))/24 > 12:
            return "Check " + df['raw-Id'].iloc[0] + ", difference is not good. " + "Difference is " + str(int((float(df['arrTime'].iloc[1]) - float(df['arrTime'].iloc[0]))/24))
        else:
            return "Looks good. Difference is " + str(int((float(df['arrTime'].iloc[1]) - float(df['arrTime'].iloc[0]))/24))
    except IndexError:
        return "Data not correctly formatted"

if __name__ == "__main__":
    filename = '../72GM/DON/DON_solution.csv'

    df_sol = pd.read_csv(filename)

    df_sol = df_sol.dropna()

    df_sol['raw-Id'] = df_sol['job-Id'].apply(lambda x: x.split("_")[0])
    df_sol['service-level'] = df_sol['job-Id'].apply(lambda x: x.split("_")[-1])

    for raw_Id in df_sol['raw-Id'].unique():
        df = df_sol[df_sol['raw-Id'] == raw_Id]
        if df['service-level'].iloc[0] == 'B1':
            print(checkB1Diff(df))

