import backtest
from random import randint

'''
A silly example algorithm for demonstration purposes.
BUY/SELL or HOLD based on a coin flip.
'''

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
results = backtest.run(stubAlgo, currency='USDT_BTC')

print 'total profit: ' + str(sum(results[1]))