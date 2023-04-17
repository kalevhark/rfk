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

MENETLEJA_ARST = [
    'TUULI KIENS', 'JULIJA ALEKSANDROVA ', 'KERSTI PEDAKMÄE', 'REET TALI ',
    'LAURA MIHKLA ', 'EVA LEMMING ', 'ANDRES MESILA ', 'ASTA PÄRLI ',
    'HELENA GRAUBERG', 'IVAR VIPP ', 'HELI PENU ', 'EVE MÄNNIK',
    'JUTA RATASSEPP ', 'KADI KALJULA', 'REET MOOR ', 'TIINA VARBLANE',
    'MERIS TAMMIK ', 'AUNE TAMM', 'PIIBE PAI ', 'KADRI KELLAMÄE ',
    'MAIU ELKEN ', 'MARGOT LIIDEMANN ',
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
        with open(DATA_DIR / 'ekspertarstid_menetlused_2021.pickle', 'rb') as f:
            df = pickle.load(f)
    except:
        with open(DATA_DIR / 'ekspertarstid_menetlused_2021.xlsx', 'rb') as file:
            df = pd.read_excel(
                file,
                parse_dates=[1, 2, 8, 9],
            )
        print(df.shape, '->', end=' ')
        df.replace({pd.NaT: ''}, inplace=True)

        df.sort_values(['MEN_ID', 'OLEK_ALGUS_AEG'], inplace=True)
        with open(DATA_DIR / 'ekspertarstid_menetlused_2021.pickle', 'wb') as f:
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

def save(salvestamiseks):
    # df_result.to_csv(DATA_DIR / 'output.csv')
    with pd.ExcelWriter(DATA_DIR / 'ekspertarstid_menetlused_2021_computed.xlsx') as writer:
        for salvestis in salvestamiseks.keys():
            salvestamiseks[salvestis].to_excel(writer, sheet_name=salvestis)
            # salvestamiseks[salvestis].to_csv(DATA_DIR / f'{salvestis}.csv')

def show_unique(df):
    print(df['MENETLEJA'].unique())
    print('MEN_OLEK', df['MEN_OLEK'].unique())
    print(df['S_OLEK'].unique())
    print(df['TV_VALISTAV_SEISUND'].unique())
    print(df['HYVITIS'].unique())
    print(df['O_LIIK'].unique())
    print(df['O_TYYP'].unique())
    print(df['RASKUSASTE'].unique())

def make_table_ekspertiis_toos_avgtime(df):
    print('Ekspertiisid töös')
    filter = (df['S_OLEK'] == 'Töös') & \
            (df['O_TYYP'] != 'Läbi vaatamata jätmise otsus')

    df_filter = df[filter]
    print(df_filter.shape, 'menetlusi:', len(df_filter.MEN_ID.unique()))

    # Kes teevad ekspertiise
    ska_arstid_ekspertiise = [df_filter.mean()['TD_MINUTES'], df_filter.median()['TD_MINUTES']]
    ska_arstid_ekspertiise_vanusgrupiti = pd.pivot_table(
        df_filter,
        values=['TD_MINUTES'],
        columns=['HYVITIS'],
        # index=['MENETLEJA'],
        aggfunc={
            'TD_MINUTES': [np.mean, np.median]
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
    filter = (df['S_OLEK'] == 'Töös') & \
             (df['TD_MINUTES'] <= 120) & \
             (df['O_TYYP'] != 'Läbi vaatamata jätmise otsus')

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
    filter = (df['S_OLEK'] == 'Töös') & \
            (df['O_TYYP'] != 'Läbi vaatamata jätmise otsus')

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
    filter = (df['S_OLEK'] == 'Töös') & \
            (df['O_TYYP'] != 'Läbi vaatamata jätmise otsus')

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
    filter = (df['S_OLEK'] == 'Töös') & \
            (df['TD_MINUTES'] <= 120) & \
            (df['O_TYYP'] != 'Läbi vaatamata jätmise otsus')

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
    filter = (df['S_OLEK'] == 'Töös') & \
            (df['TD_MINUTES'] <= 120) & \
            (df['O_TYYP'] != 'Läbi vaatamata jätmise otsus')

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
    filter = (df['S_OLEK'] == 'Töös') & \
            (df['TD_MINUTES'] > 120) & \
            (df['O_TYYP'] != 'Läbi vaatamata jätmise otsus')

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
    filter = (df['S_OLEK'] == 'Töös') & \
            (df['TD_MINUTES'] > 120) & \
            (df['O_TYYP'] != 'Läbi vaatamata jätmise otsus')

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
    filter = (df['S_OLEK'] == 'Alustamata') & \
            (df['O_TYYP'] != 'Läbi vaatamata jätmise otsus')

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
    filter = (df['S_OLEK'] == 'Töös') & \
            (df['O_TYYP'] != 'Läbi vaatamata jätmise otsus')

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


if __name__ == "__main__":
    print('start', datetime.now())
    salvestamiseks = dict()
    # Loeme andmed
    df = read_excel2df()
    show_unique(df)

    # Algses andmesetis menetlusi
    menetlused = df['MEN_ID'].unique()
    print('Menetlusi:', len(menetlused))

    result = make_table_ekspertiis_toos_avgtime(df)
    salvestamiseks['Töös ajakulu keskmine'] = result

    result = make_table_ekspertiis_toos_lte_120minutes_all_avgtime(df)
    salvestamiseks['Töös kuni 120min keskmine'] = result

    result = make_table_ekspertiis_toos_avgtime_ekspertarstid(df)
    salvestamiseks['Töös ajakulu EAd'] = result

    result = make_table_ekspertiis_toos_count_ekspertarstid(df)
    salvestamiseks['Töös kordi EAd'] = result

    result = make_table_ekspertiis_toos_lte_120minutes_avgtime(df)
    salvestamiseks['Töös kuni 120min aeg'] = result

    result = make_table_ekspertiis_toos_lte_120minutes_count(df)
    salvestamiseks['Töös kuni 120min kordi'] = result

    result = make_table_ekspertiis_toos_gt_120minutes_avgtime(df)
    salvestamiseks['Töös pikem 120min aeg'] = result

    result = make_table_ekspertiis_toos_gt_120minutes_count(df)
    salvestamiseks['Töös pikem 120min kordi'] = result

    result = make_table_ekspertiis_alustamata_avgtime(df)
    salvestamiseks['Alustamata olekus'] = result

    result = make_table_ekspertiis_toos_timeperiods_count(df)
    salvestamiseks['Töö ajakulu järgi'] = result

    # Arstide koond
    # result = make_table_arstid(df_result)
    # salvestamiseks['Arstid'] = result

    # Arstide ajakulu
    # result = make_table_arstid_keskmine_aeg(df_result)
    # salvestamiseks['Arstid aeg'] = result

    # Menetlusaja koond
    # result = make_table_menetlusajad_koond(df_result)
    # salvestamiseks['Menetlusajad'] = result

    # Menetlusaja koond TÖE
    # result = make_table_ekspertiisid_toe(df_result)
    # salvestamiseks['Eksp TÖE'] = result

    # Menetlusaja koond TÖE
    # result = make_table_ekspertiisid_toe_tvhotsus(df_result)
    # salvestamiseks['Eksp TÖE TVH otsus'] = result

    # Menetlusaja koond TÖE
    # result = make_table_ekspertiisid_toe_tvvalistav(df_result)
    # salvestamiseks['Eksp TÖE TV väl'] = result

    # TVH vs PRT
    # result = make_table_tvh_vs_prt(df_result)
    # salvestamiseks['TVH vs PRT'] = result

    # Salvestame tulemused
    save(salvestamiseks)
    print('stopp', datetime.now())


