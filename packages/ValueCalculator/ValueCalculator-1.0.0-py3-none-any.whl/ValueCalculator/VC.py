# import time
# import OS, sys


'''
def GenerateStockMarketChart():
    pass
'''

'''
class StockMarket():
    def Forecast():
        pass
'''




def SM_Forecast(HAYear, Now, BBHAY=3):
    if type(HAYear) != list:
        return '参数HAYear必须为列表'
    else:
        for i in HAYear:
            if type(i) == int:
                pass
            else:
                return 'HAYear列表里的参数不全为整数，请参考ValueCalculator官方文档\nhttps://pypi.org/ '
    
    lenyear = len(HAYear)
    objectivity = 0
    for i in HAYear:
        objectivity += i
    if objectivity == 0:
        pass
    elif objectivity == 1:
        pass
    elif objectivity == 2:
        pass
    elif objectivity >= 3:
        if BBHAY >= 2 and BBHAY < 3:
            if HAYear[1] == +1:
                return '-1, +1, +1, go'
            if HAYear[1] == +2:
                return '+1, @+1, -1, +1, about'
            
        if BBHAY >= 3:
            return '-1, +2, go'
        if BBHAY == 1:
            if HAYear[0] == +2 and (HAYear[1] == +1 or HAYear[1] == +2):
                return '@-1, @+1, -1, go'
    elif objectivity == -1:
        if BBHAY == 3:
            return '+1, +1, @+1, -1, go, about'
        if BBHAY == 1 or BBHAY == 2:
            return '@-1, +1, @+1, go ,about'
    elif objectivity == -2:
        pass
    elif objectivity <= -3:
        if BBHAY <= 1 and Now == -1:
            if HAYear[0] >= 1:
                return '+1, go2, about'
            else:
                return '0, go1, about'




# HAYear参数说明：
'''
1. 参数HAYear必须为列表
2. 参数HAYear的用意为 “在半年内是涨还是跌”
3. 参数设置说明：
    “涨”                 为   “1”
    “大涨”               为   “2”
    “没有多大涨/跌幅度”  为   “0”
    “跌了”               为   “-1”
    “跌的多”             为   “-2”
'''


# SM_Forecast(列表, 现在行情, 股票出厂时间=3)

# zd = SM_Forecast([+3, -3, +1, -1], -1, BBHAY=2)
# print(zd)



