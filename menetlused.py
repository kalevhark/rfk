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

def read_excel2df():
    try:
        with open(DATA_DIR / 'puuded_menetlussammud_26012022.pickle', 'rb') as f:
            df = pickle.load(f)
    except:
        with open(DATA_DIR / 'puuded_menetlussammud_26012022.xlsx', 'rb') as file:
            df = pd.read_excel(
                file,
                parse_dates=[1, 2, 8, 9],
            )
        print(df.shape, '->', end=' ')
        # df.drop_duplicates(inplace=True)
        df.replace({pd.NaT: ''}, inplace=True)
        print(df.shape)
        df.sort_values(['MEN_ID', 'SAMM_ALATES_AEG'], inplace=True)
        with open(DATA_DIR / 'puuded_menetlussammud_26012022.pickle', 'wb') as f:
            pickle.dump(df, f, pickle.HIGHEST_PROTOCOL)
    return df

def filter_lopetatud_menetlused(df):
    # Jätame ainult 2021 lõpetatud tööd
    filter = (df['S_OLEK'] == 'Lõpetatud') & (df['MENETLUS_LOPP_KPV'].dt.year == 2021)
    df_filter = df[filter]
    return df_filter

def get_hours(timedelta):
    days = timedelta.days
    seconds = timedelta.seconds
    return days * 24 + int(seconds / 3600)

def get_koond_df(df):
    try:
        with open(DATA_DIR / 'puuded_menetlussammud_26012022_computed.pickle', 'rb') as f:
            df_result = pickle.load(f)
    except:
        # sorteerime välja pos või neg otsusega TÖE menetlused
        df_filter = df[
            (df['O_TYYP'] != 'Läbi vaatamata jätmise otsus')
        ]
        menetlused = df_filter['MEN_ID'].unique()
        print('Menetlusi:', len(menetlused))

        data = dict()

        n = 0
        for menetlus in menetlused:
            n += 1
            if n % 5000 == 0:
                print(n)
            df_menetlus = df[df['MEN_ID'] == menetlus]
            menetlusandmed = df_menetlus.iloc[0]
            menetlus_algus_kpv = menetlusandmed.MENETLUS_ALGUS_KPV
            menetlus_lopp_kpv = menetlusandmed.MENETLUS_LOPP_KPV
            menetlus_hyvitis = menetlusandmed.HYVITIS
            menetlus_raskusaste = menetlusandmed.RASKUSASTE

            menetlejad = df_menetlus[df_menetlus['MEN_OLEK'] == 'Menetlus']['MENETLEJA'].unique()
            arstid = df_menetlus[df_menetlus['MEN_OLEK'] == 'Arstlik ekspertiis SKA']['MENETLEJA'].unique()
            otsused = df_menetlus[df_menetlus['MEN_OLEK'] == 'Otsuse koostamine']['OTSUS_NR'].unique()
            sammud = set(df_menetlus['MEN_OLEK'].unique())

            # taotluse esitamine
            filter = df_menetlus['MEN_OLEK'] == 'Taotluse esitamine'
            try:
                taotlus_alates_aeg = df_menetlus[filter].iloc[0].SAMM_ALATES_AEG
            except:
                print(menetlus)
                break

            # TVH
            filter = df_menetlus['MEN_OLEK'] == 'Töövõime hindamine TK'
            filter_set = df_menetlus[filter]
            if filter_set.empty:
                tvh_kuni_aeg = ''
                tvh_otsus = ''
            else:
                tvh_kuni_aeg = filter_set.iloc[0].SAMM_KUNI_AEG
                tvh_otsus = filter_set.iloc[0].TVH

            # SKA ekspertiis
            filter = df_menetlus['MEN_OLEK'] == 'Arstlik ekspertiis SKA'
            filter_set = df_menetlus[filter]
            if filter_set.empty:
                arstlik_ekspertiis_ska_alates_aeg = ''
                arstlik_ekspertiis_ska_kuni_aeg = ''
                arstlik_ekspertiis_ska_arst = ''
                tv_valistav_seisund = ''
            else: # v6tame viimase arsti
                arstlik_ekspertiis_ska_alates_aeg = filter_set.iloc[-1].SAMM_ALATES_AEG
                arstlik_ekspertiis_ska_kuni_aeg = filter_set.iloc[-1].SAMM_KUNI_AEG
                arstlik_ekspertiis_ska_arst = filter_set.iloc[-1].MENETLEJA
                tv_valistav_seisund = filter_set.iloc[-1].TV_VALISTAV_SEISUND

            # Menetlused
            filter = df_menetlus['MEN_OLEK'] == 'Menetlus'
            filter_set = df_menetlus[filter]

            # Nullmenetlus - kelle töölaualt ja millal alustatakse
            menetlus_null_alates_aeg = filter_set.iloc[0].SAMM_ALATES_AEG
            menetlus_null_kuni_aeg = filter_set.iloc[0].SAMM_KUNI_AEG
            menetlus_null_menetleja = filter_set.iloc[0].MENETLEJA

            # Järelmenetlus - kes ja millal teeb otsuse
            menetlus_jarel_kuni_aeg = filter_set.iloc[-1].SAMM_KUNI_AEG
            menetlus_jarel_alates_aeg = filter_set.iloc[-1].SAMM_ALATES_AEG
            menetlus_jarel_menetleja = filter_set.iloc[-1].MENETLEJA

            # Eelmenetlus - kes valmistab ette ekspertiisiks
            if arstlik_ekspertiis_ska_alates_aeg:
                filter = (
                        (df_menetlus['MEN_OLEK'] == 'Menetlus') &
                        (df_menetlus['SAMM_ALATES_AEG'] <= arstlik_ekspertiis_ska_alates_aeg)
                )
                filter_set = df_menetlus[filter]
                try:
                    menetlus_eel_alates_aeg = filter_set.iloc[-1].SAMM_ALATES_AEG
                    menetlus_eel_kuni_aeg = filter_set.iloc[-1].SAMM_KUNI_AEG
                    menetlus_eel_menetleja = filter_set.iloc[-1].MENETLEJA
                except:
                    print(menetlus)
                    break
            else:
                menetlus_eel_alates_aeg = ''
                menetlus_eel_kuni_aeg = ''
                menetlus_eel_menetleja = ''

            # otsuse koostamine
            filter = df_menetlus['MEN_OLEK'] == 'Otsuse koostamine'
            otsus_kuni_aeg = df_menetlus[filter].iloc[0].SAMM_KUNI_AEG

            # print(
            #     menetlus,
            #     menetlus_algus_kpv,
            #     'T', taotluse_esitamine,
            #     'M0', menetlus_null_alates_aeg, menetlus_null_menetleja,
            #     'TVH', toovoime_hindamine_tk,
            #     'M1', menetlus_eel_kuni_aeg, menetlus_eel_menetleja,
            #     'EA', arstlik_ekspertiis_ska_kuni_aeg if arstlik_ekspertiis_ska_kuni_aeg == pd.NaT else menetlus_jarel_alates_aeg, arstlik_ekspertiis_ska_arst,
            #     'M2', menetlus_jarel_kuni_aeg, menetlus_jarel_menetleja,
            #     'O', otsuse_koostamine,
            #     menetlus_lopp_kpv,
            #     menetlejad,
            #     arstid
            # )
            toolauale_tuli = get_hours(menetlus_null_alates_aeg - menetlus_algus_kpv)
            tvh_saabus = get_hours(tvh_kuni_aeg - menetlus_algus_kpv) if tvh_kuni_aeg else None
            arstile = get_hours(arstlik_ekspertiis_ska_alates_aeg - menetlus_algus_kpv) if arstlik_ekspertiis_ska_alates_aeg else None
            arstilt = get_hours(arstlik_ekspertiis_ska_kuni_aeg - menetlus_algus_kpv) if arstlik_ekspertiis_ska_kuni_aeg else None
            otsus_valmis = get_hours(otsus_kuni_aeg - menetlus_algus_kpv)
            tk_aeg = tvh_saabus if tvh_kuni_aeg else 0
            ska_arsti_aeg = (arstilt - arstile) if arstilt else 0
            ska_menetlus_aeg = otsus_valmis - ska_arsti_aeg - tk_aeg

            data[menetlus] = [
                menetlus,
                menetlus_hyvitis,
                menetlus_algus_kpv,
                taotlus_alates_aeg,
                menetlus_null_alates_aeg,
                menetlus_null_menetleja,
                tvh_kuni_aeg,
                tvh_otsus,
                tv_valistav_seisund,
                menetlus_eel_kuni_aeg,
                menetlus_eel_menetleja,
                arstlik_ekspertiis_ska_alates_aeg,
                arstlik_ekspertiis_ska_kuni_aeg,
                arstlik_ekspertiis_ska_arst,
                menetlus_raskusaste,
                menetlus_jarel_kuni_aeg,
                menetlus_jarel_menetleja,
                otsus_kuni_aeg,
                menetlus_lopp_kpv,
                ';'.join(menetlejad),
                ';'.join(arstid),
                ';'.join(otsused),
                ';'.join(sammud),
                toolauale_tuli,
                tvh_saabus,
                arstile,
                arstilt,
                otsus_valmis,
                tk_aeg,
                ska_menetlus_aeg,
                ska_arsti_aeg
            ]

        columns = [
            'MEN_ID',
            'HYVITIS',
            'MENETLUS_ALGUS_KPV',
            'TAOTLUS_ALGUS_AEG',
            'M0_ALATES_AEG',
            'M0_MENETLEJA',
            'TVH_KUNI_AEG',
            'TVH_OTSUS',
            'TV_VALISTAV_SEISUND',
            'M1_KUNI_AEG',
            'M1_MENETLEJA',
            'PRT_ALATES_AEG',
            'PRT_KUNI_AEG',
            'PRT_EA',
            'PRT_RASKUSASTE',
            'M2_KUNI_AEG',
            'M2_MENETLEJA',
            'OTSUS_KUNI_AEG',
            'MENETLUS_LOPP_KPV',
            'MENETLEJAD',
            'ARSTID',
            'OTSUSED',
            'SAMMUD',
            'TOOLAUALE_TULI',
            'TVH_SAABUS',
            'ARSTILE',
            'ARSTILT',
            'OTSUS_VALMIS',
            'TK_AEG',
            'SKA_MENETLUS_AEG',
            'SKA_ARSTI_AEG'
        ]
        df_result = pd.DataFrame.from_dict(
            data,
            orient='index',
            columns=columns
        )
        print(df_result.shape)
        with open(DATA_DIR / 'puuded_menetlussammud_26012022_computed.pickle', 'wb') as f:
            pickle.dump(df_result, f, pickle.HIGHEST_PROTOCOL)

    return df_result

def save(salvestamiseks):
    # df_result.to_csv(DATA_DIR / 'output.csv')
    with pd.ExcelWriter(DATA_DIR / 'puuded_menetlussammud_26012022_computed.xlsx') as writer:
        for salvestis in salvestamiseks.keys():
            salvestamiseks[salvestis].to_excel(writer, sheet_name=salvestis)
            # salvestamiseks[salvestis].to_csv(DATA_DIR / f'{salvestis}.csv')

def show_unique(df):
    print(df.shape, df.columns, df.head())
    # for col in df.columns:
    #     print(col, len(df[col].unique()))
    print(df['MENETLEJA'].unique())
    print('MEN_OLEK', df['MEN_OLEK'].unique())
    print(df['S_OLEK'].unique())
    print(df['TV_VALISTAV_SEISUND'].unique())
    print(df['HYVITIS'].unique())
    print(df['O_LIIK'].unique())
    print(df['O_TYYP'].unique())
    print(df['RASKUSASTE'].unique())
    print(df['TVH_OTSUS'].unique())

# Menetlejate koond
def make_table_menetlejad(df_result):
    # Kelle töölauale saabuvad tööd
    m0_menetlejad_null = df_result.groupby(['M0_MENETLEJA']).count()['MEN_ID'].sort_values(ascending=False)
    # Kes teevad otsuseid
    m2_menetlejad_otsus = df_result.groupby(['M2_MENETLEJA']).count()['MEN_ID'].sort_values(ascending=False)
    # Vanusgruppide j2rgi
    m2_menetlejad_otsus_vanusgrupiti = pd.pivot_table(
        df_result,
        values=['MEN_ID'],
        columns=['HYVITIS'],
        index=['M2_MENETLEJA'],
        aggfunc={'MEN_ID': 'count'}
    )
    m2_menetlejad_otsus_vanusgrupiti.columns = [
        'LA',
        'VPI',
        'TÖE'
    ]
    frame = {
        'Taotlusi': m0_menetlejad_null,
        'Otsuseid': m2_menetlejad_otsus,
        'LA': m2_menetlejad_otsus_vanusgrupiti['LA'],
        'TÖE': m2_menetlejad_otsus_vanusgrupiti['TÖE'],
        'VPI': m2_menetlejad_otsus_vanusgrupiti['VPI'],
    }
    result = pd.DataFrame(frame).fillna(0).astype('int32').sort_values(['Otsuseid'], ascending=False)
    return result

# Teeme arstide koondi
def make_table_arstid(df_result):
    # Kes teevad ekspertiise
    ska_arstid_ekspertiise = df_result.groupby(['PRT_EA']).count()['MEN_ID'].sort_values(ascending=False)
    ska_arstid_ekspertiise_vanusgrupiti = pd.pivot_table(
        df_result,
        values=['MEN_ID'],
        columns=['HYVITIS'],
        index=['PRT_EA'],
        aggfunc={'MEN_ID': 'count'}
    )
    ska_arstid_ekspertiise_vanusgrupiti.columns = [
        'LA',
        'VPI',
        'TÖE'
    ]
    frame = {
        'Ekspertiise': ska_arstid_ekspertiise,
        'LA': ska_arstid_ekspertiise_vanusgrupiti['LA'],
        'TÖE': ska_arstid_ekspertiise_vanusgrupiti['TÖE'],
        'VPI': ska_arstid_ekspertiise_vanusgrupiti['VPI'],
    }
    result = pd.DataFrame(frame).fillna(0).astype('int32').sort_values(['Ekspertiise'], ascending=False)
    return result

# Teeme arstide koondi
def make_table_arstid_keskmine_aeg(df_result):
    # Kes teevad ekspertiise
    ska_arstid_ekspertiise = df_result.groupby(['PRT_EA']).mean()['SKA_ARSTI_AEG'].sort_values(ascending=False)
    ska_arstid_ekspertiise_vanusgrupiti = pd.pivot_table(
        df_result,
        values=['SKA_ARSTI_AEG'],
        columns=['HYVITIS'],
        index=['PRT_EA'],
        aggfunc={'SKA_ARSTI_AEG': np.mean}
    )
    ska_arstid_ekspertiise_vanusgrupiti.columns = [
        'LA',
        'VPI',
        'TÖE'
    ]
    frame = {
        'Keskmine aeg (h)': ska_arstid_ekspertiise,
        'LA': ska_arstid_ekspertiise_vanusgrupiti['LA'],
        'TÖE': ska_arstid_ekspertiise_vanusgrupiti['TÖE'],
        'VPI': ska_arstid_ekspertiise_vanusgrupiti['VPI'],
    }
    result = pd.DataFrame(frame).fillna(0).astype('int32').sort_values(['Keskmine aeg (h)'], ascending=False)
    # print(result)
    return result

import numpy as np
def make_table_menetlusajad_koond(df_result):
    menetlusajad_vanusgrupiti = pd.pivot_table(
        df_result,
        values=['MEN_ID', 'TK_AEG', 'SKA_MENETLUS_AEG', 'SKA_ARSTI_AEG'],
        # columns=['TV_VALISTAV_SEISUND'],
        index=['HYVITIS'],
        aggfunc={
            'MEN_ID': 'count',
            'TK_AEG': np.mean,
            'SKA_MENETLUS_AEG': np.mean,
            'SKA_ARSTI_AEG': np.mean
        }
    ).round(0)
    return menetlusajad_vanusgrupiti

def ekspertiisid(tk, ska):
    # tk, ska = len(str(tk).strip()), len(str(ska).strip())
    if tk > 0 and ska > 0:
        return 'TK SKA'
    elif tk > 0:
        return 'TK'
    elif ska > 0:
        return 'SKA'
    else:
        return 'None'

def make_table_ekspertiisid_toe(df_result):
    filter_set = df_result[df_result['HYVITIS'] == HYVITIS[1]]
    filter_set['EKSPERTIISID'] = filter_set.apply(
        lambda row : ekspertiisid(row['TK_AEG'], row['SKA_ARSTI_AEG']),
        axis = 1
    )

    menetlusajad_ekspertiisiti = pd.pivot_table(
        filter_set,
        values=['MEN_ID', 'TK_AEG', 'SKA_MENETLUS_AEG', 'SKA_ARSTI_AEG'],
        # columns=['TV_VALISTAV_SEISUND'],
        index=['EKSPERTIISID'],
        aggfunc={
            'MEN_ID': 'count',
            'TK_AEG': np.mean,
            'SKA_MENETLUS_AEG': np.mean,
            'SKA_ARSTI_AEG': np.mean
        }
    ).round(0)
    # print(menetlusajad_ekspertiisiti)
    return menetlusajad_ekspertiisiti

def make_table_ekspertiisid_toe_tvhotsus(df_result):
    filter_set = df_result[df_result['HYVITIS'] == HYVITIS[1]]
    filter_set['EKSPERTIISID'] = filter_set.apply(
        lambda row : ekspertiisid(row['TK_AEG'], row['SKA_ARSTI_AEG']),
        axis = 1
    )

    menetlusajad_ekspertiisiti = pd.pivot_table(
        filter_set,
        values=['MEN_ID', 'TK_AEG', 'SKA_MENETLUS_AEG', 'SKA_ARSTI_AEG'],
        # columns=['TV_VALISTAV_SEISUND'],
        index=['EKSPERTIISID', 'TVH_OTSUS'],
        aggfunc={
            'MEN_ID': 'count',
            'TK_AEG': np.mean,
            'SKA_MENETLUS_AEG': np.mean,
            'SKA_ARSTI_AEG': np.mean
        }
    ).round(0)
    # print(menetlusajad_ekspertiisiti)
    return menetlusajad_ekspertiisiti

def make_table_ekspertiisid_toe_tvvalistav(df_result):
    filter_set = df_result[df_result['HYVITIS'] == HYVITIS[1]]
    filter_set['EKSPERTIISID'] = filter_set.apply(
        lambda row : ekspertiisid(row['TK_AEG'], row['SKA_ARSTI_AEG']),
        axis = 1
    )

    menetlusajad_ekspertiisiti = pd.pivot_table(
        filter_set,
        values=['MEN_ID', 'TK_AEG', 'SKA_MENETLUS_AEG', 'SKA_ARSTI_AEG'],
        # columns=['TV_VALISTAV_SEISUND'],
        index=['EKSPERTIISID', 'TV_VALISTAV_SEISUND'],
        aggfunc={
            'MEN_ID': 'count',
            'TK_AEG': np.mean,
            'SKA_MENETLUS_AEG': np.mean,
            'SKA_ARSTI_AEG': np.mean
        }
    ).round(0)
    # print(menetlusajad_ekspertiisiti)
    return menetlusajad_ekspertiisiti

# tvhotsus vs prt
def make_table_tvh_vs_prt(df_result):
    filter_set = df_result[df_result['HYVITIS'] == HYVITIS[1]]

    menetlusajad_ekspertiisiti = pd.pivot_table(
        filter_set,
        values=['MEN_ID'],
        columns=['TVH_OTSUS'],
        index=['PRT_RASKUSASTE'],
        aggfunc='count'
    ).fillna(0).astype('int32')
    # print(menetlusajad_ekspertiisiti)
    return menetlusajad_ekspertiisiti


if __name__ == "__main__":
    print('start', datetime.now())
    salvestamiseks = dict()
    # Loeme andmed
    df = read_excel2df()
    # Filtreerime l6petatud ja 2021 aasta
    df = filter_lopetatud_menetlused(df)

    # Koondame menetluse yhele reale
    df_result = get_koond_df(df)
    salvestamiseks['Koond'] = df_result
    # print(df_result['SAMMUD'].unique())
    # Menetlejate koond
    result = make_table_menetlejad(df_result)
    salvestamiseks['Menetlejad'] = result

    # Arstide koond
    result = make_table_arstid(df_result)
    salvestamiseks['Arstid'] = result

    # Arstide ajakulu
    result = make_table_arstid_keskmine_aeg(df_result)
    salvestamiseks['Arstid aeg'] = result

    # Menetlusaja koond
    result = make_table_menetlusajad_koond(df_result)
    salvestamiseks['Menetlusajad'] = result

    # Menetlusaja koond TÖE
    result = make_table_ekspertiisid_toe(df_result)
    salvestamiseks['Eksp TÖE'] = result

    # Menetlusaja koond TÖE
    result = make_table_ekspertiisid_toe_tvhotsus(df_result)
    salvestamiseks['Eksp TÖE TVH otsus'] = result

    # Menetlusaja koond TÖE
    result = make_table_ekspertiisid_toe_tvvalistav(df_result)
    salvestamiseks['Eksp TÖE TV väl'] = result

    # TVH vs PRT
    result = make_table_tvh_vs_prt(df_result)
    salvestamiseks['TVH vs PRT'] = result

    # Salvestame tulemused
    save(salvestamiseks)
    print('stopp', datetime.now())


