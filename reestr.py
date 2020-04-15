#!/bin/env python
"""
Скрипт для преобразования реестра Сбербанка в формат BGBilling
"""

import sys
import pymysql
from datetime import datetime

con = pymysql.connect('ip', 'user', 'password', 'base') # Подключение к базе
data = [] # Массив для промежуточных данных
resfname = 'sber_' + datetime.now().strftime("%d-%m-%Y") + '.csv' # Имя выходного файла

with open(sys.argv[1], encoding='cp1251') as file_in: # Сохранение данных входного файла в data
    for line in file_in:  
        data.append(line)
        
with con: #Подключаемся к базе
    cur = con.cursor()
    
    with open(resfname, 'w') as file_out: # Открываем выходной файл
        for line in data[:-1]: # Извлекаем данные из data
            s = line.split(';')
            date = s[0] # Дата платежа
            title = s[5] # Номер договора
            summ = s[-4] # Сумма платежа
            cur.execute("SELECT id FROM contract WHERE title = '" + title + "'") # Извлекаем из базы ID по номеру договора
            cid = str(cur.fetchone()[0])
            res = cid + ';' + summ + ';' + date + '\n' # Выходной формат данных
            file_out.write(res)
