import pandas as pd
import re,datetime,warnings,akshare
from fwshare.symbolVar import chinese_to_english, find_chinese,symbol2varietie
from fwshare import cons


pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大行

calendar = cons.get_calendar()

columns=['spotPrice','nearSymbol','nearPrice','nearBasis','domSymbol','domPrice','domBasis']

def get_spotPrice_daily(date=None):
    date = cons.convert_date(date) if date is not None else datetime.date.today()

    # url='http://www.100ppi.com/sf/day-'++'.html'
    url=cons.SYS_SPOTPRICE_URL % date.strftime('%Y-%m-%d')
    table = pd.read_html(url, match='.+', flavor=None, header=0, index_col=0, skiprows=1)[1]
    table = pd.DataFrame(table.iloc[:, :7])
    table.columns = columns
    table.loc[:, 'variety'] = table.index
    # table = table[~table['variety'].isin(['上海期货交易所','郑州商品交易所','大连商品交易所'])]
    table = table.reset_index(drop=True)
    data = pd.DataFrame()
    for string in table['variety'].tolist():
        if string == 'PTA':
            news = 'PTA'
        else:
            news = "".join(re.findall(r"[\u4e00-\u9fa5]", string))
        if news != "" and news not in ["上海期货交易所", "郑州商品交易所", "大连商品交易所"]:
            symbol = chinese_to_english(news)
            df = pd.DataFrame(table[table['variety'] == string])
            df['variety'] = symbol
            df['nearSymbol'] = df['variety']+df['nearSymbol']
            df['domSymbol'] = df['variety'] + df['domSymbol']
            df = df.apply(pd.to_numeric, errors="ignore")
            if symbol=='FG':
                df['spotPrice']=df['spotPrice']*80
            elif symbol=='JD':
                df['spotPrice']=df['spotPrice']*500
            data = data.append(df)
            #
            data['nearBasis'] = data.apply(lambda x:x['spotPrice']-x['nearPrice'],axis=1)
            data['nearBasisRate'] = round(data.apply(lambda x: (x['spotPrice']/x['nearPrice']-1)*100, axis=1),2)
            data['domBasis'] = data.apply(lambda x: x['spotPrice'] - x['domPrice'], axis=1)
            data['domBasisRate'] = round(data.apply(lambda x: (x['spotPrice']/x['domPrice']-1)*100, axis=1),2)

            # data['date']=date.strftime('%Y%m%d')

    return data

if __name__ == '__main__':
    print(get_spotPrice_daily('20201224'))
