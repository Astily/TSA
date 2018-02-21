from func import *
from pandas import read_csv
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.dates as md
import datetime as dt
import seaborn as sns
import time




PATH = "usddata.csv"
s_data = 30
t_data_b = 10
t_data_c = 30
t_data_d = 180
y_data = 6

x_train_a = np.zeros((10, s_data))
x_train_b = np.zeros((10, s_data))
x_train_c = np.zeros((10, s_data))
x_train_d = np.zeros((10, s_data))

y_train = np.zeros((10, y_data))

print('Чтение файла: ', PATH)
#чтение исходных данных
rowdata = read_data(PATH, ',')
rowdata.index = rowdata.Timestamp
#print(rowdata)

#подсчет длины масива
lendata = len(rowdata.index)
print('Количество прочитаных строк: ',lendata)

i = lendata

#rowdata.info()

#вывод исходного графика
#rowdata['Timestamp'] = pd.to_datetime(rowdata['Timestamp'],unit='s')
#rowdata.plot(x='Timestamp', y='Weighted_Price')
#plt.show(block = True)

'''
def f_train_a(a):
    a -= 1
    r = rowdata.Weighted_Price[a]
    return r

def f_train_b(a):
    a -= 1
    k = 0
    r = 0
    while(k < t_data_b):
        r += rowdata.Weighted_Price[a-k]
        k = k + 1
    r = r / t_data_b
    return r

def f_train_c(a):
    a -= 1
    k = 0
    r = 0
    while(k < t_data_c):
        r += rowdata.Weighted_Price[a-k]
        k = k + 1
    r = r / t_data_c
    return r

def f_train_d(a):
    a -= 1
    k = 0
    r = 0
    while(k < t_data_d):
        r += rowdata.Weighted_Price[a-k]
        k = k + 1
    r = r / t_data_d
    return r

i=0
while(i<0):

    # заполнение масива А
    j=0
    while(j<s_data):
        x_train_a[i,j]=f_train_a(i+1184428-j)
        j=j+1

    # заполнение масива B
    j = 0
    while (j < s_data):
        x_train_b[i, j] = f_train_b(i + 1184428 - j*t_data_b)
        j = j + 1

    # заполнение масива C
    j = 0
    while (j < s_data):
        x_train_c[i, j] = f_train_c(i + 1184428 - j * t_data_c)
        j = j + 1

    # заполнение масива D
    j = 0
    while (j < s_data):
        x_train_d[i, j] = f_train_d(i + 1184428 - j * t_data_d)
        j = j + 1
    i = i + 1
'''
'''yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'''
"""
l = 0
i = random.randint(1200000, 1459070)
while(l < 10):
    #i = i+3
    i = random.randint(1200000, 1459070)

    pie_data = rowdata.Weighted_Price[i:i+30]
    cur_val = rowdata.Weighted_Price[i-2:i+3]
    print(cur_val)
    cur_val = cur_val.sum() / 5
    median = pie_data.median()
    #print(pie_data)

    max = pie_data.nlargest(5)
    min = pie_data.nsmallest(5)
    max = max.sum() / 5
    min = min.sum() / 5

   # '''
    abs_max = abs(cur_val - max)
    abs_min = abs(cur_val - min)
    abs_median = abs(cur_val - median)

    if abs_max > abs_min :
        print('курс растет')
    else:
        print('курс падает')

    '''print('-')
    if abs(abs_median - abs_max) > abs(abs_median - abs_min) and abs_max > abs_min :
        print('курс растет')
    if abs(abs_median - abs_max) < abs(abs_median - abs_min) and abs_max < abs_min :
        print('курс падает')'''
    


    if cur_val > min:
        rate = (cur_val - min) / (max - min)
    else:
        rate = 0.01 / (max - min)

    if rate > 0.9:
        print('мы в максимуме')
    if rate < 0.1:
        print('мы в минимуме')

    print()



    pie_data.plot()
    plt.show()
    #'''

    l = l + 1
"""


elem = 14000
start_elem = 1038115
start_elem = random.randint(1100000, lendata - elem)
#start_elem = 1163977

start_elem = 1038115
#elem = lendata - start_elem - 100


print('\nВыборка элементов начиная с: ', start_elem, ',длинной: ', elem)
#x = rowdata.Weighted_Price[start_elem: start_elem + elem]
x = rowdata.Weighted_Price[start_elem:]

#rrr(x)

print('Сглаживание данных')
z = exponential_smoothing(x, 0.2)
#z = exponential_smoothing(z, 0.07)


print('Поиск минимумов и максимумов')

list_min_max = find_min_max(z)

print('Транспонирование данных')
data = pd.DataFrame({"price": x})

tmp_d = pd.DataFrame(list_min_max)
tmp_d.columns = ['time', 'maxmin' ]
tmp_d.index = tmp_d['time']
tmp_d = tmp_d.drop('time', 1)

data = data.merge(tmp_d[tmp_d.maxmin == 'min'], left_index=True, right_index=True, how='left')
data = data.merge(tmp_d[tmp_d.maxmin == 'max'], left_index=True, right_index=True, how='left')
data.columns = ['price', 'min', 'max']
#print(data.min[data['min'] != 'min'])
#data.min[data.min != 'min'] = ''
##print(data)


'''
print('Транспонирование данных')
data = pd.DataFrame({"price": x})
data.insert(1, 'min', '')
data.insert(2, 'max', '')

for k in tqdm(list_min_max):
    if k[1] == 'min':
        data.loc[k[0], 'min'] = 'min'
    elif k[1] == 'max':
        data.loc[k[0], 'max'] = 'max'
'''


print('Добавление флагов границ, минимумов и максимумов')
add_flags(data)
#print(data)

print('Определение направления движения')
add_up_col(data)

data.index.name = 'timestamp'


print('Вычисление силы движения')
edges = find_delta(data)

print(edges)
#n = int(input())
n = 2
#edges = [0, 0.6, 1.09, 1.45, 2.23, 2.72, 3.06, 6.55, 9999999]
add_profit_class(data, edges[n])

print('Сохранение данных')
save_data(data)



print('Генерация графика')
print_graph(data, z)



print('\nЗавершение работы')




#print(x_train_a.dtype)
#print(x_train_c)


