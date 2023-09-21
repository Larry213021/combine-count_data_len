import os
import pandas as pd
import numpy as np
import string
import matplotlib.pyplot as plt
import collections
from scipy.spatial import distance
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = '0'


def datalength(df):
    all = 0
    df = df.fillna(0)
    df = df[['subject_id']]
    groups = df.groupby('subject_id',sort = False)
    identity_list = []
    Datalength = "資料長度:"+str(len(groups))

    for count in range(len(df)):

        if (df.iloc[count].at["subject_id"]) not in identity_list:
            identity_list.append(df.iloc[count].at["subject_id"])
            grp = groups.get_group(df.iloc[count].at["subject_id"])
            all = all + len(grp)

    onePersonAverageDisease = "每人平均得到疾病數量:"+str(all/len(groups))

    return Datalength,onePersonAverageDisease


def age_average_And_Std(df):
    all = 0
    df = df.fillna(0)
    df = df[['subject_id','anchor_age']]
    age_list = []
    groups = df.groupby('subject_id',sort = False)
    identity_list = []

    for count in range(len(df)):

        if (df.iloc[count].at["subject_id"]) not in identity_list:
            identity_list.append(df.iloc[count].at["subject_id"])
            all = all + df.iloc[count].at["anchor_age"]
            age_list.append(df.iloc[count].at["anchor_age"])

    std = np.std(age_list, ddof=1)
    showStd = "年齡標準差:" + str(std)
    AgeAverage = "平均年齡:"+str(all/len(groups))

    return AgeAverage,showStd

def setOfICD(df):
    identity_list = []
    letter = 0
    number = 0
    df = df[['icd_code']]

    for count in range(len(df)):

        if (df.iloc[count].at["icd_code"]) not in identity_list:
            identity_list.append(df.iloc[count].at["icd_code"])

            if df.iloc[count].at["icd_code"][0].isdigit():
                number+=1

            for i in df.iloc[count].at["icd_code"][0]:
                if i in string.ascii_letters:
                    letter+=1

    print("全部ICD9種類:",number)
    print("全部ICD10種類:",letter)


def AvgPersonICD(df):
    letter = 0
    number = 0
    df = df[['subject_id','icd_code']]
    groups = df.groupby('subject_id', sort=False)

    for count in range(len(df)):

        if df.iloc[count].at["icd_code"][0].isdigit():
            number+=1

        if df.iloc[count].at["icd_code"][0] in string.ascii_letters:
            letter += 1

    print("平均一人得到的ICD9數量:",number/len(groups))
    print("平均一人得到的ICD10數量:",letter/len(groups))


def setOfPersonDisease_And_Std(df):

    identity_list = []
    df = df[['subject_id','icd_code']]
    groups = df.groupby('subject_id', sort=False)
    setPersonDisease = []
    counter = 0
    std_list = []
    disease_count_list = []

    for count in range(len(df)):

        if (df.iloc[count].at["subject_id"]) not in identity_list:
            identity_list.append(df.iloc[count].at["subject_id"])
            grp = groups.get_group(df.iloc[count].at["subject_id"])

            for i in range(len(grp)):
                setPersonDisease.append(grp.iloc[i].at["icd_code"])
            setPersonDisease = set(setPersonDisease)
            counter = counter +len(setPersonDisease)
            setPersonDisease = []

            for i in range(len(grp)):
                disease_count_list.append(grp.iloc[i].at["icd_code"])
            disease_count_list = set(disease_count_list)
            std_list.append(len(disease_count_list))
            disease_count_list = []

    std = np.std(std_list, ddof=1)
    print("每個人平均得到疾病種類數:"+str(counter/len(groups)))
    print("每個人得到疾病種類數的標準差:" + str(std))


def setOfPersonICDDisease_And_Std(df):

    identity_list = []
    df = df[['subject_id','icd_code']]
    groups = df.groupby('subject_id', sort=False)
    setICD9PersonDisease = []
    setICD10PersonDisease = []
    setICD9PersonDiseaseStd = []
    setICD10PersonDiseaseStd = []
    letter = 0
    number = 0


    for count in range(len(df)):
        if (df.iloc[count].at["subject_id"]) not in identity_list:
            identity_list.append(df.iloc[count].at["subject_id"])
            grp = groups.get_group(df.iloc[count].at["subject_id"])

            for i in range(len(grp)):
                if grp.iloc[i].at["icd_code"][0].isdigit():
                    setICD9PersonDisease.append(grp.iloc[i].at["icd_code"])
                if grp.iloc[i].at["icd_code"][0] in string.ascii_letters:
                    setICD10PersonDisease.append(grp.iloc[i].at["icd_code"])

            setICD9PersonDisease = set(setICD9PersonDisease)
            number = number +len(setICD9PersonDisease)
            setICD9PersonDiseaseStd.append(len(setICD9PersonDisease))

            setICD10PersonDisease = set(setICD10PersonDisease)
            letter = letter + len(setICD10PersonDisease)
            setICD10PersonDiseaseStd.append(len(setICD10PersonDisease))

            setICD9PersonDisease = []
            setICD10PersonDisease = []

    ICD9std = np.std(setICD9PersonDiseaseStd, ddof=1)
    ICD10std = np.std(setICD10PersonDiseaseStd, ddof=1)

    print("每個人平均得到ICD9疾病種類數:" + str(number/len(groups)))
    print("每個人平均得到ICD10疾病種類數:" + str(letter / len(groups)))
    print("每人ICD9種類標準差:" + str(ICD9std))
    print("每人ICD10種類標準差:" + str(ICD10std))


def diagnosis_Avg_ICD_And_Std(df):
    letter = 0
    number = 0
    df = df[['subject_id','admit_date','icd_code']]
    groups = df.groupby('subject_id', sort=False)
    identity_list = []
    identity_list2 = []
    setICD9PersonDisease = []
    setICD10PersonDisease = []
    setICD9PersonDiseaseStd = []
    setICD10PersonDiseaseStd = []


    for count in range(len(df)):
        if (df.iloc[count].at["subject_id"]) not in identity_list:
            identity_list.append(df.iloc[count].at["subject_id"])
            grp = groups.get_group(df.iloc[count].at["subject_id"])
            # print(grp["admit_date"])
            groups2 = grp.groupby('admit_date', sort=False)

            for count2 in range(len(grp)):
                if (grp.iloc[count2].at["admit_date"]) not in identity_list2:
                    identity_list2.append(grp.iloc[count2].at["admit_date"])
                    grp2 = groups2.get_group(grp.iloc[count2].at["admit_date"])

                    for i in range(len(grp2)):
                        if grp2.iloc[i].at["icd_code"][0].isdigit():
                            setICD9PersonDisease.append(grp2.iloc[i].at["icd_code"])
                        if grp2.iloc[i].at["icd_code"][0] in string.ascii_letters:
                            setICD10PersonDisease.append(grp2.iloc[i].at["icd_code"])

                    setICD9PersonDisease = set(setICD9PersonDisease)
                    number = number + len(setICD9PersonDisease)
                    setICD9PersonDiseaseStd.append(len(setICD9PersonDisease))

                    setICD10PersonDisease = set(setICD10PersonDisease)
                    letter = letter + len(setICD10PersonDisease)
                    setICD10PersonDiseaseStd.append(len(setICD10PersonDisease))

                    setICD9PersonDisease = []
                    setICD10PersonDisease = []
            identity_list2 = []

    ICD9std = np.std(setICD9PersonDiseaseStd, ddof=1)
    ICD10std = np.std(setICD10PersonDiseaseStd, ddof=1)

    print("每次就診平均得到ICD9疾病種類數:" + str(number / len(groups)))
    print("每次就診平均得到ICD10疾病種類數:" + str(letter / len(groups)))
    print("每次就診ICD9種類標準差:" + str(ICD9std))
    print("每次就診ICD10種類標準差:" + str(ICD10std))



def MIMIC_diagnosis_Avg_ICD_And_Std(df):
    letter = 0
    number = 0
    df = df[['subject_id','admittime','icd_code']]
    groups = df.groupby('subject_id', sort=False)
    identity_list = []
    identity_list2 = []
    setICD9PersonDisease = []
    setICD10PersonDisease = []
    setICD9PersonDiseaseStd = []
    setICD10PersonDiseaseStd = []


    for count in range(len(df)):
        if (df.iloc[count].at["subject_id"]) not in identity_list:
            identity_list.append(df.iloc[count].at["subject_id"])
            grp = groups.get_group(df.iloc[count].at["subject_id"])
            # print(grp["admit_date"])

            groups2 = grp.groupby('admittime', sort=False)
            for count2 in range(len(grp)):
                if (grp.iloc[count2].at["admittime"]) not in identity_list2:
                    identity_list2.append(grp.iloc[count2].at["admittime"])
                    grp2 = groups2.get_group(grp.iloc[count2].at["admittime"])

                    for i in range(len(grp2)):
                        if grp2.iloc[i].at["icd_code"][0].isdigit():
                            setICD9PersonDisease.append(grp2.iloc[i].at["icd_code"])
                        if grp2.iloc[i].at["icd_code"][0] in string.ascii_letters:
                            setICD10PersonDisease.append(grp2.iloc[i].at["icd_code"])

                    setICD9PersonDisease = set(setICD9PersonDisease)
                    number = number + len(setICD9PersonDisease)
                    setICD9PersonDiseaseStd.append(len(setICD9PersonDisease))

                    setICD10PersonDisease = set(setICD10PersonDisease)
                    letter = letter + len(setICD10PersonDisease)
                    setICD10PersonDiseaseStd.append(len(setICD10PersonDisease))

                    setICD9PersonDisease = []
                    setICD10PersonDisease = []
            identity_list2 = []
    ICD9std = np.std(setICD9PersonDiseaseStd, ddof=1)
    ICD10std = np.std(setICD10PersonDiseaseStd, ddof=1)

    print("每次就診平均得到ICD9疾病種類數:" + str(number / len(groups)))
    print("每次就診平均得到ICD10疾病種類數:" + str(letter / len(groups)))
    print("每次就診ICD9種類標準差:" + str(ICD9std))
    print("每次就診ICD10種類標準差:" + str(ICD10std))


def MFcount_And_ICDcount(df):

    male = 0
    female = 0
    icd9 = 0
    icd10 = 0
    caseicd9 = 0
    caseicd10 = 0
    df = df.fillna(0)
    df = df[['subject_id','gender','icd_version','icd_code']]
    groups = df.groupby('subject_id',sort = False)
    identity_list = []
    caseicd9_list = []
    caseicd10_list = []

    for count in range(len(df)):

        if (df.iloc[count].at["subject_id"]) not in identity_list:
            identity_list.append(df.iloc[count].at["subject_id"])
            grp = groups.get_group(df.iloc[count].at["subject_id"])

            # 可新增ICD相關疾病代碼
            for i in range(len(grp)):

                if grp.iloc[i].at["icd_code"][0].isdigit():
                    caseicd9_list.append(grp.iloc[i].at["icd_code"])
                if grp.iloc[i].at["icd_code"][0] in string.ascii_letters:
                    caseicd10_list.append(grp.iloc[i].at["icd_code"])

                if(grp.iloc[i].at["icd_code"]) == "2967":
                    caseicd9 = caseicd9 + 1

                if (grp.iloc[i].at["icd_code"]) == "F3170  ":
                    caseicd10 = caseicd10 + 1

                if (grp.iloc[i].at["icd_code"]) == "F3171  ":
                    caseicd10 = caseicd10 + 1

                if (grp.iloc[i].at["icd_code"]) == "F3172  ":
                    caseicd10 = caseicd10 + 1

                if (grp.iloc[i].at["icd_code"]) == "F319   ":
                    caseicd10 = caseicd10 + 1
            # 新增到這邊

            if (df.iloc[count].at["gender"]) == "M":
                male = male + 1

            if (df.iloc[count].at["gender"]) == "F":
                female = female + 1

        if (df.iloc[count].at["icd_version"]) == 9:
            icd9 = icd9 + 1

        if (df.iloc[count].at["icd_version"]) == 10:
            icd10 = icd10 + 1

    MalePercent = "男性比例:" + str(np.round((male / len(groups)),1)*90) + "%"
    FemalePercent = "女性比例:" + str(np.round((female / len(groups)),1)*90) + "%"
    Malecount = "男性個數:" + str(male)
    Femalecount = "女性個數:" + str(female)
    icd9count = "ICD9總個數:" + str(icd9)
    icd10count = "ICD10總個數:" + str(icd10)
    caseicd9 = "ICD9_case總個數:" + str(caseicd9)
    caseicd10 = "ICD10_case總個數:" + str(caseicd10)
    caseicd9_list = set(caseicd9_list)
    caseicd10_list = set(caseicd10_list)
    caseicd9len = "caseicd9len:" + str(len(caseicd9_list))
    caseicd10len = "caseicd10len:" + str(len(caseicd10_list))

    print(MalePercent,Malecount)
    print(FemalePercent,Femalecount)
    print(icd9count,icd10count)
    print(caseicd9, caseicd10)
    print(caseicd9len,caseicd10len)

    return caseicd9_list,caseicd10_list


def collections_Counter(df,df2):

    identity_list = []
    identity_list2 = []
    caseicd9_list = []
    caseicd10_list = []
    controlicd9_list = []
    controlicd10_list = []

    df = df.fillna(0)
    df = df[['subject_id', 'gender', 'icd_version', 'icd_code']]
    groups = df.groupby('subject_id', sort=False)

    df2 = df2.fillna(0)
    df2 = df2[['subject_id', 'gender', 'icd_version', 'icd_code']]
    groups2 = df2.groupby('subject_id', sort=False)

    for count in range(len(df)):

        if (df.iloc[count].at["subject_id"]) not in identity_list:
            identity_list.append(df.iloc[count].at["subject_id"])
            grp = groups.get_group(df.iloc[count].at["subject_id"])

            for i in range(len(grp)):
                if grp.iloc[i].at["icd_code"][0].isdigit():
                    caseicd9_list.append(grp.iloc[i].at["icd_code"])
                if grp.iloc[i].at["icd_code"][0] in string.ascii_letters:
                    caseicd10_list.append(grp.iloc[i].at["icd_code"])

    for count2 in range(len(df2)):

        if (df2.iloc[count2].at["subject_id"]) not in identity_list2:
            identity_list2.append(df2.iloc[count2].at["subject_id"])
            grp2 = groups2.get_group(df2.iloc[count2].at["subject_id"])

            for i in range(len(grp2)):
                if grp2.iloc[i].at["icd_code"][0].isdigit():
                    controlicd9_list.append(grp2.iloc[i].at["icd_code"])
                if grp2.iloc[i].at["icd_code"][0] in string.ascii_letters:
                    controlicd10_list.append(grp2.iloc[i].at["icd_code"])

    cai9 = collections.Counter(caseicd9_list)
    coni9 = collections.Counter(controlicd9_list)
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    for x,y in sorted(cai9.items()):
        x1.append(x)
        y1.append(y)
    for x,y in sorted(coni9.items()):
        x2.append(x)
        y2.append(y)
    y1_1 = []
    y2_1 = []
    caseicd9_list_len = len(caseicd9_list)
    controlicd9_list_len = len(controlicd9_list)
    for i in range(len(y1)):
        a1 = (y1[i]/caseicd9_list_len)
        y1_1.append(a1)
    for i in range(len(y2)):
        a2 = (y2[i]/controlicd9_list_len)
        y2_1.append(a2)
    plt.title('ICD9_case&control_DiseaseCodeDistribution')
    plt.xlabel('ICD9DiseaseCode')
    plt.bar(x1, y1_1, color='blue',label='caseIcd9_count',alpha=0.7,width=40)
    plt.bar(x2, y2_1, color='red',label='controlIcd9_count',alpha=0.5,width=30)
    plt.xticks(color='w')
    plt.legend()
    plt.savefig('icd9_diseasecode_count.png')
    # plt.show()

    cai10 = collections.Counter(caseicd10_list)
    coni10 = collections.Counter(controlicd10_list)
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    for x,y in sorted(cai10.items()):
        x1.append(x)
        y1.append(y)
    for x , y in sorted(coni10.items()):
        x2.append(x)
        y2.append(y)
    y1_1 = []
    y2_1 = []
    caseicd10_list_len = len(caseicd10_list)
    controlicd10_list_len = len(controlicd10_list)
    for i in range(len(y1)):
        a1 = (y1[i]/caseicd10_list_len)
        y1_1.append(a1)
    for i in range(len(y2)):
        a2 = (y2[i]/controlicd10_list_len)
        y2_1.append(a2)
    plt.figure()# 新增圖，順便洗掉舊圖
    plt.title('ICD10_case&control_DiseaseCodeDistribution')
    plt.xlabel('ICD10DiseaseCode')
    plt.bar(x1, y1_1, color='blue', label='caseIcd10_count',alpha=0.7,width=40)
    plt.bar(x2, y2_1, color='red', label='controlIcd10_count',alpha=0.5,width=30)
    plt.xticks(color='w')
    plt.legend()
    plt.savefig('icd10_diseasecode_count.png')
    # plt.show()

def correlation_coeficient_dist(df,df2):

    identity_list = []
    identity_list2 = []
    caseicd9_list = []
    caseicd10_list = []
    controlicd9_list = []
    controlicd10_list = []

    df = df.fillna(0)
    df = df[['subject_id', 'gender', 'icd_version', 'icd_code']]
    groups = df.groupby('subject_id', sort=False)

    df2 = df2.fillna(0)
    df2 = df2[['subject_id', 'gender', 'icd_version', 'icd_code']]
    groups2 = df2.groupby('subject_id', sort=False)

    for count in range(len(df)):

        if (df.iloc[count].at["subject_id"]) not in identity_list:
            identity_list.append(df.iloc[count].at["subject_id"])
            grp = groups.get_group(df.iloc[count].at["subject_id"])

            for i in range(len(grp)):
                if grp.iloc[i].at["icd_code"][0].isdigit():
                    caseicd9_list.append(grp.iloc[i].at["icd_code"])
                if grp.iloc[i].at["icd_code"][0] in string.ascii_letters:
                    caseicd10_list.append(grp.iloc[i].at["icd_code"])

    for count2 in range(len(df2)):

        if (df2.iloc[count2].at["subject_id"]) not in identity_list2:
            identity_list2.append(df2.iloc[count2].at["subject_id"])
            grp2 = groups2.get_group(df2.iloc[count2].at["subject_id"])

            for i in range(len(grp2)):
                if grp2.iloc[i].at["icd_code"][0].isdigit():
                    controlicd9_list.append(grp2.iloc[i].at["icd_code"])
                if grp2.iloc[i].at["icd_code"][0] in string.ascii_letters:
                    controlicd10_list.append(grp2.iloc[i].at["icd_code"])

    # icd9分布狀態--------------------------------------------
    cai9 = collections.Counter(caseicd9_list)
    coni9 = collections.Counter(controlicd9_list)

    x1 = []
    x2 = []
    y1 = []
    y2 = []

    for x,y in sorted(cai9.items()):
        x1.append(x)
        y1.append(y)
    for x,y in sorted(coni9.items()):
        x2.append(x)
        y2.append(y)

    y1_1 = []
    y2_1 = []

    caseicd9_list_len = len(caseicd9_list)
    controlicd9_list_len = len(controlicd9_list)

    for i in range(len(y1)):
        temp1 = (y1[i]/caseicd9_list_len)
        y1_1.append(temp1)
    for i in range(len(y2)):
        temp1 = (y2[i]/controlicd9_list_len)
        y2_1.append(temp1)

    t1 = []
    t2 = []
    n1 = []
    n2 = []

    if len(x1) > len(x2):
        for i in range(len(x1)):
            if x1[i] in x2:
                t2.append(x1[i])
                n2.append(y2_1[x2.index(x1[i])])
            if x1[i] not in x2:
                t2.append(0)
                n2.append(0)
        for i in range(len(x2)):
            if x2[i] not in x1:
                t2.append(x2[i])
                n2.append(y2_1[i])
                x1.append(x2[i])
                y1_1.append(0)
        y1_1 = pd.Series(y1_1, dtype='float64')
        y2_1 = pd.Series(n2, dtype='float64')
        cor1 = y1_1.corr(y2_1)
        print("icd9_case_前10筆:",y1_1[:10])
        print("icd9_case_後10筆:",y1_1[-10:])
        print("icd9_control_前10筆:",y2_1[:10])
        print("icd9_control_後10筆:",y2_1[-10:])
        print("icd9_case&control_correcoef:", cor1)
        print("icd9_case&control_dist:", distance.euclidean(y1_1, y2_1))

    if len(x1) < len(x2):
        for i in range(len(x2)):
            if x2[i] in x1:
                t1.append(x2[i])
                n1.append(y1_1[x1.index(x2[i])])
            if x2[i] not in x1:
                t1.append(0)
                n1.append(0)
        for i in range(len(x1)):
            if x1[i] not in x2:
                t1.append(x1[i])
                n1.append(y1_1[i])
                x2.append(x1[i])
                y2_1.append(0)

        y1_1 = pd.Series(n1, dtype='float64')
        y2_1 = pd.Series(y2_1, dtype='float64')
        cor1 = y1_1.corr(y2_1)
        print("icd9_case_前10筆:", y1_1[:10])
        print("icd9_case_後10筆:", y1_1[-10:])
        print("icd9_control_前10筆:", y2_1[:10])
        print("icd9_control_後10筆:", y2_1[-10:])
        print("icd9_case&control_correcoef", cor1)
        print("icd9_case&control_dist:", distance.euclidean(y1_1, y2_1))
    # --------------------------------------------

    # icd10分布狀態--------------------------------------------
    cai10 = collections.Counter(caseicd10_list)
    coni10 = collections.Counter(controlicd10_list)

    x1 = []
    x2 = []
    y1 = []
    y2 = []

    for x,y in sorted(cai10.items()):
        x1.append(x)
        y1.append(y)
    for x,y in sorted(coni10.items()):
        x2.append(x)
        y2.append(y)

    y1_1 = []
    y2_1 = []

    caseicd10_list_len = len(caseicd10_list)
    controlicd10_list_len = len(controlicd10_list)

    for i in range(len(y1)):
        temp1 = (y1[i]/caseicd10_list_len)
        y1_1.append(temp1)
    for i in range(len(y2)):
        temp1 = (y2[i]/controlicd10_list_len)
        y2_1.append(temp1)

    t1 = []
    t2 = []
    n1 = []
    n2 = []

    if len(x1) > len(x2):
        for i in range(len(x1)):
            if x1[i] in x2:
                t2.append(x1[i])
                n2.append(y2_1[x2.index(x1[i])])
            if x1[i] not in x2:
                t2.append(0)
                n2.append(0)
        for i in range(len(x2)):
            if x2[i] not in x1:
                t2.append(x2[i])
                n2.append(y2_1[i])
                x1.append(x2[i])
                y1_1.append(0)

        y1_1 = pd.Series(y1_1, dtype='float64')
        y2_1 = pd.Series(n2, dtype='float64')
        cor1 = y1_1.corr(y2_1)
        print("icd10_case_前10筆:", y1_1[:10])
        print("icd10_case_後10筆:", y1_1[-10:])
        print("icd10_control_前10筆:", y2_1[:10])
        print("icd10_control_後10筆:", y2_1[-10:])
        print("icd10_case&control_correcoef", cor1)
        print("icd10_case&control_dist:", distance.euclidean(y1_1, y2_1))

    if len(x1) < len(x2):
        for i in range(len(x2)):
            if x2[i] in x1:
                t1.append(x2[i])
                n1.append(y1_1[x1.index(x2[i])])
            if x2[i] not in x1:
                t1.append(0)
                n1.append(0)
        for i in range(len(x1)):
            if x1[i] not in x2:
                t1.append(x1[i])
                n1.append(y1_1[i])
                x2.append(x1[i])
                y2_1.append(0)
        y1_1 = pd.Series(n1, dtype='float64')
        y2_1 = pd.Series(y2_1, dtype='float64')
        cor1 = y1_1.corr(y2_1)
        print("icd10_case_前10筆:", y1_1[:10])
        print("icd10_case_後10筆:", y1_1[-10:])
        print("icd10_control_前10筆:", y2_1[:10])
        print("icd10_control_後10筆:", y2_1[-10:])
        print("icd10_case&control_correcoef", cor1)
        print("icd10_case&control_dist:", distance.euclidean(y1_1, y2_1))
    # --------------------------------------------

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

    df = pd.read_csv('D:\school\disease_type\mimic_data\mimic_mind/bipolar和schizophrenia分開做出case和control/or_case.csv')
    df2 = pd.read_csv('D:\school\disease_type\mimic_data\mimic_mind/bipolar和schizophrenia分開做出case和control/or_control_3times.csv')

    # 改變control數量
    choose_datalen = 12500
    df2 = df2.head(data_length(df2, choose_datalen))

    correlation_coeficient_dist(df, df2)
    # collections_Counter(df, df2)


    # df = pd.read_csv('D:\school\disease_type\mimic_data/bipolar/case.csv')
    # print("case:")
    # print(MFcount_And_ICDcount(df))
    # x1,y1 = MFcount_And_ICDcount(df)
    #
    # df = pd.read_csv('D:\school\disease_type\mimic_data/bipolar/control.csv')
    # print("control:")
    # print(MFcount_And_ICDcount(df))
    # x2,y2 = MFcount_And_ICDcount(df)
    #
    # ICD9_AB = "ICD9_AB交集"+str(len(x1.intersection(x2)))
    # ICD9_AB_dif = "ICD9_AB差集"+str(len(x1.difference(x2)))
    # ICD9_BA_dif = "ICD9_BA差集"+str(len(x2.difference(x1)))
    # print(ICD9_AB)
    # print(ICD9_AB_dif)
    # print(ICD9_BA_dif)
    #
    # ICD10_AB = "ICD10_AB交集"+str(len(y1.intersection(y2)))
    # ICD10_AB_dif = "ICD10_AB差集"+str(len(y1.difference(y2)))
    # ICD10_BA_dif = "ICD10_BA差集"+str(len(y2.difference(y1)))
    # print(ICD10_AB)
    # print(ICD10_AB_dif)
    # print(ICD10_BA_dif)










    # df = pd.read_csv('D:\school\disease_type\mimic_data/bipolar/case.csv')
    # print("case:")
    # print(MFcount_And_ICDcount(df))
    # print(datalength(df))
    # print(age_average_And_Std(df))
    # print(setOfICD(df))
    # print(AvgPersonICD(df))
    # print(setOfPersonDisease_And_Std(df))
    # print(setOfPersonICDDisease_And_Std(df))
    # print(diagnosis_Avg_ICD_And_Std(df))

    # df2 = pd.read_csv('D:/nkust_1108_Lab\mimic_data\schizophrenia/control.csv')
    # print("control:")
    # print(datalength(df2))
    # print(age_average_And_Std(df2))
    # print(MFcount_And_ICDcount(df2))
    # print(setOfICD(df2))
    # print(AvgPersonICD(df2))
    # print(setOfPersonDisease_And_Std(df2))
    # print(setOfPersonICDDisease_And_Std(df2))
    # print(diagnosis_Avg_ICD_And_Std(df2))


    # df3 = pd.read_csv('D:\school\disease_type\mimic_data\mimic/mimic2.csv')
    # print("mimic:")
    # print(datalength(df3))
    # print(age_average_And_Std(df3))
    # print(MFcount_And_ICDcount(df3))
    # print(setOfICD(df3))
    # print(AvgPersonICD(df3))
    # print(setOfPersonDisease_And_Std(df3))
    # print(setOfPersonICDDisease_And_Std(df3))
    # print(MIMIC_diagnosis_Avg_ICD_And_Std(df3))