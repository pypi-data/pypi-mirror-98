#!/usr/bin/python
# -*- coding: UTF-8 –*-
import threading, json
import time, datetime, re
import pandas as pd
import requests as req
from bs4 import BeautifulSoup as BS
import numpy as np
import jsonpath
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
#import sys
#import codecs
#sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
# sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
class GetPriceThread(threading.Thread):
    def __init__(self, func, args):
        super(GetPriceThread, self).__init__()
        #self.name = name
        self.func = func
        #self.codes = codes
        #self.start = start
        self.args = args
        self.result = self.func(*args)  # codes, start, end

    def get_result(self):
        try:
            return self.result
        except Exception as ex:
            return pd.DataFrame()

def get_hs300_codes():
    # 获取沪深300成分股
    hs300_codes = []#list(ts.get_hs300s()['code'])
    return hs300_codes

def get_sz50_codes():
    # 获取上证50成分股
    sz50_codes = []#list(ts.get_sz50s()['code'])
    return sz50_codes

def get_zz500_codes():
    # 获取中证500成分股
    zz500_codes = []#ts.get_zz500s()['code']
    return zz500_codes

def get_zz800_codes():
    # 获取中证800成分股
    zz500_codes = []#list(ts.get_zz500s()['code'])
    hs300_codes = []#list(ts.get_hs300s()['code'])
    zz500_codes.extend(hs300_codes)
    return zz500_codes

def get_all_codes():
    # 获取全市场的股票代码
    data_ = pd.DataFrame() #pro_ts.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    return list(data_['symbol'])

def get_a_codes(max_count = 5000):
    header = {
        "Content-Type": 'application/javascript; charset=UTF-8',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
        'Referer': 'http://quote.eastmoney.com/',  # 'Referer': 'http://data.eastmoney.com/',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        #'Cookie': 'cowminicookie=true; intellpositionL=1289.59px; em_hq_fls=js; qgqp_b_id=49621c65b51724aed8f10c0feea8ebdd; HAList=a-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sz-002541-%u9E3F%u8DEF%u94A2%u6784%2Ca-sz-000723-%u7F8E%u9526%u80FD%u6E90; cowCookie=true; st_si=06090884493304; st_asi=delete; intellpositionT=807px; st_pvi=07634999118497; st_sp=2019-10-18%2023%3A34%3A34; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=25; st_psi=20210130152119416-0-1409535082'
    }
    params = {
        'cb': 'jQuery112407285217582388686_1611985850544',
        'pn': '1',
        'pz': '{}'.format(max_count),
        'po': '1',
        'np': '1',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': '2',
        'invt': '2',
        'fid': 'f3',
        'fs': 'm:0 t:6,m:0 t:13,m:0 t:80,m:1 t:2,m:1 t:23',
        'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152',
        '_': '1611985850717',
        # 'fields': 'f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124^',
        # fs: m:0 t:6,m:0 t:13,m:0 t:80,m:1 t:2,m:1 t:23
    }
    cookies = {
        'cowminicookie': 'true',
        'em_hq_fls': 'js',
        'intellpositionL': '1289.59px',
        'qgqp_b_id': '49621c65b51724aed8f10c0feea8ebdd',
        'HAList': 'a-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sz-002541-%u9E3F%u8DEF%u94A2%u6784%2Ca-sz-000723-%u7F8E%u9526%u80FD%u6E90',
        'cowCookie': 'true',
        'st_si': '06090884493304',
        'st_asi': 'delete',
        'intellpositionT': '807px',
        'st_pvi': '07634999118497',
        'st_sp': '2019-10-18%2023%3A34%3A34',
        'st_inirUrl': 'https%3A%2F%2Fwww.baidu.com%2Flink',
        'st_psi': '20210130152119416-0-1409535082',
    }
    respon = req.get(url='http://push2.eastmoney.com/api/qt/clist/get', headers=header, cookies=cookies, params=params)
    res_txt = (respon.text).replace('jQuery112407285217582388686_1611985850544(', '')
    res_txt = res_txt.replace(');', '')
    data = json.loads(res_txt)
    target_df = data_change(data)
    return target_df

def data_change(data):
    # 在json文本中提取需要的数据
    # code
    stock_code_list = jsonpath.jsonpath(data, '$..f12')
    # name
    name_list = jsonpath.jsonpath(data, '$..f14')
    # 收盘价
    latest_price_list = jsonpath.jsonpath(data, '$..f2')
    # 涨跌幅
    price_pct_list = jsonpath.jsonpath(data, '$..f3')
    # 昨收价
    pre_price_list = jsonpath.jsonpath(data, '$..f18')
    # # 换手率
    TurRate_list1 = jsonpath.jsonpath(data, '$..f8')
    # open
    Open_list1 = jsonpath.jsonpath(data, '$..f17')
    # high
    High_list2 = jsonpath.jsonpath(data, '$..f15')
    # low
    LowPrice_list2 = jsonpath.jsonpath(data, '$..f16')
    # PE
    PE_list2 = jsonpath.jsonpath(data, '$..f9')
    # PS
    PS_list2 = jsonpath.jsonpath(data, '$..f23')
    # f5 成交量
    trade_vol_list2 = jsonpath.jsonpath(data, '$..f5')
    # f6 成交额
    trade_money_list2 = jsonpath.jsonpath(data, '$..f6')

    df = pd.DataFrame(stock_code_list, columns=['代码'])
    df['name'] = name_list
    df['code'] = stock_code_list
    df['last_price'] = latest_price_list
    df['pct_rate'] = price_pct_list
    df['pre_price'] = pre_price_list
    df['tur_rate'] = TurRate_list1
    df['open'] = Open_list1
    df['high'] = High_list2
    df['low'] = LowPrice_list2
    df['PE'] = PE_list2
    df['PS'] = PS_list2
    df['trade_volume'] = trade_vol_list2
    df['trade_money'] = trade_money_list2

    return df

def get_a_codes_by_req():
    # 通过爬虫获取网页上全A的股票代码
    respon_codes = list(get_a_codes()['code'])
    return respon_codes

def req_url(url):
    # 通过url页面的数据
    respon_ = req.get(url=url)
    respon_.encoding = respon_.apparent_encoding
    respon_data = respon_.text
    soup = BS(respon_data, 'lxml')
    #print('soup:{}'.format(soup))
    data_soup_chos = soup.findAll('div', {'class': 'u-postcontent cz'})[0].findAll('li')
    data_soup_chos = [re.sub("\D", '', n.text.replace('(', '').replace(')', '')) for n in data_soup_chos]
    data_soup_chos = ['sh' + n if n[0] == '6' else('sz' + n) for n in data_soup_chos]
    return data_soup_chos

def get_a_queto_data(start_date, end_date, code):
    # 获取全A的历史行情 [date_type:20200101, code_type: 0000001-->0代表沪市, 1300001-->1代表深市]
    if code[:1] == '6':code = '0' + code
    else:
        code = '1' + code
    url_ = 'http://quotes.money.163.com/service/chddata.html?code={}&start={}&end={}'.format(code, start_date, end_date)
    respon = req.get(url=url_)
    respon.encoding = respon.apparent_encoding
    respon = respon.text
    respon = list(respon.split('\r\n'))
    res_df = pd.DataFrame(respon)
    np_arr = np.array(list(filter(lambda x: x[0] != '', np.array(res_df.values))))
    # date	open	high	close	low	volume	turnover	code
    cols = ['date', 'code', 'name', 'close', 'high', 'low', 'open', 'PRE_CLOSE', 'CHG', 'PCHG', 'turnover', 'volume', 'VOL_MONEY', 'MARKET', 'CIR_MARKET', 'TRADE_NUM']
    np_arr_list = np_arr[1:]
    np_arr_list = (nparr[0].split(',') for nparr in np_arr_list)
    res_11_df = pd.DataFrame(np_arr_list, columns=cols)
    return res_11_df

def func_callback(fun1):
    return fun1()

def all_get_index_code_method(index_code):
    # 根据指定的index_code获取对应的一揽子股票
    the_dic_ = {'000300': get_hs300_codes, '000016': get_sz50_codes, '000905': get_zz500_codes, '000906': get_zz800_codes, 'ALLSTOCKS': get_a_codes_by_req}
    return list(func_callback(the_dic_[index_code]))

def indxx():
    today = datetime.datetime.now()
    date_count = 365 * 1
    pre_date = datetime.datetime.strftime(today + datetime.timedelta(days=0), '%Y-%m-%d')
    pre_1_y_date = datetime.datetime.strftime(today + datetime.timedelta(days=-date_count), '%Y-%m-%d')
    print('当前日期:{}'.format(pre_date))
    print('一年前日期:{}'.format(pre_1_y_date))
    t = time.time()
    th_code = 'ALLSTOCKS'
    # 1. 第一步过滤需要用到的初步股票篮子【沪深300/中证500/上证50/中证800/创业板/全A】
    cho_index_codes = all_get_index_code_method(th_code)  # 获取除全A以外的指数成分股
    # cho_index_codes = cho_index_codes[-5:]
    print('选中的股票篮子:{}'.format(len(cho_index_codes)))
    print('开始的时间:{}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    # 2.1 获取历史行情数据 ##
    price_df = get_stock_price(cho_index_codes, pre_1_y_date, pre_date)  # get_stock_his_price_by_sina(cho_index_codes, date_count)
    price_df = price_df.sort_index(ascending=True)
    price_df['code'] = ['SH.' + cd[1:] if cd[0] == '6' else 'SZ.' + cd[1:] for cd in price_df['code']]

    #price_df.to_pickle(r'D:\PythonStrategy\all_codes_price_df.pkl')
    price_df.to_csv("all_codes_price_df.csv", encoding='utf-8')#r'D:\PythonFile\PythonStrategys\all_codes_price_df.csv')
    print('完成的时间:{}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('写入完成,运行过程总共耗时:{}分钟'.format(round(time.time()-t, 3)/60.0))

def cocat_df(cd, start, end):
    try:
        time.sleep(0.2)  # 频率过快会被屏蔽
        df = get_a_queto_data(start, end, cd)  # ts.get_hist_data(cd, start=start, end=end)
    except Exception as e:
        print('合约:{},抛异常:{}'.format(cd, e))
        df = pd.DataFrame()
    return df

def get_stock_price_thread(codes, start, end):
    # 分段获取股票行情
    res_df = pd.DataFrame()
    start_d1 = time.time()
    for cd in codes:
        time.sleep(0.2)  # 频率过快会被屏蔽
        try:
            df = get_a_queto_data(start, end, cd)  #ts.get_hist_data(cd, start=start, end=end)
            res_df = pd.concat([res_df, df], axis=0)
        except Exception as e:
            print('合约:{},抛异常:{}'.format(cd, e))
            continue
    return res_df

def avg_list_func(listTemp, n):
    # 平分list,每n个一组
    for i in np.arange(0, len(listTemp), n):
        yield listTemp[i:i + n]

def get_stock_price(codes, start, end):
    # 获取股票行情
    #codes = codes[:1000]
    std0 = time.time()
    n = 500  # 20-->937.4 # 500-->876.2  # 100-->890.8  # 200-->966.2
    all_code_list = list(avg_list_func(codes, n))
    par_cls = partial(get_stock_price_thread, start=start, end=end)
    pool = ThreadPool()
    res_data_list = pool.map(par_cls, all_code_list)
    result_df = pd.concat(res_data_list)
    print('res_data:{}'.format(result_df))
    print('多进程耗时:{}s'.format(round(time.time()-std0, 3)))

    # std00 = time.time()
    # for lo in range(0, len(all_code_list)):
    #     t = GetPriceThread(get_stock_price_thread, args=(all_code_list[lo], start, end))
    #     threads.append(t)
    # for t in range(len(all_code_list)):
    #     threads[t].setDaemon(True)
    #     # start threads 此处并不会执行线程,而是将任务分发到每个线程,同步线程.等同步完成后再开始执行start方法
    #     threads[t].start()
    # for t in range(len(all_code_list)):
    #     threads[t].join()
    # cocat_df_list = [t.get_result() for t in threads]
    # result_df = pd.concat(cocat_df_list)
    # print('多线程耗时:{}s'.format(round(time.time() - std00, 3)))
    # print('result_df:{}'.format(result_df))
    return result_df

if __name__ == '__main__':
    indxx()