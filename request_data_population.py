import time
import requests
import sqlite3
import json
import matplotlib.pyplot as plt

def gettime():
    return int(round(time.time()*1000))

def get_year_list(start_year, end_year):
    year_list = []
    for i in range(start_year, end_year+1):
        year_list.append(str(i))
    return year_list


if __name__ == '__main__':
    # get_total_population()

    headers = {}
    # transfer parameters
    keyvalue = {}
    start_year = 1999
    end_year =2018
    year_list = get_year_list(start_year ,end_year)
    # target website
    url = 'http://data.stats.gov.cn/easyquery.htm'
    # headers
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"

    conn = sqlite3.connect("data_1.db")
    conn.execute('''DROP TABLE data''')
    conn.commit()
    conn.execute('''CREATE TABLE data
           (Year          INT PRIMARY KEY  NOT NULL,
           Total          REAL     NOT NULL,
           Male           REAL     NOT NULL,
           Female         REAL     NOT NULL,
           Town           REAL     NOT NULL,
           Countryside    REAL     NOT NULL);''')

    for i in range(len(year_list)):
        keyvalue['m'] = 'QueryData'
        keyvalue['dbcode'] = 'hgnd'
        keyvalue['rowcode'] = 'zb'
        keyvalue['colcode'] = 'sj'
        keyvalue['wds'] = '[]'
        keyvalue['dfwds'] = '[{"wdcode":"zb","valuecode":"A0301"}]'
        keyvalue['k1'] = str(gettime())
        r = requests.get(url, headers=headers, params=keyvalue)
        # request
        # set up a Session
        s = requests.session()
        # request based on Session
        r = s.get(url, params=keyvalue, headers=headers)
        keyvalue['dfwds'] = '[{"wdcode":"sj","valuecode":"'+year_list[i]+'"}]'
        # request again
        r = s.get(url, params=keyvalue, headers=headers)
        # get data
        jsdata = json.loads(r.text)
        data = jsdata['returndata']['datanodes']

        conn.execute("INSERT INTO data (Year, Total, Male, Female, Town, Countryside) \
              VALUES (?, ?, ?, ?, ?, ? )", (year_list[i], float(data[0]['data']['data']), float(data[1]['data']['data']),\
                                    float(data[2]['data']['data']), float(data[3]['data']['data']), float(data[4]['data']['data'])))

        item = {
            'Year': year_list[i] ,
            'Total': data[0]['data']['data'],  # total population (10thousands)
            'Male': data[1]['data']['data'],  # male
            'Female': data[2]['data']['data'],  # female
            'Town': data[3]['data']['data'],  # town
            'Contryside': data[4]['data']['data'],  # countryside
        }
        conn.commit()
        print(item)
    conn.close()

