import  csv
from tkinter import *
from ftplib import FTP, FTP_TLS
import os
from datetime import datetime
import pickle
from tkinter.messagebox import *
import helpic_client_factory as helpic

# parser for creating original dictionary
# analize position with price in the text file

#import csv

#with open('text.txt', 'r', encoding='utf-8') as f:
#    data = csv.reader(f)
#    l = []
#    for i in data:
#        i = '.'.join(i)
#        i = i.split('\t')
#        if i[5]:  # !!! the price of item is included in the 'text.txt' !!!
#            l.append(i)
#    print(l)
#    for i in l:
#        t = i[3][:3]
#        print ("['{}', '{}', '{}'],".format(i[1], i[3], t) ) # nomenklatura for dictionary
# dictionary for parsing loading
d_original = {
'00000014290': ['ААИР 122128-03', 'ААИР'],
'00000008656': ['ААИР 123125-01', 'ААИР'],
'00000014309': ['ААИР 123125-02', 'ААИР'],
'00000014311': ['ААИР 123125-03', 'ААИР'],
'00000014313': ['ААИР 123125-04', 'ААИР'],
'00000008653': ['ААИР 123125-05', 'ААИР'],
'00000014329': ['ААИР 123125-07', 'ААИР'],
'00000014331': ['ААИР 123125-08', 'ААИР'],
'00000014315': ['ААИР 123125-09', 'ААИР'],
'00000008655': ['ААИР 123125-10', 'ААИР'],
'00000011101': ['ААИР 123125-11', 'ААИР'],
'00000012492': ['ААИР 123125-12', 'ААИР'],
'00000014300': ['ААИР 123126-00', 'ААИР'],
'00000014303': ['ААИР 123126-02', 'ААИР'],
'00000014305': ['ААИР 123126-03', 'ААИР'],
'00000014307': ['ААИР 123126-04', 'ААИР'],
'00000014327': ['ААИР 123126-05', 'ААИР'],
'00000014325': ['ААИР 123126-06', 'ААИР'],
'00000008652': ['ААИР 123126-07', 'ААИР'],
'00000008651': ['ААИР 123126-08', 'ААИР'],
'00000011104': ['ААИР 123126-10', 'ААИР'],
'00000014293': ['ААИР 123127-01', 'ААИР'],
'00000014298': ['ААИР 123127-02', 'ААИР'],
'00000014295': ['ААИР 123127-03', 'ААИР'],
'00000008654': ['ААИР 123127-04', 'ААИР'],
'00000014471': ['ААИР 123127-07', 'ААИР'],
'00000014472': ['ААИР 123127-08', 'ААИР'],
'00000014473': ['ААИР 123127-09', 'ААИР'],
'00000014474': ['ААИР 123127-10', 'ААИР'],
'00000014292': ['ААИР 123128-01', 'ААИР'],
'00000014323': ['ААИР 123128-02', 'ААИР'],
'00000014321': ['ААИР 123128-04', 'ААИР'],
'00000014319': ['ААИР 123128-05', 'ААИР'],
'00000014776': ['ВК4.15 Козырёк водоотливной', 'Козырёк водоотливной'],
'00000014993': ['ВК4.25 Козырёк водоотливной', 'Козырёк водоотливной'],
'00000014990': ['ВК42 Козырёк водоотливной', 'Козырёк водоотливной'],
'00000008647': ['ВК5.25 Козырек водоотливной', 'Козырёк водоотливной'],
'00000008535': ['ВК52 Козырёк водоотливной', 'Козырёк водоотливной'],
'00000013769': ['ВК6.25 Козырек водоотливной', 'Козырёк водоотливной'],
'00000015005': ['ВК62 Козырек водоотливной', 'Козырёк водоотливной'],
'00000008610': ['ВК63 Козырёк водоотливной', 'Козырёк водоотливной'],
'00000012727': ['ВК64 Козырек водоотливной', 'Козырёк водоотливной'],
'00000010044': ['ВК65.24 Козырёк водоотливной', 'Козырёк водоотливной'],
'00000008609': ['ВК73.Козырёк водоотливной.', 'Козырёк водоотливной'],
'00000010045': ['ВК75.24 Козырёк водоотливной', 'Козырёк водоотливной'],
'00000015013': ['ВК83 Козырёк водоотливной', 'Козырёк водоотливной'],
'00000014931': ['ВК84 Козырёк водоотливной', 'Козырёк водоотливной'],
'00000008643': ['Др1-05.Din-рейка.', 'Дин рейка'],
'00000010312': ['Др1-12.Din-рейка.', 'Дин рейка'],
'00000010057': ['Др1-14.Din-рейка.', 'Дин рейка'],
'00000010058': ['Др1-15.Din-рейка.', 'Дин рейка'],
'00000008536': ['Др1-24.Din-рейка.', 'Дин рейка'],
'00000009896': ['Др1-26.Din-рейка.', 'Дин рейка'],
'00000008680': ['ДР1-50.Din-рейка  (двусторон.)', 'Дин рейка'],
'00000008468': ['Др2-32 Д.Дин-рейка.', 'Дин рейка'],
'00000008624': ['Др2-54 Д.Дин-рейка.', 'Дин рейка'],
'00000013791': ['ЕР 16104/2В', 'ЕР '],
'00000014750': ['ЕР 16106/2В', 'ЕР '],
'00000014751': ['ЕР 16124/2В', 'ЕР '],
'00000014752': ['ЕР 16126/2В', 'ЕР '],
'00000011694': ['ЕР 1664/1', 'ЕР '],
'00000011695': ['ЕР 1666/1', 'ЕР '],
'00000010749': ['ЕР 1684/1', 'ЕР '],
'00000012878': ['ЕР 1686/1', 'ЕР '],
'00000014753': ['ЕР 18104/2В', 'ЕР '],
'00000014754': ['ЕР 18106/2В', 'ЕР '],
'00000012099': ['ЕР 18124/2В', 'ЕР '],
'00000014755': ['ЕР 18126/2В', 'ЕР '],
'00000011693': ['ЕР 1864/1', 'ЕР '],
'00000008611': ['ЕР 1866/1', 'ЕР '],
'00000010764': ['ЕР 1884/1', 'ЕР '],
'00000011696': ['ЕР 1884/2 В', 'ЕР '],
'00000008548': ['ЕР 1886/1', 'ЕР '],
'00000011697': ['ЕР 20104/2В', 'ЕР '],
'00000012261': ['ЕР 20106/2В', 'ЕР '],
'00000010770': ['ЕР 20124/2В', 'ЕР '],
'00000012262': ['ЕР 20126/2В', 'ЕР '],
'00000011698': ['ЕР 2064/1', 'ЕР '],
'00000008573': ['ЕР 2066/1', 'ЕР '],
'00000011699': ['ЕР 2084/1', 'ЕР '],
'00000012801': ['ЕР 2084/2 В', 'ЕР '],
'00000008635': ['ЕР 2086/1', 'ЕР '],
'00000016764': ['ЕС 14104/2В IP31', 'ЕС '],
'00000016765': ['ЕС 14104/2В IP54', 'ЕС '],
'00000016767': ['ЕС 14124/2В IP31', 'ЕС '],
'00000016766': ['ЕС 14124/2В IP54', 'ЕС '],
'00000016698': ['ЕС 1464/1 IP31', 'ЕС '],
'00000016744': ['ЕС 1464/1 IP54', 'ЕС '],
'00000016964': ['ЕС 1466/1 IP31', 'ЕС '],
'00000016699': ['ЕС 1484/1 IP31', 'ЕС '],
'00000016745': ['ЕС 1484/1 IP54', 'ЕС '],
'00000016965': ['ЕС 1486/1 IP31', 'ЕС '],
'00000008749': ['Короб для опломбировки АВР', 'Прочее'],
'00000010070': ['Короб для опломбировки ВА', 'Прочее'],
'00000008692': ['Коробка соединительная', 'Прочее'],
'00000008681': ['Кронштейн БВО ЭП018301.021', 'КронштейнЫ'],
'00000010076': ['Кронштейн ВА5139', 'КронштейнЫ'],
'00000008717': ['Кронштейн ВР ЭП018301.020', 'КронштейнЫ'],
'00000015131': ['Кронштейн Д-22', 'КронштейнЫ'],
'00000010079': ['Кронштейн РБ ЭП018301.014СБ','КронштейнЫ'],
'00000012825': ['Кронштейн рейки DIN 325', 'КронштейнЫ'],
'00000012582': ['Кронштейн рейки DIN 425', 'КронштейнЫ'],
'00000012586': ['Кронштейн рейки DIN 500', 'КронштейнЫ'],
'00000012583': ['Кронштейн рейки DIN 525', 'КронштейнЫ'],
'00000012584': ['Кронштейн рейки DIN 550', 'КронштейнЫ'],
'00000012585': ['Кронштейн рейки DIN 650', 'КронштейнЫ'],
'00000012587': ['Кронштейн рейки DIN 700', 'КронштейнЫ'],
'00000008686': ['Кронштейн трансформаторов ЭП.018301.004', 'КронштейнЫ'],
'00000009152': ['Кронштейн УПЗ 2014 (Устройства помехозащиты)ЭП021601.00', 'КронштейнЫ'],
'00000017010': ['ЛП 1000.15Т', 'Лицевые панели'],
'00000017007': ['ЛП 1000.30Т', 'Лицевые панели'],
'00000017000': ['ЛП 1000.60Т', 'Лицевые панели'],
'00000017008': ['ЛП 1200.15Т', 'Лицевые панели'],
'00000017004': ['ЛП 1200.30Т', 'Лицевые панели'],
'00000017003': ['ЛП 1200.60Т', 'Лицевые панели'],
'00000012809': ['ЛП 325.15-16', 'Лицевые панели'],
'00000012810': ['ЛП 325.15-С', 'Лицевые панели'],
'00000014015': ['ЛП 325.20-16', 'Лицевые панели'],
'00000012279': ['ЛП 425.15-21', 'Лицевые панели'],
'00000012287': ['ЛП 425.15-С', 'Лицевые панели'],
'00000012275': ['ЛП 425.20-21', 'Лицевые панели'],
'00000012283': ['ЛП 425.20-С', 'Лицевые панели'],
'00000012280': ['ЛП 500.15-25', 'Лицевые панели'],
'00000012288': ['ЛП 500.15-С', 'Лицевые панели'],
'00000012276': ['ЛП 500.20-25', 'Лицевые панели'],
'00000012284': ['ЛП 500.20-С', 'Лицевые панели'],
'00000012281': ['ЛП 525.15-27', 'Лицевые панели'],
'00000012289': ['ЛП 525.15-С', 'Лицевые панели'],
'00000012277': ['ЛП 525.20-27', 'Лицевые панели'],
'00000012285': ['ЛП 525.20-С', 'Лицевые панели'],
'00000012595': ['ЛП 550.15-28', 'Лицевые панели'],
'00000013074': ['ЛП 550.20-28', 'Лицевые панели'],
'00000012596': ['ЛП 550.20-С', 'Лицевые панели'],
'00000015642': ['ЛП 600.20Т. Лицевая панель', 'Лицевые панели'],
'00000015643': ['ЛП 600.30Т. Лицевая панель', 'Лицевые панели'],
'00000015644': ['ЛП 600.60Т. Лицевая панель', 'Лицевые панели'],
'00000015645': ['ЛП 600.75Т. Лицевая панель', 'Лицевые панели'],
'00000012594': ['ЛП 650.15-34', 'Лицевые панели'],
'00000013075': ['ЛП 650.20-34', 'Лицевые панели'],
'00000012593': ['ЛП 650.20-С', 'Лицевые панели'],
'00000012282': ['ЛП 700.15-36', 'Лицевые панели'],
'00000012290': ['ЛП 700.15-С', 'Лицевые панели'],
'00000012278': ['ЛП 700.20-36', 'Лицевые панели'],
'00000012286': ['ЛП 700.20-С', 'Лицевые панели'],
'00000014733': ['ЛП 750.20-39', 'Лицевые панели'],
'00000013757': ['ЛП 750.20-С', 'Лицевые панели'],
'00000015647': ['ЛП 800.20Т. Лицевая панель', 'Лицевые панели'],
'00000015648': ['ЛП 800.30Т. Лицевая панель', 'Лицевые панели'],
'00000015649': ['ЛП 800.45Т. Лицевая панель', 'Лицевые панели'],
'00000015650': ['ЛП 800.60Т. Лицевая панель', 'Лицевые панели'],
'00000015646': ['ЛП 800.75Т. Лицевая панель', 'Лицевые панели'],
'00000014009': ['М 10.150 В', 'Монтажные пластины'],
'00000012031': ['М 10.150 С', 'Монтажные пластины'],
'00000012157': ['М 10.25', 'Монтажные пластины'],
'00000014013': ['М 10.25 В', 'Монтажные пластины'],
'00000014010': ['М 10.250 В', 'Монтажные пластины'],
'00000012030': ['М 10.250 С', 'Монтажные пластины'],
'00000012150': ['М 10.75', 'Монтажные пластины'],
'00000014014': ['М 10.75 В', 'Монтажные пластины'],
'00000012260': ['М 12.150 С', 'Монтажные пластины'],
'00000012158': ['М 12.25', 'Монтажные пластины'],
'00000012235': ['М 12.250 С', 'Монтажные пластины'],
'00000012151': ['М 12.75', 'Монтажные пластины'],
'00000012161': ['М 4.25 В', 'Монтажные пластины'],
'00000015318': ['М 4.25 В (1.5)', 'Монтажные пластины'],
'00000012162': ['М 4.75 В', 'Монтажные пластины'],
'00000012487': ['М 5.150 С', 'Монтажные пластины'],
'00000012488': ['М 5.250 С', 'Монтажные пластины'],
'00000012591': ['М 6.150 В', 'Монтажные пластины'],
'00000011702': ['М 6.150 С', 'Монтажные пластины'],
'00000012155': ['М 6.25', 'Монтажные пластины'],
'00000012231': ['М 6.25 В', 'Монтажные пластины'],
'00000015319': ['М 6.25 В (1.5)', 'Монтажные пластины'],
'00000012592': ['М 6.250 В', 'Монтажные пластины'],
'00000011704': ['М 6.250 С', 'Монтажные пластины'],
'00000012148': ['М 6.75', 'Монтажные пластины'],
'00000012163': ['М 6.75 В', 'Монтажные пластины'],
'00000012589': ['М 7.150 В', 'Монтажные пластины'],
'00000012543': ['М 7.25 В', 'Монтажные пластины'],
'00000012590': ['М 7.250 В', 'Монтажные пластины'],
'00000012544': ['М 7.75 В', 'Монтажные пластины'],
'00000013722': ['М 8.150 В', 'Монтажные пластины'],
'00000011703': ['М 8.150 С', 'Монтажные пластины'],
'00000012156': ['М 8.25', 'Монтажные пластины'],
'00000012850': ['М 8.25 В', 'Монтажные пластины'],
'00000013139': ['М 8.250 В', 'Монтажные пластины'],
'00000011705': ['М 8.250 С', 'Монтажные пластины'],
'00000012149': ['М 8.75', 'Монтажные пластины'],
'00000013213': ['М 8.75 В', 'Монтажные пластины'],
'00000013549': ['МК ЩО 2046 (ЕР)', 'Металлоконструкции ЩО'],
'00000013550': ['МК ЩО 2066 (ЕР)', 'Металлоконструкции ЩО'],
'00000013551': ['МК ЩО 2076 (ЕР)', 'Металлоконструкции ЩО'],
'00000007808': ['МКН 10.65.24М IP31', 'МКН'],
'00000008689': ['МКН 10.65.24М IP54', 'МКН'],
'00000008022': ['МКН 106.25М IP31', 'МКН'],
'00000008574': ['МКН 106.25М IP54', 'МКН'],
'00000007812': ['МКН 1063М IP31', 'МКН'],
'00000012775': ['МКН 1063М IP31 (Без МП)', 'МКН'],
'00000008638': ['МКН 1063М IP54', 'МКН'],
'00000012840': ['МКН 1063М IP54 (Без МП)', 'МКН'],
'00000012777': ['МКН 1064М IP31 (Без МП)', 'МКН'],
'00000012841': ['МКН 1064М IP54 (Без МП)', 'МКН'],
'00000007545': ['МКН 1083М IP31', 'МКН'],
'00000012776': ['МКН 1083М IP31 (Без МП)', 'МКН'],
'00000008459': ['МКН 1083М IP54', 'МКН'],
'00000012854': ['МКН 1083М IP54 (Без МП) /4замка', 'МКН'],
'00000007944': ['МКН 12.75.24М IP31', 'МКН'],
'00000009153': ['МКН 12.75.24М IP54', 'МКН'],
'00000012999': ['МКН 12103М IP31', 'МКН'],
'00000013241': ['МКН 12103М IP54', 'МКН'],
'00000008132': ['МКН 126.25М IP31', 'МКН'],
'00000009707': ['МКН 126.25М IP54', 'МКН'],
'00000007817': ['МКН 1263М IP31', 'МКН'],
'00000012779': ['МКН 1263М IP31 (Без МП)', 'МКН'],
'00000008475': ['МКН 1263М IP54', 'МКН'],
'00000012837': ['МКН 1263М IP54 (Без МП)', 'МКН'],
'00000012780': ['МКН 1264М IP31 (Без МП)', 'МКН'],
'00000012843': ['МКН 1264М IP54 (Без МП)', 'МКН'],
'00000007821': ['МКН 1283М IP31', 'МКН'],
'00000012778': ['МКН 1283М IP31 (Без МП)', 'МКН'],
'00000008568': ['МКН 1283М IP54', 'МКН'],
'00000008604': ['МКН 33.15М IP54', 'МКН'],
'00000008504': ['МКН 33.15М ІР31', 'МКН'],
'00000008473': ['МКН 332М IP54', 'МКН'],
'00000004482': ['МКН 332М ІР31', 'МКН'],
'00000008503': ['МКН 43.15М IP31', 'МКН'],
'00000008551': ['МКН 43.15М IP54', 'МКН'],
'00000008650': ['МКН 43.25М IP54', 'МКН'],
'00000000660': ['МКН 43.25М ІР31', 'МКН'],
'00000000227': ['МКН 432М IP31', 'МКН'],
'00000008483': ['МКН 432М IP54', 'МКН'],
'00000000792': ['МКН 44.15М IP31', 'МКН'],
'00000008754': ['МКН 44.15М IP54', 'МКН'],
'00000004839': ['МКН 44.25М IP31', 'МКН'],
'00000011161': ['МКН 44.25М IP54', 'МКН'],
'00000000574': ['МКН 442М IP31', 'МКН'],
'00000008518': ['МКН 442М ІР54', 'МКН'],
'00000017956': ['МКН 532М IP31', 'МКН'],
'00000000847': ['МКН 54.15М IP31', 'МКН'],
'00000009105': ['МКН 54.15М ІР54', 'МКН'],
'00000000504': ['МКН 54.25М IP31', 'МКН'],
'00000008555': ['МКН 54.25М ІР54', 'МКН'],
'00000000027': ['МКН 542М IP31', 'МКН'],
'00000008488': ['МКН 542М IP54', 'МКН'],
'00000008539': ['МКН 55.14 IP31', 'МКН'],
'00000013772': ['МКН 55.15М IP31', 'МКН'],
'00000000499': ['МКН 55.25М IP31', 'МКН'],
'00000008616': ['МКН 55.25М ІР54', 'МКН'],
'00000000705': ['МКН 552М IP31', 'МКН'],
'00000008519': ['МКН 552М ІР54', 'МКН'],
'00000008291': ['МКН 64.15М IP31', 'МКН'],
'00000009106': ['МКН 64.15М IP54', 'МКН'],
'00000004163': ['МКН 64.25М IP31', 'МКН'],
'00000008549': ['МКН 64.25М IP54', 'МКН'],
'00000004623': ['МКН 642М IP31', 'МКН'],
'00000008608': ['МКН 642М IP54', 'МКН'],
'00000007901': ['МКН 643М IP31', 'МКН'],
'00000008508': ['МКН 643М IP54', 'МКН'],
'00000007939': ['МКН 65.25М IP31', 'МКН'],
'00000008545': ['МКН 65.25М IP54', 'МКН'],
'00000008001': ['МКН 652М IP31', 'МКН'],
'00000008605': ['МКН 652М IP54', 'МКН'],
'00000008576': ['МКН 653М IP31', 'МКН'],
'00000008766': ['МКН 653М IP54', 'МКН'],
'00000007683': ['МКН 66.25М IP31', 'МКН'],
'00000008476': ['МКН 66.25М IP54', 'МКН'],
'00000008142': ['МКН 662М IP31', 'МКН'],
'00000008713': ['МКН 662М IP54', 'МКН'],
'00000007543': ['МКН 663М IP31', 'МКН'],
'00000008579': ['МКН 663М IP54', 'МКН'],
'00000008126': ['МКН 75.17М IP31', 'МКН'],
'00000011165': ['МКН 75.17М IP54', 'МКН'],
'00000008059': ['МКН 75.25М IP31', 'МКН'],
'00000008665': ['МКН 75.25М IP54', 'МКН'],
'00000008151': ['МКН 752М IP31', 'МКН'],
'00000008747': ['МКН 752М IP54', 'МКН'],
'00000013068': ['МКН 753М IP31', 'МКН'],
'00000013228': ['МКН 753М IP54', 'МКН'],
'00000007801': ['МКН 8.65.24М IP31', 'МКН'],
'00000011166': ['МКН 8.65.24М IP54', 'МКН'],
'00000008212': ['МКН 85.25М IP31', 'МКН'],
'00000011170': ['МКН 85.25М IP54', 'МКН'],
'00000011168': ['МКН 852М IP31', 'МКН'],
'00000011169': ['МКН 852М IP54', 'МКН'],
'00000008216': ['МКН 853М IP31', 'МКН'],
'00000011171': ['МКН 853М IP54', 'МКН'],
'00000012922': ['МКН 853М IP54 (СПЕЦ.. без МП)', 'МКН'],
'00000007785': ['МКН 86.25М IP31', 'МКН'],
'00000008556': ['МКН 86.25М IP54', 'МКН'],
'00000007780': ['МКН 862М IP31', 'МКН'],
'00000008699': ['МКН 862М IP54', 'МКН'],
'00000007694': ['МКН 863М IP31', 'МКН'],
'00000008507': ['МКН 863М IP54', 'МКН'],
'00000013739': ['МКН 864М IP31', 'МКН'],
'00000014723': ['МКН 864М IP54', 'МКН'],
'00000007793': ['МКН 883М IP31', 'МКН'],
'00000011282': ['МКН 883М IP54', 'МКН'],
'00000014851': ['МКН 884М IP31', 'МКН'],
'00000007953': ['МКН 95.17М IP31', 'МКН'],
'00000011172': ['МКН 95.17М IP54', 'МКН'],
'00000008201': ['МКС 10.75.24М IP31', 'МКС'],
'00000011173': ['МКС 10.75.24М IP54', 'МКС'],
'00000012520': ['МКС 1063 IP31 (без МП)', 'МКС'],
'00000012575': ['МКС 1063 IP54 (без МП)', 'МКС'],
'00000014852': ['МКС 1064 IP31 (без МП)', 'МКС'],
'00000008069': ['МКС 12.75.24М IP31', 'МКС'],
'00000008667': ['МКС 12.75.24М IP54', 'МКС'],
'00000012521': ['МКС 1263 IP31 (без МП)', 'МКС'],
'00000012576': ['МКС 1263 IP54 (без МП)', 'МКС'],
'00000014853': ['МКС 1264 IP31 (без МП)', 'МКС'],
'00000007984': ['МКС 14.75.24М IP31', 'МКС'],
'00000008615': ['МКС 14.75.24М IP54', 'МКС'],
'00000012522': ['МКС 1463 IP31 (без МП)', 'МКС'],
'00000012577': ['МКС 1463 IP54 (без МП)', 'МКС'],
'00000014854': ['МКС 1464 IP31 (без МП)', 'МКС'],
'00000014932': ['МКС 1464 IP54 (без МП)', 'МКС'],
'00000014524': ['МКС 1483 IP31 (без МП)', 'МКС'],
'00000014522': ['МКС 1483 IP54 (без МП)', 'МКС'],
'00000014855': ['МКС 1484 IP31 (без МП)', 'МКС'],
'00000014963': ['МКС 1484 IP54 (без МП)', 'МКС'],
'00000012523': ['МКС 1663 IP31 (без МП)', 'МКС'],
'00000012578': ['МКС 1663 IP54 (без МП)', 'МКС'],
'00000012525': ['МКС 1664 IP31 (без МП)', 'МКС'],
'00000012579': ['МКС 1664 IP54 (без МП)', 'МКС'],
'00000012524': ['МКС 1673 IP31 (без МП)', 'МКС'],
'00000012580': ['МКС 1673 IP54 (без МП)', 'МКС'],
'00000013645': ['МКС 1684 IP31 (без МП)', 'МКС'],
'00000013646': ['МКС 1684 IP54 (без МП)', 'МКС'],
'00000013643': ['МКС 1864 IP31 (без МП)', 'МКС'],
'00000013644': ['МКС 1864 IP54 (без МП)', 'МКС'],
'00000012998': ['МКС 1884 IP31 (без МП)', 'МКС'],
'00000013138': ['МКС 1884 IP54 (без МП)', 'МКС'],
'00000008629': ['Мп 10.65М. Панель монтажная', 'Монтажные панели МП/МПС'],
'00000008577': ['Мп 12.75М. Панель монтажная (RAL 7032)', 'Монтажные панели МП/МПС'],
'00000002264': ['Мп 55М. Панель монтажная .Д ЭП.049830.001-04.Д', 'Монтажные панели МП/МПС'],
'00000008329': ['Мп 75М. Панель монтажна.Д', 'Монтажные панели МП/МПС'],
'00000008630': ['Мп 8.65М. Панель монтажная', 'Монтажные панели МП/МПС'],
'00000008567': ['Мп 95М. Панель монтажная', 'Монтажные панели МП/МПС'],
'00000012526': ['МПС 106 Панель монтажная (оц)', 'Монтажные панели МП/МПС'],
'00000008668': ['МПС 12.75 Панель монтажная (RAL 7032)','Монтажные панели МП/МПС'],
'00000012527': ['МПС 126 Панель монтажная  (оц)', 'Монтажные панели МП/МПС'],
'00000008566': ['МПС 14.75 Панель монтажная (RAL 7032)', 'Монтажные панели МП/МПС'],
'00000012528': ['МПС 146 Панель монтажная (оц)', 'Монтажные панели МП/МПС'],
'00000014927': ['МПС 148 Панель монтажная (оц)', 'Монтажные панели МП/МПС'],
'00000012529': ['МПС 166 Панель монтажная (оц)', 'Монтажные панели МП/МПС'],
'00000014928': ['МПС 167 Панель монтажная (оц)', 'Монтажные панели МП/МПС'],
'00000014929': ['МПС 168 Панель монтажная (оц)', 'Монтажные панели МП/МПС'],
'00000013649': ['МПС 186 Панель монтажная  (оц)', 'Монтажные панели МП/МПС'],
'00000014930': ['МПС 188 Панель монтажная (оц)', 'Монтажные панели МП/МПС'],
'00000015638': ['Направляющая экрана НЭ 16Т', 'Прочее'],
'00000015639': ['Направляющая экрана НЭ 18Т', 'Прочее'],
'00000015637': ['Направляющая экрана НЭ 20Т', 'Прочее'],
'00000013344': ['П 10.25 Т. Профіль монтажний', 'Профиль монтажный'],
'00000013351': ['П 10.75 Т. Профіль монтажний', 'Профиль монтажный'],
'00000013345': ['П 12.25 Т. Профіль монтажний', 'Профиль монтажный'],
'00000013352': ['П 12.75 Т. Профіль монтажний', 'Профиль монтажный'],
'00000013346': ['П 3.25 Т Профіль монтажний (поперечний)', 'Профиль монтажный'],
'00000013353': ['П 3.75 Т Профіль монтажний (поперечний)', 'Профиль монтажный'],
'00000013347': ['П 5.25 Т Профіль монтажний (поперечний)', 'Профиль монтажный'],
'00000013354': ['П 5.75 Т Профіль монтажний (поперечний)', 'Профиль монтажный'],
'00000013342': ['П 6.25 Т. Профіль монтажний', 'Профиль монтажный'],
'00000013349': ['П 6.75 Т. Профіль монтажний', 'Профиль монтажный'],
'00000013348': ['П 7.25 Т Профіль монтажний (поперечний)', 'Профиль монтажный'],
'00000013355': ['П 7.75 Т Профіль монтажний (поперечний)', 'Профиль монтажный'],
'00000013343': ['П 8.25 Т. Профіль монтажний', 'Профиль монтажный'],
'00000013350': ['П 8.75 Т. Профіль монтажний', 'Профиль монтажный'],
'00000013761': ['П 9.75 Т. Профіль монтажний', 'Профиль монтажный'],
'00000014856': ['Панель В 6.250 (ККУ)', 'Прочее'],
'00000008687': ['Панель счетчика 3ф/323 ЭП.018301.003', 'Прочее'],
'00000013547': ['Панель торцевая 206 ЩО', 'Прочее'],
'00000014154': ['Планка кабельная ПК 5Т', 'Прочее'],
'00000008543': ['Планка кабельная ПК 6Т', 'Прочее'],
'00000014155': ['Планка кабельная ПК 7Т', 'Прочее'],
'00000010109': ['Планка кабельная ПК 8Т', 'Прочее'],
'00000013330': ['ПМ 10.25 Т. Пластина монтажна', 'Пластины монтажные'],
'00000013707': ['ПМ 10.250 Т. Пластина монтажна', 'Пластины монтажные'],
'00000013337': ['ПМ 10.75 Т. Пластина монтажна', 'Пластины монтажные'],
'00000013331': ['ПМ 12.25 Т. Пластина монтажна', 'Пластины монтажные'],
'00000013710': ['ПМ 12.250 Т. Пластина монтажна', 'Пластины монтажные'],
'00000013338': ['ПМ 12.75 Т. Пластина монтажна', 'Пластины монтажные'],
'00000013332': ['ПМ 3.25 Т Пластина монтажна (поперечна)', 'Пластины монтажные'],
'00000013339': ['ПМ 3.75 Т Пластина монтажна (поперечна)', 'Пластины монтажные'],
'00000013333': ['ПМ 5.25 Т Пластина монтажна (поперечна)', 'Пластины монтажные'],
'00000013340': ['ПМ 5.75 Т Пластина монтажна (поперечна)', 'Пластины монтажные'],
'00000013328': ['ПМ 6.25 Т. Пластина монтажна', 'Пластины монтажные'],
'00000013708': ['ПМ 6.250 Т. Пластина монтажна', 'Пластины монтажные'],
'00000013335': ['ПМ 6.75 Т. Пластина монтажна', 'Пластины монтажные'],
'00000013334': ['ПМ 7.25 Т Пластина монтажна (поперечна)', 'Пластины монтажные''ПМ '],
'00000013341': ['ПМ 7.75 Т Пластина монтажна (поперечна)', 'Пластины монтажные'],
'00000017181': ['ПМ 8.150 Т. Пластина монтажна', 'Пластины монтажные'],
'00000013329': ['ПМ 8.25 Т. Пластина монтажна', 'Пластины монтажные'],
'00000013709': ['ПМ 8.250 Т. Пластина монтажна', 'Пластины монтажные'],
'00000013336': ['ПМ 8.75 Т. Пластина монтажна', 'Пластины монтажные'],
'00000014022': ['ПМ 9.75 Т. Пластина монтажна', 'Пластины монтажные'],
'00000013713': ['Полка стационарная ПС 1010 Т', 'Пластины монтажные'],
'00000014301': ['Профиль шинопровода ПШ 35х1500', 'Прочее'],
'00000008578': ['СМ-11М', 'СМ / СМГ'],
'00000008731': ['СМ-6М',  'СМ / СМГ'],
'00000008752': ['СМ-7М',  'СМ / СМГ'],
'00000008464': ['СМ-8М',  'СМ / СМГ'],
'00000008465': ['СМ-9М',  'СМ / СМГ'],
'00000012553': ['СМГ 10.35М',  'СМ / СМГ'],
'00000015396': ['СМГ 10.35М (1.5)',  'СМ / СМГ'],
'00000012552': ['СМГ 12.35М', 'СМ / СМГ'],
'00000015397': ['СМГ 12.35М (1.5)',  'СМ / СМГ'],
'00000012551': ['СМГ 14.35М',  'СМ / СМГ'],
'00000015398': ['СМГ 14.35М (1.5)',  'СМ / СМГ'],
'00000012230': ['СМГ 16.35',  'СМ / СМГ'],
'00000015597': ['СМГ 16.35 (1.5)',  'СМ / СМГ'],
'00000012550': ['СМГ 16.35М',  'СМ / СМГ'],
'00000015320': ['СМГ 16.35М (1.5)',  'СМ / СМГ'],
'00000012229': ['СМГ 18.35',  'СМ / СМГ'],
'00000015596': ['СМГ 18.35 (1.5)',  'СМ / СМГ'],
'00000013214': ['СМГ 18.35М',  'СМ / СМГ'],
'00000015842': ['СМГ 18.35М (1.5)',  'СМ / СМГ'],
'00000011909': ['СМГ 20.35',  'СМ / СМГ'],
'00000015595': ['СМГ 20.35 (1.5)',  'СМ / СМГ'],
'00000012880': ['СМГ 8.35М',  'СМ / СМГ'],
'00000008520': ['СМС-11М',  'СМ / СМГ'],
'00000008521': ['СМС-13М',  'СМ / СМГ'],
'00000012128': ['СТ-100.65 (стійка таврова)', 'Прочее'],
'00000012129': ['СТ-150.135 (стійка таврова)', 'Прочее'],
'00000017221': ['Стойка монтажная СМ 14.50Т', 'Стойки монтажные'],
'00000013356': ['Стойка монтажная СМ 14.75Т', 'Стойки монтажные'],
'00000017222': ['Стойка монтажная СМ 16.50Т', 'Стойки монтажные'],
'00000012860': ['Стойка монтажная СМ 16.75Т', 'Стойки монтажные'],
'00000017223': ['Стойка монтажная СМ 18.50Т', 'Стойки монтажные'],
'00000012858': ['Стойка монтажная СМ 18.75Т', 'Стойки монтажные'],
'00000017224': ['Стойка монтажная СМ 20.50Т', 'Стойки монтажные'],
'00000012859': ['Стойка монтажная СМ 20.75Т', 'Стойки монтажные'],
'00000017225': ['Стойка монтажная СМ 22.50Т', 'Стойки монтажные'],
'00000013357': ['Стойка монтажная СМ 22.75Т', 'Стойки монтажные'],
'00000013051': ['Уголок монтажный (82х20х20мм)', 'Прочее'],
'00000008682': ['Уголок универсальный', 'Прочее'],
'00000013052': ['Уголок фасадный (40х25х20 мм)', 'Прочее'],
'00000008554': ['УЗ ЕР600.Устройство заземления', 'Устройства заземления'],
'00000008516': ['УЗ ЕР800.Устройство заземления', 'Устройства заземления'],
'00000017178': ['УЗ ЕС. Устройство заземления', 'Устройства заземления'],
'00000007750': ['УЗ МКН.Устройство заземления', 'Устройства заземления'],
'00000017107': ['УЗ ЩЭ. Устройство заземления', 'Устройства заземления'],
'00000013459': ['Усилитель монтажной панели УМП 10', 'Устройства заземления'],
'00000013460': ['Усилитель монтажной панели УМП 12', 'Устройства заземления'],
'00000013457': ['Усилитель монтажной панели УМП 6', 'Устройства заземления'],
'00000013458': ['Усилитель монтажной панели УМП 8', 'Устройства заземления'],
'00000008571': ['Устройство заземления ГРЩ02М', 'Устройства заземления'],
'00000013176': ['Цоколь Ц-1103 МК', 'Цоколя'],
'00000012172': ['Цоколь Ц-1104 ЕР', 'Цоколя'],
'00000012345': ['Цоколь Ц-1106 ЕР', 'Цоколя'],
'00000012173': ['Цоколь Ц-1124 ЕР', 'Цоколя'],
'00000012300': ['Цоколь Ц-1126 ЕР', 'Цоколя'],
'00000012921': ['Цоколь Ц-153 МК', 'Цоколя'],
'00000013111': ['Цоколь Ц-163 МК', 'Цоколя'],
'00000012174': ['Цоколь Ц-164 ЕР', 'Цоколя'],
'00000013114': ['Цоколь Ц-164 МК', 'Цоколя'],
'00000012176': ['Цоколь Ц-166 ЕР', 'Цоколя'],
'00000013112': ['Цоколь Ц-173 МК', 'Цоколя'],
'00000012852': ['Цоколь Ц-183 МК', 'Цоколя'],
'00000012175': ['Цоколь Ц-184 ЕР', 'Цоколя'],
'00000013117': ['Цоколь Ц-184 МК', 'Цоколя'],
'00000012177': ['Цоколь Ц-186 ЕР', 'Цоколя'],
'00000008612': ['Цоколь Ц-2.75.24 МК', 'Цоколя'],
'00000011857': ['Цоколь Ц-2104 ЕР', 'Цоколя'],
'00000012485': ['Цоколь Ц-2106 ЕР', 'Цоколя'],
'00000011858': ['Цоколь Ц-2124 ЕР', 'Цоколя'],
'00000012486': ['Цоколь Ц-2126 ЕР', 'Цоколя'],
'00000008559': ['Цоколь Ц-263 МК', 'Цоколя'],
'00000011859': ['Цоколь Ц-264 ЕР', 'Цоколя'],
'00000013115': ['Цоколь Ц-264 МК', 'Цоколя'],
'00000008678': ['Цоколь Ц-266 ЕР', 'Цоколя'],
'00000008505': ['Цоколь Ц-273 МК', 'Цоколя'],
'00000012868': ['Цоколь Ц-283 МК', 'Цоколя'],
'00000011860': ['Цоколь Ц-284 ЕР', 'Цоколя'],
'00000013116': ['Цоколь Ц-284 МК', 'Цоколя'],
'00000012484': ['Цоколь Ц-286 ЕР', 'Цоколя'],
'00000008758': ['Щит этажный 2кв. 1ф.', 'Щиты этажные'],
'00000012732': ['Щит этажный 2кв. 3ф.', 'Щиты этажные'],
'00000008659': ['Щит этажный 2кв. 3ф. (антивандальний)', 'Щиты этажные'],
'00000009119': ['Щит этажный 3кв. 1ф.', 'Щиты этажные'],
'00000009118': ['Щит этажный 3кв. 3ф.', 'Щиты этажные'],
'00000008661': ['Щит этажный 3кв. 3ф. (антивандальний)', 'Щиты этажные'],
'00000012028': ['Щит этажный 4кв. 1ф.', 'Щиты этажные'],
'00000012616': ['Щит этажный 4кв. 1ф. (антивандальний)','Щиты этажные'],
'00000008759': ['Щит этажный 4кв. 3ф.', 'Щиты этажные'],
'00000008662': ['Щит этажный 4кв. 3ф. (антивандальний)', 'Щиты этажные'],
'00000012088': ['Щит этажный 5кв. 1ф.', 'Щиты этажные'],
'00000008760': ['Щит этажный 5кв. 3ф.', 'Щиты этажные'],
'00000008663': ['Щит этажный 5кв. 3ф.(антивандальный)', 'Щиты этажные'],
'00000009120': ['Щит этажный 6 кв. 1ф.', 'Щиты этажные'],
'00000012473': ['Щит этажный 6кв. 3ф.', 'Щиты этажные'],
'00000012036': ['Щит этажный 6кв. 3ф.(антивандальный)', 'Щиты этажные'],
'00000012892': ['Щит этажный 7кв. 1ф.', 'Щиты этажные'],
'00000012474': ['Щит этажный 7кв. 3ф.', 'Щиты этажные'],
'00000012068': ['Щит этажный 7кв. 3ф. (антивандальный)', 'Щиты этажные'],
'00000012574': ['Щит этажный 8кв. 1ф.', 'Щиты этажные'],
'00000012035': ['Щит этажный 8кв. 3ф. (антивандальный)', 'Щиты этажные'],
'00000008677': ['ЩН 40.25.12М', 'ЩН / ЩУ'],
'00000011517': ['ЩН 40.40.12', 'ЩН / ЩУ'],
'00000008691': ['ЩНИз', 'ЩН / ЩУ'],
'00000009149': ['ЩУ 34.40.12', 'ЩН / ЩУ'],
'00000012203': ['ЩУ 40.25.12 (7032)', 'ЩН / ЩУ'],
'00000015651': ['Экран боковой 20х223Т.', 'Экраны'],
'00000008720': ['Экран ВР ЭП018301.019', 'Экраны'],
'00000014860': ['Ячейка К1 (ККУ)', 'Ячейки ККУ'],
'00000014861': ['Ячейка К2 (ККУ)', 'Ячейки ККУ'],
'00000014862': ['Ячейка К3 (ККУ)', 'Ячейки ККУ'],
'00000014857': ['Ячейка КО (ККУ)', 'Ячейки ККУ']
}

l_send = ''
info_sync = ''

# Menu File/About
def f_about():
    showinfo('ELETON REMOTE ORDER main',
    """
                            !!! Beta  Version !!!
    При запуске:
        1. Загрузка остатков из файла 'text.txt'
        2. Отправка файла на FTP-server
        3. Получение ЗАКАЗОВ
                 
    Кропка CLOUDS:
        - Отправка файла с остатками на FTP-server)
        - получение ЗАКАЗОВ
                   
    Кнопка 'TXT'- выводит список, который загружается на  FTP-server
                 
    FILE - дата/время последнего изменения файла 'text.txt'
                 
    SYNC - дата/время последней синхронизации с FTP-server
        - Отправка файла на FTP-server)
        - получение ЗАКАЗОВ
         
    Файл хранения заказов: 'client_recieved_order.txt'
    (внутри можно удалять)
         
    Все остальные файлы - служебные
                  
    Верхнее  "чистое поле" - место для сообщения "ВСЕМ !!!, ВСЕМ !!!"
         
                 Don't throw the slippers!!!
                 Good luck!
         
                 Konstiantyn Sh
                 August_2019'
    """)

def f_close(event):
    f_exit()

def f_exit():
    root.destroy()
# parser
def parser(l):  # works for every STRING in the LIST, not the LIST
    global l_send
    list = []
    for i in l:
       list.append(i.replace('\t', '*'))
    s = ','.join(list)
    s = s.split('*')

    if d_original.get(s[1], 0) != 0:  # if nomenklatura code in the 'd_original'
        nomenklatura, quantity, price, group = s[3], s[4], s[5], d_original.get(s[1])[1]
        quantity = quantity.split(',')[0]  # removing ZEROs after ','

        # nomenklatura for sending
        l_send += '{} ; {} ; {}; {}\n'.format(nomenklatura, quantity, price, group)

def f_start():
    global l_send
    # removing from text.txt odd information
    with open ('text.txt', 'r', encoding = 'utf-8') as f:
       data = csv.reader(f)
       for i in data:
          parser(i)

    # writing file for FTP-server
    with open('leftovers.txt', 'w', encoding = 'utf-8') as f:
       # getting date/time text.txt
       sec = os.path.getmtime('text.txt')
       last_time_change = datetime.fromtimestamp(sec).strftime('%Y-%m-%d %H:%M:%S')

       l_send += last_time_change  # in index[-1]
       f.write(l_send)
    # for keeping date/time last syncronization
    with open('information.pkl', 'rb') as f:
        data = pickle.load(f)
        info_sync = data
        print('Last syncronization: {}'.format(data))
        lab_s.config(text='SYNC = ' + info_sync)  # reset date/time of file on label


     # Button 'Send to clouds', FTP connection, sending 'leftovers.txt'
def f_send():
    global l_send
    print('start loading......')
    try:
       ftps = FTP_TLS(helpic.place_ftp, helpic.user_ftp, helpic.password_ftp)
    except:
        showinfo('Connection', 'You don\'t have internet conection\n\
                               or login/pasword were changed')
        return None  # for prevent doing next code
    ftps.cwd(helpic.directory_ftp)

    # for adding message into 'leftovers.txt'
    with open('leftovers.txt', 'w', encoding='utf-8') as f:
        message = 'Message: '+ text_message.get(1.0, END) # message from 'text_message'
        index = l_send.find('Message')       # deleting previous message
        l_send = l_send[:index-2]            #  '\2' - two indiches

        l_send += '\n'+message  # put in index[-1]

        f.write(l_send)

    file_name = 'leftovers.txt'

    ftps.storbinary('STOR ' + file_name, open(file_name, 'rb'))  # загрузка файла НА сервер
    ftps.quit()
    print('Finish loading')
    f_write_inf()
    lab_s.config(text='SYNC = ' + info_sync)   # reset date/time of file on label
    print('File for FTP-server was SENT')


# getting the time of last changes 'text.txt'
def f_get_time_file():
    global info_sync
    sec = os.path.getmtime('text.txt')
    last_time_change = datetime.fromtimestamp(sec).strftime('%Y-%m-%d %H:%M:%S')
    lab_f.config(text='FILE = ' + last_time_change)
    lab_s.config(text='SYNC = ' + info_sync)

# keeping inner information
def f_write_inf():
    global info_sync
    t = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    info_sync = str(t)
    with open('information.pkl', 'wb') as f:
         pickle.dump(info_sync, f)

#recieving client's  orders from FTP
def f_orders():
        # trying to connect with FTP-server
        try:
           ftps = FTP_TLS(helpic.place_ftp,helpic.user_ftp, helpic.password_ftp)
           ftps.cwd(helpic.directory_ftp)
        except:
            showinfo('Connection', 'You don\'t have internet conection\n\
                                   or login/pasword were changed')
            return None
        print('ORDERS loading......')

        list = ftps.nlst()                   # getting the list of files from FOLDER='eleton.zzz.com.ua'
        list_order = [i for i in list if i.startswith('order')]


        for i in list_order:
            file_name = i
            with open('client_recieved_orders.pkl', 'wb') as f:

                ftps.retrbinary('RETR ' + file_name, f.write)   # loading 'order'-files from server

            ftps.delete(file_name) # deleting from FTP server after writing

            with open('client_recieved_orders.pkl', 'rb') as f:
               data = pickle.load(f)
            # data[:-3]  - list of order
            # data[-3]  - Castomer
            # data[:-2]  - message
            # data[:-1]  - time of creating order

            # puting data to the 'text_orders'
            for i in data[:-3]:
                 text_orders.insert(END, '\n{} : {}'.format(i[0], i[3]))

            text_orders.insert(END, '\n\nCastomer:   {}\nMessage:   {}\nTime:   {}\n{}'.format(data[-3], data[-2], data[-1], 60*'-'))

            # creating .txt ORDER file
            with open('client_recieved_orders.txt', 'r', encoding='utf-8') as f:
                data_keep = f.read()
            data_keep += '\n'
            for i in data[:-3]:
                data_keep += '{}: {} item x {}\n'.format(i[0], i[3], i[2])

            data_keep += '\n\nCastomer:   {}\nMessage:   {}\nTime:   {}\n{}'.format(data[-3], data[-2], data[-1],
                                                                                   60 * '-')
            with open('client_recieved_orders.txt', 'w', encoding='utf-8') as f:
                f.write(data_keep)

        print('Conection is finished')
        ftps.quit()
def f_cloud():
    f_start()   # getting data (parsing) from file 'text.txt' and creating actual 'l_send'
    f_send()    # sending 'leftovers.txt' to FTP-server
    f_orders()  # getting orders from FTP-server

# PRINT nomenklatura for srnding
def f_print_txt():
    for i in l_send.split('\n'):
        print(i)


root = Tk()
root.geometry('400x700')
root.title('Sending File with items')

m = Menu()
root.config(menu=m)
fm = Menu(m, fg='green', font='arial 12')

m.add_cascade(label='File', menu=fm)
fm.add_command(label='About', command=f_about)
fm.add_command(label='Exit', command=f_exit)

btn_send_to_cloud = Button(root, text='CLOUDS', font='arial 16', bg='lightblue', fg='blue',\
                           activebackground='lightgreen', pady=10, bd=5, relief=RAISED, command=f_cloud)
lab_f = Label(root, width=25, font='arial 12', fg='green', pady=10, bd=5, relief=RAISED)
lab_s = Label(root, width=25, font='arial 12', fg='green', pady=10, bd=5, relief=RAISED)
text_orders = Text(root, width=40, height=20, fg='black', bg='white', font='arial 12', relief=SUNKEN, wrap=WORD)
text_message = Text(root, width=40, height=2, fg='black', bg='white', font='arial 12', relief=SUNKEN, wrap=WORD)
scr_text_orders=Scrollbar(root, command=text_orders.yview)
text_orders.config(yscrollcommand=scr_text_orders.set)
btn_print_txt = Button(root, text='TXT', font='arial 12', bg='lightgreen', fg='blue',\
                           activebackground='lightblue', pady=5, bd=5, relief=RAISED, command=f_print_txt)

text_message.grid(row=1, column=0, pady=2, padx=2)
btn_send_to_cloud.grid(row=2, column=0, pady=2, padx=2)
lab_f.grid(row=3, column=0, pady=2, padx=2)
lab_s.grid(row=4, column=0, pady=2, padx=2)
text_orders.grid(row=5, column=0, pady=2, padx=2)
scr_text_orders.grid(row=5, column=1, pady=2, padx=2, sticky='ns')
btn_print_txt.grid(row=6, column=0, pady=2, padx=2, sticky='ns')

#functions for start
f_get_time_file()
f_cloud() # sending FILE and RECEIVING ORDERS


root.mainloop()