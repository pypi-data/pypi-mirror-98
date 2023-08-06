
import zzlogger
from urllib import request,parse
import time,datetime
import json
import re
import pandas as pd
import numpy as np

logger = zzlogger.logger

def get_sinacodelist(stock_list):
    """根据股票代码转译为sina所需要的代码，香港hk，沪sh，深sz""" #https://www.cnblogs.com/xuliangxing/p/8492705.html
    new_codelist = []
    for code in stock_list:

        if len(code) == 5:         #香港交易所
            code = "hk" + code
        elif len(code) == 6:    #沪深交易所
            if code.startswith('600') or code.startswith('601') or code.startswith('603') or code.startswith('688') or code.startswith('501') or code.startswith('516') or code.startswith('113'):
                code = "sh" + code
            elif code.startswith('000') or code.startswith('001') or code.startswith('002') or code.startswith('300') or code.startswith('128') or code.startswith('127'):
                code = "sz" + code
            else:
                logger.error("Error: code " + code + " not found in stock market!")
                continue
        else:
                logger.error("Error: code " + code + " not found in stock market!")
                continue

        new_codelist.append(code)

    #print(new_codelist)
    return new_codelist


def get_stocklistprice(stock_list):
    """获取当前股票价格"""
    stocks = ','.join(get_sinacode(stock_list))
    stock_price = pd.DataFrame(columns=('name','open_price','lastday_price','current_price','highest_price','lowest_price'))

    try:
        page = request.urlopen("http://hq.sinajs.cn/?list=" + stocks)
        result = page.read().decode('gb2312')
    except request.URLError as e:
        logger.error(e)
    else:
        price_list = result.split('\n')

        for stock in price_list:
            if len(stock.strip()) <= 0:
                continue

            data = re.findall(r'"(.+?)"', stock)
            code = re.findall(r'str_[hkszsh]{2}(.+?)=', stock)
            #print(data)

            data = data[0].split(',')
            if "str_hk" in stock:                #如果是港股，则将英文名去掉和沪深的格式看齐,且将当前价格位置位移到第3位
                del data[0]
                data.insert(3,data[5])
            stock = data
            df = pd.DataFrame([stock[0:6]], index=code, columns=('name','open_price','lastday_price','current_price','highest_price','lowest_price'))
            stock_price = stock_price.append(df)

        stock_price['open_price']=stock_price['open_price'].apply(float)
        stock_price['lastday_price']=stock_price['lastday_price'].apply(float)
        stock_price['current_price']=stock_price['current_price'].apply(float)
        stock_price['highest_price']=stock_price['highest_price'].apply(float)
        stock_price['lowest_price']=stock_price['lowest_price'].apply(float)

    return stock_price

def get_sinacode(stock_code):
    """根据股票代码转译为sina所需要的代码，香港hk，沪sh，深sz""" #https://www.cnblogs.com/xuliangxing/p/8492705.html
    code = stock_code
    if len(code) == 5:  # 香港交易所
        code = "hk" + code
    elif len(code) == 6:  # 沪深交易所
         if code.startswith('600') or code.startswith('601') or code.startswith('603') or code.startswith('688') or code.startswith('501') or code.startswith('516') or code.startswith('113'):              
            code = "sh" + code
         elif code.startswith('000') or code.startswith('001') or code.startswith('002') or code.startswith('300') or code.startswith('128') or code.startswith('127'):
            code = "sz" + code
         else:
            logger.error("Error: code " + code +" not found in stock market!")
                
    else:
        logger.error("Error: code " + code + " not found in stock market!")
               
    return code

def get_lastday_stockprice(stock_code):
    """获取当前股票价格"""
    
    try:
        page = request.urlopen("http://hq.sinajs.cn/?list=" + get_sinacode(stock_code))
        result = page.read().decode('gb2312')
        #print(result)
    except request.URLError as e:
        logger.error(e)
    else:
        content_data = re.findall(r'"(.+?)"', result)
        #print(content_data)
        data = content_data[0].split(',')
        if "str_hk" in result:                #如果是港股，则将英文名去掉和沪深的格式看齐,且将当前价格位置位移到第3位
           del data[0]
           data.insert(3,data[5])
        stock_lastday_price = data[2]
        #df = pd.DataFrame([stock[0:6]], index=code, columns=('name','open_price','lastday_price','current_price','highest_price','lowest_price'))
        

    return float(stock_lastday_price)
