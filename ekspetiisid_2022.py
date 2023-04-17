from collections import Counter
from datetime import date, datetime, timedelta
import json
import os
from pathlib import Path, PurePath
import pickle

import numpy as np
import pandas as pd

if __name__ == "__main__":
    import django
    os.environ['DJANGO_SETTINGS_MODULE'] = 'rfk.settings'
    django.setup()

from django.conf import settings

path = settings.BASE_DIR
DATA_DIR = path / 'main' / 'static' / 'main' / 'data'
FAIL = 'ekspertarstid_menetlused_2021'
# FAIL = 'ekspertarstid_menetlused_2022_I_PA'

MENETLEJA_ARST = [
    'AUNE TAMM', 'REET MOOR ', 'MAIU ELKEN ', 'KERSTI PEDAKMÄE', 'REET TALI ',
    'PIIBE PAI ', 'MARGOT LIIDEMANN ', 'ASTA PÄRLI ', 'MERIS TAMMIK ',
    'HELI PENU ', 'TUULI KIENS', 'EVE MÄNNIK', 'ANDRES MESILA ', 'EVA LEMMING ',
    'LAURA MIHKLA ', 'KADRI KELLAMÄE ', 'JULIJA ALEKSANDROVA ',
    'HELENA GRAUBERG', 'TIINA VARBLANE', 'IVAR VIPP ', 'JUTA RATASSEPP ',
    'KADI OJALA'
]

MENETLEJA_SP = [
    'KAIDI OTT', 'VEEVI KÕRGMÄE ', 'HELENA KANGRO', 'ANU IVA',
    'MERIKE RJABOV', 'IRINA KUPINSKAJA ', 'KERSTI TALTS', 'SIRJE LEPIK ',
    'MIRLIAN KASK ', 'ANNELE RANDMAA', 'SIIRI ROSENTHAL',
    'KÜLLI KLEMMER', 'KADRI KANNE ', 'EILI NURMETALO', 'ÜLVE HELSTEIN ',
    'TRIIN HALLIK', 'SIRJE POSKA', 'JANIKA MEIKAR ', 'TIIU OJA',
    'NATALJA MINTŠENKOVA', 'EPP NOOBEL ', 'SIGNE VESKIOJA', 'KAIE MARANDI ',
    'LIANA KINKMAN', 'AILI MÄEMAT', 'ANNEMARI OHERD', 'JANNE LAANES'
]

HYVITIS = [
    'Lapse puude raskusastme tuvastamine',
    'Tööealise inimese puude raskusastme tuvastamine',
    'Pensioniealise inimese puude raskusastme tuvastamine'
]

def timedelta_minutes(algus, l6pp):
    try:
        # ajakulu = l6pp - algus
        return int((l6pp - algus).total_seconds()/60)
    except:
        return -1

# ajaslotid 10min, 15min, 30min, 60min, 2h, 4h, 8h, 24h, 2p, 4p, 8p, 16p, 16+p
def minutes_to_timeperiod(minutid):
    if minutid > (16 * 24 * 60):
        return '384:00+'
    if minutid > (8 * 24 * 60):
        return '384:00'
    if minutid > (4 * 24 * 60):
        return '192:00'
    if minutid > (2 * 24 * 60):
        return '096:00'
    if minutid > (24 * 60):
        return '048:00'
    if minutid > (8 * 60):
        return '024:00'
    if minutid > (4 * 60):
        return '008:00'
    if minutid > (2 * 60):
        return '004:00'
    if minutid > 60:
        return '002:00'
    if minutid > 30:
        return '001:00'
    if minutid > 15:
        return '000:30'
    if minutid > 10:
        return '000:15'
    if minutid <= 10:
        return '000:10'

def read_excel2df():
    try:
        with open(DATA_DIR / f'{FAIL}.pickle', 'rb') as f:
            df = pickle.load(f)
    except:
        with open(DATA_DIR / f'{FAIL}.xlsx', 'rb') as file:
            df = pd.read_excel(
                file,
                parse_dates=[1, 2, 8, 9],
            )
        print(df.shape, '->', end=' ')
        df.replace({pd.NaT: ''}, inplace=True)

        df.sort_values(['MEN_ID', 'OLEK_ALGUS_AEG'], inplace=True)
        with open(DATA_DIR / f'{FAIL}.pickle', 'wb') as f:
            pickle.dump(df, f, pickle.HIGHEST_PROTOCOL)
    df['TD_MINUTES'] = df.apply(
        lambda row: timedelta_minutes(row['OLEK_ALGUS_AEG'], row['OLEK_KUNI_AEG']),
        axis=1
    )
    df['TIMEPERIOD'] = df.apply(
        lambda row: minutes_to_timeperiod(row['TD_MINUTES']),
        axis=1
    )
    print(df.shape, df.columns)
    return df

def make_koondtabel(df):
    print('Ekspertiiside koondtabel')
    filter = (
            (df['MENETLEJA'].isin(MENETLEJA_ARST)) &
            (df['O_TYYP'] != 'Läbi vaatamata jätmise otsus')
    )
    df_filter = df[filter]

    # Sorteerime menetluste järgi
    menetlused = df_filter['MEN_ID'].unique()
    print(df_filter.shape, 'menetlusi:', len(menetlused))

    data = dict()
    n = 0
    for menetlus in menetlused:
        n += 1
        if n % 5000 == 0:
            print(n)
        df_menetlus = df_filter[df_filter['MEN_ID'] == menetlus]
        menetlusandmed = df_menetlus.iloc[0]
        arst = menetlusandmed.MENETLEJA
        if arst not in MENETLEJA_ARST:
            continue
        else:
            menetlus_hyvitis = menetlusandmed.HYVITIS

            try:
                algus = df_menetlus[df_menetlus['S_OLEK'] == 'Alustamata'].iloc[0]['OLEK_ALGUS_AEG']
            except:
                algus = None
            try:
                l6pp = df_menetlus[df_menetlus['S_OLEK'] == 'Lõpetatud'].iloc[0]['OLEK_ALGUS_AEG']
            except:
                l6pp = None
            try:
                toos = df_menetlus[df_menetlus['S_OLEK'] == 'Töös'].iloc[0]['OLEK_ALGUS_AEG']
            except:
                toos = None
            if all([algus, toos, l6pp]) and (algus < toos < l6pp):
                data[menetlus] = [
                    menetlus,
                    menetlus_hyvitis,
                    arst,
                    algus,
                    toos,
                    l6pp
                ]

    columns = [
        'MEN_ID',
        'HYVITIS',
        'MENETLEJA',
        'ALGUS',
        'TÖÖS',
        'LÕPP'
    ]
    df_result = pd.DataFrame.from_dict(
        data,
        orient='index',
        columns=columns
    )
    df_result['TD_MINUTES'] = df_result.apply(
        lambda row: timedelta_minutes(row['ALGUS'], row['LÕPP']),
        axis=1
    )
    df_result['TD_HOURS'] = df_result['TD_MINUTES'] / 60
    df_result['TD_DAYS'] = df_result['TD_MINUTES'] / 60 / 24
    df_result[['TD_MINUTES', 'TD_HOURS', 'TD_DAYS']] = df_result[['TD_MINUTES', 'TD_HOURS', 'TD_DAYS']].astype(int)
    df_result.sort_values(['ALGUS'], inplace=True)
    return df_result

def save(salvestamiseks):
    # df_result.to_csv(DATA_DIR / 'output.csv')
    with pd.ExcelWriter(DATA_DIR / f'{FAIL}_computed.xlsx') as writer:
        # for salvestis in salvestamiseks.keys():
        #     salvestamiseks[salvestis].to_excel(writer, sheet_name=salvestis)
        #     salvestamiseks[salvestis].to_csv(DATA_DIR / f'{salvestis}.csv')
        for salvestis in salvestamiseks.keys():
            df_tosheet = salvestamiseks[salvestis]['df']
            df_title = salvestamiseks[salvestis]['title']
            df_tosheet.to_excel(writer, sheet_name=salvestis, startcol = 0, startrow = 5)
            worksheet = writer.sheets[salvestis]
            for i in range(len(df_title)):
                worksheet.write_string(i, 0, df_title[i])

def show_unique(df):
    print(df['MENETLEJA'].unique())
    # print('MEN_OLEK', df['MEN_OLEK'].unique())
    # print(df['S_OLEK'].unique())
    # print(df['TV_VALISTAV_SEISUND'].unique())
    # print(df['HYVITIS'].unique())
    # print(df['O_LIIK'].unique())
    # print(df['O_TYYP'].unique())
    # print(df['RASKUSASTE'].unique())

def make_table_ekspertiis_menetluses_lte_7days_count(df):
    print('Ekspertiisid töös 7 päeva: rohkem ja vähem')
    # Kes teevad ekspertiise
    ska_arstid_ekspertiise_cnt = df.groupby(['MENETLEJA']).count()['TD_DAYS'] # .sort_values(ascending=False)
    ska_arstid_ekspertiise_mean = df.groupby(['MENETLEJA']).mean()['TD_DAYS'] # .sort_values(ascending=False)

    print('Ekspertiisid töös 7 päeva või vähem')
    filter = (
            (df['TD_DAYS'] <= 7)
    )
    df_filter = df[filter]
    print(df_filter.shape, 'menetlusi:', len(df_filter.MEN_ID.unique()))

    ska_arstid_ekspertiise_lte_cnt = df_filter.groupby(['MENETLEJA']).count()['TD_DAYS']
    ska_arstid_ekspertiise_vanusgrupiti_lte = pd.pivot_table(
        df_filter,
        values=['TD_DAYS'],
        columns=['HYVITIS'],
        index=['MENETLEJA'],
        aggfunc={'TD_DAYS': 'count'}
    )
    ska_arstid_ekspertiise_vanusgrupiti_lte.columns = [
        'LA',
        'VPI',
        'TÖE'
    ]

    print('Ekspertiisid töös 8 päeva ja rohkem')
    filter = (
        (df['TD_DAYS'] > 7)
    )

    df_filter = df[filter]
    print(df_filter.shape, 'menetlusi:', len(df_filter.MEN_ID.unique()))

    ska_arstid_ekspertiise_gt_cnt = df_filter.groupby(['MENETLEJA']).count()['TD_DAYS']
    ska_arstid_ekspertiise_vanusgrupiti_gt = pd.pivot_table(
        df_filter,
        values=['TD_DAYS'],
        columns=['HYVITIS'],
        index=['MENETLEJA'],
        aggfunc={'TD_DAYS': 'count'}
    )
    ska_arstid_ekspertiise_vanusgrupiti_gt.columns = [
        'LA',
        'VPI',
        'TÖE'
    ]

    frame = {
        'Menetlusi KOKKU': ska_arstid_ekspertiise_cnt,
        'Menetlusaeg keskmiselt (päeva)': ska_arstid_ekspertiise_mean,
        'Menetlusi KOKKU lte7d': ska_arstid_ekspertiise_lte_cnt,
        'LA lte7d': ska_arstid_ekspertiise_vanusgrupiti_lte['LA'],
        'TÖE lte7d': ska_arstid_ekspertiise_vanusgrupiti_lte['TÖE'],
        'VPI lte7d': ska_arstid_ekspertiise_vanusgrupiti_lte['VPI'],
        'Menetlusi KOKKU gt7d': ska_arstid_ekspertiise_gt_cnt,
        'LA gt7d': ska_arstid_ekspertiise_vanusgrupiti_gt['LA'],
        'TÖE gt7d': ska_arstid_ekspertiise_vanusgrupiti_gt['TÖE'],
        'VPI gt7d': ska_arstid_ekspertiise_vanusgrupiti_gt['VPI']
    }
    result = pd.DataFrame(frame).\
        fillna(0).\
        astype('int32').\
        sort_values(['Menetlusaeg keskmiselt (päeva)'], ascending=False)
    # print(result)
    return result

def make_table_ekspertiis_toos_avgtime(df):
    print('Ekspertiisid töös')
    filter = (
            (df['MENETLEJA'].isin(MENETLEJA_ARST)) &
            (df['S_OLEK'] == 'Töös') &
            (df['O_TYYP'] != 'Läbi vaatamata jätmise otsus')
    )

    df_filter = df[filter]
    print(df_filter.shape, 'menetlusi:', len(df_filter.MEN_ID.unique()))

    # Kes teevad ekspertiise
    ska_arstid_ekspertiise = [
        df_filter.mean()['TD_MINUTES'],
        df_filter.median()['TD_MINUTES'],
        # df_filter.percentile(80)['TD_MINUTES']
    ]
    ska_arstid_ekspertiise_vanusgrupiti = pd.pivot_table(
        df_filter,
        values=['TD_MINUTES'],
        columns=['HYVITIS'],
        # index=['MENETLEJA'],
        aggfunc={
            'TD_MINUTES': [
                np.mean,
                np.median,
                # lambda x: np.percentile(x, 80)
            ]
        }
    )
    ska_arstid_ekspertiise_vanusgrupiti.columns = [
        'LA',
        'VPI',
        'TÖE'
    ]
    frame = {
        'Keskmine aeg (min)': ska_arstid_ekspertiise,
        'LA': ska_arstid_ekspertiise_vanusgrupiti['LA'],
        'TÖE': ska_arstid_ekspertiise_vanusgrupiti['TÖE'],
        'VPI': ska_arstid_ekspertiise_vanusgrupiti['VPI'],
    }
    result = pd.DataFrame(frame).fillna(0).astype('int32')
    print(result)
    return result

def make_table_ekspertiis_toos_lte_120minutes_all_avgtime(df):
    print('Ekspertiisid töös')
    filter = (
            (df['MENETLEJA'].isin(MENETLEJA_ARST)) &
            (df['S_OLEK'] == 'Töös') &
            (df['O_TYYP'] != 'Läbi vaatamata jätmise otsus') &
            (df['TD_MINUTES'] <= 120)
    )

    df_filter = df[filter]
    print(df_filter.shape, 'menetlusi:', len(df_filter.MEN_ID.unique()))

    # Kes teevad ekspertiise
    ska_arstid_ekspertiise = [df_filter.mean()['TD_MINUTES'], df_filter.median()['TD_MINUTES']]
    ska_arstid_ekspertiise_vanusgrupiti = pd.pivot_table(
        df_filter,
        values=['TD_MINUTES'],
        columns=['HYVITIS'],
        # index=['MENETLEJA'],
        aggfunc={'TD_MINUTES': [np.mean, np.median]}
    )
    ska_arstid_ekspertiise_vanusgrupiti.columns = [
        'LA',
        'VPI',
        'TÖE'
    ]
    frame = {
        'Keskmine aeg (min)': ska_arstid_ekspertiise,
        'LA': ska_arstid_ekspertiise_vanusgrupiti['LA'],
        'TÖE': ska_arstid_ekspertiise_vanusgrupiti['TÖE'],
        'VPI': ska_arstid_ekspertiise_vanusgrupiti['VPI'],
    }
    result = pd.DataFrame(frame).fillna(0).astype('int32')
    print(result)
    return result

def make_table_ekspertiis_toos_avgtime_ekspertarstid(df):
    print('Ekspertiisid töös')
    filter = (
            (df['MENETLEJA'].isin(MENETLEJA_ARST)) &
            (df['S_OLEK'] == 'Töös') &
            (df['O_TYYP'] != 'Läbi vaatamata jätmise otsus')
    )

    df_filter = df[filter]
    print(df_filter.shape, 'menetlusi:', len(df_filter.MEN_ID.unique()))

    # Kes teevad ekspertiise
    ska_arstid_ekspertiise = df_filter.groupby(['MENETLEJA']).mean()['TD_MINUTES'].sort_values(ascending=False)
    ska_arstid_ekspertiise_vanusgrupiti = pd.pivot_table(
        df_filter,
        values=['TD_MINUTES'],
        columns=['HYVITIS'],
        index=['MENETLEJA'],
        aggfunc={'TD_MINUTES': np.mean}
    )
    ska_arstid_ekspertiise_vanusgrupiti.columns = [
        'LA',
        'VPI',
        'TÖE'
    ]
    frame = {
        'Keskmine aeg (min)': ska_arstid_ekspertiise,
        'LA': ska_arstid_ekspertiise_vanusgrupiti['LA'],
        'TÖE': ska_arstid_ekspertiise_vanusgrupiti['TÖE'],
        'VPI': ska_arstid_ekspertiise_vanusgrupiti['VPI'],
    }
    result = pd.DataFrame(frame).fillna(0).astype('int32').sort_values(['Keskmine aeg (min)'], ascending=False)
    # print(result)
    return result

def make_table_ekspertiis_toos_count_ekspertarstid(df):
    print('Ekspertiisid töös')
    filter = (
            (df['MENETLEJA'].isin(MENETLEJA_ARST)) &
            (df['S_OLEK'] == 'Töös') &
            (df['O_TYYP'] != 'Läbi vaatamata jätmise otsus')
    )

    df_filter = df[filter]
    print(df_filter.shape, 'menetlusi:', len(df_filter.MEN_ID.unique()))

    # Kes teevad ekspertiise
    ska_arstid_ekspertiise = df_filter.groupby(['MENETLEJA']).count()['TD_MINUTES'].sort_values(ascending=False)
    ska_arstid_ekspertiise_vanusgrupiti = pd.pivot_table(
        df_filter,
        values=['TD_MINUTES'],
        columns=['HYVITIS'],
        index=['MENETLEJA'],
        aggfunc={'TD_MINUTES': 'count'}
    )
    ska_arstid_ekspertiise_vanusgrupiti.columns = [
        'LA',
        'VPI',
        'TÖE'
    ]
    frame = {
        'Menetlusi': ska_arstid_ekspertiise,
        'LA': ska_arstid_ekspertiise_vanusgrupiti['LA'],
        'TÖE': ska_arstid_ekspertiise_vanusgrupiti['TÖE'],
        'VPI': ska_arstid_ekspertiise_vanusgrupiti['VPI'],
    }
    result = pd.DataFrame(frame).fillna(0).astype('int32').sort_values(['Menetlusi'], ascending=False)
    # print(result)
    return result

def make_table_ekspertiis_toos_lte_120minutes_avgtime(df):
    print('Ekspertiisid töös 120 minutit või vähem')
    filter = (
            (df['MENETLEJA'].isin(MENETLEJA_ARST)) &
            (df['S_OLEK'] == 'Töös') &
            (df['O_TYYP'] != 'Läbi vaatamata jätmise otsus') &
            (df['TD_MINUTES'] <= 120)
    )

    df_filter = df[filter]
    print(df_filter.shape, 'menetlusi:', len(df_filter.MEN_ID.unique()))

    # Kes teevad ekspertiise
    ska_arstid_ekspertiise = df_filter.groupby(['MENETLEJA']).mean()['TD_MINUTES'].sort_values(ascending=False)
    ska_arstid_ekspertiise_vanusgrupiti = pd.pivot_table(
        df_filter,
        values=['TD_MINUTES'],
        columns=['HYVITIS'],
        index=['MENETLEJA'],
        aggfunc={'TD_MINUTES': np.mean}
    )
    ska_arstid_ekspertiise_vanusgrupiti.columns = [
        'LA',
        'VPI',
        'TÖE'
    ]
    frame = {
        'Keskmine aeg (min)': ska_arstid_ekspertiise,
        'LA': ska_arstid_ekspertiise_vanusgrupiti['LA'],
        'TÖE': ska_arstid_ekspertiise_vanusgrupiti['TÖE'],
        'VPI': ska_arstid_ekspertiise_vanusgrupiti['VPI'],
    }
    result = pd.DataFrame(frame).fillna(0).astype('int32').sort_values(['Keskmine aeg (min)'], ascending=False)
    # print(result)
    return result

def make_table_ekspertiis_toos_lte_120minutes_count(df):
    print('Ekspertiisid töös 120 minutit või vähem')
    filter = (
            (df['MENETLEJA'].isin(MENETLEJA_ARST)) &
            (df['S_OLEK'] == 'Töös') &
            (df['O_TYYP'] != 'Läbi vaatamata jätmise otsus') &
            (df['TD_MINUTES'] <= 120)
    )

    df_filter = df[filter]
    print(df_filter.shape, 'menetlusi:', len(df_filter.MEN_ID.unique()))

    # Kes teevad ekspertiise
    ska_arstid_ekspertiise = df_filter.groupby(['MENETLEJA']).count()['TD_MINUTES'].sort_values(ascending=False)
    ska_arstid_ekspertiise_vanusgrupiti = pd.pivot_table(
        df_filter,
        values=['TD_MINUTES'],
        columns=['HYVITIS'],
        index=['MENETLEJA'],
        aggfunc={'TD_MINUTES': 'count'}
    )
    ska_arstid_ekspertiise_vanusgrupiti.columns = [
        'LA',
        'VPI',
        'TÖE'
    ]
    frame = {
        'Menetlusi': ska_arstid_ekspertiise,
        'LA': ska_arstid_ekspertiise_vanusgrupiti['LA'],
        'TÖE': ska_arstid_ekspertiise_vanusgrupiti['TÖE'],
        'VPI': ska_arstid_ekspertiise_vanusgrupiti['VPI'],
    }
    result = pd.DataFrame(frame).fillna(0).astype('int32').sort_values(['Menetlusi'], ascending=False)
    # print(result)
    return result

def make_table_ekspertiis_toos_gt_120minutes_avgtime(df):
    print('Ekspertiisid töös rohkem kui 120 minutit')
    filter = (
            (df['MENETLEJA'].isin(MENETLEJA_ARST)) &
            (df['S_OLEK'] == 'Töös') &
            (df['O_TYYP'] != 'Läbi vaatamata jätmise otsus') &
            (df['TD_MINUTES'] > 120)
    )

    df_filter = df[filter]
    print(df_filter.shape, 'menetlusi:', len(df_filter.MEN_ID.unique()))

    # Kes teevad ekspertiise
    ska_arstid_ekspertiise = df_filter.groupby(['MENETLEJA']).mean()['TD_MINUTES'].sort_values(ascending=False)
    ska_arstid_ekspertiise_vanusgrupiti = pd.pivot_table(
        df_filter,
        values=['TD_MINUTES'],
        columns=['HYVITIS'],
        index=['MENETLEJA'],
        aggfunc={'TD_MINUTES': np.mean}
    )
    ska_arstid_ekspertiise_vanusgrupiti.columns = [
        'LA',
        'VPI',
        'TÖE'
    ]
    frame = {
        'Keskmine aeg (min)': ska_arstid_ekspertiise,
        'LA': ska_arstid_ekspertiise_vanusgrupiti['LA'],
        'TÖE': ska_arstid_ekspertiise_vanusgrupiti['TÖE'],
        'VPI': ska_arstid_ekspertiise_vanusgrupiti['VPI'],
    }
    result = pd.DataFrame(frame).fillna(0).astype('int32').sort_values(['Keskmine aeg (min)'], ascending=False)
    # print(result)
    return result

def make_table_ekspertiis_toos_gt_120minutes_count(df):
    print('Ekspertiisid töös rohkem kui 120 minutit')
    filter = (
            (df['MENETLEJA'].isin(MENETLEJA_ARST)) &
            (df['S_OLEK'] == 'Töös') &
            (df['O_TYYP'] != 'Läbi vaatamata jätmise otsus') &
            (df['TD_MINUTES'] > 120)
    )

    df_filter = df[filter]
    print(df_filter.shape, 'menetlusi:', len(df_filter.MEN_ID.unique()))

    # Kes teevad ekspertiise
    ska_arstid_ekspertiise = df_filter.groupby(['MENETLEJA']).count()['TD_MINUTES'].sort_values(ascending=False)
    ska_arstid_ekspertiise_vanusgrupiti = pd.pivot_table(
        df_filter,
        values=['TD_MINUTES'],
        columns=['HYVITIS'],
        index=['MENETLEJA'],
        aggfunc={'TD_MINUTES': 'count'}
    )
    ska_arstid_ekspertiise_vanusgrupiti.columns = [
        'LA',
        'VPI',
        'TÖE'
    ]
    frame = {
        'Menetlusi': ska_arstid_ekspertiise,
        'LA': ska_arstid_ekspertiise_vanusgrupiti['LA'],
        'TÖE': ska_arstid_ekspertiise_vanusgrupiti['TÖE'],
        'VPI': ska_arstid_ekspertiise_vanusgrupiti['VPI'],
    }
    result = pd.DataFrame(frame).fillna(0).astype('int32').sort_values(['Menetlusi'], ascending=False)
    # print(result)
    return result

def make_table_ekspertiis_alustamata_avgtime(df):
    print('Ekspertiisid alustamata olekus')
    filter = (
            (df['MENETLEJA'].isin(MENETLEJA_ARST)) &
            (df['S_OLEK'] == 'Alustamata') &
            (df['O_TYYP'] != 'Läbi vaatamata jätmise otsus')
    )

    df_filter = df[filter]
    print(df_filter.shape, 'menetlusi:', len(df_filter.MEN_ID.unique()))

    # Kes teevad ekspertiise
    ska_arstid_ekspertiise = df_filter.groupby(['MENETLEJA']).mean()['TD_MINUTES'].sort_values(ascending=False)
    ska_arstid_ekspertiise_vanusgrupiti = pd.pivot_table(
        df_filter,
        values=['TD_MINUTES'],
        columns=['HYVITIS'],
        index=['MENETLEJA'],
        aggfunc={'TD_MINUTES': np.mean}
    )
    ska_arstid_ekspertiise_vanusgrupiti.columns = [
        'LA',
        'VPI',
        'TÖE'
    ]
    frame = {
        'Keskmine aeg (min)': ska_arstid_ekspertiise,
        'LA': ska_arstid_ekspertiise_vanusgrupiti['LA'],
        'TÖE': ska_arstid_ekspertiise_vanusgrupiti['TÖE'],
        'VPI': ska_arstid_ekspertiise_vanusgrupiti['VPI'],
    }
    result = pd.DataFrame(frame).fillna(0).astype('int32').sort_values(['Keskmine aeg (min)'], ascending=False)
    # print(result)
    return result

def make_table_ekspertiis_toos_timeperiods_count(df):
    print('Ekspertiisid töös ajakulu järgi')
    filter = (
            (df['MENETLEJA'].isin(MENETLEJA_ARST)) &
            (df['S_OLEK'] == 'Töös') &
            (df['O_TYYP'] != 'Läbi vaatamata jätmise otsus')
    )

    df_filter = df[filter]
    print(df_filter.shape, 'menetlusi:', len(df_filter.MEN_ID.unique()))

    # Kes teevad ekspertiise
    # ska_arstid_ekspertiise = df_filter.groupby(['MENETLEJA']).count()['TD_MINUTES'].sort_values(ascending=False)
    ska_arstid_ekspertiise_vanusgrupiti = pd.pivot_table(
        df_filter,
        values=['TD_MINUTES'],
        columns=['TIMEPERIOD'],
        index=['MENETLEJA'],
        aggfunc={'TD_MINUTES': 'count'}
    ).fillna(0).astype('int32')

    # print(ska_arstid_ekspertiise_vanusgrupiti)
    return ska_arstid_ekspertiise_vanusgrupiti

def make_table_crosstab_monthly(koondtabel):
    df = koondtabel[koondtabel['LÕPP'].dt.year == 2021]
    result = pd.crosstab(df.MENETLEJA, df['LÕPP'].dt.strftime('%m/%Y')) # \
        # .reset_index() \
        # .rename_axis([None], axis=1)
    return result

def make_table_crosstab_daily(koondtabel):
    df = koondtabel[koondtabel['LÕPP'].dt.year == 2021]
    result = pd.crosstab(df.MENETLEJA, df['LÕPP'].dt.strftime('%m/%d')) # \
        # .reset_index() \
        # .rename_axis([None], axis=1)
    return result

def make_table_crosstab_hourly(koondtabel):
    df = koondtabel[koondtabel['LÕPP'].dt.year == 2021]
    result = pd.crosstab(df.MENETLEJA, df['LÕPP'].dt.strftime('%H')) # \
        # .reset_index() \
        # .rename_axis([None], axis=1)
    return result

def make_table_crosstab_weekday(koondtabel):
    df = koondtabel[koondtabel['LÕPP'].dt.year == 2021]
    result = pd.crosstab(df.MENETLEJA, df['LÕPP'].dt.weekday) # \
        # .reset_index() \
        # .rename_axis([None], axis=1)
    return result

if __name__ == "__main__":
    print('start', datetime.now())
    salvestamiseks = dict()

    # Loeme andmed
    df = read_excel2df()
    # show_unique(df)

    # Algses andmesetis menetlusi
    menetlused = df['MEN_ID'].unique()
    print('Menetlusi:', len(menetlused))

    koondtabel = make_koondtabel(df)
    title = [
        'Koondtabel'
    ]
    salvestamiseks[title[0]] = {
        'df': koondtabel,
        'title': title
    }

    result = make_table_crosstab_monthly(koondtabel)
    title = [
        'Menetluste arv kuude kaupa'
    ]
    salvestamiseks[title[0]] = {
        'df': result,
        'title': title
    }

    result = make_table_crosstab_daily(koondtabel)
    title = [
        'Menetluste arv päevade kaupa'
    ]
    salvestamiseks[title[0]] = {
        'df': result,
        'title': title
    }

    result = make_table_crosstab_hourly(koondtabel)
    title = [
        'Menetluste arv tundide kaupa'
    ]
    salvestamiseks[title[0]] = {
        'df': result,
        'title': title
    }

    result = make_table_crosstab_weekday(koondtabel)
    title = [
        'Menetluste arv n-päevade kaupa'
    ]
    salvestamiseks[title[0]] = {
        'df': result,
        'title': title
    }

    result = make_table_ekspertiis_menetluses_lte_7days_count(koondtabel)
    title = [
        'Menetluste arv periooditi'
    ]
    salvestamiseks[title[0]] = {
        'df': result,
        'title': title
    }

    result = make_table_ekspertiis_toos_avgtime(df)
    title = [
        'Töös ajakulu keskmine'
    ]
    salvestamiseks['Töös ajakulu keskmine'] = {
        'df': result,
        'title': title
    }

    result = make_table_ekspertiis_toos_lte_120minutes_all_avgtime(df)
    title = [
        'Töös kuni 120min keskmine'
    ]
    salvestamiseks[title[0]] = {
        'df': result,
        'title': title
    }

    result = make_table_ekspertiis_toos_avgtime_ekspertarstid(df)
    title = [
        'Töös ajakulu EAd'
    ]
    salvestamiseks[title[0]] = {
        'df': result,
        'title': title
    }

    result = make_table_ekspertiis_toos_count_ekspertarstid(df)
    title = [
        'Töös kordi EAd'
    ]
    salvestamiseks[title[0]] = {
        'df': result,
        'title': title
    }

    result = make_table_ekspertiis_toos_lte_120minutes_avgtime(df)
    title = [
        'Töös kuni 120min aeg'
    ]
    salvestamiseks[title[0]] = {
        'df': result,
        'title': title
    }

    result = make_table_ekspertiis_toos_lte_120minutes_count(df)
    title = [
        'Töös kuni 120min kordi'
    ]
    salvestamiseks[title[0]] = {
        'df': result,
        'title': title
    }

    result = make_table_ekspertiis_toos_gt_120minutes_avgtime(df)
    title = [
        'Töös pikem 120min aeg'
    ]
    salvestamiseks[title[0]] = {
        'df': result,
        'title': title
    }

    result = make_table_ekspertiis_toos_gt_120minutes_count(df)
    title = [
        'Töös pikem 120min kordi'
    ]
    salvestamiseks[title[0]] = {
        'df': result,
        'title': title
    }

    result = make_table_ekspertiis_alustamata_avgtime(df)
    title = [
        'Alustamata olekus'
    ]
    salvestamiseks[title[0]] = {
        'df': result,
        'title': title
    }

    result = make_table_ekspertiis_toos_timeperiods_count(df)
    title = [
        'Töö ajakulu järgi'
    ]
    salvestamiseks[title[0]] = {
        'df': result,
        'title': title
    }

    # Salvestame tulemused
    save(salvestamiseks)
    print('stopp', datetime.now())


