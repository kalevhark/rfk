from collections import Counter
from datetime import date, datetime, timedelta
import json
import os
from pathlib import Path, PurePath
import pickle
from random import random

import numpy as np
import pandas as pd
import xlsxwriter

if __name__ == "__main__":
    import django
    os.environ['DJANGO_SETTINGS_MODULE'] = 'rfk.settings'
    django.setup()

from django.conf import settings

path = settings.BASE_DIR
DATA_DIR = path / 'main' / 'static' / 'main' / 'data'

MENETLEJA_ARST = {
    'TUULI KIENS': {
        'leping': 'TVL', 'koormus': 200,
        'kinni': [(date(2021, 7, 12), date(2021, 7, 25)), (date(2021, 12, 15), date(2021, 12, 31))],
        'menetlused': {}, 'tehtud': {}
    },
    'JULIJA ALEKSANDROVA': {
        'leping': 'TL', 'koormus': 150,
        'kinni': [(date(2021, 5, 10), date(2021, 5, 14)), (date(2021, 6, 14), date(2021, 6, 22)), (date(2021, 8, 23), date(2021, 9, 10)), (date(2021, 11, 15), date(2021, 11, 19))],
        'menetlused': {}, 'tehtud': {}
    },
    'KERSTI PEDAKMÄE': {
        'leping': 'TVL', 'koormus': 200,
        'kinni': [(date(2021, 7, 26), date(2021, 8, 9))],
        'menetlused': {}, 'tehtud': {}
    },
    'REET TALI': {
        'leping': 'TVL', 'koormus': 200,
        'kinni': [(date(2021, 7, 15), date(2021, 7, 30))],
        'menetlused': {}, 'tehtud': {}
    },
    'LAURA MIHKLA': {
        'leping': 'TL', 'koormus': 100,
        'kinni': [(date(2021, 2, 19), date(2021, 2, 26)), (date(2021, 6, 21), date(2021, 7, 9)), (date(2021, 8, 2), date(2021, 8, 26))],
        'menetlused': {}, 'tehtud': {}
    },
    'EVA LEMMING': {
        'leping': 'TVL', 'koormus': 200,
        'kinni': [(date(2021, 6, 30), date(2021, 7, 5)), (date(2021, 8, 23), date(2021, 8, 31)), (date(2021, 11, 4), date(2021, 11, 9))],
        'menetlused': {}, 'tehtud': {}
    },
    'ANDRES MESILA': {
        'leping': 'TVL', 'koormus': 200,
        'kinni': [(date(2021, 5, 10), date(2021, 5, 14)), (date(2021, 5, 31), date(2021, 6, 3)), (date(2021, 7, 1), date(2021, 7, 4)), (date(2021, 7, 12), date(2021, 7, 19))],
        'menetlused': {}, 'tehtud': {}
    },
    'ASTA PÄRLI': {
        'leping': 'TL', 'koormus': 200,
        'kinni': [(date(2021, 2, 22), date(2021, 2, 26)), (date(2021, 6, 3), date(2021, 6, 25)), (date(2021, 7, 26), date(2021, 9, 19)), (date(2021, 12, 21), date(2021, 12, 31))],
        'menetlused': {}, 'tehtud': {}
    },
    'HELENA GRAUBERG': {'leping': 'TVL', 'koormus': 200, 'kinni': [(date(2021, 7, 4), date(2021, 8, 4))], 'menetlused': {}, 'tehtud': {}},
    'IVAR VIPP': {
        'leping': 'TVL', 'koormus': 200,
        'kinni': [(date(2021, 6, 14), date(2021, 6, 29)), (date(2021, 8, 16), date(2021, 8, 30))],
        'menetlused': {}, 'tehtud': {}
    },
    'HELI PENU': {
        'leping': 'TVL', 'koormus': 200,
        'kinni': [(date(2021, 5, 24), date(2021, 5, 28)), (date(2021, 7, 1), date(2021, 7, 16)), (date(2021, 8, 30), date(2021, 9, 3)), (date(2021, 12, 20), date(2021, 12, 31))],
        'menetlused': {}, 'tehtud': {}
    },
    'EVE MÄNNIK': {
        'leping': 'TL', 'koormus': 100,
        'kinni': [(date(2021, 6, 28), date(2021, 7, 11)), (date(2021, 8, 23), date(2021, 9, 12))],
        'menetlused': {}, 'tehtud': {}
    },
    'JUTA RATASSEPP': {'leping': 'TVL', 'koormus': 200, 'kinni': [(date(2021, 7, 20), date(2021, 8, 20))], 'menetlused': {}, 'tehtud': {}},
    # 'KADI KALJULA': {'leping': 'TVL', 'koormus': 100, 'kinni': [(date(2021, 7, 24), date(2021, 8, 24))], 'menetlused': {}},
    'REET MOOR': {
        'leping': 'TVL', 'koormus': 200,
        'kinni': [(date(2021, 8, 9), date(2021, 8, 19))],
        'menetlused': {}, 'tehtud': {}
    },
    'TIINA VARBLANE': {
        'leping': 'TVL', 'koormus': 200,
        'kinni': [(date(2021, 7, 19), date(2021, 8, 6))],
        'menetlused': {}, 'tehtud': {}
    },
    'MERIS TAMMIK': {
        'leping': 'TL', 'koormus': 100,
        'kinni': [(date(2021, 4, 19), date(2021, 4, 25)), (date(2021, 7, 21), date(2021, 8, 10)), (date(2021, 10, 25), date(2021, 10, 31))],
        'menetlused': {}, 'tehtud': {}
    },
    'AUNE TAMM': {
        'leping': 'TL', 'koormus': 100,
        'kinni': [(date(2021, 12, 14), date(2021, 12, 31))],
        'menetlused': {}, 'tehtud': {}
    },
    'PIIBE PAI': {
        'leping': 'TVL', 'koormus': 200,
        'kinni': [(date(2021, 5, 28), date(2021, 6, 3)), (date(2021, 6, 25), date(2021, 6, 30))],
        'menetlused': {}, 'tehtud': {}
    },
    'KADRI KELLAMÄE': {
        'leping': 'TL', 'koormus': 100,
        'kinni': [(date(2021, 1, 18), date(2021, 1, 29)), (date(2021, 9, 6), date(2021, 10, 5))],
        'menetlused': {}, 'tehtud': {}
    },
    'MAIU ELKEN': {
        'leping': 'TL', 'koormus': 200,
        'kinni': [(date(2021, 6, 28), date(2021, 7, 9)), (date(2021, 7, 26), date(2021, 8, 17))],
        'menetlused': {}, 'tehtud': {}
    },
    'MARGOT LIIDEMANN': {'leping': 'TVL', 'koormus': 200, 'kinni': [(date(2021, 8, 25), date(2021, 9, 25))], 'menetlused': {}, 'tehtud': {}},
}

ENNAK = 5 # Mitu päeva enne läheb töölaud kinni

MENETLEJA_SP = [
    'KAIDI OTT', 'VEEVI KÕRGMÄE ', 'HELENA KANGRO', 'ANU IVA',
    'MERIKE RJABOV', 'IRINA KUPINSKAJA ', 'KERSTI TALTS', 'SIRJE LEPIK ',
    'MIRLIAN KASK ', 'ANNELE RANDMAA', 'SIIRI ROSENTHAL',
    'KÜLLI KLEMMER', 'KADRI KANNE ', 'EILI NURMETALO', 'ÜLVE HELSTEIN ',
    'TRIIN HALLIK', 'SIRJE POSKA', 'JANIKA MEIKAR ', 'TIIU OJA',
    'NATALJA MINTŠENKOVA', 'EPP NOOBEL ', 'SIGNE VESKIOJA', 'KAIE MARANDI ',
    'LIANA KINKMAN', 'AILI MÄEMAT', 'ANNEMARI OHERD', 'JANNE LAANES'
]

HYVITIS = {
    'Lapse puude raskusastme tuvastamine': 'LA',
    'Tööealise inimese puude raskusastme tuvastamine': 'TÖE',
    'Pensioniealise inimese puude raskusastme tuvastamine': 'VPI'
}

def timedelta_minutes(algus, l6pp):
    try:
        # ajakulu = l6pp - algus
        return int((l6pp - algus).total_seconds()/60)
    except:
        return -1

def read_excel2df():
    try:
        with open(DATA_DIR / 'ekspertarstid_menetlused_2021_mudel.pickle', 'rb') as f:
            df = pickle.load(f)
    except:
        with open(DATA_DIR / 'ekspertarstid_menetlused_2021.xlsx', 'rb') as file:
            df = pd.read_excel(
                file,
                parse_dates=[1, 2, 8, 9],
            )
        print(df.shape, '->', end=' ')
        df.replace({pd.NaT: ''}, inplace=True)
        df['MENETLEJA'] = df['MENETLEJA'].str.strip()
        df.sort_values(['MEN_ID', 'OLEK_ALGUS_AEG'], inplace=True)

        # Sorteerime menetluste järgi
        menetlused = df['MEN_ID'].unique()
        print('Menetlusi:', len(menetlused))
        data = dict()
        n = 0
        for menetlus in menetlused:
            n += 1
            if n % 5000 == 0:
                print(n)
            df_menetlus = df[df['MEN_ID'] == menetlus]
            menetlusandmed = df_menetlus.iloc[0]
            arst = menetlusandmed.MENETLEJA
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
        df_result.sort_values(['ALGUS'], inplace=True)

        with open(DATA_DIR / 'ekspertarstid_menetlused_2021_mudel.pickle', 'wb') as f:
            pickle.dump(df_result, f, pickle.HIGHEST_PROTOCOL)
        df = df_result

    print(df.shape, df.columns)
    return df

def save(salvestamiseks):
    # writer = pd.ExcelWriter(DATA_DIR / 'pandas_with_rich_strings.xlsx', engine='xlsxwriter')
    # workbook = writer.book
    # bold = workbook.add_format({'bold': True})
    # italic = workbook.add_format({'italic': True})
    # red = workbook.add_format({'color': 'red'})
    # df = pd.DataFrame({
    #     'numCol': [1, 50, 327],
    #     'plainText': ['plain', 'text', 'column'],
    #     'richText': [
    #         ['This is ', bold, 'bold'],
    #         ['This is ', italic, 'italic'],
    #         ['This is ', red, 'red']
    #     ]
    # })
    # df.to_excel(writer, sheet_name='Sheet1', index=False)
    # worksheet = writer.sheets['Sheet1']
    # # you then need to overwite the richtext column with
    # for idx, x in df['richText'].iteritems():
    #     worksheet.write_rich_string(idx + 1, 2, *x)
    # writer.save()

    # df_result.to_csv(DATA_DIR / 'output.csv')
    with pd.ExcelWriter(DATA_DIR / 'ekspertarstid_menetlused_2021_mudel.xlsx', engine='xlsxwriter') as writer:
        for salvestis in salvestamiseks.keys():
            df_tosheet = salvestamiseks[salvestis]['df']
            df_title = salvestamiseks[salvestis]['title']
            df_tosheet.to_excel(writer, sheet_name=salvestis, startcol = 0, startrow = 5)
            worksheet = writer.sheets[salvestis]
            for i in range(len(df_title)):
                worksheet.write_string(i, 0, df_title[i])
            # salvestamiseks[salvestis].to_csv(DATA_DIR / f'{salvestis}.csv')

def make_table_ekspertiis_toos_avgs(df):
    print('Arstide tabel')
    filter = df['MENETLEJA'].isin(MENETLEJA_ARST.keys())
    df_filter = df[filter]
    print(df_filter.shape, 'menetlusi:', len(df_filter.MEN_ID.unique()))

    # Kes teevad ekspertiise aeg (minutid)
    ska_arstid_ekspertiise_aeg = df_filter.groupby(['MENETLEJA']).mean()['TD_MINUTES'].sort_values(ascending=False)
    ska_arstid_ekspertiise_vanusgrupiti_aeg = pd.pivot_table(
        df_filter,
        values=['TD_MINUTES'],
        columns=['HYVITIS'],
        index=['MENETLEJA'],
        aggfunc={'TD_MINUTES': np.mean}
    )
    ska_arstid_ekspertiise_vanusgrupiti_aeg.columns = [
        'LA',
        'VPI',
        'TÖE'
    ]

    # Kes teevad ekspertiise (tykke)
    ska_arstid_ekspertiise_tykke = df_filter.groupby(['MENETLEJA']).count()['TD_MINUTES'].sort_values(ascending=False)
    ska_arstid_ekspertiise_vanusgrupiti_tykke = pd.pivot_table(
        df_filter,
        values=['TD_MINUTES'],
        columns=['HYVITIS'],
        index=['MENETLEJA'],
        aggfunc={'TD_MINUTES': 'count'}
    )
    ska_arstid_ekspertiise_vanusgrupiti_tykke.columns = [
        'LA',
        'VPI',
        'TÖE'
    ]
    frame = {
        'Menetlusi': ska_arstid_ekspertiise_tykke,
        'LA tykke': ska_arstid_ekspertiise_vanusgrupiti_tykke['LA'],
        'TÖE tykke': ska_arstid_ekspertiise_vanusgrupiti_tykke['TÖE'],
        'VPI tykke': ska_arstid_ekspertiise_vanusgrupiti_tykke['VPI'],
        'Keskmine aeg (min)': ska_arstid_ekspertiise_aeg,
        'LA minutit': ska_arstid_ekspertiise_vanusgrupiti_aeg['LA'],
        'TÖE minutit': ska_arstid_ekspertiise_vanusgrupiti_aeg['TÖE'],
        'VPI minutit': ska_arstid_ekspertiise_vanusgrupiti_aeg['VPI'],
        'Keskmine aeg (päevi)': ska_arstid_ekspertiise_aeg / 60 / 24 + 1,
        'LA päevi': ska_arstid_ekspertiise_vanusgrupiti_aeg['LA'] / 60 / 24 + 1,
        'TÖE päevi': ska_arstid_ekspertiise_vanusgrupiti_aeg['TÖE'] / 60 / 24 + 1,
        'VPI päevi': ska_arstid_ekspertiise_vanusgrupiti_aeg['VPI'] / 60 / 24 + 1,
    }
    result = pd.DataFrame(frame).\
        fillna(0).\
        astype('int32').\
        sort_values(['Menetlusi'], ascending=False)

    result['LA lubatud'] = result.apply(
        lambda row: (row['LA tykke'] / row['Menetlusi'] * 100) > 1,
        axis=1
    )
    result['TÖE lubatud'] = result.apply(
        lambda row: (row['TÖE tykke'] / row['Menetlusi'] * 100) > 1,
        axis=1
    )
    result['VPI lubatud'] = result.apply(
        lambda row: (row['VPI tykke'] / row['Menetlusi'] * 100) > 1,
        axis=1
    )

    # print(result)
    return result

def show_arsti_info(arstide_tabel):
    arstid = arstide_tabel.index
    for arst in arstid:
        print(
            arst,
            MENETLEJA_ARST[arst]['leping'],
            arstide_tabel[arstide_tabel.index==arst]['Keskmine aeg (päevi)'].values[0]
        )

def reset_arstide_andmed(MENETLEJA_ARST):
    # j22giga = False
    # try:
    #     with open(DATA_DIR / 'ekspertarstid_menetlused_2021_mudel_aastal6puj22k.pickle', 'rb') as f:
    #         MENETLEJA_ARST = pickle.load(f)
    #     j22giga = True
    # except:
    #     pass
    # print(j22giga)
    # n = 0
    for arst in MENETLEJA_ARST:
    #     print(len(MENETLEJA_ARST[arst]['tehtud']), len(MENETLEJA_ARST[arst]['menetlused']))
        MENETLEJA_ARST[arst]['tehtud'] = {}
        MENETLEJA_ARST[arst]['menetlused'] = {}
    #     if j22giga:
    #         for menetlus in MENETLEJA_ARST[arst]['menetlused']:
    #             MENETLEJA_ARST[arst]['menetlused'][menetlus]['ALGUS'] -= timedelta(days=365)
    #             MENETLEJA_ARST[arst]['menetlused'][menetlus]['ETA'] -= timedelta(days=365)
    #     else:
    #         MENETLEJA_ARST[arst]['menetlused'] = {}
    #     print(len(MENETLEJA_ARST[arst]['tehtud']), len(MENETLEJA_ARST[arst]['menetlused']))
    #     n += len(MENETLEJA_ARST[arst]['menetlused'])
    # print('Töid jäägis:', n)
    return MENETLEJA_ARST

def get_arst(kuup2ev, arstide_tabel, vanusgrupp, valitud_strateegiad):
    pool = MENETLEJA_ARST.copy()
    arstid = [arst for arst in arstide_tabel.index if arst in pool.keys()]
    vanusgrupi_column = f'{HYVITIS[vanusgrupp]} lubatud'

    # S6elume arstid, kelle toolauad lahti, kes teevad vanusgruppi ja kelle toolaual on ruumi
    for arst in arstid:
        # Toolaud kinni?
        if MENETLEJA_ARST[arst]['kinni']:
            for vahemik in MENETLEJA_ARST[arst]['kinni']:
                if (kuup2ev >= (vahemik[0] - timedelta(days=ENNAK))) and (kuup2ev <= vahemik[1]):
                    del pool[arst]
                    break
        # Vanusgrupp lubatud?
        if arst in pool.keys() and not arstide_tabel[arstide_tabel.index == arst][vanusgrupi_column].values[0]:
            del pool[arst]
        # Max kuunorm t2is?
        if arst in pool.keys():
            tehtud_menetlused = [
                menetlus
                for menetlus
                in MENETLEJA_ARST[arst]['tehtud']
                if (kuup2ev - MENETLEJA_ARST[arst]['tehtud'][menetlus]['ETA']).days <= 30
            ]
            if MENETLEJA_ARST[arst]['koormus'] <= len(tehtud_menetlused):
                del pool[arst]
        # Max töölauakoormus t2is?
        if arst in pool.keys():
            if (MENETLEJA_ARST[arst]['koormus'] / 4) <= len(MENETLEJA_ARST[arst]['menetlused']):
                del pool[arst]

    # Teeme arstide j2rjestuse
    valitud_arstid = [
        (arst, pool[arst]['leping'], pool[arst]['koormus'], len(pool[arst]['menetlused']))
        for arst
        in pool
    ]
    strateegiad = [
        lambda arst: arst[1], # lepingu liik
        lambda arst: arst[3] / arst[2], # laual olevad / max koormus
        lambda arst: random(),
        lambda arst: 1,
        lambda arst: -1 * arst[2], # kuukoormus suurimast alates
        lambda arst: arst[3], # laual olevate tööde arv
    ]
    for strateegia in valitud_strateegiad:
        valitud_arstid = sorted(valitud_arstid, key=strateegiad[strateegia])
    # valitud_arstid = sorted(valitud_arstid, key=strateegiad[1])
    # print(kuup2ev, len(valitud_arstid), sum([arst[2] for arst in valitud_arstid]))
    # print(valitud_arstid)
    return valitud_arstid


def shuffle_work(df, arstide_tabel, MENETLEJA_ARST, valitud_strateegiad=(1, 0)):
    """
    :param df:
    :param arstide_tabel:
    :param valitud_strateegiad:
        0 - j2rjestus TL, TVL
        1 - töölaual olevate tööde arv / koormus - asc
        2 - random
        3 - ekpertiisi aeg kõigil fix
        4 - 30 p2eva koormuse kahanevalt
        5 - laual olevate tööde arv kasvavalt
    :return:
    """
    # nulline jooksvate ja tehtud menetluste andmestiku
    MENETLEJA_ARST = reset_arstide_andmed(MENETLEJA_ARST)
    tehtud_lugude_andmed = {}
    kinni = 0 # k6ik lauad kinni
    mudel = { arst : [MENETLEJA_ARST[arst]['koormus']] for arst in arstide_tabel.index } # mudeldus kuup2evade kaupa
    kuup2ev = date(2021, 1, 1)
    testea = 'JULIJA ALEKSANDROVA'

    while kuup2ev < date(2022, 1, 1):
        # kustutame tehtud tööd
        print(kuup2ev, len(MENETLEJA_ARST[testea]['menetlused']), len(MENETLEJA_ARST[testea]['tehtud']), end='->')
        for arst in arstide_tabel.index:
            toos_menetlused = MENETLEJA_ARST[arst]['menetlused'].copy()
            if len(toos_menetlused) > 0:
                for menetlus in toos_menetlused:
                    if MENETLEJA_ARST[arst]['menetlused'][menetlus]['ETA'] <= kuup2ev:
                        MENETLEJA_ARST[arst]['tehtud'][menetlus] = MENETLEJA_ARST[arst]['menetlused'][menetlus]
                        tehtud_lugude_andmed[menetlus] = MENETLEJA_ARST[arst]['menetlused'][menetlus]
                        del MENETLEJA_ARST[arst]['menetlused'][menetlus]
        # lükkame puhkusele minejate tööd teistele
        # puhkuseleminejate_menetlused = {}
        # for arst in arstide_tabel.index:
        #     if MENETLEJA_ARST[arst]['kinni']:
        #         for vahemik in MENETLEJA_ARST[arst]['kinni']:
        #             if kuup2ev == vahemik[0]:
        #                 toos_menetlused = MENETLEJA_ARST[arst]['menetlused'].copy()
        #                 if len(toos_menetlused) > 0:
        #                     # print(toos_menetlused)
        #                     for menetlus in toos_menetlused:
        #                         puhkuseleminejate_menetlused[menetlus] = {
        #                             'MEN_ID': menetlus,
        #                             'ETA': MENETLEJA_ARST[arst]['menetlused'][menetlus]['ETA']
        #                         }
        # puhkuseminejate_tood = df[
        #     df['MEN_ID'].isin(puhkuseleminejate_menetlused.keys())
        # ]
        # otsime uued lood
        tegemata_tood = df[
            (df['ALGUS'].dt.year == kuup2ev.year) & (df['ALGUS'].dt.month == kuup2ev.month) & (df['ALGUS'].dt.day == kuup2ev.day)
            ]
        # uued_tood = pd.concat([puhkuseminejate_tood, tegemata_tood])
        uued_tood = tegemata_tood # puhkuseleminejate töid ei jaota ümber
        toode_arv_p2evas = uued_tood.shape[0]
        # jagame uued tööd
        for i in range(toode_arv_p2evas):
            menetlus = uued_tood.iloc[i]
            vanusgrupp = menetlus['HYVITIS']
            # print(menetlus)
            arst = get_arst(kuup2ev, arstide_tabel, vanusgrupp, valitud_strateegiad)
            if arst: # Kui leiti vaba arst, siis v6tame esimese neist
                vanusgrupi_veerg = HYVITIS[vanusgrupp]
                days = int(arstide_tabel[arstide_tabel.index == arst[0][0]][f'{vanusgrupi_veerg} päevi'].values[0])
                if 3 in valitud_strateegiad:
                    if days > 7:
                        days = 7 # tegelikut peaks olema 5 tööpäeva

                ETA = kuup2ev + timedelta(days=days)

                MENETLEJA_ARST[arst[0][0]]['menetlused'][menetlus['MEN_ID']] = {
                    'MENETLEJA': arst[0][0], # menetlus['MENETLEJA'],
                    'MEN_ID': menetlus['MEN_ID'],
                    'HYVITIS': menetlus['HYVITIS'],
                    'ALGUS': menetlus['ALGUS'],
                    'ETA': ETA
                }
            else: # vaba arsti ei leitud
                print(kuup2ev, 'k6ik kinni')
                kinni += 1
        print(len(MENETLEJA_ARST[testea]['menetlused']), len(MENETLEJA_ARST[testea]['tehtud']))

        # lisame kuup2evarea mudelisse
        for arst in arstide_tabel.index:
            mudel[arst].append(len(MENETLEJA_ARST[arst]['menetlused']))
        kuup2ev += timedelta(days=1)

    # lisame menetluse kestuse aja
    for menetlus in tehtud_lugude_andmed:
        algus = tehtud_lugude_andmed[menetlus]['ALGUS']
        eta = pd.to_datetime(tehtud_lugude_andmed[menetlus]['ETA'])
        menetluse_aeg = (eta - algus).days
        if menetluse_aeg < 0:
            print(tehtud_lugude_andmed[menetlus])
        tehtud_lugude_andmed[menetlus]['KESTUS'] = menetluse_aeg

    menetlus_ajad = [
        tehtud_lugude_andmed[menetlus]['KESTUS']
        for menetlus
        in tehtud_lugude_andmed
    ]
    keskmine_menetlusaeg = sum(menetlus_ajad) / len(menetlus_ajad)
    print('Keskmine menetlusaeg:', sum(menetlus_ajad) / len(menetlus_ajad))
    print('K6ik kinni:', kinni)
    data = {
        'MENETLEJA': [tehtud_lugude_andmed[menetlus]['MENETLEJA'] for menetlus in tehtud_lugude_andmed],
        'HYVITIS': [tehtud_lugude_andmed[menetlus]['HYVITIS'] for menetlus in tehtud_lugude_andmed],
        'ALGUS': [tehtud_lugude_andmed[menetlus]['ALGUS'] for menetlus in tehtud_lugude_andmed],
        'ETA': [tehtud_lugude_andmed[menetlus]['ETA'] for menetlus in tehtud_lugude_andmed],
        'KESTUS': [tehtud_lugude_andmed[menetlus]['KESTUS'] for menetlus in tehtud_lugude_andmed]
    }
    df_result = pd.DataFrame.from_dict(data)
    df_mudel = pd.DataFrame.from_dict(mudel)
    indeks = ['max koormus']
    indeks.extend(pd.date_range(start=date(2021, 1, 1), end=date(2021, 12, 31)))
    df_mudel.index = indeks
    return df_result, df_mudel, keskmine_menetlusaeg, kinni

if __name__ == "__main__":
    print('start', datetime.now())
    salvestamiseks = dict()

    # Loeme andmed
    df = read_excel2df()

    # Algses andmesetis menetlusi
    menetlused = df['MEN_ID'].unique()
    print('Menetlusi:', len(menetlused))

    arstide_tabel = make_table_ekspertiis_toos_avgs(df)
    arstide_tabel['Koormus'] = arstide_tabel.apply(
        lambda x: MENETLEJA_ARST[x.name]['koormus'], axis=1
    )
    arstide_tabel['Leping'] = arstide_tabel.apply(
        lambda x: MENETLEJA_ARST[x.name]['leping'], axis=1
    )

    salvestamiseks['EXP andmestik'] = {
        'df': arstide_tabel,
        'title': ['Ekspertarstide tööde agregeeritud näitajad', '2021. a. menetlusandmete põhjal']
    }

    # show_arsti_info(arstide_tabel)
    # result, mudel, keskmine_menetlusaeg, jaotamata = shuffle_work(df, arstide_tabel, MENETLEJA_ARST, valitud_strateegiad=(1, 0))
    # print([(arst, len(MENETLEJA_ARST[arst]['tehtud'])) for arst in MENETLEJA_ARST])
    # salvestamiseks['Mudel 1'] = {
    #     'df': mudel,
    #     'title': [
    #         'Ekspertarstide tööde jagunemise mudel 1',
    #         '1. TL, 2. TVL',
    #         'Arvestatakse senist keskmist menetlusaega',
    #         'Jagatakse väikseima töölauaseisuga EAle',
    #         f'Keskmine menetlusaeg: {keskmine_menetlusaeg}'
    #     ]
    # }
    #
    # ska_arstid_ekspertiise_vanusgrupiti = pd.pivot_table(
    #     result,
    #     values=['KESTUS'],
    #     columns=['HYVITIS'],
    #     index=['MENETLEJA'],
    #     aggfunc={'KESTUS': np.mean}
    # ).round(1)
    #
    # salvestamiseks['Mudel 1 aeg'] = {
    #     'df': ska_arstid_ekspertiise_vanusgrupiti,
    #     'title': [
    #         'Ekspertarstide tööde jagunemise mudel 1',
    #         '1. TL, 2. TVL',
    #         'Arvestatakse senist keskmist menetlusaega',
    #         'Jagatakse väikseima töölauaseisuga EAle',
    #         f'Keskmine menetlusaeg: {keskmine_menetlusaeg}'
    #     ]
    # }
    #
    # ska_arstid_ekspertiise_vanusgrupiti = pd.pivot_table(
    #     result,
    #     values=['KESTUS'],
    #     columns=['HYVITIS'],
    #     index=['MENETLEJA'],
    #     aggfunc={'MENETLEJA': 'count'}
    # ).round(0)
    # ska_arstid_ekspertiise_vanusgrupiti['Kokku'] = ska_arstid_ekspertiise_vanusgrupiti.sum(axis=1)
    # ska_arstid_ekspertiise_vanusgrupiti['Koormus'] = ska_arstid_ekspertiise_vanusgrupiti.apply(
    #     lambda x: MENETLEJA_ARST[x.name]['koormus'], axis=1
    # )
    # ska_arstid_ekspertiise_vanusgrupiti.sort_values('Kokku', axis=0, ascending=False, inplace=True)
    #
    # salvestamiseks['Mudel 1 kogus'] = {
    #     'df': ska_arstid_ekspertiise_vanusgrupiti,
    #     'title': [
    #         'Ekspertarstide tööde jagunemise mudel 1',
    #         '1. TL, 2. TVL',
    #         'Arvestatakse senist keskmist menetlusaega',
    #         'Jagatakse väikseima töölauaseisuga EAle',
    #         f'Keskmine menetlusaeg: {keskmine_menetlusaeg}'
    #     ]
    # }
    #
    # # Salvestame aastal6puseisu
    # # with open(DATA_DIR / 'ekspertarstid_menetlused_2021_mudel_aastal6puj22k.pickle', 'wb') as f:
    # #     pickle.dump(MENETLEJA_ARST, f, pickle.HIGHEST_PROTOCOL)
    #
    # result, mudel, keskmine_menetlusaeg, jaotamata = shuffle_work(df, arstide_tabel, MENETLEJA_ARST, valitud_strateegiad=(2, 0))
    # print([(arst, len(MENETLEJA_ARST[arst]['tehtud'])) for arst in MENETLEJA_ARST])
    # salvestamiseks['Mudel 2'] = {
    #     'df': mudel,
    #     'title': [
    #         'Ekspertarstide tööde jagunemise mudel 2',
    #         '1. TL, 2. TVL',
    #         'Arvestatakse senist keskmist menetlusaega',
    #         'Jagatakse random',
    #         f'Keskmine menetlusaeg: {keskmine_menetlusaeg}'
    #     ]
    # }
    #
    # ska_arstid_ekspertiise_vanusgrupiti = pd.pivot_table(
    #     result,
    #     values=['KESTUS'],
    #     columns=['HYVITIS'],
    #     index=['MENETLEJA'],
    #     aggfunc={'KESTUS': np.mean}
    # ).round(1)
    # # print(ska_arstid_ekspertiise_vanusgrupiti)
    # salvestamiseks['Mudel 2 aeg'] = {
    #     'df': ska_arstid_ekspertiise_vanusgrupiti,
    #     'title': [
    #         'Ekspertarstide tööde jagunemise mudel 2',
    #         '1. TL, 2. TVL',
    #         'Arvestatakse senist keskmist menetlusaega',
    #         'Jagatakse random',
    #         f'Keskmine menetlusaeg: {keskmine_menetlusaeg}'
    #     ]
    # }
    #
    # ska_arstid_ekspertiise_vanusgrupiti = pd.pivot_table(
    #     result,
    #     values=['KESTUS'],
    #     columns=['HYVITIS'],
    #     index=['MENETLEJA'],
    #     aggfunc={'MENETLEJA': 'count'}
    # ).round(0)
    # ska_arstid_ekspertiise_vanusgrupiti['Kokku'] = ska_arstid_ekspertiise_vanusgrupiti.sum(axis=1)
    # ska_arstid_ekspertiise_vanusgrupiti['Koormus'] = ska_arstid_ekspertiise_vanusgrupiti.apply(
    #     lambda x: MENETLEJA_ARST[x.name]['koormus'], axis=1
    # )
    # ska_arstid_ekspertiise_vanusgrupiti.sort_values('Kokku', axis=0, ascending=False, inplace=True)
    #
    # salvestamiseks['Mudel 2 kogus'] = {
    #     'df': ska_arstid_ekspertiise_vanusgrupiti,
    #     'title': [
    #         'Ekspertarstide tööde jagunemise mudel 2',
    #         '1. TL, 2. TVL',
    #         'Arvestatakse senist keskmist menetlusaega',
    #         'Jagatakse random',
    #         f'Keskmine menetlusaeg: {keskmine_menetlusaeg}'
    #     ]
    # }
    #
    result, mudel, keskmine_menetlusaeg, jaotamata = shuffle_work(df, arstide_tabel, MENETLEJA_ARST, valitud_strateegiad=(2, 4, 0, 3))
    print([(arst, len(MENETLEJA_ARST[arst]['tehtud'])) for arst in MENETLEJA_ARST])
    title = [
        'Ekspertarstide tööde jagunemise mudel 3',
        'Filtrid: töölaud kinni; vanusgrupp; jooksva kuu max koormus; töölaual tööde max arv ',
        'Järjestus: 1. TL, 2. TVL -> jooksva kuu lubatud koormus kahanevalt -> random()',
        'Arvestatakse senist keskmist menetlusaega, aga max 7 päeva',
        f'Jaotamata: {jaotamata}; Keskmine menetlusaeg: {keskmine_menetlusaeg}'
    ]
    salvestamiseks['Mudel 3'] = {
        'df': mudel,
        'title': title
    }

    ska_arstid_ekspertiise_vanusgrupiti = pd.pivot_table(
        result,
        values=['KESTUS'],
        columns=['HYVITIS'],
        index=['MENETLEJA'],
        aggfunc={'KESTUS': np.mean}
    ).round(1)
    # print(ska_arstid_ekspertiise_vanusgrupiti)
    salvestamiseks['Mudel 3 aeg'] = {
        'df': ska_arstid_ekspertiise_vanusgrupiti,
        'title': title
    }

    ska_arstid_ekspertiise_vanusgrupiti = pd.pivot_table(
        result,
        values=['KESTUS'],
        columns=['HYVITIS'],
        index=['MENETLEJA'],
        aggfunc={'MENETLEJA': 'count'}
    ).round(0)
    ska_arstid_ekspertiise_vanusgrupiti['Kokku'] = ska_arstid_ekspertiise_vanusgrupiti.sum(axis=1)
    ska_arstid_ekspertiise_vanusgrupiti['Koormus'] = ska_arstid_ekspertiise_vanusgrupiti.apply(
        lambda x: MENETLEJA_ARST[x.name]['koormus'], axis=1
    )
    ska_arstid_ekspertiise_vanusgrupiti['2021 tegelik'] = ska_arstid_ekspertiise_vanusgrupiti.apply(
        lambda x: arstide_tabel[arstide_tabel.index == x.name]['Menetlusi'].values[0], axis=1
    )
    ska_arstid_ekspertiise_vanusgrupiti.sort_values('Kokku', axis=0, ascending=False, inplace=True)

    salvestamiseks['Mudel 3 kogus'] = {
        'df': ska_arstid_ekspertiise_vanusgrupiti,
        'title': title
    }

    result, mudel, keskmine_menetlusaeg, jaotamata = shuffle_work(df, arstide_tabel, MENETLEJA_ARST, valitud_strateegiad=(2, 4, 0))
    print([(arst, len(MENETLEJA_ARST[arst]['tehtud'])) for arst in MENETLEJA_ARST])
    title = [
        'Ekspertarstide tööde jagunemise mudel 4',
        'Filtrid: töölaud kinni; vanusgrupp; jooksva kuu max koormus; töölaual tööde max arv ',
        'Järjestus: 1. TL, 2. TVL -> jooksva kuu lubatud koormus kahanevalt -> random()',
        'Arvestatakse senist keskmist menetlusaega',
        f'Jaotamata: {jaotamata}; Keskmine menetlusaeg: {keskmine_menetlusaeg}'
    ]
    salvestamiseks['Mudel 4'] = {
        'df': mudel,
        'title': title
    }

    ska_arstid_ekspertiise_vanusgrupiti = pd.pivot_table(
        result,
        values=['KESTUS'],
        columns=['HYVITIS'],
        index=['MENETLEJA'],
        aggfunc={'KESTUS': np.mean}
    ).round(1)
    salvestamiseks['Mudel 4 aeg'] = {
        'df': ska_arstid_ekspertiise_vanusgrupiti,
        'title': title
    }

    ska_arstid_ekspertiise_vanusgrupiti = pd.pivot_table(
        result,
        values=['KESTUS'],
        columns=['HYVITIS'],
        index=['MENETLEJA'],
        aggfunc={'MENETLEJA': 'count'}
    ).round(0)
    ska_arstid_ekspertiise_vanusgrupiti['Kokku'] = ska_arstid_ekspertiise_vanusgrupiti.sum(axis=1)
    ska_arstid_ekspertiise_vanusgrupiti['Koormus'] = ska_arstid_ekspertiise_vanusgrupiti.apply(
        lambda x: MENETLEJA_ARST[x.name]['koormus'], axis=1
    )
    ska_arstid_ekspertiise_vanusgrupiti['2021 tegelik'] = ska_arstid_ekspertiise_vanusgrupiti.apply(
        lambda x: arstide_tabel[arstide_tabel.index==x.name]['Menetlusi'].values[0], axis=1
    )
    ska_arstid_ekspertiise_vanusgrupiti.sort_values('Kokku', axis=0, ascending=False, inplace=True)

    salvestamiseks['Mudel 4 kogus'] = {
        'df': ska_arstid_ekspertiise_vanusgrupiti,
        'title': title
    }

    result, mudel, keskmine_menetlusaeg, jaotamata = shuffle_work(df, arstide_tabel, MENETLEJA_ARST,
                                                                  valitud_strateegiad=(2, 5, 0))
    print([(arst, len(MENETLEJA_ARST[arst]['tehtud'])) for arst in MENETLEJA_ARST])
    title = [
        'Ekspertarstide tööde jagunemise mudel 5',
        'Filtrid: töölaud kinni; vanusgrupp; jooksva kuu max koormus; töölaual tööde max arv ',
        'Järjestus: 1. TL, 2. TVL -> töölaual tööde arv vähimast -> random()',
        'Arvestatakse senist keskmist menetlusaega',
        f'Jaotamata: {jaotamata}; Keskmine menetlusaeg: {keskmine_menetlusaeg}'
    ]
    salvestamiseks['Mudel 5'] = {
        'df': mudel,
        'title': title
    }

    ska_arstid_ekspertiise_vanusgrupiti = pd.pivot_table(
        result,
        values=['KESTUS'],
        columns=['HYVITIS'],
        index=['MENETLEJA'],
        aggfunc={'KESTUS': np.mean}
    ).round(1)
    salvestamiseks['Mudel 5 aeg'] = {
        'df': ska_arstid_ekspertiise_vanusgrupiti,
        'title': title
    }

    ska_arstid_ekspertiise_vanusgrupiti = pd.pivot_table(
        result,
        values=['KESTUS'],
        columns=['HYVITIS'],
        index=['MENETLEJA'],
        aggfunc={'MENETLEJA': 'count'}
    ).round(0)
    ska_arstid_ekspertiise_vanusgrupiti['Kokku'] = ska_arstid_ekspertiise_vanusgrupiti.sum(axis=1)
    ska_arstid_ekspertiise_vanusgrupiti['Koormus'] = ska_arstid_ekspertiise_vanusgrupiti.apply(
        lambda x: MENETLEJA_ARST[x.name]['koormus'], axis=1
    )
    ska_arstid_ekspertiise_vanusgrupiti['2021 tegelik'] = ska_arstid_ekspertiise_vanusgrupiti.apply(
        lambda x: arstide_tabel[arstide_tabel.index == x.name]['Menetlusi'].values[0], axis=1
    )
    ska_arstid_ekspertiise_vanusgrupiti.sort_values('Kokku', axis=0, ascending=False, inplace=True)

    salvestamiseks['Mudel 5 kogus'] = {
        'df': ska_arstid_ekspertiise_vanusgrupiti,
        'title': title
    }

    # Salvestame tulemused
    save(salvestamiseks)
    print('stopp', datetime.now())
