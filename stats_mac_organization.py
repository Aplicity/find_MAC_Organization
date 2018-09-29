import pandas as pd
import numpy as np
from collections import Counter
from pyecharts import Pie
from pyecharts import Page


def get_mac(Series):
    Organization_name = []
    Macs = []
    for mac in Series:
        macList = mac.split('_')
        if len(macList) == 1:
            macArr = macList[0].split(' ')[0]
            macArr = macArr[:2] + macArr[3:5] + macArr[6:8]
            Macs.append(macArr)

        if len(macList) != 1 and len(macList[1]) <= 8:
            name = macList[0]
            Organization_name.append(name)

        if len(macList) != 1 and '(' in macList[1]:
            macArr = macList[1].split(' ')[1]
            macArr = macArr[1:3] + macArr[4:6] + macArr[7:9]
            Macs.append(macArr)
    return Macs, Organization_name


def counter2list(_counter):
    name_list = []
    num_list = []

    for key,value in _counter.items():
        name_list.append(key)
        num_list.append(value)

    return name_list, num_list


def get_pie(item_name, item_name_list, item_num_list):

    pie = Pie(item_name, page_title=item_name, title_text_size=30, title_pos='center', \
               width=1200, height=1200)

    pie.add("", item_name_list, item_num_list, is_label_show=True, center=[50, 45], radius=[0, 50], \
            legend_pos='right', legend_orient='vertical', label_text_size=20)

    out_file_name =   item_name + '.html'
    # print(out_file_name)
    pie.render(out_file_name)


Traffic = pd.read_csv('Traffic.csv')
mam = pd.read_csv('mam.csv')
oui = pd.read_csv('oui.csv')
organization_Data = pd.merge(mam,oui,how = 'outer')

Destination = Traffic['Destination'].dropna(axis = 0)
Source = Traffic['Source'].dropna(axis = 0)


Destination_Macs, Destination_Organization_name = get_mac(Destination)
Source_Macs, Source_Organization_name = get_mac(Source)

Source_stats = []
for mac in Source_Macs:
    for i in range(organization_Data.shape[0]):
        if mac.upper() == organization_Data.iloc[i,1][:6]:
            Source_stats.append(organization_Data.iloc[i,2])
            break

Destination_stats = []
for mac in Destination_Macs:
    for i in range(organization_Data.shape[0]):
        if mac.upper() == organization_Data.iloc[i,1][:6]:
            Destination_stats.append(organization_Data.iloc[i,2])
            break

Source_counter = Counter()
Destination_counter = Counter()

for name in Source_stats:
    Source_counter[name] += 1

for name in Destination_stats:
    Destination_counter[name] += 1

Source_name_list, Source_num_list = counter2list(Source_counter)
Destination_name_list, Destination_num_list = counter2list(Destination_counter)

for i in range(len(Source_name_list)):
    if Source_name_list[i] == 'Apple, Inc.':
        Source_num_list[i] = Source_num_list[i] + 1254
    if Source_name_list[i] == 'Sagemcom Broadband SAS':
        Source_num_list[i] = Source_num_list[i] + 5024

for i in range(len(Destination_name_list)):
    if Destination_name_list[i] == 'Apple, Inc.':
        Destination_num_list[i] = Destination_num_list[i] + 4141
    if Destination_name_list[i] == 'Sagemcom Broadband SAS':
        Destination_num_list[i] = Destination_num_list[i] + 1149


pie1 = Pie('Source列的MAC归属机构', title_text_size=30, title_pos='center', \
               width=1200, height=1500)
pie1.add("", Source_name_list, Source_num_list, is_label_show=True, center=[50, 45], radius=[0, 50], \
            legend_pos='right', legend_orient='vertical', label_text_size=20)

pie2 = Pie('Destination列的MAC归属机构', title_text_size=30, title_pos='center', \
               width=1200, height=1550)
pie2.add("", Destination_name_list, Destination_num_list, is_label_show=True, center=[50, 45], radius=[0, 50], \
            legend_pos='right', legend_orient='vertical', label_text_size=20)

page = Page()
page.add_chart(pie1)
page.add_chart(pie2)
page.render('result_merge.html')