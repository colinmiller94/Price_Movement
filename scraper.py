import pandas as pd
import math
import sqlite3
import datetime
import numpy as np
import warnings
import random
from collections import Counter

#Tickers to be selected for prediction
tickers = ['BAC', 'XLF', 'EEM', 'TVIX', 'MU', 'GE','NVCN','PBR', 'VXX']
pred_ticker = 'SPY'
tickers.append(pred_ticker)
num_days = 60


#K-nearest parameters
test_size = 0.5
train_set= {1:[], 0:[], -1:[]}
test_set= {1:[], 0:[], -1:[]}

#Most k_nearest code, including the majority of this function was taken from Sentdex's YouTube ML tutorial video series
def k_nearest_neighbors(data, predict, k):
    if len(data) >= k:
        warnings.warn('K is set to value of less than total voting groups')

    distances = []
    for group in data:
        for features in data[group]:
            euclidean_dist = np.linalg.norm(np.array(features) - np.array(predict))
            distances.append([euclidean_dist, group])

    votes = [i[1] for i in sorted(distances)[:k]]
    vote_result = Counter(votes).most_common(1)[0][0]

    magnitude = sum(votes)/len(votes)

    return vote_result, magnitude



# "05/25/2018" ----> "2018-05-25"
def convert_date(dstring):
    newstring = dstring[-4:]+ "-" + dstring[0:2]+"-" +dstring[3:5]
    return newstring


def classify_returns(ret):
    if ret == 0:
        return 0
    elif ret > 0:
        return 1
    return -1


def reset_tables():
    for ticker in tickers:
        c.execute("drop table hist_ret_" +ticker + ";")


def init_tables():
    for ticker in tickers:
        query ="CREATE TABLE hist_ret_" + ticker + "(ticker text,date date,return integer)"
        c.execute(query)


def pull_data():
    query = "select MAX(date) from hist_ret_"+tickers[-1] +";"
    c.execute(query)
    max_date = c.fetchone()[0]

    if max_date == None:
        num_days= 60
        recalc_num_days = False
    else:
        recalc_num_days = True

    for ticker in tickers:
        url = 'https://www.nasdaq.com/symbol/'+ ticker + '/historical'

        dfs = pd.read_html(url)
        df = dfs[2]
        column_string = df.columns.values[4]


        dates = df['Date'].tolist()[0:]
        dates = [str(date) for date in dates]
        #print(dates)
        closes = df[column_string].tolist()[0:]
        closes =[str(close) for close in closes]
        #print(closes)

        new_dates = []
        new_closes = []

        for i in range(len(dates)):
            if len(dates[i]) == 10:
                new_dates.append(dates[i])
                new_closes.append(closes[i])

        if ticker == pred_ticker:
            new_closes = [new_closes[0]] + new_closes[:-1]


        if recalc_num_days:
            num_days = 0
            for day in new_dates:
                if (datetime.datetime.strptime(day, "%m/%d/%Y").date() - datetime.datetime.strptime(max_date, "%Y-%m-%d").date()).days > 0:
                    num_days+=1

        new_closes = [float(close) for close in new_closes]


        i = 0
        returns = []
        while i < num_days:
            daily_return = math.log(new_closes[i] /new_closes[i+1])
            returns.append(daily_return)
            i +=1
            #print(len(returns))
        new_dates = [convert_date(str(date)) for date in new_dates[:num_days]]

        if ticker == pred_ticker:
            returns = [classify_returns(i) for i in returns]

        for i in range(len(new_dates)):
            query = "INSERT INTO hist_ret_" +ticker + "(ticker, date, return) values (" + "\'" + ticker + "\'" + "," +  "\'" +new_dates[i] + "\'" +"," + str(returns[i])[:6] + ");"
            #print(query)
            c.execute(query)


def learn():
    returns_list = []
    for ticker in tickers:

        query = "select * from hist_ret_" + ticker + ";"
        df = pd.read_sql_query(query, conn)
        returns = df['return'].tolist()

        returns_list.append(returns)

    new_returns_list = []

    i = 0
    while i < len(returns_list[-1]):
        j = 0
        list =[]
        while j < len(returns_list):
            list.append(returns_list[j][i])
            j += 1
        new_returns_list.append(list)
        i+=1
    predict_list = new_returns_list[0][:-1]
    new_returns_list = new_returns_list[1:]
    random.shuffle(new_returns_list)
    train_data = new_returns_list[:-int(test_size * len(new_returns_list))]
    test_data = new_returns_list[-int(test_size * len(new_returns_list)):]

    for i in train_data:
        train_set[i[-1]].append(i[:-1])
        #print(train_data)

    for i in test_data:
        test_set[i[-1]].append(i[:-1])

    correct = 0
    total = 0


    prediction, magnitude = k_nearest_neighbors(train_set, predict_list, k = 11)
    print("Today's Resuls: ")
    print("Prediction: ", prediction)
    print("Magnitude(-1<m<1): ", magnitude,"\n")

    for group in test_set:
        for data in test_set[group]:
            vote, magnitude= k_nearest_neighbors(train_set,data,k =11)
            if group == vote:
                correct +=1
            total +=1

    print("Backtest Results: ")
    print('Correct: ',correct)
    print('Total: ',total)
    print('Accuracy: ',correct/total)

    return prediction, correct, total

#Connect to database
conn = sqlite3.connect('returns.db')
c = conn.cursor()

#
# reset_tables()
# init_tables()
pull_data()
learn()

conn.commit()
conn.close()