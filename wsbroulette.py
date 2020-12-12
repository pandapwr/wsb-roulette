from wallstreet import Stock, Call, Put
from tabulate import tabulate
import datetime
import sys
import os
import warnings
import argparse
import numpy as np, numpy.random
import threading
from random import randint, randrange
from math import floor

warnings.filterwarnings('ignore', 'The iteration is not making good progress')

ap = argparse.ArgumentParser()
ap.add_argument("-t","--tickers", required=True, help="List of tickers")
ap.add_argument("-e","--expiration_range", default=4, required=False, help="Expiration Date Range")
ap.add_argument("-s","--strike_range", default=3, required=False, help="Strike Range")
ap.add_argument("-b","--balance", required=True, help="Account Balance")
ap.add_argument("-d","--distribution", default=10, required=False, help="Distribution of funds")
ap.add_argument("-f","--fd", action="store_true", required=False, help="FD mode")
args = ap.parse_args()

expiration_range = args.expiration_range
strikes_range = int(args.strike_range)
account_balance = float(args.balance)
option_distribution = args.distribution

if args.fd:
    expiration_range = 1


#tickers = ["TSLA","NIO","GME","BB","PLTR","MSFT","MRNA","DIS","SPY","CRSR"]
tickers = args.tickers.split(",")
options = ["P", "C"]
options_list = []
current_date = datetime.datetime.now()
total = 0


def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

def calc_dte(date):
    day = datetime.datetime.strptime(date, '%d-%m-%Y')
    dte = day - datetime.datetime.now()
    return (int(dte.days)+1)

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx], idx

def grab_options(ticker, cost):
    underlying = Stock(ticker)
    option = options[randint(0,1)]
    
    available_cash = round(account_balance * cost,2)
    
    if option == "P":
        g = Put(ticker, d=current_date.day, m=current_date.month, y=current_date.year)
    else:
        g = Call(ticker, d=current_date.day, m=current_date.month, y=current_date.year)

    expiration = datetime.datetime.strptime(g.expirations[randint(0,expiration_range)], '%d-%m-%Y')

    
    if option == "P":
        g = Put(ticker, d=expiration.day, m=expiration.month, y=expiration.year)
    else:
        g = Call(ticker, d=expiration.day, m=expiration.month, y=expiration.year)

    strikes_arr = np.array(g.strikes)
    
    if args.fd:
        if option == "P":
            strike_offset = -1 * randint(2, 5)
        else:
            strike_offset = randint(2, 5)
    else:
        strike_offset = [-1,1][randrange(2)] * randint(0, strikes_range)
    
    
    nearest_strike, strike_index = find_nearest(strikes_arr, underlying.price)
    strike_index = strike_index + strike_offset
    new_strike = strikes_arr[strike_index]
    
    g.set_strike(new_strike)

    exp_date = f"{expiration.month}/{expiration.day}/{expiration.year}"
    
    qty = floor(available_cash/(g.price*100))
    total_cost = qty*g.price*100
    price = "{:.2f}".format(g.price)
    iv = abs(round(g.delta()*100, 1))
    delta = round(g.delta(), 3)
    theta = round(g.theta(), 3)
    gamma = round(g.gamma(), 3)
    vega = round(g.vega(), 3)
    rho = round(g.rho(), 3)
    
    options_list.append([f'${ticker} {exp_date} {new_strike}{option}',f'${underlying.price}', f'${price}', qty, total_cost, iv, delta, theta, gamma, vega, rho])


print(
'''
   __       __   ______   _______         _______                       __              __      __               
  /  |  _  /  | /      \ /       \       /       \                     /  |            /  |    /  |              
  $$ | / \ $$ |/$$$$$$  |$$$$$$$  |      $$$$$$$  |  ______   __    __ $$ |  ______   _$$ |_  _$$ |_     ______  
  $$ |/$  \$$ |$$ \__$$/ $$ |__$$ |      $$ |__$$ | /      \ /  |  /  |$$ | /      \ / $$   |/ $$   |   /      \ 
  $$ /$$$  $$ |$$      \ $$    $$<       $$    $$< /$$$$$$  |$$ |  $$ |$$ |/$$$$$$  |$$$$$$/ $$$$$$/   /$$$$$$  |
  $$ $$/$$ $$ | $$$$$$  |$$$$$$$  |      $$$$$$$  |$$ |  $$ |$$ |  $$ |$$ |$$    $$ |  $$ | __ $$ | __ $$    $$ |
  $$$$/  $$$$ |/  \__$$ |$$ |__$$ |      $$ |  $$ |$$ \__$$ |$$ \__$$ |$$ |$$$$$$$$/   $$ |/  |$$ |/  |$$$$$$$$/ 
  $$$/    $$$ |$$    $$/ $$    $$/       $$ |  $$ |$$    $$/ $$    $$/ $$ |$$       |  $$  $$/ $$  $$/ $$       |
  $$/      $$/  $$$$$$/  $$$$$$$/        $$/   $$/  $$$$$$/   $$$$$$/  $$/  $$$$$$$/    $$$$/   $$$$/   $$$$$$$/ 
===============================================================================================================

'''
    )

threads = list()

if args.fd:
    print(
    '''
    
    !!!!!!!!!! FD MODE ENGAGED !!!!!!!!!!!!
    
    '''
    )
print("Spinning the wheel for " + ", ".join(tickers) + "\n")

cost_distribution = np.random.dirichlet(np.ones(len(tickers))*float(option_distribution),size=1)


blockPrint()

for i in range(0,len(tickers)):
    
    x = threading.Thread(target=grab_options, args=(tickers[i],cost_distribution[0][i]))
    threads.append(x)
    x.start()
    
for index, thread in enumerate(threads):
    thread.join()

enablePrint()

print(tabulate(options_list, headers=["Option", "Underlying", "Price", "Qty", "Cost", "IV", "Delta", "Theta", "Gamma", "Vega", "Rho"]))

for i in range(0,len(options_list)):

    total = total + options_list[i][4]

print(f'\nTotal Cost: ${total}')
