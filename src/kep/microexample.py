from kep.csv2df.specification import PARSING_SPECIFICATION, yield_parsing_assingments
from kep.csv2df.parser import evaluate_assignment
from kep.parsing_definition import PARSING_DEFINITIONS
from kep.helper.path import InterimCSV


#txt = InterimCSV(2018, 1).text()
txt = """4.2.2. Реальная начисленная заработная плата работников организаций / Accrued average monthly wages per employee																	
в % к соответствующему периоду предыдущего года / percent of corresponding period of previous year																	
1999	78,0	60,7	65,1	76,4	104,7	58,6	59,0	62,8	64,0	65,1	66,0	65,0	69,3	93,9	97,8	102,5	113,6
2000	120,9	125,3	122,0	124,7	117,8	126,1	126,4	123,5	123,3	122,3	121,4	123,1	123,3	122,0	121,9	119,4	113,4
2001	119,9	120,0	116,2	122,3	123,4	123,7	118,2	118,9	115,7	116,8	116,7	120,4	122,8	120,8	122,6	120,8	127,2
2002	116,2	117,2	119,5	117,0	112,9	115,8	119,5	116,6	121,3	118,3	118,5	119,0	116,2	115,7	115,3	114,3	110,2
2003	110,9	109,7	109,4	108,4	113,8	110,2	110,7	108,3	108,4	110,0	109,5	107,8	108,1	109,2	112,1	114,1	114,7
2004	110,6	115,0	113,5	111,4	105,2	112,1	116,7	115,7	113,9	112,8	113,8	111,7	111,6	110,9	104,6	104,3	106,3
2005	112,6	108,4	107,6	110,0	113,4	108,9	106,7	109,7	107,8	107,7	107,6	108,3	110,1	112,3	111,8	113,1	114,9
2006	113,3	110,3	114,3	114,3	114,8	110,1	110,7	110,0	111,1	115,0	116,7	115,0	113,9	114,2	115,2	115,1	114,3
2007	117,2	118,2	116,6	113,9	116,1	117,7	118,8	118,2	118,8	116,4	114,9	115,3	113,2	113,3	114,9	116,8	116,4
2008	111,5	113,4	112,5	112,2	105,0	113,3	114,1	112,8	114,6	112,0	111,1	113,6	112,1	111,4	109,7	104,9	101,8
2009	96,5	99,2	96,1	94,8	99,3	101,9	97,6	98,2	95,7	95,7	96,7	94,6	94,8	95,1	96,5	99,5	101,3
2010	105,2	103,1	106,1	105,1	104,2	101,2	102,5	103,0	105,9	105,8	106,7	106,6	105,6	103,2	103,0	102,6	106,3
2011	102,8	101,6	102,7	103,8	108,5	101,3	100,7	102,4	102,4	103,5	102,4	102,4	103,9	105,3	106,2	107,0	111,4
2012	108,4	110,3	111,3	106,3	106,2	110,5	112,1	109,0	111,1	112,4	110,2	108,1	106,0	104,7	107,1	106,7	105,0
2013	104,8	104,5	106,2	106,4	103,9	105,4	103,3	105,1	108,5	104,7	105,3	106,4	106,8	106,3	105,4	104,1	102,7
2014	101,2	104,4	102,4	100,6	98,3	105,2	104,6	103,8	103,2	102,1	102,1	101,4	98,8	101,5	100,6	98,8	96,0
20151)	91,0	91,0	91,5	90,5	90,2	91,6	92,6	89,4	90,4	92,6	91,4	90,8	91,0	89,6	89,5	89,6	91,6
2016	100,8	99,4	100,3	101,2	101,8	96,4	100,6	101,5	98,9	101,0	101,1	98,7	102,7	101,9	100,4	102,1	102,8
2017	103,52)	101,8	103,4	103,1	105,92)	101,0	100,8	103,1	103,8	102,7	103,8	103,0	102,3	104,3	105,4	105,8	106,22)
2018						106,23)											
1) В целях обеспечения статистической сопоставимости данных показатели по Российской Федерации рассчитаны без учета сведений по Республике Крым и г.Севастополю. / In order to insure the statistical comparability of data the indicators on the Russian Federation are calculated without taking into account data on the Republic of Crimea and Sevastopol city. 2) Данные изменены по сравнению с ранее опубликованными в связи с получением итогов за отчетный период. / Data are revised using final results of reporting period. 3) Оценка. / Estimation.																	
в % к предыдущему периоду / percent of previous period																	
1999		80,9	111,5	102,4	112,9	72,5	99,1	111,7	100,0	101,2	107,7	96,9	98,1	103,1	100,4	103,0	124,4
2000		94,4	109,1	103,4	108,1	80,9	99,4	108,9	100,2	101,1	106,4	98,8	98,5	102,1	100,5	101,9	118,8
2001		98,3	104,9	107,6	110,8	88,3	94,9	109,8	96,7	102,7	105,7	101,9	100,3	100,1	102,2	100,4	124,7
2002		93,7	107,1	104,9	107,2	80,7	97,9	107,1	100,7	100,1	105,9	102,2	98,0	99,8	101,7	99,6	120,4
2003		90,7	107,0	103,4	112,9	80,6	98,5	104,8	101,2	101,5	105,5	100,6	98,3	100,9	104,6	101,1	121,3
2004		92,9	105,0	102,0	106,5	78,7	102,3	103,9	99,4	100,4	106,5	98,8	98,2	100,3	98,8	100,9	123,5
2005		95,8	104,6	104,1	109,7	80,9	100,4	107,1	97,9	100,2	106,5	99,5	100,6	102,2	98,2	101,8	125,7
2006		93,1	108,7	104,3	110,3	76,8	101,0	106,2	99,0	103,7	108,0	97,8	99,7	102,4	99,2	101,8	125,2
2007		94,1	107,1	101,8	112,8	79,6	101,7	105,4	99,7	101,8	106,3	98,0	97,9	102,3	100,7	103,5	125,5
2008		97,7	105,9	101,4	105,5	77,0	102,9	104,2	101,0	99,4	105,4	100,0	97,2	102,1	98,6	98,9	122,3
2009		87,9	102,8	100,2	110,4	77,2	98,5	104,4	98,6	99,4	106,3	97,6	97,4	102,7	99,7	101,9	124,3
2010		91,0	105,3	99,7	109,3	76,7	100,1	107,5	98,7	99,2	107,1	97,5	96,8	100,4	99,3	101,7	129,0
2011		87,7	106,6	100,8	114,3	72,8	99,1	108,9	98,9	100,5	105,7	97,8	98,1	101,8	100,1	102,5	134,4
2012		89,5	107,2	96,3	114,2	72,2	100,8	105,7	100,9	101,9	103,3	96,0	96,3	100,5	102,6	102,1	132,1
2013		88,7	109,0	96,4	111,7	72,7	99,0	107,5	104,2	98,4	103,9	96,8	96,8	100,2	101,9	100,8	130,2
2014		88,6	107,1	94,8	109,1	74,3	98,4	106,9	103,8	97,1	104,1	95,9	94,4	103,1	100,9	99,0	126,5
2015		82,21)	107,5	93,7	109,1	71,31)	99,3	103,4	104,9	99,8	102,8	95,0	94,7	101,7	100,6	99,3	129,2
2016		90,5	108,5	94,6	110,3	74,3	103,2	104,3	102,3	101,7	102,7	92,8	98,5	101,0	99,4	100,9	130,9
2017		92,1	110,5	94,0	113,32)	74,4	102,7	106,6	103,3	100,8	103,9	92,1	98,1	102,8	100,6	101,1	131,22)
2018						74,83)											
___________________ 1) В целях обеспечения статистической сопоставимости данных показатели по Российской Федерации рассчитаны без учета сведений по Республике Крым и г.Севастополю. / In order to insure the statistical comparability of data the indicators on the Russian Federation are calculated without taking into account data on the Republic of Crimea and Sevastopol city. 2) Данные изменены по сравнению с ранее опубликованными в связи с получением итогов за отчетный период. / Data are revised using final results of reporting period. 3) Оценка. / Estimation.																	
"""

parsing_spec = PARSING_SPECIFICATION
parsing_spec.definitions[0].commands = [PARSING_SPECIFICATION.definition_default.commands[4]]
del parsing_spec.definitions[1:]
parsing_spec.attach_data(txt)

from pandas import Timestamp 
from kep.parsing_definition.parsing_definition import DL

csv_text = InterimCSV(2018, 3).text()
ass_list = list(yield_parsing_assingments(DL, csv_text))
values = [v for a in ass_list for v in evaluate_assignment(a)]
assert ({'freq': 'a',
  'label': 'EXPORT_GOODS_bln_usd',
  'time_index': Timestamp('1999-12-31 00:00:00'),
  'value': 75.6} in values)

New pseudocode:
===============    

1 COMMANDS_DEFAULT + COMMANDS_BY_SEGMENT -> parsing definition
2 parsing definition + csv_text -> assignments(data and parsing parameters)
3 assignments are evaluated to produce values
4 values produce dataframes 
5 dataframes are saves 






