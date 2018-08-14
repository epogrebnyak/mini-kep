[![Build Status](https://travis-ci.org/mini-kep/parser-rosstat-kep.svg?branch=master)](https://travis-ci.org/mini-kep/parser-rosstat-kep)
[![Build Status](https://travis-ci.org/mini-kep/parser-rosstat-kep.svg?branch=dev)](https://travis-ci.org/mini-kep/parser-rosstat-kep)
[![Coverage badge](https://codecov.io/gh/mini-kep/parser-rosstat-kep/branch/master/graphs/badge.svg)](https://codecov.io/gh/mini-kep/parser-rosstat-kep)


Parser          |                       KEP    
----------------|-------------------------------------------------------------------------------------------------
Data source     | [Short-term Economic Indicators (KEP) by Rosstat][Rosstat]
Parsing result  | [Annual, quarterly and monthly time series in CSV files][backend]
Releases        | [2018 schedule][schedule]

Concept
-------

In this repo I publish a dataset of Russian macroeconomic time series 
as machine-readable [CSV files][backend]. 
I keep track of monthly macroeconomic data releases (vintages) 
since April 2009.
Original files by Rosstat are in [MS Word format][Rosstat]. 


Interface 
---------

[manage.py](https://github.com/mini-kep/parser-rosstat-kep/blob/master/src/kep/manage.py) does the following job:
- download and unpack MS Word files from Rosstat
- convert MS Word to interim csv files
- parse interim csv files to get pandas dataframes with time series (at annual, quarterly and monthly frequency) 
- save dataframes as [CSV files at stable URL][backend] 
- create Excel file, if needed

[kep]: https://github.com/mini-kep/parser-rosstat-kep
[Rosstat]: http://www.gks.ru/wps/wcm/connect/rosstat_main/rosstat/ru/statistics/publications/catalog/doc_1140080765391
[backend]: https://github.com/mini-kep/parser-rosstat-kep/tree/master/data/processed/latest
[schedule]: http://www.gks.ru/gis/images/graf-oper2018.htm
[excel]: https://github.com/mini-kep/parser-rosstat-kep/tree/master/output/kep.xlsx

Access to parsing result
------------------------

Stable URL: <https://github.com/mini-kep/parser-rosstat-kep/tree/master/data/processed/latest> 



```python
import pandas as pd

def get_dataframe_from_web(freq):
    filename = f'df{freq}.csv'
    url = ('https://raw.githubusercontent.com/mini-kep/parser-rosstat-kep/'
          f'master/data/processed/latest/{filename}')
    return pd.read_csv(url, converters={0: pd.to_datetime}, index_col=0)

dfa, dfq, dfm = (get_dataframe_from_web(freq) for freq in 'aqm')
```
 
Repo management
---------------

Around [this schedule][schedule] on a Windows machine I run:   

```
invoke add <year> <month>
```

and commit changes to this repo.

This command:
- downloads a rar file from Rosstat, 
- unpacks MS Word files, 
- dumps all tables from MS Word files to an interim CSV file, 
- parses interim CSV file to three dataframes by frequency 
- validates parsing result
- transforms some variables (eg. deaccumulates government expenditures)
- saves dataframes as processed CSV files
- saves csv for latest date
- saves an Excel file for latest date.

Same job can be done by [manage.py](https://github.com/mini-kep/parser-rosstat-kep/blob/master/src/manage.py)

Parcer summary
--------------

Parcer              |  mini-kep 
--------------------|----------------------------------------
Job                 |  Parse sections of Short-term Economic Indicators (KEP) monthly Rosstat publication 
Source URL          |  [Rosstat KEP page](http://www.gks.ru/wps/wcm/connect/rosstat_main/rosstat/ru/statistics/publications/catalog/doc_1140080765391)
Source type         |  MS Word  <!-- Word, Excel, CSV, HTML, XML, API, other -->
Frequency           |  Monthly
When released       |  Start of month as in [schedule](http://www.gks.ru/gis/images/graf-oper2017.htm) 
Code                | <https://github.com/epogrebnyak/mini-kep/tree/master/src/>
Test health         |  [![Build Status](https://travis-ci.org/mini-kep/parser-rosstat-kep.svg?branch=master)](https://travis-ci.org/mini-kep/parser-rosstat-kep)
Test coverage       |  [![Coverage badge](https://codecov.io/gh/mini-kep/parser-rosstat-kep/branch/master/graphs/badge.svg)](https://codecov.io/gh/mini-kep/parser-rosstat-kep)
Documentation       |  [![Documentation Status](https://readthedocs.org/projects/mini-kep-parcer-for-rosstat-kep-publication/badge/?version=latest)](http://mini-kep-parcer-for-rosstat-kep-publication.readthedocs.io/en/latest/?badge=latest)
CSV endpoint        | <https://github.com/epogrebnyak/mini-kep/tree/master/data/processed/latest>
Transformation      |  Government revenue/expenses deaccumaulated to monthly values 
Validation          |  Hardcoded checkpoints and consistency checks 


All historic raw data available on internet? 
- [ ] Yes
- [x] No (data prior to 2016-12 is in this repo only)  



Notes
-----

- We follow [cookiecutter-data-science](https://github.com/drivendata/cookiecutter-data-science) template for 
directory structure. 

- Windows and MS Word are required to create interim text dumps from MS Word files. Оnce these text files are created, they can be parsed on a linux machine.

- This repo replaces a predecessor, [data-rosstat-kep](https://github.com/epogrebnyak/data-rosstat-kep), which could not handle vintages of macroeconomic data. 
