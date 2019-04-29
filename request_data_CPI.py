import time
import requests
import sqlite3
import json
import matplotlib.pyplot as plt

def gettime():
    return int(round(time.time()*1000))

def get_year_list(start_year, end_year):
    year_list = []
    for i in reversed(range(start_year,end_year+1)):
        year_list.append(str(i))
    return year_list
'''
not finished
'''

if __name__ == '__main__':
    # get_total_population()

    headers = {}
    # transfer parameters
    keyvalue = {}
    start_year = 2009
    end_year =2018
    year_list = get_year_list(start_year ,end_year)
    # target website
    url = 'http://data.stats.gov.cn/easyquery.htm'

    # headers
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"

    conn = sqlite3.connect("data_cpi.db")
    conn.execute('''DROP TABLE data_cpi''')
    conn.commit()
    conn.execute('''CREATE TABLE data_cpi
           (Year           INT PRIMARY KEY  NOT NULL,
           CPI             REAL     NOT NULL,
           Town_CPI          REAL     NOT NULL,
           Countryside_CPI   REAL     NOT NULL);''')

    keyvalue['m'] = 'QueryData'
    keyvalue['dbcode'] = 'hgnd'
    keyvalue['rowcode'] = 'zb'
    keyvalue['colcode'] = 'sj'
    keyvalue['wds'] = '[]'
    keyvalue['dfwds'] = '[{"wdcode":"zb","valuecode":"A0901"}]'
    keyvalue['k1'] = str(gettime())
    r = requests.get(url, headers=headers, params=keyvalue)

    jsdata = json.loads(r.text)
    data = jsdata['returndata']['datanodes']

    for i in range(len(year_list)):

        conn.execute("INSERT INTO data_cpi (Year, CPI, Town_CPI, Countryside_CPI) \
              VALUES (?, ?, ?, ?)", (year_list[i], float(data[i]['data']['data']), float(data[i+len(year_list)]['data']['data']),float(data[i+2*len(year_list)]['data']['data'])))

        item = {
            'Year': year_list[i] ,
            'CPI': data[i]['data']['data'],
            'Town_CPI': data[i+len(year_list)]['data']['data'],
            'Countryside_CPI': data[i+2*len(year_list)]['data']['data']
        }
        conn.commit()
        print(item)
    conn.close()

