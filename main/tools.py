import os
from xml.dom import minidom

import pandas as pd

FILE = "Valdkondade loogika ja vaated_LAVA.xlsx"

def add_valdkonnad(root, valdkonnadChild):
    valdkonnad_pd = pd.read_excel(
        FILE, sheet_name='Valdkonnad',
        index_col=None,
        dtype=str
    )
    for n in valdkonnad_pd.index:
        row = valdkonnad_pd.iloc[n]
        valdkondChild = root.createElement('valdkond')
        valdkondChild.setAttribute('nr', row['valdkond_nr'])
        text = root.createTextNode(row['nimetus'])
        valdkondChild.appendChild(text)
        valdkonnadChild.appendChild(valdkondChild)
    return valdkonnadChild

def add_vanusgrupp_muutumatudseisundid(root, vanusrguppChild, row):
    vanusrgupp_muutumatudseisundidChild = root.createElement('muutumatudSeisundid')
    vanusrgupp_muutumatudseisundidChild.setAttribute('kohustuslik', row['on_kohustuslik_muutumatudseisundid'])
    text = root.createTextNode(row['kysimus_muutumatudseisundid'])
    vanusrgupp_muutumatudseisundidChild.appendChild(text)
    vanusrguppChild.appendChild(vanusrgupp_muutumatudseisundidChild)
    return vanusrguppChild

def add_vanusgrupp_v6tmetegevused(root, vanusgruppChild, row):
    vanusrgupp_v6tmetegevusedChild = root.createElement('vanusgrupiV6tmetegevused')
    v6tmetegevused_pd = pd.read_excel(
        FILE, sheet_name='Võtmetegevused',
        index_col=None,
        dtype=str
    )
    for n in v6tmetegevused_pd.index:
        v6tmetegevus = v6tmetegevused_pd.iloc[n]
        if v6tmetegevus['vanusgrupp_id'] == row['vanusgrupp_id']:
            v6tmetegevusChild = root.createElement('v6tmetegevus')
            v6tmetegevusChild.setAttribute('valdkond_nr', v6tmetegevus['valdkond_nr'])
            v6tmetegevusChild.setAttribute('v6tmetegevus_nr', v6tmetegevus['v6tmetegevus_nr'])
            text = root.createTextNode(v6tmetegevus['nimetus'])
            v6tmetegevusChild.appendChild(text)
            vanusrgupp_v6tmetegevusedChild.appendChild(v6tmetegevusChild)
    vanusgruppChild.appendChild(vanusrgupp_v6tmetegevusedChild)
    return vanusgruppChild

def add_vanusgrupp_kysimused(root, vanusgruppChild, row):
    vanusgrupp_skaalakysimusedChild = root.createElement('vanusgrupiKysimused')
    vanusgrupp_skaalakysimusedChild.setAttribute('question', str(row['kysimustik_eeltekst']))
    skaalakysimused_pd = pd.read_excel(
        FILE, sheet_name='Skaalaküsimused',
        index_col=None,
        dtype=str
    )
    for n in skaalakysimused_pd.index:
        skaalakysimus = skaalakysimused_pd.iloc[n]
        if skaalakysimus['vanusgrupp_id'] == row['vanusgrupp_id'] and str(skaalakysimus['nimetus']) != 'nan':
            skaalakysimusChild = root.createElement('kysimus')
            skaalakysimusChild.setAttribute('valdkond_nr', skaalakysimus['valdkond_nr'])
            skaalakysimusChild.setAttribute('v6tmetegevus_nr', skaalakysimus['v6tmetegevus_nr'])
            skaalakysimusChild.setAttribute('rfk_kategooria', skaalakysimus['rfk_kategooria'])
            skaalakysimusChild.setAttribute('kohustuslik', skaalakysimus['on_kohustuslik'])
            text = root.createTextNode(skaalakysimus['nimetus'])
            skaalakysimusChild.appendChild(text)
            vanusgrupp_skaalakysimusedChild.appendChild(skaalakysimusChild)
    vanusgruppChild.appendChild(vanusgrupp_skaalakysimusedChild)
    return vanusgruppChild

def add_vanusgrupp_yldkysimused(root, vanusgruppChild, row):
    vanusgrupp_yldkysimusedChild = root.createElement('vanusgrupiYldKysimused')
    vanusgrupp_yldkysimusedChild.setAttribute('question', '')
    yldkysimused_pd = pd.read_excel(
        FILE, sheet_name='Üldküsimused',
        index_col=None,
        dtype=str
    )
    for n in yldkysimused_pd.index:
        yldkysimus = yldkysimused_pd.iloc[n]
        if yldkysimus['vanusgrupp_id'] == row['vanusgrupp_id']:
            yldkysimusChild = root.createElement('kysimus')
            yldkysimusChild.setAttribute('kohustuslik', yldkysimus['on_kohustuslik'])
            text = root.createTextNode(yldkysimus['nimetus'])
            yldkysimusChild.appendChild(text)
            vanusgrupp_yldkysimusedChild.appendChild(yldkysimusChild)
    vanusgruppChild.appendChild(vanusgrupp_yldkysimusedChild)
    return vanusgruppChild

def add_vanusgrupid(root, vanusgrupidChild):
    vanusgrupid_pd = pd.read_excel(
        FILE, sheet_name='Vanusgrupid',
        index_col=None,
        dtype=str
    )
    for n in vanusgrupid_pd.index:
        row = vanusgrupid_pd.iloc[n]
        vanusgruppChild = root.createElement('vanusgrupp')
        vanusgruppChild.setAttribute('name', row['nimetus'])
        vanusgruppChild.setAttribute('kysimustik', row['on_skaalakysimustik'])
        # Muutumatute seisundite küsimus
        vanusgruppChild = add_vanusgrupp_muutumatudseisundid(root, vanusgruppChild, row)
        # V6tmetegevused
        vanusgruppChild = add_vanusgrupp_v6tmetegevused(root, vanusgruppChild, row)
        #Skaalakysimused
        vanusgruppChild = add_vanusgrupp_kysimused(root, vanusgruppChild, row)
        #Yldkysimused
        vanusgruppChild = add_vanusgrupp_yldkysimused(root, vanusgruppChild, row)
        # Faili lisamise tekst
        vanusgrupp_failitekstChild = root.createElement('vanusgrupiFailiTekst')
        text = root.createTextNode(row['failitekst'])
        vanusgrupp_failitekstChild.appendChild(text)
        vanusgruppChild.appendChild(vanusgrupp_failitekstChild)

        vanusgrupidChild.appendChild(vanusgruppChild)
    return vanusgrupidChild

def create_xml_file(versioon='0'):
    root = minidom.Document()

    xml = root.createElement('kysimustik')
    xml.setAttribute('versioon', versioon)
    root.appendChild(xml)

    valdkonnadChild = root.createElement('valdkonnad')
    valdkonnadChild = add_valdkonnad(root, valdkonnadChild)

    vanusgupidChild = root.createElement('vanusgrupid')
    vanusgupidChild = add_vanusgrupid(root, vanusgupidChild)

    xml.appendChild(valdkonnadChild)
    xml.appendChild(vanusgupidChild)

    xml_str = root.toprettyxml(indent="\t", encoding='UTF-8')

    save_path_file = f"kysimustik_v{versioon}.xml"

    with open(save_path_file, "wb") as f:
        f.write(xml_str)

if __name__ == "__main__":
    create_xml_file(versioon='5')