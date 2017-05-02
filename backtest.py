## Module for running a backtest on an algo.

## Algo interface:
##   Params:  DataFrame
##   Returns: Enum Buy|Sell|Hold

from datetime import datetime, timedelta
from time import time
from poloniex import Poloniex

import pdb

polo = Poloniex()

def getData(currency, length, delta):
    start = time() - (length * 60 * 60 * 24)
    end = time()
    return polo.returnChartData(currency, delta, start, end)

def run(algo, currency='btc_xmr', length=30, delta=900, outputDir='./'):
    '''
    Params:
        algo -> Algo object. Must implement tick()
        currency -> Poloniex currency_pair
        length -> Number of days to run test on.
        delta -> Period of readings to run test on.
    '''
    
    # Pull all the data
    data = getData(currency, length, delta)
    
    executions = []
    
    for i, frame in enumerate(data):
        #d = datetime.utcfromtimestamp(float(frame['date']))
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