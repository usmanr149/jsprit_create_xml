import pandas as pd

#Check that the B1 turfs are serviced 8 to 12 days apart
def checkB1Diff(df):
    try:
        if (float(df['arrTime'].iloc[1]) - float(df['arrTime'].iloc[0]))/24 <= 7 or (float(df['arrTime'].iloc[1]) - float(df['arrTime'].iloc[0]))/24 >= 14:
            print("Check " + df['raw-Id'].iloc[0] + ", difference is not good. " + "Difference is " + str(int((float(df['arrTime'].iloc[1]) - float(df['arrTime'].iloc[0]))/24)))
            return False
        else:
            print("Looks good. Difference is " + str(int((float(df['arrTime'].iloc[1]) - float(df['arrTime'].iloc[0]))/24)))
            return True
    except IndexError:
        print("Data not correctly formatted")
        return False

if __name__ == "__main__":
    filename = '../580D/GBY/GBY_solution.csv'

    df_sol = pd.read_csv(filename)

    df_sol = df_sol.dropna()

    df_sol['raw-Id'] = df_sol['job-Id'].apply(lambda x: x.split("_")[0])
    df_sol['service-level'] = df_sol['job-Id'].apply(lambda x: x.split("_")[-1])

    good = 0

    for raw_Id in df_sol['raw-Id'].unique():
        df = df_sol[df_sol['raw-Id'] == raw_Id]
        if df['service-level'].iloc[0] == 'B1':
            good+=checkB1Diff(df)

    print(good)
    print(len(df_sol[df_sol['service-level'] == 'B1'])/2 - good)

