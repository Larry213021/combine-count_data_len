import pandas as pd

def data_length(df,group):
    df = df.fillna(0)
    df = df[['subject_id', 'gender','age','icd_code','icd_version']]
    groups = df.groupby('subject_id',sort = False)
    all = 0
    time = 0
    identity_list = []
    for count in range(len(df)):
        if (df.iloc[count].at["subject_id"]) not in identity_list:
            identity_list.append(df.iloc[count].at["subject_id"])
            grp = groups.get_group(df.iloc[count].at["subject_id"])
            all = all + len(grp)
            time += 1
        if time == group:
            break
    print("time:", time)
    print("data_length:",all)

    return all



if __name__ == '__main__':

    a = pd.read_csv("D:\school\disease_type\mimic_data\mimic_mind/bipolar和schizophrenia分開做出case和control/or_case.csv")
    b = pd.read_csv("D:\school\disease_type\mimic_data\mimic_mind/bipolar和schizophrenia分開做出case和control/or_control_3times.csv")

    choose_b_datalen = 15000
    b_new = b.head(data_length(b,choose_b_datalen))

    merged = a.merge(b_new, on=['subject_id', 'gender','age','icd_code','icd_version'],how='outer')
    # merged = a.merge(b, on=['identity', 'sex','age','func_type','func_date','icd9_1','icd9_2','icd9_3','icd9_4','icd9_5'],how = 'outer')
    # merged = a.merge(b_new, on=['identity', 'sex','age','func_type','func_date','icd9_1','icd9_2','icd9_3','icd9_4','icd9_5'],how = 'outer')
    # merged = a.merge(b, on=['identity', 'icd9_1', 'icd9_2', 'icd9_3', 'icd9_4','icd9_5'], how='outer')

    merged.to_csv("D:\school\disease_type\mimic_data\mimic_mind/bipolar和schizophrenia分開做出case和control/testssss.csv", index = False)

