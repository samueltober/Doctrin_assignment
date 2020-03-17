#############################################################################################################
####################################DATA ASSIGNMENT FOR DOCTRIN##############################################
#############################################################################################################

import json
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join

pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 10000)
pd.set_option('display.max_colwidth', -1)


def main():
    li = []
    onlyfiles = [f for f in listdir('/home/samuel/PycharmProjects/Doctrin/venv/Data') if isfile(join('/home/samuel/PycharmProjects/Doctrin/venv/Data', f))]

    for file in onlyfiles:
        with open('/home/samuel/PycharmProjects/Doctrin/venv/Data/' + str(file)) as fd:
            df = pd.read_json(fd)
        li.append(df)

    df = pd.concat(li, axis=0, ignore_index=True)
    new_df = group_by_anamnesis(df)

    print(stiff_neck(new_df))
    print(find_fever(new_df, 36, 40))


def group_by_anamnesis(df):
    """Groups data by anamnesis_id and adds question, start_time, end_time and anamnesis_completed
       columns for each id"""
    df.groupby('id')  # Group by id
    df.sort_values('time')  # Makes sure questions are sorted by time

    df2 = pd.DataFrame({'id': df.id.unique()}) # Only unique id's

    df2['question'] = [list(df['question'].loc[df['id'] == x['id']]) for _, x in df2.iterrows()]  # Questions per unique id
    df2['anamnesis_completed'] = True
    df2['number_of_questions'] = 0

    for i, row in df2.iterrows():
        start = df['time'].loc[(df['id'] == row['id']) & (df['action'] == 'start_anamnesis')]
        if len(start.values) > 0:
            df2.at[i, 'start_time'] = start.values

        end = df['time'].loc[(df['id'] == row['id']) & (df['action'] == 'end_anamnesis')]
        if len(end.values) > 0:
            df2.at[i, 'end_time'] = end.values

    for i, row in df2.iterrows():
        count = 0
        if isinstance(row['end_time'], float):  # Makes sure not nan
            df2.at[i, 'end_time'] = None
            df2.at[i, 'anamnesis_completed'] = False

        for el in row['question']:
            if not isinstance(el, float):
                count = count + 1

        df2.at[i, 'number_of_questions'] = count

    df2.to_csv(r'doctrin.csv', index=False)

    return df2


def find_fever(data, low, high):
    """Counts the number of answers with a fever between low and high"""
    question_data = data['question']
    count = 0

    for row in question_data:
        if len(row) > 1:
            temp_q = row[1].values()
            temperature = temp_q[0]

            if is_number(temperature):
                if low < int(temperature) < high:
                    count = count + 1

    return count


def stiff_neck(data):
    """Counts the number of answers that HAS neck pain, chest pain and has NOT been abroad"""
    question_data = data['question']
    count = 0

    for row in question_data:
        if len(row) > 5:
            if not isinstance(row[5], float):
                abroad = row[5].values()
                abroad = str(abroad[0])

                neck_chest = row[3].values()
                neck_chest = neck_chest[0]

                neck = neck_chest[1].values()  # index 1 <=> Stiff neck
                chest = neck_chest[2].values()  # index 2 <=> Chest pain

                neck = str(neck[0])
                chest = str(chest[0])

                if 'no' in abroad and 'yes' in chest and 'yes' in neck:
                    count = count + 1

    return count


def is_number(s):
    """Returns True if input is a number and False otherwise"""
    try:
        float(s)
        return True
    except ValueError:
        return False


if __name__ == '__main__': main()