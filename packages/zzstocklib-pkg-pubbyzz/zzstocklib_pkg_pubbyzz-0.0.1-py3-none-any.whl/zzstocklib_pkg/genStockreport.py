import sinaFinanceUtility as sina
import pandas as pd

excel_url = r'https://api.onedrive.com/v1.0/shares/u!aHR0cHM6Ly8xZHJ2Lm1zL3gvcyFBb2NpM3BwNVE0LXRwenR1ZmlWRld0S0NJR2NKP2U9U2RJT2NR/root/content'
df = pd.read_excel(excel_url, dtype={'股票代码': str})
#将NaN(缺失值）替换为0
df = df.fillna(0)
df1 = df.groupby(['股票代码', '股票名称'])['数量'].sum().reset_index(name='持仓数量')

stocks = df1.sort_values(by='持仓数量',ascending=False)
    
stocks['成本价'] = 0.0
stocks['最近交易价格'] = 0.0
stocks['最近交易数量'] = 0
stocks['最近目标价格'] = 0.0
stocks['收盘价'] = 0.0
stocks['最近交易价格+3%'] = 0.0
stocks['收盘价+3%'] = 0.0
stocks['止损价-10%'] = 0.0

for index, row in stocks.iterrows():  # dataframe 遍历

    df3 = df[df['股票代码'] == row['股票代码']].sort_values(by='交易日期', ascending=False)
    df3['成本'] = df3['数量']*df3['交易价格']
    row['最近交易价格'] = df3.iloc[0, 4]
    row['最近交易数量'] = df3.iloc[0, 3]
    row['最近目标价格'] = df3['目标价格'].max()
    
    row['收盘价'] = sina.get_lastday_stockprice(row['股票代码'])
    row['收盘价+3%'] = row['收盘价']*1.03

    if row['持仓数量'] > 0:  # 只关注于持仓股票池
       row['成本价'] = df3['成本'].sum()/row['持仓数量']
       row['最近交易价格+3%'] = row['最近交易价格']*1.03
       row['止损价-10%'] = row['成本价']*0.9

    

    stocks.iloc[index] = row

stocks = stocks.sort_values(by='持仓数量',ascending=False)
stocks.to_excel('C:\workspace\stock\stockdata\dict\stock_updated.xlsx')