## Module for running a backtest on an algo.

## Algo interface:
##   Params:  DataFrame
##   Returns: Enum Buy|Sell|Hold

from datetime import datetime, timedelta
from time import time
from poloniex import Poloniex
from random import randint
import matplotlib.pyplot as plt, mpld3

#plt.plot([3,1,4,1,5], 'ks-', mec='w', mew=5, ms=20)
#mpld3.show()


import pdb

polo = Poloniex()

def getData(currency, length, delta):
    start = time() - (length * 60 * 60 * 24)
    end = time()
    return polo.returnChartData(currency, delta, start, end)


def run(algo, currency='btc_xmr', length=30, delta=900, outputDir='./'):
    '''
    algo -> Algo object. Must implement tick!()
    currency -> poloniex currency pair
    length -> num days
    delta -> how many data points to test on.  
    '''
    
    # Pull all the data
    data = getData(currency, length, delta)
    
    executions = []
    
    for i, frame in enumerate(data):
        #d = datetime.utcfromtimestamp(float(frame['date']))
        #pdb.set_trace()
        result = algo.tick(data[0:i])
        action = result[0]
        if action in ['BUY', 'SELL']:
            price = frame['weightedAverage']
            shares = result[1]
            executions.append((action, price, shares))
        
    # Calculate Profits/Losses
    profits = []
    for i in xrange(0, len(executions), 2):
        # Simple PL formula: price_bought - price_sold
        profit_per_share = float(executions[i-1][1]) - float(executions[i][1])
        profits.append(profit_per_share * executions[i][2])

    return executions, profits

## Stub Algo
class Algo:
    def __init__(self):
        self.holding = False
        
    def tick(self, frame):
        res = randint(0,1)
        if res == 0 and not self.holding:
            self.holding = True
            return 'BUY', 100
        elif res == 1 and self.holding:
            self.holding = False
            return 'SELL', 100
        else:
            return 'NOTHING'

stubAlgo = Algo()
results = run(stubAlgo, currency='USDT_BTC')

#print 'First 10 executions: ' + str(results[1][0:10])
print 'total profit: ' + str(sum(results[1]))

'''
results_2 = run(stubAlgo, currency='USDT_XMR')

print 'First 10 executions: ' + str(results_2[1][0:10])
print 'total profit: ' + str(sum(results_2[1]))
'''

'''
tickers = polo.returnTicker()

keys = [key for key, value in tickers.iteritems()]
#print sorted(keys)
for item in sorted(keys):
    print item
'''
#for key, value in tickers.iteritems():
    #print key
#print tickers