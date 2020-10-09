#!/bin/env python
import sys
import pymysql
from datetime import datetime

def transfer(filename):
    con = pymysql.connect('10.11.12.13', 'dashuser', 'dashpassword', 'bgbilling')
    data = []
    resfname = 'sber_' + datetime.now().strftime("%d-%m-%Y") + '.csv'

    with open(filename, encoding='cp1251') as file_in:
        for line in file_in:  
            data.append(line)
        
    with con.cursor() as cur:
        with open(resfname, 'w') as file_out:
            for line in data[:-1]:
                s = line.split(';')
                date = s[0]
                title = s[5]
                summ = s[-4]
                cur.execute("SELECT id FROM contract WHERE title = '" + title + "'")
                cid = str(cur.fetchone()[0])
                res = cid + ';' + summ + ';' + date + '\n'
                file_out.write(res)

if __name__ == '__main__':
    transfer(sys.argv[1])
