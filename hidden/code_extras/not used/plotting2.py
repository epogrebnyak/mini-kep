import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as dates
matplotlib.style.use('ggplot')


def plot(df, title, minor_ticks, major_ticks):
    ax = df.plot(x_compat=True)           
    # set ticks
    ax.set_xticks(minor_ticks, minor=True)
    ax.xaxis.set_ticks(major_ticks, minor=False)
    ax.xaxis.set_major_formatter(dates.DateFormatter('%Y'))
    plt.gcf().autofmt_xdate(rotation=0, ha="center") 
    # other formatting
    plt.legend(loc="lower left")
    ax.set_title(title, loc='left', fontdict = {'fontsize': 11})
    return ax    


def plot_long(df, title, start=2005, end=2020, left_offset=1):
    df = df[df.index>=str(start)]
    minor_ticks = pd.date_range(str(start-left_offset), str(end), freq='YS')
    major_ticks = pd.date_range(str(start), str(end), freq='5YS') 
    return plot(df, title, minor_ticks, major_ticks)

import access    
dfa, dfq, dfm = (access.get_dataframe(freq) for freq in 'aqm')
df = dfa['EXPORT_GOODS_bln_usd'] - dfa['IMPORT_GOODS_bln_usd']

# TODO: 
"""
  Plotting
  --------
  #a4: place charts on one A4 sheet and make PDF via html (Jinja/Weasyprint) see code below'
  #ae: light blue background for grid

  #vt: variable transforms
  ---------------
  - accumulate CPI_rog to yoy
  - MA(12) smoothing 
  - % of GDP (at least annual)
    
"""

# NOT TODO NOW:
"""
  New charts
  ----------
  - seasonal adjustment/detrending 
  - additional 'latest value' chart
  - add comments/annoatations under header
  
  New data
  --------
  - add oil prices
  - parsing defintions
  
  Formatting
  -------------  
  - names in legend
  - same height on Y axis
"""


from ruamel.yaml import YAML
yaml = YAML()

doc = """
Валовый внутренний продукт (ВВП):    
   comment:       
       Comment text
       on 2 lines       
   charts:      
    
       - title: ВВП, темп прироста за 12 мес.
         names: GDP_yoy
    
       - title: Инвестиции, темп прироста за 12 мес.
         names: INVESTMENT_yoy


Выпуск:     
   comment:       
       Comment text
       on 2 lines       
   charts:    
       - title: Промышленное производство, темп прироста за 12 мес.
         names: INDPRO_yoy
         
       - title: Сельское хозяйство, темп прироста за 12 мес.
         names: AGROPROD_yoy

Цены:
   charts: 
       - names: CPI_rog
         title: Индекс потребительских цен (ИПЦ), в % пред.периоду
       
       - names: CPI_FOOD_rog, CPI_NONFOOD_rog, CPI_SERVICES_rog
         title: ИПЦ по компонентам, в % пред.периоду    
       

Дефицит(-)/профицит бюджета:    
   charts:     
       - names: GOV_SURPLUS_FEDERAL_bln_rub
         title: Федеральный бюджет, млрд.руб.

       - names: GOV_SURPLUS_SUBFEDERAL_bln_rub
         title: Региональные бюджеты, млрд.руб.

Внешняя торговля:    
   charts:     
       - names: EXPORT_GOODS_bln_usd, IMPORT_GOODS_bln_usd
         title: Экспорт и импорт товаров, млрд.долл.
    
       - names: TRADE_SURPLUS_bln_usd
         title: Сальдо торгового баланса, млрд.долл.
     
     
"""
z = yaml.load(doc)


from collections import namedtuple
Chart = namedtuple('Chart', 'names title')

def as_chart(d):
        title = d['title']
        names = [s.strip() for s in d['names'].split(',')]
        return Chart(names, title)
   
rows = {k: list(map(as_chart, v['charts'])) for k,v in z.items()}
print (rows)

    
df = dfq
df['TRADE_SURPLUS_bln_usd'] = (df['EXPORT_GOODS_bln_usd'] 
                             - df['IMPORT_GOODS_bln_usd'])    
for topic in rows.keys():
    # this becomes a header for a pair of graphs
    print(topic)
    for d in rows[topic]:
        plt.figure()
        try:
            plot_long(df[d.names],
                      title=d.title, 
                      start=2005)
        except KeyError:
            print ('Not plotted:', d)

# #a4: adapt code below to writing a PDF with charts to file

table_doc = """<table>
{% for item in items %}
<TR>
   <TD colspan=2>{{item.header}}</TD>
<TR>
   <TD>insert image 1 here </TD>
   <TD>insert image 2 here</TD>
</TR>
{% endfor %}
</table>"""
   
template_doc = """
<!DOCTYPE html>
<html>
<head lang="ru">
    <meta charset="UTF-8">
    <title>{{ page_header }}</title>
</head>
<body>
      insert table_doc here
</body>
</html>"""

from pathlib import Path
Path('ts.html').write_text(template_doc)


from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('ts.html')

template_vars = {"title" : "Sales Funnel Report - National",
                 "national_pivot_table": df.to_html()}
html_out = template.render(template_vars)

from weasyprint import HTML
HTML(string=html_out).write_pdf("ts.pdf")

# end - adapt code below to writing a PDF with charts to file


# what variables not grouped?    
groups = {
'GDP': ['GDP_bln_rub', 'GDP_yoy'],
'output': ['INDPRO_rog', 'INDPRO_yoy', 'AGROPROD_yoy', 
           'TRANSPORT_FREIGHT_bln_tkm'],
'prices': ['CPI_rog', 'PPI_rog', 'CPI_FOOD_rog', 'CPI_NONFOOD_rog', 
         'CPI_SERVICES_rog', 'CPI_ALCOHOL_rog',], 
'employment':['UNEMPL_pct'],
'wages': ['WAGE_NOMINAL_rub', 'WAGE_REAL_rog', 'WAGE_REAL_yoy'],
'foreing trade': ['IMPORT_GOODS_bln_usd', 'EXPORT_GOODS_bln_usd'],
'budget': ['GOV_EXPENSE_CONSOLIDATED_bln_rub',
       'GOV_EXPENSE_FEDERAL_bln_rub', 'GOV_EXPENSE_SUBFEDERAL_bln_rub',
       'GOV_REVENUE_CONSOLIDATED_bln_rub', 'GOV_REVENUE_FEDERAL_bln_rub',
       'GOV_REVENUE_SUBFEDERAL_bln_rub', 'GOV_SURPLUS_FEDERAL_bln_rub',
       'GOV_SURPLUS_SUBFEDERAL_bln_rub'],
'investment':  ['INVESTMENT_bln_rub', 'INVESTMENT_rog', 'INVESTMENT_yoy'] ,               

'retail sales': ['RETAIL_SALES_FOOD_bln_rub', 'RETAIL_SALES_FOOD_rog', 
                 'RETAIL_SALES_FOOD_yoy', 'RETAIL_SALES_NONFOOD_bln_rub', 
                 'RETAIL_SALES_NONFOOD_rog', 'RETAIL_SALES_NONFOOD_yoy', 
                 'RETAIL_SALES_bln_rub', 'RETAIL_SALES_rog', 
                 'RETAIL_SALES_yoy'],   
'corporate': ['CORP_RECEIVABLE_OVERDUE_bln_rub', 'CORP_RECEIVABLE_bln_rub']
}   
all_vars = list(set(dfa.columns + dfq.columns + dfm.columns))
x = [k for keys in groups.values() for k in keys]
not_found = [y for y in all_vars if y not in x]
print('Variables not grouped:\n', not_found)