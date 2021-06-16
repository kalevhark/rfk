from collections import Counter, deque
import csv
import math
import re

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from pyhtml import *

RFK_REGEX = r"[bdes](?:\d{3,}\.\d+)"
STATIC_DIR = settings.BASE_DIR / 'main' / 'static' / 'main'
SCRORE_CLASSES = ['', 'w3-pale-yellow', 'w3-yellow', 'w3-pale-red', 'w3-red']
#
# Kooditabelite import ja töötlus
#

class ICF_Eng():
    # Loeb ICF kooditabeli sõnastikuks:
    # keys = code
    # element.keys:
    # 'version',
    # 'Dimension', 'Chapter',
    # 'Block', 'SecondLevel', 'ThirdLevel', 'FourthLevel', 'levelno',
    # 'code', 'parent', 'mlsort', 'leafnode',
    # 'Title', 'Description', 'Inclusions', 'Exclusions', 'selected',
    # 'Translated_title', 'Translated_description', 'Translated_inclusions', 'Translated_exclusions']

    def __init__(self):
        self.df = dict()
        with open(STATIC_DIR / 'icf2017_eng_v20210601.csv', newline='', encoding='windows-1252') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
            n = 0
            for row in reader:
                self.df[row['code']] = row
                n += 1
        print(n, len(self.df))



class ICF_Est():

    def __init__(self):
        self.df = dict()
        with open(STATIC_DIR / 'icf2017_est_v20210513.csv', newline='', encoding='windows-1252') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
            n = 0
            for row in reader:
                if row['Kood']:
                    self.df[row['Kood']] = row
                    n += 1
        print(n, len(self.df))

def icf_add_translations(icf_eng_set, icf_est_set):
    # Lisame eestikeelsed tõlked
    for key in icf_est_set.keys():
        try:
            _ = icf_eng_set[key]
        except:
            # print(key)
            continue
        icf_eng_set[key]['Translated_title'] = icf_est_set[key]['Kirjeldus']
        icf_eng_set[key]['Translated_description'] = icf_est_set[key]['Selgitus']
        icf_eng_set[key]['Translated_inclusions'] = icf_est_set[key]['KA']
        icf_eng_set[key]['Translated_exclusions'] = icf_est_set[key]['VA']
    # Kontrollime settide sisalduvust
    print('Missing EST: ', end='')
    n = ''
    for key in icf_eng_set.keys():
        if key not in icf_est_set.keys():
            # print(key)
            n += key[0]
    print(Counter(n))
    print('Missing ENG: ', end='')
    n = ''
    for key in icf_est_set.keys():
        if key not in icf_eng_set.keys():
            # print(key)
            n += key[0]
    print(Counter(n))
    return icf_eng_set

icf_eng = ICF_Eng().df
icf_est = ICF_Est().df
icf_eng = icf_add_translations(icf_eng, icf_est)

def get_icf_group(code):
    # Tagastab valitud koodi koodigrupi vahemiku d4105 -> d410-d429
    codestr = code[:4]
    while int(icf_eng[codestr]['levelno']) > 3 and icf_eng[codestr]['parent']:
        codestr = icf_eng[codestr]['parent']
    # print(code, codestr, icf_eng[codestr]['Translated_title'])
    return codestr

def get_rfk_title(code):
    if code[0] in icf_eng.keys():
        try:
            return icf_eng[code]['Translated_title']
        except KeyError: # ilmselt osaline kood nt b23
            return ''
    else:
        return 'Täpsustamata'

def get_icf_path(request=None, code=None):
    if request:
        code = request.GET.get('code', '')
    codestr = f'{code} {get_rfk_title(code)}'
    if code[0] in icf_eng.keys():
        try:
            parent = icf_eng[code]['parent']
            while parent:
                codestr = '->'.join([codestr, f'{parent} {get_rfk_title(parent)}'])
                parent = icf_eng[parent]['parent']
        except KeyError: # ilmselt osaline kood nt b23
            codestr = ''
    else:
        codestr = 'Täpsustamata'
    if request:
        return JsonResponse(
            {
                'rfkPath': codestr,
            },
            safe=False
        )
    else:
        return codestr

#
# Vaated
#

def index(request):
    return render(
        request,
        'main/index.html',
        {}
    )

# Loeb textareast kõik RFK koodid koos määrajatega listi ja eraldab komponentideks
def read_content_to_rfk(icf_eng_set, content):
    data = re.findall(RFK_REGEX, content)
    codeset = dict()
    for el in data:
        code = el.strip().split('.')
        if code[0] in icf_eng_set.keys():
            if code[1][0] in ['0', '1', '2', '3', '4']:
                codeset[code[0]] = (
                    code[0][:2], # 1. taseme kood d4
                    code[0][:4], # 2. taseme kood d410
                    get_icf_group(code[0][:4]), # koodigrupp nt d410-d429
                    int(code[1][0]) # ainult esimene määraja
                    )
            else:
                print('Viga: vale määraja: ', code)
        else:
            print('Viga: pole koodi: ', code)
    return codeset

def make_icf_table(rfk_set):
    trs = []
    for el in rfk_set:
        trs.append(tr(td(f'{el}:{rfk_set[el]}')))
    icf_table_html = table(trs)
    return icf_table_html.render()

def make_icf_matrix(rfk_set, rows=['d'], columns=['b'], ignore=['s', 'e'], level=1):
    parts = dict()
    for code in rfk_set:
        if level == 0 or level == 1:
            part = code[:2] # kahekohaline nt b2
        elif level == 2:
            part = code[:4] # kahekohaline nt b230
        else:
            part = rfk_set[code][2] # koodigrupp nt b230-b239
        if code[0] not in ignore:
            try:
                parts[part] = [
                    parts[part][0] + rfk_set[code][3],
                    parts[part][1] + 1,
                    ' + '.join([f'{code}.{rfk_set[code][3]}', parts[part][2]])
                ]
            except:
                parts[part] = [rfk_set[code][3], 1, f'{code}.{rfk_set[code][3]}']

    if level == 0: # võetakse kõik kahekohalised klassifikaatorikoodid (b1, b2, ..., d1, d2 jne)
        vect_rows = [
            code
            for code
            in icf_eng.keys()
            if (code[0] in rows and len(code) == 2)
        ]
        columns_exist = any((code[0] in columns) for code in rfk_set) # kas on func või strukt koode?
        # columns_exist = True
        if columns_exist:
            vect_columns = [
                code
                for code
                in icf_eng.keys()
                if (code[0] in columns and len(code) == 2)
            ]
        else:
            vect_columns = ['TTa']  # kui func või struct piiranguid pole, siis Täpsustamata (TTa)
    else:
        vect_rows = [
            code_block
            for code_block
            in parts.keys()
            if code_block[0] in rows
            ]
        if vect_rows:
            vect_rows.sort()
        else:
            vect_rows = ['TTa']  # kui tegevus/osalus piiranguid pole, siis Täpsustamata (TTa)

        vect_columns = [
            code_block
            for code_block
            in parts.keys()
            if code_block[0] in columns
            ]
        if vect_columns:
            vect_columns.sort()
        else:
            vect_columns = ['TTa'] # kui func või struct piiranguid pole, siis Täpsustamata (TTa)

    if max(map(len, vect_columns)) > 4:
        column_header_class = 'verticalColumnHeader' # kui veerupealkirjad pikad, siis vertikaalselt
    else:
        column_header_class = 'w3-center'

    header = tr(
        th(''),
        [
            th(
                div(
                    class_=column_header_class,
                    title=get_icf_path(request=None, code=col)
                )(col)
            )
            for col
            in vect_columns
        ]
    )
    trs = []
    for r in vect_rows:
        row = [td(title=get_icf_path(request=None, code=r))(r)]
        for c in vect_columns:
            title = ''
            try:
                score = round(
                    (parts[r][0]/parts[r][1] + parts[c][0]/parts[c][1]) / 2,
                    1
                )
                title = f'({parts[r][2]})/{parts[r][1]} + ({parts[c][2]})/{parts[c][1]} / 2 = {score}'
                score = int(math.ceil(score))
            except:
                if c == 'TTa': # kui func/struct t2psustamata, siis ainult d keskmine
                    try:
                        score = round(
                            parts[r][0] / parts[r][1], 1
                        )
                        title = f'({parts[r][2]})/{parts[r][1]} = {score}'
                        score = int(math.ceil(score))
                    except KeyError:
                        score = ''
                elif r == 'TTa': # kui tegevus/osalus t2psustamata, siis ainult b/s keskmine
                    score = round(
                        parts[c][0] / parts[c][1], 1
                    )
                    title = f'({parts[c][2]})/{parts[c][1]} = {score}'
                    score = int(math.ceil(score))
                else:
                    score = ''
            if score:
                score_class = SCRORE_CLASSES[score]
            else:
                score_class = ''
            el = str(score)

            row.append(td(class_=f"w3-center {score_class}", title=title)(el))
        trs.append(tr(row))
    return table(border="1", class_="w3-table-all w3-small w3-card-4")(header, trs).render()

# Vue küsib siit andmeid valdkondade jaoks
def get_icf_calcs(request):
    content = request.GET.get('content', '')
    rfk_set = read_content_to_rfk(icf_eng, content)
    # icf_table_html = make_icf_table(rfk_set)
    icf_table_matrix_level1 = make_icf_matrix(rfk_set, level=1)
    icf_table_matrix_level2 = make_icf_matrix(rfk_set, level=2)
    icf_table_matrix_level3 = make_icf_matrix(rfk_set, level=3)
    return JsonResponse(
        {
            # 'icf_table_html': icf_table_html,
            'icf_table_matrix_level1': icf_table_matrix_level1,
            'icf_table_matrix_level2': icf_table_matrix_level2,
            'icf_table_matrix_level3': icf_table_matrix_level3,
            'rfk_codeset_count': len(rfk_set.keys())
        },
        safe=False
    )

# Vue küsib siit andmeid kokkuvõtte jaoks
def get_icf_summary(request):
    content = request.GET.get('content', '')
    rfk_set = read_content_to_rfk(icf_eng, content)
    icf_table_html = make_icf_table(rfk_set)
    icf_table_matrix_level0 = make_icf_matrix(rfk_set, level=0)
    icf_table_matrix_level1 = make_icf_matrix(rfk_set, level=1)
    icf_table_matrix_level2 = make_icf_matrix(rfk_set, level=2)
    icf_table_matrix_level3 = make_icf_matrix(rfk_set, level=3)
    return JsonResponse(
        {
            'icf_table_html': icf_table_html,
            'icf_table_matrix_level0': icf_table_matrix_level0,
            'icf_table_matrix_level1': icf_table_matrix_level1,
            'icf_table_matrix_level2': icf_table_matrix_level2,
            'icf_table_matrix_level3': icf_table_matrix_level3,
        },
        safe=False
    )