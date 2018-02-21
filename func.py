from pandas import read_csv
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.dates as md
import datetime as dt
import seaborn as sns
from tqdm import tqdm
import time


def read_data(path,sep):
    """чтение исходных данных"""
    if os.path.exists(path):
        rowdata = read_csv(path, sep=sep)
    else:
        print("Файл", os.path.abspath(path), " не существует")
    if not rowdata.empty:
        print("Масив", os.path.abspath(path), "прочитан")
    else:
        print("Ошибка чтения масива", os.path.abspath(path))
    return rowdata


def find_min_max(data):
    time.sleep(0.05)
    window_width = 100
    #half_wifth =

    n = int(window_width * 0.04)
    cur = int(window_width * 0.3)

    l = range(0, len(data.index) - window_width)

    list = []

    for pie_data in tqdm(map(lambda x: data[x: x + window_width], l), total=len(l)):
        window_width = window_width
        n_cur_items = 2
        n = n

        rate_max = 0.95
        rate_min = 0.05

        cur = cur

        cur_val_begin = pie_data.iloc[cur]
        cur_val_end = pie_data.iloc[window_width - cur]

        #cur_val_begin = pie_data[0: n_cur_items]
        #cur_val_end = pie_data[window_width - n_cur_items: window_width]

        #cur_val_begin = cur_val_begin.sum() / n_cur_items
        #cur_val_end = cur_val_end.sum() / n_cur_items


        max = pie_data.nlargest(n)
        min = pie_data.nsmallest(n)
        max = max.sum() / n
        min = min.sum() / n

        if cur_val_begin > min:
            rate_b = (cur_val_begin - min) / (max - min)
        else:
            rate_b = 0.001 / (max - min)

        if cur_val_end > min:
            rate_e = (cur_val_end - min) / (max - min)
        else:
            rate_e = 0.001 / (max - min)

        if rate_b > rate_max:
            list.append([pie_data.index[cur], 'max'])
        elif rate_b < rate_min:
            list.append([pie_data.index[cur], 'min'])

        if rate_e > rate_max:
            list.append([pie_data.index[window_width - cur], 'max'])
        elif rate_e < rate_min:
            list.append([pie_data.index[window_width - cur], 'min'])
    time.sleep(0.1)
    return list


def exponential_smoothing(series, alpha):
    time.sleep(0.1)
    result = series.copy(deep=True)
    fff = len(series) - 2

    #result.iloc[1:l] = (alpha * result.iloc[1:l] + (1 - alpha) * result.iloc[0:l - 1])

    for n in tqdm(range(fff, 0, -1)):
        result.iloc[n] = (alpha * result.iloc[n] + (1 - alpha) * result.iloc[n+1])
    #result.append(result[k-1])
    time.sleep(0.1)
    return result


def print_graph(data, z):
    sns.set()

    plt.xticks(rotation=25)
    ax = plt.gca()
    xfmt = md.DateFormatter('%H:%M %d-%m-%Y ')
    ax.xaxis.set_major_formatter(xfmt)

    # plt.plot(x, color = 'grey')

    # xmin = [dt.datetime.fromtimestamp(ts) for ts in xmin]
    # plt.plot(xmin, ymin, 'ro', color='green')

    # xmax = [dt.datetime.fromtimestamp(ts) for ts in xmax]
    # plt.plot(xmax, ymax, 'ro', color='red')

    # print(xmax)

    c = [dt.datetime.fromtimestamp(ts) for ts in z.index]
    plt.plot(c, z, color='xkcd:silver', alpha=1)

    c = [dt.datetime.fromtimestamp(ts) for ts in data.index]
    plt.plot(c, data.price, color='xkcd:cerulean', linewidth=1.5)
    '''

    for a in range(0, len(data.index)):
        if data.iloc[a, 1] == 'min':
            if data.iloc[a + 1, 1] == 'min':
                x1 = dt.datetime.fromtimestamp(data.index[a])
                x2 = dt.datetime.fromtimestamp(data.index[a + 1])
                y1 = data.iloc[a, 0]
                y2 = data.iloc[a + 1, 0]
                plt.plot([x1, x2], [y1, y2], color='xkcd:jade', linewidth=3, alpha=0.7)

    for a in range(0, len(data.index)):
        if data.iloc[a, 2] == 'max':
            if data.iloc[a + 1, 2] == 'max':
                x1 = dt.datetime.fromtimestamp(data.index[a])
                x2 = dt.datetime.fromtimestamp(data.index[a + 1])
                y1 = data.iloc[a, 0]
                y2 = data.iloc[a + 1, 0]
                plt.plot([x1, x2], [y1, y2], color='xkcd:dull red', linewidth=3, alpha=0.7)
    '''
    '''
    a = 0
    while a < len(data) - 1:
        a = a + 1
        if data.iloc[a, 4] == 'up':
            i = 1
            for i in range(1, len(data) - a -3):
                #print(a, i, a + i, len(data))
                if data.iloc[a, 4] != data.iloc[a + i, 4]:
                    x1 = dt.datetime.fromtimestamp(data.index[a])
                    x2 = dt.datetime.fromtimestamp(data.index[a + i])
                    y1 = data.iloc[a, 0]
                    y2 = data.iloc[a + i, 0]
                    plt.plot([x1, x2], [y1, y2], color='xkcd:red', linewidth=1, alpha=0.7)

                    a = a + i
                    break
    '''
    tmp_d = None
    tmp_u = None
    for cur in range(0, len(data) - 1):
        if data.iloc[cur, 4] == '' and data.iloc[cur + 1, 4] == 'up':
            tmp_u = cur + 1
        if data.iloc[cur, 4] == 'up' and data.iloc[cur + 1, 4] == '':
                x1 = dt.datetime.fromtimestamp(data.index[tmp_u])
                x2 = dt.datetime.fromtimestamp(data.index[cur])
                y1 = data.iloc[tmp_u, 0]
                y2 = data.iloc[cur, 0]
                plt.plot([x1, x2], [y1, y2], color='xkcd:red', linewidth=1, alpha=0.7)

        if data.iloc[cur, 5] == '' and data.iloc[cur + 1, 5] == 'down':
            tmp_d = cur + 1
        if data.iloc[cur, 5] == 'down' and data.iloc[cur + 1, 5] == '':
            x1 = dt.datetime.fromtimestamp(data.index[tmp_d])
            x2 = dt.datetime.fromtimestamp(data.index[cur])
            y1 = data.iloc[tmp_d, 0]
            y2 = data.iloc[cur, 0]
            plt.plot([x1, x2], [y1, y2], color='xkcd:green', linewidth=1, alpha=0.7)

    '''
    a = 0
    while a < len(data) - 1:
        a = a + 1
        if data.iloc[a, 5] == 'down':
            i = 1
            for i in range(1, len(data) - a - 3):
                #print(a, i, a + i, len(data))
                if data.iloc[a, 5] != data.iloc[a + i, 5]:
                    x1 = dt.datetime.fromtimestamp(data.index[a])
                    x2 = dt.datetime.fromtimestamp(data.index[a + i])
                    y1 = data.iloc[a, 0]
                    y2 = data.iloc[a + i, 0]
                    plt.plot([x1, x2], [y1, y2], color='xkcd:green', linewidth=1, alpha=0.7)

                    a = a + i
                    break
    '''





    plt.show()

    return


def add_flags(data):
    data.insert(3, 'flag', False)
    len_data = len(data)
    pr_row = 0
    cur_row = 0

    time.sleep(0.07)
    for next_row in tqdm(data.itertuples(index=True), total=len_data):
        #print(next_row)
        if cur_row == 0:
            if pr_row == 0:
                pr_row = next_row
            else:
                cur_row = next_row
        else:

            if pr_row.min != cur_row.min and cur_row.min == next_row.min:
                if cur_row.min == 'min':
                    data.loc[cur_row.Index, 'flag'] = True
                else:
                    data.loc[pr_row.Index, 'flag'] = True
            elif pr_row.max != cur_row.max and cur_row.max == next_row.max:
                if cur_row.max == 'max':
                    data.loc[cur_row.Index, 'flag'] = True
                else:
                    data.loc[pr_row.Index, 'flag'] = True
            pr_row = cur_row
            cur_row = next_row
    time.sleep(0.07)


    '''
    for i in range(1, len(data.index) - 1):

        if (data.iloc[i - 1, 1] != data.iloc[i, 1]) and (data.iloc[i, 1] == data.iloc[i + 1, 1]):
            if data.iloc[i, 1] == 'min':
                data.iloc[i, 3] = True
            else:
                data.iloc[i-1, 3] = True

        if (data.iloc[i - 1, 2] != data.iloc[i, 2]) and (data.iloc[i, 2] == data.iloc[i + 1, 2]):
            if data.iloc[i, 2] == 'max':
                data.iloc[i, 3] = True
            else:
                data.iloc[i-1, 3] = True
    '''

    return


def add_up_col(data):
    data.insert(4, 'up', '')
    data.insert(5, 'down', '')
    #print(data)
    mas = data[data['flag'] == True]
    #print(mas)
    #print(mas.iloc[0])
    #print(mas.iloc[1])
    tmp = False
    tmp_row = False

    '''
    for row in tqdm(gen, total=len(mas)):
        if tmp_row == False:
            tmp_row = row
            #tmp = row.price
        else:
            a = tmp_row.Index - 60
            b = row.Index + 60

            if tmp_row.min == 'min':
                cur = data.loc[a:b, 'price'].nsmallest(1)
            elif tmp_row.max == 'max':
                cur = data.loc[a:b, 'price'].nlargest(1)
            else:
                print('error up down')

            a = tmp.index[0]
            b = cur.index[0]
            a_price = tmp.iloc[0]
            b_price = cur.iloc[0]

            if tmp.price < cur.price:
                if (b_price % a_price > a_price / 125) or data.loc[a - 120, 'up'] == 'up':
                    data.loc[a:b, 'up'] = 'up'
                    tmp = cur
            else:
                if (a_price % b_price > a_price / 125) or data.loc[a - 120, 'down'] == 'down':
                    data.loc[a:b, 'down'] = 'down'
                    tmp = cur




    '''
    loc_tmp = False

    time.sleep(0.07)
    for i in tqdm(range(0, len(mas) - 1, 2)):
        a = mas.index[i] - 60
        b = mas.index[i + 1] + 60

        if mas.iloc[i, 1] == 'min':
            cur = data.loc[a:b, 'price'].nsmallest(1)
        elif mas.iloc[i, 2] == 'max':
            cur = data.loc[a:b, 'price'].nlargest(1)
        else:
            print('error up down')
        if i > 0:
            a = tmp.index[0]
            b = cur.index[0]
            a_price = tmp.iloc[0]
            b_price = cur.iloc[0]
            if a_price < b_price:
                if (b_price % a_price > a_price / 65) or loc_tmp == 'up':
                    data.loc[a:b, 'up'] = 'up'
                    loc_tmp = 'up'
                    tmp = cur
            else:
                if (a_price % b_price > a_price / 65) or loc_tmp == 'down':
                    data.loc[a:b, 'down'] = 'down'
                    loc_tmp = 'down'
                    tmp = cur
        if i == 0:
            tmp = cur
    time.sleep(0.07)

    return

def add_up_col_old(data):
    data.insert(4, 'up', '')
    data.insert(5, 'down', '')
    #print(data)
    mas = data[data['flag'] == True]
    #print(mas)
    #print(mas.iloc[0])
    #print(mas.iloc[1])

    tmp = False

    #print(data)
    print(mas)
    for i in range(0, len(mas) - 1, 2):
        a = mas.index[i] - 60
        b = mas.index[i + 1] + 60

        if mas.iloc[i, 1] == 'min':
            cur = data.loc[a:b, 'price'].nsmallest(1)
        elif mas.iloc[i, 2] == 'max':
            cur = data.loc[a:b, 'price'].nlargest(1)
        else:
            print('error up down')

        #print(a % 100000, b % 100000, ' = ', cur.iloc[0], cur)
        #print('sss')
        if i > 0:
            #print('hhh', tmp, cur)
            a = tmp.index[0]
            b = cur.index[0]
            a_price = tmp.iloc[0]
            b_price = cur.iloc[0]
            print(data.loc[a - 120, 'up'])
            print(data.loc[a - 120, 'down'])
            if a_price < b_price:
                print(a, b, a_price, b_price, i)
                if (b_price % a_price > a_price / 125) or data.loc[a - 120, 'up'] == 'up':
                    data.loc[a:b, 'up'] = 'up'
                    tmp = cur
            else:
                print(a, b, a_price, b_price, i)
                if (a_price % b_price > a_price / 125) or data.loc[a - 120, 'down'] == 'down':
                    data.loc[a:b, 'down'] = 'down'
                    tmp = cur
        if i == 0:
            tmp = cur
    return

def find_delta(data):
    data.insert(6, 'delta', '0')
    tmp = 0
    len_data = len(data)
    tmp_data = []
    time.sleep(0.07)
    tmp_row = data.iloc[0]
    tmp = data.index[0]
    #print(tmp_row)

    for row in tqdm(data[1:len_data - 1].itertuples(index=True), total=len_data - 2):
        #print(row.price)
        #print(row)
        if tmp_row.up != row.up:
            cur_price = row.price
            data.loc[tmp:row.Index + 60, 'delta'] = (abs(data.loc[tmp:row.Index + 60, 'price'] - cur_price) / cur_price)* 100
            tmp_data.append((abs(tmp_row.price - cur_price) / cur_price) * 100)
            tmp_row = row
            tmp = row.Index
    #print(data)

    time.sleep(0.07)


    '''
    for i in tqdm(range(1, len(data) - 1, 1)):
        if data.iloc[i - 1, 4] != data.iloc[i, 4]:
            cur_price = data.iloc[i, 0]
            for a in range(tmp, i + 1):
                data.iloc[a, 6] = (abs(data.iloc[a, 0] - cur_price) / cur_price)*100
            tmp_data.append((abs(data.iloc[tmp, 0] - cur_price) / cur_price) * 100)
            tmp = i
    time.sleep(0.07)
    '''

    #tmp_data = data.loc[data['delta'] != '0']
    #print(tmp_data)
    #tmp_data = tmp_data['delta']
    #print(tmp_data)
    tmp_data = pd.Series(tmp_data)
    tmp_data = tmp_data[1:]

    tmp_sum = tmp_data.value_counts().sum()
    #tmp_sum = tmp_data.sum()
    print('\nsum: ', tmp_sum, 'min: ', tmp_data.min(), 'max: ', tmp_data.max())
    #tmp_data.plot(kind='bar')

    tmp_data = tmp_data.sort_values(ascending=True)
    #print(tmp_data)
    res_list = []
    for k in range(3, 10):
        size = tmp_sum / k
        loc_tmp = 0
        list = []
        list.append(0)
        list.append(0.6)
        #print(k, end='')
        for z in tmp_data:
            if loc_tmp >= size:
                list.append(z)
                #print('%5.2f' % z, end='')
                loc_tmp = 0
            loc_tmp = loc_tmp + 1
        list.append(9999999999)
        res_list.append(list)
        #print()


    #plt.show()


    #print(tmp_data.sum())
    #plt.plot(data.delta, color='xkcd:violet', linewidth=1, alpha=0.7)



    return res_list


def add_profit_class(data, edges):
    #n = 8
    edges = [0, 1.1, 3.06, 6.55, 9999999]
    n = len(edges)

    s = 7 #Индекс первого столбца

    print(n, edges)
    for a in range(0, n - 1):
        name = 'pclass' + str(a)
        i = a + s
        data.insert(i, name, '0')
        data[name] = data['delta'].apply(lambda x: 1 if float(x) > float(edges[a]) and float(x) < float(edges[a + 1]) else 0)

    return


def save_data(data):
    data.to_csv('processed_data.csv', index=True, sep=';')
    return


def get_processing_array(data, ind, delta, num):
    l = range(ind, ind - delta*(num), -delta)
    res_list = []
    for pie in map(lambda x: data[x - delta: x], l):
        res_list.append(pie.sum() / delta)
    return res_list


def get_processing_array2(data, delta):
    lendata = len(data)
    l = range(0, lendata, delta)
    res_list = []
    for pie in map(lambda x: data[x: x + delta], l):
        res_list.append(pie.sum() / delta)
    return res_list


def rrr(data):
    f = data.values
    print(f)

    return



