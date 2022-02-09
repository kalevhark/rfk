from collections import Counter
from datetime import date, datetime, timedelta
import json
import os
from pathlib import Path, PurePath
import pickle

import pandas as pd

if __name__ == "__main__":
    import django
    os.environ['DJANGO_SETTINGS_MODULE'] = 'rfk.settings'
    django.setup()

from django.conf import settings

path = settings.BASE_DIR
DATA_DIR = path / 'main' / 'static' / 'main' / 'data'

VALDKONNAD = [
'LIIKUMINE_1',
'LIIGUTAMINE_2',
'KEEL_KÕNE_3_1',
'NÄGEMINE_3_2',
'KUULMINE_3_3',
'ENESEHOOLDUS_4',
'ÕPPIMINE_5',
'KOHANEMINE_6',
'SUHTED_7',
]

ASTMED = [
    (3.5, 'sügav'),
    (2.76, 'raske'),
    (2, 'keskmine'),
]

def read_excel2df():
    try:
        with open(DATA_DIR / 'toe2021.pickle', 'rb') as f:
            df = pickle.load(f)
    except:
        with open(DATA_DIR / 'toe2021.xlsx', 'rb') as file:
            df = pd.read_excel(
                file,
                parse_dates=[2, 5, 9, 15, 16],
            )
        print(df.shape, '->', end=' ')
        # df.drop_duplicates(inplace=True)
        df.replace({pd.NaT: ''}, inplace=True)
        print(df.shape)
        # df.sort_values(['MEN_ID', 'SAMM_ALATES_AEG'], inplace=True)
        with open(DATA_DIR / 'toe2021.pickle', 'wb') as f:
            pickle.dump(df, f, pickle.HIGHEST_PROTOCOL)
    return df

def filter_lopetatud_menetlused(df):
    # Jätame ainult 2021 lõpetatud tööd
    filter = (
        (df['OTSUSE_KPV'].dt.year == 2021) &
        ((df['O_TÜÜP'] == 'Positiivne') | (df['O_TÜÜP'] == 'Negatiivne'))
    )
    df_filter = df[filter]
    print(df.shape, '->', df_filter.shape)
    return df_filter

def get_raskusaste(valdkond, skoor):
    if skoor < 2:
        return ''
    elif skoor < 2.76:
        if valdkond in ['LIIGUTAMINE_2', 'ENESEHOOLDUS_4']:
            return ''
        else:
            return 'Keskmine puue'
    elif skoor < 3.5:
        if valdkond in ['LIIGUTAMINE_2', 'ENESEHOOLDUS_4']:
            return 'Keskmine puue'
        else:
            return 'Raske puue'
    elif skoor <= 4:
        if valdkond in ['LIIGUTAMINE_2', 'ENESEHOOLDUS_4']:
            return 'Raske puue'
        else:
            return 'Sügav puue'
    else:
        return 'ERROR'

def get_raskusaste_final(raskusastmed):
    astmed = ['Sügav puue', 'Raske puue', 'Keskmine puue']
    for aste in astmed:
        if aste in raskusastmed:
            return aste
    return ''

def add_raskusaste(df):
    try:
        with open(DATA_DIR / 'toe2021_computed.pickle', 'rb') as f:
            df = pickle.load(f)
    except:
        for valdkond in VALDKONNAD:
            df['PRT_' + valdkond] = df.apply(
                lambda row : get_raskusaste(valdkond, row[valdkond]),
                axis = 1
            )
        for valdkond in VALDKONNAD:
            df['TVH_' + valdkond + '_A'] = df.apply(
                lambda row : get_raskusaste(valdkond, row[valdkond+'_A']),
                axis=1
            )
        df['TVH_PUUE'] = df.apply(
            lambda row : get_raskusaste_final(
                set(row['TVH_'+valdkond+'_A'] for valdkond in VALDKONNAD)
            ),
            axis=1
        )
        with open(DATA_DIR / 'toe2021_computed.pickle', 'wb') as f:
            pickle.dump(df, f, pickle.HIGHEST_PROTOCOL)
    return df

def make_table_tvh_puue_vs_prt_puue_all(df):
    table = pd.pivot_table(
        df,
        values=['ISIKUKOOD'],
        columns=['TVH_PUUE'],
        index=['PUUE'],
        aggfunc='count'
    ).fillna(0).astype('int32')
    # print(table)
    return table

def make_table_tvh_puue_vs_prt_puue_decr(df):
    filter = df['KORRIG_ALLA'] == -0.5
    df_filter = df[filter]
    table = pd.pivot_table(
        df_filter,
        values=['ISIKUKOOD'],
        columns=['TVH_PUUE'],
        index=['PUUE'],
        aggfunc='count'
    ).fillna(0).astype('int32')
    # print(table)
    return table

def make_table_tvh_puue_vs_prt_puue_incr(df):
    filter = df['KORRIG_ÜLES'] == 0.5
    df_filter = df[filter]
    table = pd.pivot_table(
        df_filter,
        values=['ISIKUKOOD'],
        columns=['TVH_PUUE'],
        index=['PUUE'],
        aggfunc='count'
    ).fillna(0).astype('int32')
    print(table)
    return table

def make_table_tvh_valdkond_vs_prt_valdkond(df):
    menetlused = df['TAOTLUS'].unique()
    print('Menetlusi:', len(menetlused))

    data_valdkonnad = []
    data_diagnoosid = []

    n = 0
    for menetlus in menetlused:
        n += 1
        if n % 5000 == 0:
            print(n)
        df_menetlus = df[df['TAOTLUS'] == menetlus]
        menetlusandmed = df_menetlus.iloc[0]
        for valdkond in VALDKONNAD:
            dgnid = [dgn.split('.')[0] for dgn in menetlusandmed['DIAGNOOSID'].split(';')]
            if menetlusandmed[valdkond] > menetlusandmed[valdkond+'_A']:
                data_valdkonnad.append('+'+valdkond)
                data_diagnoosid.extend(dgnid)
            if menetlusandmed[valdkond] < menetlusandmed[valdkond+'_A']:
                data_valdkonnad.append('-'+valdkond)
                data_diagnoosid.extend(dgnid)
    series = [el[1] for el in Counter(data_valdkonnad).items()]
    index =  [el[0] for el in Counter(data_valdkonnad).items()]
    table_valdkonnad = pd.DataFrame(series, index=index, columns=['count']).sort_values(['count'], ascending=False)
    # print(table_valdkonnad)

    series = [el[1] for el in Counter(data_diagnoosid).items()]
    index = [el[0] for el in Counter(data_diagnoosid).items()]
    table_diagnoosid = pd.DataFrame(series, index=index, columns=['count']).sort_values(['count'], ascending=False)
    print(table_diagnoosid)

    return table_valdkonnad, table_diagnoosid

def make_table_tvh_valdkond_vs_prt_valdkond_incr(df):
    filter = df['KORRIG_ÜLES'] == 0.5
    df_filter = df[filter]

    menetlused = df_filter['TAOTLUS'].unique()
    print('Menetlusi:', len(menetlused))

    data_valdkonnad = []
    data_diagnoosid = []

    n = 0
    for menetlus in menetlused:
        n += 1
        if n % 5000 == 0:
            print(n)
        df_menetlus = df_filter[df_filter['TAOTLUS'] == menetlus]
        menetlusandmed = df_menetlus.iloc[0]
        for valdkond in VALDKONNAD:
            dgnid = [dgn.split('.')[0] for dgn in menetlusandmed['DIAGNOOSID'].split(';')]
            if menetlusandmed[valdkond] > menetlusandmed[valdkond + '_A']:
                data_valdkonnad.append('+' + valdkond)
                data_diagnoosid.extend(dgnid)
            if menetlusandmed[valdkond] < menetlusandmed[valdkond + '_A']:
                data_valdkonnad.append('-' + valdkond)
                data_diagnoosid.extend(dgnid)
    series = [el[1] for el in Counter(data_valdkonnad).items()]
    index = [el[0] for el in Counter(data_valdkonnad).items()]
    table_valdkonnad = pd.DataFrame(series, index=index, columns=['count']).sort_values(['count'], ascending=False)
    # print(table_valdkonnad)

    series = [el[1] for el in Counter(data_diagnoosid).items()]
    index = [el[0] for el in Counter(data_diagnoosid).items()]
    table_diagnoosid = pd.DataFrame(series, index=index, columns=['count']).sort_values(['count'], ascending=False)
    print(table_diagnoosid)

    return table_valdkonnad, table_diagnoosid

def make_table_tvh_valdkond_vs_prt_valdkond_decr(df):
    filter = df['KORRIG_ALLA'] == -0.5
    df_filter = df[filter]

    menetlused = df_filter['TAOTLUS'].unique()
    print('Menetlusi:', len(menetlused))

    data_valdkonnad = []
    data_diagnoosid = []

    n = 0
    for menetlus in menetlused:
        n += 1
        if n % 5000 == 0:
            print(n)
        df_menetlus = df_filter[df_filter['TAOTLUS'] == menetlus]
        menetlusandmed = df_menetlus.iloc[0]
        for valdkond in VALDKONNAD:
            dgnid = [dgn.split('.')[0] for dgn in menetlusandmed['DIAGNOOSID'].split(';')]
            if menetlusandmed[valdkond] > menetlusandmed[valdkond + '_A']:
                data_valdkonnad.append('+' + valdkond)
                data_diagnoosid.extend(dgnid)
            if menetlusandmed[valdkond] < menetlusandmed[valdkond + '_A']:
                data_valdkonnad.append('-' + valdkond)
                data_diagnoosid.extend(dgnid)

    series = [el[1] for el in Counter(data_valdkonnad).items()]
    index = [el[0] for el in Counter(data_valdkonnad).items()]
    table_valdkonnad = pd.DataFrame(series, index=index, columns=['count']).sort_values(['count'], ascending=False)
    # print(table_valdkonnad)

    series = [el[1] for el in Counter(data_diagnoosid).items()]
    index = [el[0] for el in Counter(data_diagnoosid).items()]
    table_diagnoosid = pd.DataFrame(series, index=index, columns=['count']).sort_values(['count'], ascending=False)
    print(table_diagnoosid)

    return table_valdkonnad, table_diagnoosid

def save(salvestamiseks):
    with pd.ExcelWriter(DATA_DIR / 'toe2021_computed.xlsx') as writer:
        for salvestis in salvestamiseks.keys():
            salvestamiseks[salvestis].to_excel(writer, sheet_name=salvestis)
            # salvestamiseks[salvestis].to_csv(DATA_DIR / f'{salvestis}.csv')

def show_unique(df):
    # print(df.shape, df.columns, df.head())
    n = 0
    for col in df.columns:
    #     print(col, len(df[col].unique()))
        # print(n, col)
        n += 1
    # print(df['S_OLEK'].unique())
    # print(df['TV_VALISTAV_SEISUND'].unique())
    # print(df['HYVITIS'].unique())
    # print(df['O_LIIK'].unique())
    # print(df['O_TYYP'].unique())
    # print(df['RASKUSASTE'].unique())
    # print(df['TVH_OTSUS'].unique())


if __name__ == "__main__":
    print('start', datetime.now())
    salvestamiseks = dict()
    # Loeme andmed
    df = read_excel2df()


    # Filtreerime l6petatud ja 2021 aasta
    df = filter_lopetatud_menetlused(df)

    # Lisame puude raskusastmed valdkonniti
    df = add_raskusaste(df)
    salvestamiseks['Koond'] = df # .head(100)

    result = make_table_tvh_puue_vs_prt_puue_all(df)
    salvestamiseks['TVHvsPRT_all'] = result

    result = make_table_tvh_puue_vs_prt_puue_decr(df)
    salvestamiseks['TVHvsPRT_decr'] = result

    result = make_table_tvh_puue_vs_prt_puue_incr(df)
    salvestamiseks['TVHvsPRT_incr'] = result

    result_valdkonnad, result_diagnoosid = make_table_tvh_valdkond_vs_prt_valdkond(df)
    salvestamiseks['TVHvsPRT_vk'] = result_valdkonnad
    salvestamiseks['TVHvsPRT_dgn'] = result_diagnoosid

    result_valdkonnad, result_diagnoosid = make_table_tvh_valdkond_vs_prt_valdkond_incr(df)
    salvestamiseks['TVHvsPRT_vk_incr'] = result_valdkonnad
    salvestamiseks['TVHvsPRT_dgn_incr'] = result_diagnoosid

    result_valdkonnad, result_diagnoosid = make_table_tvh_valdkond_vs_prt_valdkond_decr(df)
    salvestamiseks['TVHvsPRT_vk_decr'] = result_valdkonnad
    salvestamiseks['TVHvsPRT_dgn_decr'] = result_diagnoosid

    # show_unique(df)
    # Koondame menetluse yhele reale
    # df_result = get_koond_df(df)

    # Salvestame tulemused
    save(salvestamiseks)
    print('stopp', datetime.now())


"""
0 ISIKUKOOD
1 SÜNNIAASTA
2 SURNUD
3 SUGU
4 TAOTLUS
5 TAOTLEB_ALATES_KPV
6 EKSPERTIIS
7 VÄL_SEISUND
8 OTSUS
9 OTSUSE_KPV
10 O_LIIK
11 O_TÜÜP
12 PÕHIDIAGNOOS
13 DIAGNOOSID
14 PUUE
15 PUUE_ALGUS_KPV
16 PUUE_LOPP_KPV
17 PUE_LIIK
18 LIIT_PUE
19 KORRIG_ALLA
20 KORRIG_ÜLES
21 LIIKUMINE_1
22 LIIGUTAMINE_2
23 KEEL_KÕNE_3_1
24 NÄGEMINE_3_2
25 KUULMINE_3_3
26 ENESEHOOLDUS_4
27 ÕPPIMINE_5
28 KOHANEMINE_6
29 SUHTED_7
30 NARKO_8
31 MUUD_9
32 ERIJUHTUM
33 LIIKUMINE_1_A
34 LIIGUTAMINE_2_A
35 KEEL_KÕNE_3_1_A
36 NÄGEMINE_3_2_A
37 KUULMINE_3_3_A
38 ENESEHOOLDUS_4_A
39 ÕPPIMINE_5_A
40 KOHANEMINE_6_A
41 SUHTED_7_A
42 NARKO_8_A
43 MUUD_9_A
44 VÄLISTAV_SEISUND_A
45 ERIJUHTUM_A
46 PRT_LIIKUMINE_1
47 PRT_LIIGUTAMINE_2
48 PRT_KEEL_KÕNE_3_1
49 PRT_NÄGEMINE_3_2
50 PRT_KUULMINE_3_3
51 PRT_ENESEHOOLDUS_4
52 PRT_ÕPPIMINE_5
53 PRT_KOHANEMINE_6
54 PRT_SUHTED_7
55 TVH_LIIKUMINE_1_A
56 TVH_LIIGUTAMINE_2_A
57 TVH_KEEL_KÕNE_3_1_A
58 TVH_NÄGEMINE_3_2_A
59 TVH_KUULMINE_3_3_A
60 TVH_ENESEHOOLDUS_4_A
61 TVH_ÕPPIMINE_5_A
62 TVH_KOHANEMINE_6_A
63 TVH_SUHTED_7_A
64 TVH_PUUE
"""