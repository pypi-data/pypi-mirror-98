#!/usr/bin/python
# -*- coding: UTF-8 –*-
import requests as req
import datetime, time, re
import json
import jsonpath
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as BS
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial

#########################宏观数据#############################

############货币供应###################
def create_hbgy_params(page, type = 'GJZB', sty = 'ZGZB', ps='100'):
    params = {
        #'cb': 'datatable3922460',
        'type': '{}'.format(type),
        'sty': '{}'.format(sty),
        'p': '{}'.format(page),
        'ps': '{}'.format(ps),
        'mkt': '11',
        'pageNo': '2',
        'pageNum': "2",
        '_': '1612793889948',
    }
    return params

def get_his_bgy_capital_response(params, st_sn='145'):
    # get历史净流入数据
    cookies = {
        'cowminicookie': 'true',
        'em_hq_fls': 'js',
        'st_si': '45897351155573',
        'waptgshowtime': '202128',
        'st_asi': 'delete',
        'cowCookie': 'true',
        'qgqp_b_id': '49621c65b51724aed8f10c0feea8ebdd',
        'p_origin': 'https%3A%2F%2Fpassport2.eastmoney.com',
        'ct': 'YF2mZ_op_nsxQ6S0vjtqz7xZBug0NTW-Mm6Byp5_AN1rC_rdlYZ1xjaMxYGw83mcmWk_PvOgHooY5mVdwDQLWcvDJTfxh846lCMkqInLiT3TS937AhyMS_ifiuqFhmks-s2CxKKSWWkrtaJeqWvAGiQ_wh0i8AuDh6RvKnHApig',
        'ut': 'FobyicMgeV6W21ICVIh67y2TdalzNIRdHh6UwIU-PHyOwFPXzPncgSsKJ2qXIFgvgxtvANYmJXUHCPD3tBIvfopl7NsepVBKFQucIcTwwlq-WX3qyvbPozoLToypptAjxUkKpVqGdUL6dks4Vtv1KKLXCmaAXp8mQrDOHpTHRZ8ft9gcUqPMUaAbnxmLu5qbISM7uGrJ2eSu7EROtLBVgwBhBZtzhNA0GzziXi8iq8h4fa763eyBwUxrtLUHrte9d4B-IaRwuRtmrYTnUmA_U7MpDN0Cg9SN',
        'sid': '159309191',
        'uidal': '1002094027214364%e9%a3%8e%e4%b9%90%e5%b2%9a%e9%9b%85',
        'pi': '1002094027214364%3bm1002094027214364%3b%e9%a3%8e%e4%b9%90%e5%b2%9a%e9%9b%85%3bKkSBKC5DEQXUZK%2fEwwInj5WpbSR7S9kOZClStvOBj5vyQqwv2KUUkGsgekCzZfAp7PBnK10Vte4lIgkGg4e29UVyk8rldPKAxxCQZZB%2bFaU%2f%2bQIjCG2szv9umvRmfATQdFwMfSwM4LpINTBsihhyEuepC3aYX6qC6DijSw4dq2peQgoVVJiLtpJDnoH4sGuqGjWjS3VR%3bFq%2frXacfR4VaN3Wx18VNtjXw2KuVPNo5kOvrPHe%2bNVWyeVYEtjlWK7oBKWl%2bo75bImrRt7cx5ghJefp12JaZe5x%2fVT4ZDGpzWfGyyakddYf9QkR5GKET23%2fXOPVnJazum2ROhNUswfYRn6XX5iGKiAYjBYEToA%3d%3d',
        'vtpst': '|',
        'HAList': 'd-hk-01024%2Cd-hk-06185%2Ca-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sz-300042-%u6717%u79D1%u79D1%u6280%2Ca-sh-600916-N%u9EC4%u91D1%2Ca-sh-601818-%u5149%u5927%u94F6%u884C%2Ca-sz-002824-%u548C%u80DC%u80A1%u4EFD%2Ca-sz-002541-%u9E3F%u8DEF%u94A2%u6784%2Ca-sz-000723-%u7F8E%u9526%u80FD%u6E90',
        'st_psi': '20210208221810111-0-9871610278',
        'intellpositionL': '862px',
        'intellpositionT': '1655px',
        'EMFUND1': 'null',
        'EMFUND2': 'null',
        'EMFUND3': 'null',
        'EMFUND4': 'null',
        'EMFUND5': 'null',
        'EMFUND6': 'null',
        'EMFUND7': 'null',
        'EMFUND8': 'null',
        'EMFUND9': '02-08 14:54:20@#$%u534E%u6CF0%u67CF%u745E%u6CAA%u6DF1300ETF@%23%24510300',
        'st_pvi': '07634999118497',
        'st_sp': '2019-10-18%2023%3A34%3A34',
        'st_inirUrl': 'https%3A%2F%2Fwww.baidu.com%2Flink',
        'st_sn': '{}'.format(st_sn),
    }
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
    }
    response = req.get('http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx'
                       , headers=headers, params=params,
                       cookies=cookies, verify=False)
    # print('url-->:{}'.format(response.url))
    return response

def clean_hbgy_data(data):
    try:
        data = str(data).replace('([', '')
        data = str(data).replace('])', '')
        data = data[1:-1].split('","')
        f_list = [data_cap.split(',') for data_cap in data]
        f_df = pd.DataFrame(f_list, columns=['date', 'M2-数量(亿元)', 'M2-同比增长', 'M2-环比增长', 'M1-数量(亿元)', 'M1-同比增长', 'M1-环比增长', 'M0-数量(亿元)', 'M0-同比增长', 'M0-环比增长'])
    except Exception as ep:
        print('ep:{}'.format(ep))
        return pd.DataFrame()
    return f_df

def get_his_hbgy_capital_data(max_acount=3):
    # 获取历史货币供应数据
    this_res_df = pd.DataFrame()
    for p in range(1, max_acount):
        try:
            params = create_hbgy_params(p)
            response = get_his_bgy_capital_response(params)
            df = clean_hbgy_data(str(response.text))
            this_res_df = pd.concat([this_res_df, df], axis=0)
        except Exception as ex:
            return this_res_df
    return this_res_df

############货币供应###################

#########################宏观数据#############################

########################指数成分股数据接口###############################
def get_hs300_codes(index_code='000300'):
    # 获取沪深300成分股
    df = _get_target_index_codes(index_code)
    return df

def get_sz50_codes(index_code='000016'):
    # 获取上证50成分股
    df = _get_target_index_codes(index_code)
    return df

def get_zz500_codes(index_code='000905'):
    # 获取中证500成分股
    df = _get_target_index_codes(index_code)
    return df

def get_zz800_codes():
    # 获取中证800成分股
    zz500_df = get_zz500_codes()
    hs300_df = get_hs300_codes()
    zz_800_df = pd.concat([hs300_df, zz500_df])
    return zz_800_df

def get_a_codes(max_count = 8000):
    # 获取全A合约代码
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

def _get_target_index_codes(index_code=''):
    # 传入需要的指数合约代码
    east_url = 'http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SHSZZS&sty=SHSZZS&st=0&sr=-1&p=4&ps=500&code={}'.format(index_code)
    content = total_get(east_url)
    content = content[3:]
    content = content[:-3]
    content_list = list(content.replace('","', '|').split('|'))
    content_list = [con.split(',') for con in content_list]

    cols = ['code', 'name', 'industy', 'city', 'eps', 'net_aps', 'ROA', 'total_equity', 'cir_equity', 'last_price', 'cir_market',
            'PE', 'weight_ratio', 'index_code', 'date', 'last_price', 'rate(%)', 'total_trade_volume', 'total_trade_money']
    df = pd.DataFrame(content_list, columns=cols)
    return df

def total_get(url):
    # request.get()
    respon_ = req.get(url)
    respon_.encoding = respon_.apparent_encoding
    content = respon_.text
    return content

########################指数成分股数据接口################################

########################行业成分股数据接口###################################
def create_params_industry(page, industry_code, pz = '100'):
    params = {
        'pz': '{}'.format(pz),
        'po': '1',
        'np': '1^',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': '2',
        'invt': '2',
        'fid0': 'f4001',
        'fid': 'f3',
        'fs': 'b:BK{} f:!50'.format(industry_code),
        'stat': '1',
        'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152,f45',
        'rt': '53407822',
        # ('cb', 'jQuery1124024910121940634178_1612597304786^'),
        '_': '1612593289172',
    }
    value = str(page) + '^'
    params['pn'] = value
    # print(params)
    return params

def get_response_industry(params):
    # 行业成分股数据
    #url_ ='http://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112308236517126513889_1612519999904&fid=f267&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A0%2Bt%3A6%2Bf%3A!2%2Cm%3A0%2Bt%3A13%2Bf%3A!2%2Cm%3A0%2Bt%3A80%2Bf%3A!2%2Cm%3A1%2Bt%3A2%2Bf%3A!2%2Cm%3A1%2Bt%3A23%2Bf%3A!2%2Cm%3A0%2Bt%3A7%2Bf%3A!2%2Cm%3A1%2Bt%3A3%2Bf%3A!2&fields=f12%2Cf14%2Cf2%2Cf127%2Cf267%2Cf268%2Cf269%2Cf270%2Cf271%2Cf272%2Cf273%2Cf274%2Cf275%2Cf276%2Cf257%2Cf258%2Cf124'
    cookies = {
        'cowminicookie': 'true',
        'em_hq_fls': 'js',
        'st_si': '75137633692030',
        'waptgshowtime': '202126',
        'st_asi': 'delete',
        'cowCookie': 'true',
        'qgqp_b_id': '49621c65b51724aed8f10c0feea8ebdd',
        'p_origin': 'https%3A%2F%2Fpassport2.eastmoney.com',
        'ct': 'YF2mZ_op_nsxQ6S0vjtqz7xZBug0NTW-Mm6Byp5_AN1rC_rdlYZ1xjaMxYGw83mcmWk_PvOgHooY5mVdwDQLWcvDJTfxh846lCMkqInLiT3TS937AhyMS_ifiuqFhmks-s2CxKKSWWkrtaJeqWvAGiQ_wh0i8AuDh6RvKnHApig',
        'ut': 'FobyicMgeV6W21ICVIh67y2TdalzNIRdHh6UwIU-PHyOwFPXzPncgSsKJ2qXIFgvgxtvANYmJXUHCPD3tBIvfopl7NsepVBKFQucIcTwwlq-WX3qyvbPozoLToypptAjxUkKpVqGdUL6dks4Vtv1KKLXCmaAXp8mQrDOHpTHRZ8ft9gcUqPMUaAbnxmLu5qbISM7uGrJ2eSu7EROtLBVgwBhBZtzhNA0GzziXi8iq8h4fa763eyBwUxrtLUHrte9d4B-IaRwuRtmrYTnUmA_U7MpDN0Cg9SN',
        'sid': '159309191',
        'uidal': '1002094027214364%e9%a3%8e%e4%b9%90%e5%b2%9a%e9%9b%85',
        'pi': '1002094027214364%3bm1002094027214364%3b%e9%a3%8e%e4%b9%90%e5%b2%9a%e9%9b%85%3bKkSBKC5DEQXUZK%2fEwwInj5WpbSR7S9kOZClStvOBj5vyQqwv2KUUkGsgekCzZfAp7PBnK10Vte4lIgkGg4e29UVyk8rldPKAxxCQZZB%2bFaU%2f%2bQIjCG2szv9umvRmfATQdFwMfSwM4LpINTBsihhyEuepC3aYX6qC6DijSw4dq2peQgoVVJiLtpJDnoH4sGuqGjWjS3VR%3bFq%2frXacfR4VaN3Wx18VNtjXw2KuVPNo5kOvrPHe%2bNVWyeVYEtjlWK7oBKWl%2bo75bImrRt7cx5ghJefp12JaZe5x%2fVT4ZDGpzWfGyyakddYf9QkR5GKET23%2fXOPVnJazum2ROhNUswfYRn6XX5iGKiAYjBYEToA%3d%3d',
        'vtpst': '|',
        'HAList': 'a-sh-601818-%u5149%u5927%u94F6%u884C%2Ca-sz-002824-%u548C%u80DC%u80A1%u4EFD%2Ca-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sz-002541-%u9E3F%u8DEF%u94A2%u6784%2Ca-sz-000723-%u7F8E%u9526%u80FD%u6E90',
        'intellpositionL': '862px',
        'intellpositionT': '955px',
        'st_pvi': '07634999118497',
        'st_sp': '2019-10-18%2023%3A34%3A34',
        'st_inirUrl': 'https%3A%2F%2Fwww.baidu.com%2Flink',
        'st_sn': '15',
        'st_psi': '20210206142936585-113200301321-8482464184',
    }

    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://quote.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
    }

    response = req.get('http://push2.eastmoney.com/api/qt/clist/get'
                       , headers=headers, params=params,
                       cookies=cookies, verify=False)
    #print('url:{}'.format(response.url))
    return response

def data_cleaning_industry(data):
    # 清洗行业成分股数据
    stock_code_list = jsonpath.jsonpath(data, '$..f12')
    name_list = jsonpath.jsonpath(data, '$..f14')
    # 最新价 price
    latest_price_list = jsonpath.jsonpath(data, '$..f2')
    # 涨跌幅 rate
    price_limit_list = jsonpath.jsonpath(data, '$..f3')
    # high
    high_list1 = jsonpath.jsonpath(data, '$..f15')
    # low
    low_list1 = jsonpath.jsonpath(data, '$..f16')
    # open
    open_list2 = jsonpath.jsonpath(data, '$..f17')
    # pre_close
    pre_close_list2 = jsonpath.jsonpath(data, '$..f18')
    # 换手率 tur_rate
    tur_rate_list3 = jsonpath.jsonpath(data, '$..f8')
    # 成交量 vol
    vol_list3 = jsonpath.jsonpath(data, '$..f5')
    # 成交额
    money_list4 = jsonpath.jsonpath(data, '$..f6')
    df = pd.DataFrame(stock_code_list, columns=['code'])
    df['name'] = name_list
    df['close'] = latest_price_list
    df['rate'] = price_limit_list
    df['high'] = high_list1
    df['low'] = low_list1
    df['open'] = open_list2
    df['pre_price'] = pre_close_list2
    df['tur_rate'] = tur_rate_list3
    df['vol'] = vol_list3
    df['money'] = money_list4
    return df

def get_industry_codes(industry_code='800001', max_acount=50):
    # 获取行业成分股数据
    indus_dict = {'800001': '0475', '800002': '0485', '800003': '0420', '800004': '0725', '800005': '0421', '800006': '0474',
                   '800007': '0451', '800008': '0440', '800009': '0734', '800010': '0727', '800011': '0465', '800012': '0422',
                   '800013': '0484', '800014': '0726', '800015': '0424', '800016': '0436', '800017': '0482', '800018': '0450',
                   '800020': '0729', '800019': '0456',
                   '800021': '0425', '800022': '0476', '800023': '0740', '800024': '0427', '800025': '0429', '800026': '0728', '800027': '0433',
                   '800029': '0736', '800030': '0738', '800031': '0479', '800032': '0464', '800033': '0473', '800034': '0486', '800035': '0546',
                   '800036': '0539', '800037': '0438', '800038': '0428', '800039': '0477', '800040': '0735', '800041': '0545', '800042': '0448',
                   '800043': '0447', '800044': '0730', '800045': '0910', '800046': '0737', '800047': '0458', '800048': '0454', '800049': '0732',
                   '800050': '0478', '800051': '0480', '800052': '0733', '800053': '0457', '800054': '0481', '800055': '0538', '800056': '0470',
                   '800057': '0731', '800058': '0459', '800059': '0471', '800060': '0537', '800061': '0437', '800062': '0739'}
    this_res_df = pd.DataFrame()
    for page in range(1, max_acount):
        try:
            params = create_params_industry(page, indus_dict[industry_code])
            response = get_response_industry(params)
            data = get_data(response)
            if data['data'] == None: break
            df = data_cleaning_industry(data)
            if df.empty:continue
            if this_res_df.empty:
                this_res_df = df.copy()
            else:
                this_res_df = pd.concat([this_res_df, df], axis=0)
        except Exception as ex:
            continue
    return this_res_df

########################行业成分股数据接口###################################

##########################次新股/st股票################################
def create_params_stock(page, fid='f26', fs='m:0 f:8,m:1 f:8', _ ='1612757741404',pz='100'):
    params = {
        'pn': '{}'.format(page),
        'pz': '{}'.format(pz),
        'po': '1^',
        'np': '1^',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281^',
        'fltt': '2^',
        'invt': '2^',
        'fid': '{}'.format(fid),
        'fs': '{}'.format(fs),
        'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f11,f62,f128,f136,f115,f152',
        #'rt': '53407822^',
        # ('cb', 'jQuery1124024910121940634178_1612597304786^'),
        '_': '{}'.format(_),  # 1612763862192
    }
    return params

def get_response_stock(params, st_sn='63', st_psi='20210208131233561-111000300841-9541724436'):
    # 行业成分股数据
    cookies = {
        'cowminicookie': 'true',
        'em_hq_fls': 'js',
        'st_si': '45897351155573',
        'waptgshowtime': '202128',
        'st_asi': 'delete',
        'cowCookie': 'true',
        'qgqp_b_id': '49621c65b51724aed8f10c0feea8ebdd',
        'p_origin': 'https%3A%2F%2Fpassport2.eastmoney.com',
        'ct': 'YF2mZ_op_nsxQ6S0vjtqz7xZBug0NTW-Mm6Byp5_AN1rC_rdlYZ1xjaMxYGw83mcmWk_PvOgHooY5mVdwDQLWcvDJTfxh846lCMkqInLiT3TS937AhyMS_ifiuqFhmks-s2CxKKSWWkrtaJeqWvAGiQ_wh0i8AuDh6RvKnHApig',
        'ut': 'FobyicMgeV6W21ICVIh67y2TdalzNIRdHh6UwIU-PHyOwFPXzPncgSsKJ2qXIFgvgxtvANYmJXUHCPD3tBIvfopl7NsepVBKFQucIcTwwlq-WX3qyvbPozoLToypptAjxUkKpVqGdUL6dks4Vtv1KKLXCmaAXp8mQrDOHpTHRZ8ft9gcUqPMUaAbnxmLu5qbISM7uGrJ2eSu7EROtLBVgwBhBZtzhNA0GzziXi8iq8h4fa763eyBwUxrtLUHrte9d4B-IaRwuRtmrYTnUmA_U7MpDN0Cg9SN',
        'sid': '159309191',
        'uidal': '1002094027214364%e9%a3%8e%e4%b9%90%e5%b2%9a%e9%9b%85',
        'pi': '1002094027214364%3bm1002094027214364%3b%e9%a3%8e%e4%b9%90%e5%b2%9a%e9%9b%85%3bKkSBKC5DEQXUZK%2fEwwInj5WpbSR7S9kOZClStvOBj5vyQqwv2KUUkGsgekCzZfAp7PBnK10Vte4lIgkGg4e29UVyk8rldPKAxxCQZZB%2bFaU%2f%2bQIjCG2szv9umvRmfATQdFwMfSwM4LpINTBsihhyEuepC3aYX6qC6DijSw4dq2peQgoVVJiLtpJDnoH4sGuqGjWjS3VR%3bFq%2frXacfR4VaN3Wx18VNtjXw2KuVPNo5kOvrPHe%2bNVWyeVYEtjlWK7oBKWl%2bo75bImrRt7cx5ghJefp12JaZe5x%2fVT4ZDGpzWfGyyakddYf9QkR5GKET23%2fXOPVnJazum2ROhNUswfYRn6XX5iGKiAYjBYEToA%3d%3d',
        'vtpst': '|',
        'HAList': 'a-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sz-300042-%u6717%u79D1%u79D1%u6280%2Ca-sh-600916-N%u9EC4%u91D1%2Ca-sh-601818-%u5149%u5927%u94F6%u884C%2Ca-sz-002824-%u548C%u80DC%u80A1%u4EFD%2Ca-sz-002541-%u9E3F%u8DEF%u94A2%u6784%2Ca-sz-000723-%u7F8E%u9526%u80FD%u6E90',
        'intellpositionL': '862px',
        'intellpositionT': '4138px',
        'st_pvi': '07634999118497',
        'st_sp': '2019-10-18%2023%3A34%3A34',
        'st_inirUrl': 'https%3A%2F%2Fwww.baidu.com%2Flink',
        'st_sn': '{}'.format(st_sn),
        'st_psi': '{}'.format(st_psi),  # 20210208135742329-113200301321-2732748668
    }

    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://quote.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
    }

    response = req.get('http://push2.eastmoney.com/api/qt/clist/get'
                       , headers=headers, params=params,
                       cookies=cookies, verify=False)

    return response

def data_cleaning_industry_cinewstock(data):
    # 清洗行业成分股数据
    stock_code_list = jsonpath.jsonpath(data, '$..f12')
    name_list = jsonpath.jsonpath(data, '$..f14')
    # 最新价 price
    latest_price_list = jsonpath.jsonpath(data, '$..f2')
    # 涨跌幅 rate
    price_limit_list = jsonpath.jsonpath(data, '$..f3')
    # high
    high_list1 = jsonpath.jsonpath(data, '$..f15')
    # low
    low_list1 = jsonpath.jsonpath(data, '$..f16')
    # open
    open_list2 = jsonpath.jsonpath(data, '$..f17')
    # pre_close
    pre_close_list2 = jsonpath.jsonpath(data, '$..f18')
    # 换手率 tur_rate
    tur_rate_list3 = jsonpath.jsonpath(data, '$..f8')
    # 成交量 vol
    vol_list3 = jsonpath.jsonpath(data, '$..f5')
    # 成交额
    money_list4 = jsonpath.jsonpath(data, '$..f6')
    # 上市时间
    ipo_time = jsonpath.jsonpath(data, '$..f26')
    df = pd.DataFrame(stock_code_list, columns=['code'])
    df['name'] = name_list
    df['close'] = latest_price_list
    df['rate'] = price_limit_list
    df['high'] = high_list1
    df['low'] = low_list1
    df['open'] = open_list2
    df['pre_price'] = pre_close_list2
    df['tur_rate'] = tur_rate_list3
    df['vol'] = vol_list3
    df['money'] = money_list4
    df['ipo_time'] = ipo_time

    return df

def get_ex_new_stock_codes(max_acount=100):
    # 获取次新股净流入数据
    this_res_df = get_any_stock_codes(max_acount)
    return this_res_df

def get_st_stock_codes(max_acount=100):
    # 获取st股票
    st_psi = '20210208135742329-113200301321-2732748668'
    fs = 'm:0 f:4,m:1 f:4'
    this_res_df = get_any_stock_codes(max_acount, fid='f3', fs=fs, _='1612763862192', st_sn='71', st_psi=st_psi)
    return this_res_df

def get_any_stock_codes(max_acount=100, fid='f26', fs='m:0 f:8,m:1 f:8', _ ='1612757741404', st_sn='63', st_psi='20210208131233561-111000300841-9541724436'):
    this_res_df = pd.DataFrame()
    for page in range(1, max_acount):
        try:
            params = create_params_stock(page, fid=fid, fs=fs, _=_)
            response = get_response_stock(params, st_sn=st_sn, st_psi=st_psi)
            data = get_data(response)
            if data['data'] == None: break
            df = data_cleaning_industry_cinewstock(data)
            if df.empty: continue
            if this_res_df.empty:
                this_res_df = df.copy()
            else:
                this_res_df = pd.concat([this_res_df, df], axis=0)
        except Exception as ex:
            continue
    return this_res_df

##########################次新股/st股票################################

##########################港股全部股票代码################################
def create_hkstocks_params_stock(page, fid='f26', fs='m:0 f:8,m:1 f:8', _ ='1612757741404',pz='100'):
    params = {
        'pn': '{}'.format(page),
        'pz': '{}'.format(pz),
        'po': '1^',
        'np': '1^',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281^',
        'fltt': '2^',
        'invt': '2^',
        'fid': '{}'.format(fid),
        'fs': '{}'.format(fs),
        'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f11,f62,f128,f136,f115,f152',
        #'rt': '53407822^',
        # ('cb', 'jQuery1124024910121940634178_1612597304786^'),
        '_': '{}'.format(_),  # 1612763862192
    }
    return params

def get_hk_stocks_response_stock(params, st_sn='63', st_psi='20210208131233561-111000300841-9541724436'):
    # 行业成分股数据
    cookies = {
        'cowminicookie': 'true',
        'em_hq_fls': 'js',
        'st_si': '45897351155573',
        'waptgshowtime': '202128',
        'st_asi': 'delete',
        'cowCookie': 'true',
        'qgqp_b_id': '49621c65b51724aed8f10c0feea8ebdd',
        'p_origin': 'https%3A%2F%2Fpassport2.eastmoney.com',
        'ct': 'YF2mZ_op_nsxQ6S0vjtqz7xZBug0NTW-Mm6Byp5_AN1rC_rdlYZ1xjaMxYGw83mcmWk_PvOgHooY5mVdwDQLWcvDJTfxh846lCMkqInLiT3TS937AhyMS_ifiuqFhmks-s2CxKKSWWkrtaJeqWvAGiQ_wh0i8AuDh6RvKnHApig',
        'ut': 'FobyicMgeV6W21ICVIh67y2TdalzNIRdHh6UwIU-PHyOwFPXzPncgSsKJ2qXIFgvgxtvANYmJXUHCPD3tBIvfopl7NsepVBKFQucIcTwwlq-WX3qyvbPozoLToypptAjxUkKpVqGdUL6dks4Vtv1KKLXCmaAXp8mQrDOHpTHRZ8ft9gcUqPMUaAbnxmLu5qbISM7uGrJ2eSu7EROtLBVgwBhBZtzhNA0GzziXi8iq8h4fa763eyBwUxrtLUHrte9d4B-IaRwuRtmrYTnUmA_U7MpDN0Cg9SN',
        'sid': '159309191',
        'uidal': '1002094027214364%e9%a3%8e%e4%b9%90%e5%b2%9a%e9%9b%85',
        'pi': '1002094027214364%3bm1002094027214364%3b%e9%a3%8e%e4%b9%90%e5%b2%9a%e9%9b%85%3bKkSBKC5DEQXUZK%2fEwwInj5WpbSR7S9kOZClStvOBj5vyQqwv2KUUkGsgekCzZfAp7PBnK10Vte4lIgkGg4e29UVyk8rldPKAxxCQZZB%2bFaU%2f%2bQIjCG2szv9umvRmfATQdFwMfSwM4LpINTBsihhyEuepC3aYX6qC6DijSw4dq2peQgoVVJiLtpJDnoH4sGuqGjWjS3VR%3bFq%2frXacfR4VaN3Wx18VNtjXw2KuVPNo5kOvrPHe%2bNVWyeVYEtjlWK7oBKWl%2bo75bImrRt7cx5ghJefp12JaZe5x%2fVT4ZDGpzWfGyyakddYf9QkR5GKET23%2fXOPVnJazum2ROhNUswfYRn6XX5iGKiAYjBYEToA%3d%3d',
        'vtpst': '|',
        'HAList': 'a-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sz-300042-%u6717%u79D1%u79D1%u6280%2Ca-sh-600916-N%u9EC4%u91D1%2Ca-sh-601818-%u5149%u5927%u94F6%u884C%2Ca-sz-002824-%u548C%u80DC%u80A1%u4EFD%2Ca-sz-002541-%u9E3F%u8DEF%u94A2%u6784%2Ca-sz-000723-%u7F8E%u9526%u80FD%u6E90',
        'intellpositionL': '862px',
        'intellpositionT': '4138px',
        'st_pvi': '07634999118497',
        'st_sp': '2019-10-18%2023%3A34%3A34',
        'st_inirUrl': 'https%3A%2F%2Fwww.baidu.com%2Flink',
        'st_sn': '{}'.format(st_sn),
        'st_psi': '{}'.format(st_psi),  # 20210208135742329-113200301321-2732748668
    }

    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://quote.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
    }

    response = req.get('http://60.push2.eastmoney.com/api/qt/clist/get'
                       , headers=headers, params=params,
                       cookies=cookies, verify=False)

    return response

def data_cleaning_hk_stocks_cinewstock(data):
    # 清洗行业成分股数据
    stock_code_list = jsonpath.jsonpath(data, '$..f12')
    name_list = jsonpath.jsonpath(data, '$..f14')
    # 最新价 price
    latest_price_list = jsonpath.jsonpath(data, '$..f2')
    # 涨跌幅 rate
    price_limit_list = jsonpath.jsonpath(data, '$..f3')
    # high
    high_list1 = jsonpath.jsonpath(data, '$..f15')
    # low
    low_list1 = jsonpath.jsonpath(data, '$..f16')
    # open
    open_list2 = jsonpath.jsonpath(data, '$..f17')
    # pre_close
    pre_close_list2 = jsonpath.jsonpath(data, '$..f18')
    # 换手率 tur_rate
    tur_rate_list3 = jsonpath.jsonpath(data, '$..f8')
    # 成交量 vol
    vol_list3 = jsonpath.jsonpath(data, '$..f5')
    # 成交额
    money_list4 = jsonpath.jsonpath(data, '$..f6')
    # 上市时间
    ipo_time = jsonpath.jsonpath(data, '$..f26')
    df = pd.DataFrame(stock_code_list, columns=['code'])
    df['name'] = name_list
    df['close'] = latest_price_list
    df['rate'] = price_limit_list
    df['high'] = high_list1
    df['low'] = low_list1
    df['open'] = open_list2
    df['pre_price'] = pre_close_list2
    df['tur_rate'] = tur_rate_list3
    df['vol'] = vol_list3
    df['money'] = money_list4
    df['ipo_time'] = ipo_time

    return df

def get_hk_stock_codes(industry_code='800001', max_acount=50):
    # 获取行业成分股数据
    indus_dict = {'800001': '0475', '800002': '0485', '800003': '0420', '800004': '0725', '800005': '0421', '800006': '0474',
                   '800007': '0451', '800008': '0440', '800009': '0734', '800010': '0727', '800011': '0465', '800012': '0422',
                   '800013': '0484', '800014': '0726', '800015': '0424', '800016': '0436', '800017': '0482', '800018': '0450',
                   '800020': '0729', '800019': '0456',
                   '800021': '0425', '800022': '0476', '800023': '0740', '800024': '0427', '800025': '0429', '800026': '0728', '800027': '0433',
                   '800029': '0736', '800030': '0738', '800031': '0479', '800032': '0464', '800033': '0473', '800034': '0486', '800035': '0546',
                   '800036': '0539', '800037': '0438', '800038': '0428', '800039': '0477', '800040': '0735', '800041': '0545', '800042': '0448',
                   '800043': '0447', '800044': '0730', '800045': '0910', '800046': '0737', '800047': '0458', '800048': '0454', '800049': '0732',
                   '800050': '0478', '800051': '0480', '800052': '0733', '800053': '0457', '800054': '0481', '800055': '0538', '800056': '0470',
                   '800057': '0731', '800058': '0459', '800059': '0471', '800060': '0537', '800061': '0437', '800062': '0739'}
    this_res_df = pd.DataFrame()
    for page in range(1, max_acount):
        try:
            params = create_params_industry(page, indus_dict[industry_code])
            response = get_response_industry(params)
            data = get_data(response)
            if data['data'] == None: break
            df = data_cleaning_industry(data)
            if df.empty:continue
            if this_res_df.empty:
                this_res_df = df.copy()
            else:
                this_res_df = pd.concat([this_res_df, df], axis=0)
        except Exception as ex:
            continue
    return this_res_df

##########################港股全部股票代码################################

#↓↓↓↓↓↓↓↓↓↓↓↓↓↓个股财务数据接口↓↓↓↓↓↓↓↓↓↓↓↓↓↓

######################个股财务数据接口--主要指标#########################

def create_params_FinanceAnalysis(code):
    params = {
        'type': '1^',
        'code': '{}'.format(code),
    }
    return params

def get_response_FinanceAnalysis(params, type='1'):
    # 行业成分股数据
    cookies = {
        'cowminicookie': 'true',
        'em_hq_fls': 'js',
        'st_asi': 'delete',
        'cowCookie': 'true',
        'qgqp_b_id': '49621c65b51724aed8f10c0feea8ebdd',
        #'p_origin': 'https%3A%2F%2Fpassport2.eastmoney.com',
        'ct': 'YF2mZ_op_nsxQ6S0vjtqz7xZBug0NTW-Mm6Byp5_AN1rC_rdlYZ1xjaMxYGw83mcmWk_PvOgHooY5mVdwDQLWcvDJTfxh846lCMkqInLiT3TS937AhyMS_ifiuqFhmks-s2CxKKSWWkrtaJeqWvAGiQ_wh0i8AuDh6RvKnHApig',
        'ut': 'FobyicMgeV6W21ICVIh67y2TdalzNIRdHh6UwIU-PHyOwFPXzPncgSsKJ2qXIFgvgxtvANYmJXUHCPD3tBIvfopl7NsepVBKFQucIcTwwlq-WX3qyvbPozoLToypptAjxUkKpVqGdUL6dks4Vtv1KKLXCmaAXp8mQrDOHpTHRZ8ft9gcUqPMUaAbnxmLu5qbISM7uGrJ2eSu7EROtLBVgwBhBZtzhNA0GzziXi8iq8h4fa763eyBwUxrtLUHrte9d4B-IaRwuRtmrYTnUmA_U7MpDN0Cg9SN',
        'sid': '159309191',
        'st_si': '75137633692030',
        'uidal': '1002094027214364%e9%a3%8e%e4%b9%90%e5%b2%9a%e9%9b%85',
        'pi': '1002094027214364%3bm1002094027214364%3b%e9%a3%8e%e4%b9%90%e5%b2%9a%e9%9b%85%3bKkSBKC5DEQXUZK%2fEwwInj5WpbSR7S9kOZClStvOBj5vyQqwv2KUUkGsgekCzZfAp7PBnK10Vte4lIgkGg4e29UVyk8rldPKAxxCQZZB%2bFaU%2f%2bQIjCG2szv9umvRmfATQdFwMfSwM4LpINTBsihhyEuepC3aYX6qC6DijSw4dq2peQgoVVJiLtpJDnoH4sGuqGjWjS3VR%3bFq%2frXacfR4VaN3Wx18VNtjXw2KuVPNo5kOvrPHe%2bNVWyeVYEtjlWK7oBKWl%2bo75bImrRt7cx5ghJefp12JaZe5x%2fVT4ZDGpzWfGyyakddYf9QkR5GKET23%2fXOPVnJazum2ROhNUswfYRn6XX5iGKiAYjBYEToA%3d%3d',

        'vtpst': '|',
        'HAList': 'a-sh-601818-%u5149%u5927%u94F6%u884C%2Ca-sz-002824-%u548C%u80DC%u80A1%u4EFD%2Ca-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sz-002541-%u9E3F%u8DEF%u94A2%u6784%2Ca-sz-000723-%u7F8E%u9526%u80FD%u6E90',

        'intellpositionL': '862px',
        'intellpositionT': '4022px',
        'waptgshowtime': '202126',
        'st_pvi': '07634999118497',
        'st_sp': '2019-10-18%2023%3A34%3A34',
        'st_inirUrl': 'https%3A%2F%2Fwww.baidu.com%2Flink',
        'st_sn': '243',
        'st_psi': '20210206201949486-113301310291-2946330373',
    }
    url_ = 'http://f10.eastmoney.com/NewFinanceAnalysis/MainTargetAjax?type={}&code={}'.format(type, params.get('code'))
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        'Accept': '*/*',
       #'Referer': 'http://f10.eastmoney.com/NewFinanceAnalysis/MainTargetAjax',
        'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
    }
    #print('params:{}'.format(params))
    response = req.get(url_)
                       # , headers=headers, params=params,
                       # verify=False)
    print('url:{}'.format(response.url))
    return response

def data_cleaning_FinanceAnalysis(data):
    # 清洗行业成分股数据
    # 财务数据日期
    stock_dt_list = jsonpath.jsonpath(data, '$..date')
    # jbmgsy 基本每股收益(RMB)
    jbmgsy_list = jsonpath.jsonpath(data, '$..jbmgsy')
    # kfmgsy 扣非每股收益
    kfmgsy_list = jsonpath.jsonpath(data, '$..kfmgsy')
    # xsmgsy 稀释每股收益
    xsmgsy_list = jsonpath.jsonpath(data, '$..xsmgsy')
    # mgjzc  每股净资产
    mgjzc_list1 = jsonpath.jsonpath(data, '$..mgjzc')
    # mggjj  每股公积金(RMB)
    mggjj_list1 = jsonpath.jsonpath(data, '$..mggjj')
    # mgwfply  每股未分配利润
    mgwfply_list2 = jsonpath.jsonpath(data, '$..mgwfply')
    # mgjyxjl  每股经营现金流
    mgjyxjl_list2 = jsonpath.jsonpath(data, '$..mgjyxjl')
    # yyzsr  营业总收入(RMB)
    yyzsr_list3 = jsonpath.jsonpath(data, '$..yyzsr')
    # mlr 毛利润(RMB)
    mlr_list3 = jsonpath.jsonpath(data, '$..mlr')
    # gsjlr  归属净利润
    gsjlr_list4 = jsonpath.jsonpath(data, '$..gsjlr')
    # kfjlr  扣非净利润
    kfjlr_list6 = jsonpath.jsonpath(data, '$..kfjlr')
    # yyzsrtbzz (营业总收入同比增长(%))
    yyzsrtbzz_list6 = jsonpath.jsonpath(data, '$..yyzsrtbzz')
    # gsjlrtbzz  (归属净利润同比增长(%))
    gsjlrtbzz_list6 = jsonpath.jsonpath(data, '$..gsjlrtbzz')
    # kfjlrtbzz (扣非净利润同比增长(%))
    kfjlrtbzz_list6 = jsonpath.jsonpath(data, '$..kfjlrtbzz')
    # yyzsrgdhbzz  (营业总收入滚动环比增长(%))
    yyzsrgdhbzz_list6 = jsonpath.jsonpath(data, '$..yyzsrgdhbzz')
    # gsjlrgdhbzz  (归属净利润滚动环比增长(%))
    gsjlrgdhbzz_list6 = jsonpath.jsonpath(data, '$..gsjlrgdhbzz')
    # kfjlrgdhbzz   (扣非净利润滚动环比增长(%))
    kfjlrgdhbzz_list6 = jsonpath.jsonpath(data, '$..kfjlrgdhbzz')
    # jqjzcsyl  (ROE)
    jqjzcsyl_list6 = jsonpath.jsonpath(data, '$..jqjzcsyl')
    # tbjzcsyl  (摊薄ROE)
    tbjzcsyl_list6 = jsonpath.jsonpath(data, '$..tbjzcsyl')
    # tbzzcsyl   (摊薄ROA)
    tbzzcsyl_list6 = jsonpath.jsonpath(data, '$..tbzzcsyl')
    # mll  毛利率(%)
    mll_list6 = jsonpath.jsonpath(data, '$..mll')
    # jll  净利率(%)
    jll_list6 = jsonpath.jsonpath(data, '$..jll')
    # sjsl  实际税率(%)
    sjsl_list6 = jsonpath.jsonpath(data, '$..sjsl')
    # yskyysr   预收款/营收
    yskyysr_list6 = jsonpath.jsonpath(data, '$..yskyysr')
    # xsxjlyysr  销售现金流/营收
    xsxjlyysr_list6 = jsonpath.jsonpath(data, '$..xsxjlyysr')
    # jyxjlyysr  经营现金流/营收
    jyxjlyysr_list6 = jsonpath.jsonpath(data, '$..jyxjlyysr')
    # zzczzy   总资产周转率(次)
    zzczzy_list6 = jsonpath.jsonpath(data, '$..zzczzy')
    # yszkzzts   应收账款周转天数(天)
    yszkzzts_list6 = jsonpath.jsonpath(data, '$..yszkzzts')
    # chzzts   存款周转天数
    chzzts_list6 = jsonpath.jsonpath(data, '$..chzzts')
    # zcfzl   资产负债率
    zcfzl_list6 = jsonpath.jsonpath(data, '$..zcfzl')
    # ldzczfz   流动资产负债率
    ldzczfz_list6 = jsonpath.jsonpath(data, '$..ldzczfz')
    # ldbl   流动比率
    ldbl_list6 = jsonpath.jsonpath(data, '$..ldbl')
    # sdbl   速动比率
    sdbl_list6 = jsonpath.jsonpath(data, '$..sdbl')
    df = pd.DataFrame(jbmgsy_list, columns=['mgsy'])
    df['kfmgsy'] = kfmgsy_list
    df['xsmgsy'] = xsmgsy_list
    df['mgjzc'] = mgjzc_list1
    df['mggjj'] = mggjj_list1
    df['mgwfply'] = mgwfply_list2
    df['mgjyxjl'] = mgjyxjl_list2
    df['yyzsr'] = yyzsr_list3
    df['mlr'] = mlr_list3
    df['gsjlr'] = gsjlr_list4
    df['kfjlr'] = kfjlr_list6
    df['yyzsrtbzz'] = yyzsrtbzz_list6
    df['gsjlrtbzz'] = gsjlrtbzz_list6
    df['kfjlrtbzz'] = kfjlrtbzz_list6
    df['yyzsrgdhbzz'] = yyzsrgdhbzz_list6
    df['gsjlrgdhbzz'] = gsjlrgdhbzz_list6
    df['kfjlrgdhbzz'] = kfjlrgdhbzz_list6
    df['jqjzcsyl'] = jqjzcsyl_list6
    df['tbjzcsyl'] = tbjzcsyl_list6
    df['tbzzcsyl'] = tbzzcsyl_list6
    df['mll'] = mll_list6
    df['jll'] = jll_list6
    df['sjsl'] = sjsl_list6
    df['yskyysr'] = yskyysr_list6
    df['xsxjlyysr'] = xsxjlyysr_list6
    df['jyxjlyysr'] = jyxjlyysr_list6
    df['zzczzy'] = zzczzy_list6
    df['yszkzzts'] = yszkzzts_list6
    df['chzzts'] = chzzts_list6
    df['zcfzl'] = zcfzl_list6
    df['ldzczfz'] = ldzczfz_list6
    df['ldbl'] = ldbl_list6
    df['sdbl'] = sdbl_list6
    df['dt'] = stock_dt_list
    return df

## --主要指标(按年度)
def get_code_base_finance_year_data(code='SZ.000002'):
    # 获取个股主要财务数据数据【按年度】
    this_res_df = pd.DataFrame()
    code_ = code.replace('.', '')  #''.join(list(filter(str.isdigit, code)))
    try:
        params = create_params_FinanceAnalysis(code_)
        response = get_response_FinanceAnalysis(params)
        data = get_data(response)
        df = data_cleaning_FinanceAnalysis(data)
        this_res_df = df.copy()
        dt_list = list(this_res_df['dt'])
        this_res_df = this_res_df.T
        this_res_df.columns = dt_list
    except Exception as ex:
        return this_res_df
    return this_res_df

def get_all_codes_base_finance_year_data(code_list):
    # 获取全部个股主要财务数据数据
    this_res_df_list = []
    for code in code_list:
        this_res_df = pd.DataFrame()
        code_ = code.replace('.', '')  # ''.join(list(filter(str.isdigit, code)))
        print('code:{}'.format(code_))
        try:
            params = create_params_FinanceAnalysis(code_)
            response = get_response_FinanceAnalysis(params)
            data = get_data(response)
            df = data_cleaning_FinanceAnalysis(data)
            this_res_df_list.append(df)
        except Exception as ex:
            continue
        return this_res_df_list

## --主要指标(按报告期)
def get_code_base_finance_bgq_data(code='SH600000'):
    # 获取个股主要财务数据数据【按报告期】
    this_res_df = pd.DataFrame()
    code_ = code.replace('.', '')  # ''.join(list(filter(str.isdigit, code)))
    try:
        params = create_params_FinanceAnalysis(code_)
        response = get_response_FinanceAnalysis(params, type='0')
        data = get_data(response)
        df = data_cleaning_FinanceAnalysis(data)
        this_res_df = df.copy()
        dt_list = list(this_res_df['dt'])
        this_res_df = this_res_df.T
        this_res_df.columns = dt_list
    except Exception as ex:
        return this_res_df
    return this_res_df

def get_all_base_codes_finance_bgq_data(code_list):
    # 获取全部个股主要财务数据数据
    this_res_df_list = []
    for code in code_list:
        this_res_df = pd.DataFrame()
        code_ = code.replace('.', '')
        print('code:{}'.format(code_))
        try:
            params = create_params_FinanceAnalysis(code_)
            response = get_response_FinanceAnalysis(params, type='0')
            data = get_data(response)
            df = data_cleaning_FinanceAnalysis(data)
            this_res_df_list.append(df)
        except Exception as ex:
            continue
        return this_res_df_list

######################个股财务数据接口--主要指标#########################

#################################个股财务数据接口--现金流量#####################################
def create_params_FinanceAnalysis_xjll(code, reportDateType, reportType):
    # 个股的现金流量表
    params = {
        'companyType': '4',
        'reportDateType': '{}'.format(reportDateType),
        'reportType': '{}'.format(reportType),
        'endDate': '',
        'code': '{}'.format(code),
    }
    return params

def get_response_FinanceAnalysis_xjll(params):
    # 行业成分股数据
    cookies = {
        'cowminicookie': 'true',
        'em_hq_fls': 'js',
        'st_asi': 'delete',
        'cowCookie': 'true',
        'qgqp_b_id': '49621c65b51724aed8f10c0feea8ebdd',
        #'p_origin': 'https%3A%2F%2Fpassport2.eastmoney.com',
        'ct': 'YF2mZ_op_nsxQ6S0vjtqz7xZBug0NTW-Mm6Byp5_AN1rC_rdlYZ1xjaMxYGw83mcmWk_PvOgHooY5mVdwDQLWcvDJTfxh846lCMkqInLiT3TS937AhyMS_ifiuqFhmks-s2CxKKSWWkrtaJeqWvAGiQ_wh0i8AuDh6RvKnHApig',
        'ut': 'FobyicMgeV6W21ICVIh67y2TdalzNIRdHh6UwIU-PHyOwFPXzPncgSsKJ2qXIFgvgxtvANYmJXUHCPD3tBIvfopl7NsepVBKFQucIcTwwlq-WX3qyvbPozoLToypptAjxUkKpVqGdUL6dks4Vtv1KKLXCmaAXp8mQrDOHpTHRZ8ft9gcUqPMUaAbnxmLu5qbISM7uGrJ2eSu7EROtLBVgwBhBZtzhNA0GzziXi8iq8h4fa763eyBwUxrtLUHrte9d4B-IaRwuRtmrYTnUmA_U7MpDN0Cg9SN',
        'sid': '159309191',
        'st_si': '89957836747676',
        'uidal': '1002094027214364%e9%a3%8e%e4%b9%90%e5%b2%9a%e9%9b%85',
        'pi': '1002094027214364%3bm1002094027214364%3b%e9%a3%8e%e4%b9%90%e5%b2%9a%e9%9b%85%3bKkSBKC5DEQXUZK%2fEwwInj5WpbSR7S9kOZClStvOBj5vyQqwv2KUUkGsgekCzZfAp7PBnK10Vte4lIgkGg4e29UVyk8rldPKAxxCQZZB%2bFaU%2f%2bQIjCG2szv9umvRmfATQdFwMfSwM4LpINTBsihhyEuepC3aYX6qC6DijSw4dq2peQgoVVJiLtpJDnoH4sGuqGjWjS3VR%3bFq%2frXacfR4VaN3Wx18VNtjXw2KuVPNo5kOvrPHe%2bNVWyeVYEtjlWK7oBKWl%2bo75bImrRt7cx5ghJefp12JaZe5x%2fVT4ZDGpzWfGyyakddYf9QkR5GKET23%2fXOPVnJazum2ROhNUswfYRn6XX5iGKiAYjBYEToA%3d%3d',
        'vtpst': '|',
        'HAList': 'a-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sh-600916-N%u9EC4%u91D1%2Ca-sh-601818-%u5149%u5927%u94F6%u884C%2Ca-sz-002824-%u548C%u80DC%u80A1%u4EFD%2Ca-sz-002541-%u9E3F%u8DEF%u94A2%u6784%2Ca-sz-000723-%u7F8E%u9526%u80FD%u6E90',

        'intellpositionL': '862px',
        'intellpositionT': '4022px',
        'waptgshowtime': '202127',
        'st_pvi': '07634999118497',
        'st_sp': '2019-10-18%2023%3A34%3A34',
        'st_inirUrl': 'https%3A%2F%2Fwww.baidu.com%2Flink',
        'st_sn': '40',
        'st_psi': '20210207230123477-113200301201-0068749157',
    }
    url_ = 'http://f10.eastmoney.com/NewFinanceAnalysis/xjllbAjax?companyType=4&reportDateType={}&reportType={}&endDate=&code={}'.format(params.get('reportDateType'), params.get('reportType'), params.get('code'))
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        'Accept': '*/*',
       #'Referer': 'http://f10.eastmoney.com/NewFinanceAnalysis/MainTargetAjax',
        'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
    }
    #print('params:{}'.format(params))
    response = req.get(url_)
                       # , headers=headers, params=params,
                       # verify=False)
    print('url__:{}'.format(response.url))
    return response

def data_cleaning_FinanceAnalysis_xjll(data):
    # 清洗行业成分股数据
    js_datas = json.loads(data)
    date_list = [str(js_d['REPORTDATE'][:10]).replace('/', '-') for js_d in js_datas]
    net_operate_list = [js_d['NETOPERATECASHFLOW'] for js_d in js_datas]
    net_tinv_list = [js_d['NETINVCASHFLOW'] for js_d in js_datas]
    net_fina_list = [js_d['NETFINACASHFLOW'] for js_d in js_datas]
    df = pd.DataFrame(net_operate_list, columns=['net_operate'])
    df['net_tinv'] = net_tinv_list
    df['net_fina'] = net_fina_list
    df = df.T
    df.columns = list(date_list)
    return df

## 按年度
def get_code_finance_year_data_xjll(code='SZ.000002'):
    # 获取个股财务数据--现金流量【按年度】
    this_res_df = pd.DataFrame()
    code_ = code.replace('.', '')  #''.join(list(filter(str.isdigit, code)))
    try:
        params = create_params_FinanceAnalysis_xjll(code_, 1, 1)
        response = get_response_FinanceAnalysis_xjll(params)
        data = get_data(response)
        df = data_cleaning_FinanceAnalysis_xjll(data)
        this_res_df = df.copy()
        dt_list = list(this_res_df['dt'])
        this_res_df = this_res_df.T
        this_res_df.columns = dt_list
    except Exception as ex:
        return this_res_df
    return this_res_df

def get_all_codes_finance_year_data_xjll(code_list):
    # 获取所有个股现金流量数据【按年度】
    this_res_df_list = []
    this_res_df = pd.DataFrame()
    for code in code_list:
        code_ = code.replace('.', '')  #''.join(list(filter(str.isdigit, code)))
        try:
            params = create_params_FinanceAnalysis_xjll(code_, 1, 1)
            response = get_response_FinanceAnalysis_xjll(params)
            data = get_data(response)
            df = data_cleaning_FinanceAnalysis_xjll(data)
            this_res_df = df.copy()
            dt_list = list(this_res_df['dt'])
            this_res_df = this_res_df.T
            this_res_df.columns = dt_list
            this_res_df_list.append(this_res_df)
        except Exception as ex:
            continue
    return this_res_df_list

## 按报告期
def get_code_finance_bgq_data_xjll(code='SZ.000002'):
    # 获取个股主要财务数据数据【按报告期】
    this_res_df = pd.DataFrame()
    code_ = code.replace('.', '')
    try:
        params = create_params_FinanceAnalysis_xjll(code_, 0, 1)
        response = get_response_FinanceAnalysis_xjll(params)
        data = get_data(response)
        df = data_cleaning_FinanceAnalysis_xjll(data)
        this_res_df = df.copy()
        dt_list = list(this_res_df['dt'])
        this_res_df = this_res_df.T
        this_res_df.columns = dt_list
    except Exception as ex:
        return this_res_df
    return this_res_df

def get_all_codes_finance_bgq_data_xjll(code_list):
    # 获取所有个股现金流量数据【按报告期】
    this_res_df_list = []
    for code in code_list:
        code_ = code.replace('.', '')
        try:
            params = create_params_FinanceAnalysis_xjll(code_, 0, 1)
            response = get_response_FinanceAnalysis_xjll(params)
            data = get_data(response)
            df = data_cleaning_FinanceAnalysis_xjll(data)
            df['code'] = code
            this_res_df_list.append(df)
        except Exception as ex:
            continue
    return this_res_df_list
#################################个股财务数据接口--现金流量#####################################

#↑↑↑↑↑↑↑↑↑↑↑↑个股财务数据接口↑↑↑↑↑↑↑↑↑↑↑↑

########################个股资金净流入数据接口######################################
def create_n_params(page, pz = '5000', fid='f174', fields='f12,f14,f2,f160,f174,f175,f176,f177,f178,f179,f180,f181,f182,f183,f260,f261,f124'):
    params = {
        'fid': '{}'.format(fid),
        'po': '1',
        'pz': '{}'.format(pz),
        'pn': '{}'.format(str(page)),
        'np': '1',
        'fltt': '2',
        'invt': '2',
        'ut': 'b2884a393a59ad64002292a3e90d46a5',
        'fs': 'm:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,m:1+t:3+f:!2',
        'fields': '{}'.format(fields),
    }

    return params

def create_params(page, pz='200'):
    params = {
        'pz': '{}'.format(pz),
        'po': '1',
        'np': '1',
        'ut': 'b2884a393a59ad64002292a3e90d46a5',
        'fltt': '2',
        'invt': '2',
        'fid0': 'f4001',
        'fid': 'f62',
        'fs': 'm:0 t:6 f:^!2,m:0 t:13 f:^!2,m:0 t:80 f:^!2,m:1 t:2 f:^!2,m:1 t:23 f:^!2,m:0 t:7 f:^!2,m:1 t:3 f:^!2^',
        'stat': '1',
        'fields': 'f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124',
        'rt': '53407822',
        # ('cb', 'jQuery18307739865615069035_1602234656657^'),
        '_': '1602234665664',
    }
    value = str(page) + '^'
    params['pn'] = value
    # print(params)
    return params

def get_n_response(params, st_psi='20210208234232798-113300300813-0503004824', st_sn='149'):
    # 10日净流入数据
    cookies = {
        'cowminicookie': 'true',
        'em_hq_fls': 'js',
        'st_si': '81067005407350',
        'waptgshowtime': '202125',
        'st_asi': 'delete',
        'cowCookie': 'true',
        'qgqp_b_id': '49621c65b51724aed8f10c0feea8ebdd',
        'p_origin': 'https%3A%2F%2Fpassport2.eastmoney.com',
        'ct': 'YF2mZ_op_nsxQ6S0vjtqz7xZBug0NTW-Mm6Byp5_AN1rC_rdlYZ1xjaMxYGw83mcmWk_PvOgHooY5mVdwDQLWcvDJTfxh846lCMkqInLiT3TS937AhyMS_ifiuqFhmks-s2CxKKSWWkrtaJeqWvAGiQ_wh0i8AuDh6RvKnHApig',
        'ut': 'FobyicMgeV6W21ICVIh67y2TdalzNIRdHh6UwIU-PHyOwFPXzPncgSsKJ2qXIFgvgxtvANYmJXUHCPD3tBIvfopl7NsepVBKFQucIcTwwlq-WX3qyvbPozoLToypptAjxUkKpVqGdUL6dks4Vtv1KKLXCmaAXp8mQrDOHpTHRZ8ft9gcUqPMUaAbnxmLu5qbISM7uGrJ2eSu7EROtLBVgwBhBZtzhNA0GzziXi8iq8h4fa763eyBwUxrtLUHrte9d4B-IaRwuRtmrYTnUmA_U7MpDN0Cg9SN',
        'sid': '159309191',
        'uidal': '1002094027214364%e9%a3%8e%e4%b9%90%e5%b2%9a%e9%9b%85',
        'pi': '1002094027214364%3bm1002094027214364%3b%e9%a3%8e%e4%b9%90%e5%b2%9a%e9%9b%85%3bKkSBKC5DEQXUZK%2fEwwInj5WpbSR7S9kOZClStvOBj5vyQqwv2KUUkGsgekCzZfAp7PBnK10Vte4lIgkGg4e29UVyk8rldPKAxxCQZZB%2bFaU%2f%2bQIjCG2szv9umvRmfATQdFwMfSwM4LpINTBsihhyEuepC3aYX6qC6DijSw4dq2peQgoVVJiLtpJDnoH4sGuqGjWjS3VR%3bFq%2frXacfR4VaN3Wx18VNtjXw2KuVPNo5kOvrPHe%2bNVWyeVYEtjlWK7oBKWl%2bo75bImrRt7cx5ghJefp12JaZe5x%2fVT4ZDGpzWfGyyakddYf9QkR5GKET23%2fXOPVnJazum2ROhNUswfYRn6XX5iGKiAYjBYEToA%3d%3d',
        'vtpst': '|',
        'HAList': 'a-sh-601818-%u5149%u5927%u94F6%u884C%2Ca-sz-002824-%u548C%u80DC%u80A1%u4EFD%2Ca-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sz-002541-%u9E3F%u8DEF%u94A2%u6784%2Ca-sz-000723-%u7F8E%u9526%u80FD%u6E90',
        'st_psi': '{}'.format(st_psi),
        'intellpositionL': '862px',
        'intellpositionT': '755px',
        'st_pvi': '07634999118497',
        'st_sp': '2019-10-18%2023%3A34%3A34',
        'st_inirUrl': 'https%3A%2F%2Fwww.baidu.com%2Flink',
        'st_sn': '{}'.format(st_sn),  # 10-149  # 5-149  # 3-149
    }
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
    }
    response = req.get('http://push2.eastmoney.com/api/qt/clist/get'
                       , headers=headers, params=params,
                       cookies=cookies, verify=False)
    #print('cookies:{}'.format(cookies))
    #print('url:{}'.format(response.url))
    #print('response.text:{}'.format(response.text))
    return response

def get_5_response(params):
    # 5日净流入数据
    #url_ ='http://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112308236517126513889_1612519999904&fid=f267&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A0%2Bt%3A6%2Bf%3A!2%2Cm%3A0%2Bt%3A13%2Bf%3A!2%2Cm%3A0%2Bt%3A80%2Bf%3A!2%2Cm%3A1%2Bt%3A2%2Bf%3A!2%2Cm%3A1%2Bt%3A23%2Bf%3A!2%2Cm%3A0%2Bt%3A7%2Bf%3A!2%2Cm%3A1%2Bt%3A3%2Bf%3A!2&fields=f12%2Cf14%2Cf2%2Cf127%2Cf267%2Cf268%2Cf269%2Cf270%2Cf271%2Cf272%2Cf273%2Cf274%2Cf275%2Cf276%2Cf257%2Cf258%2Cf124'
    cookies = {
        'cowminicookie': 'true',
        'em_hq_fls': 'js',
        'ct': 'YF2mZ_op_nsxQ6S0vjtqz7xZBug0NTW-Mm6Byp5_AN1rC_rdlYZ1xjaMxYGw83mcmWk_PvOgHooY5mVdwDQLWcvDJTfxh846lCMkqInLiT3TS937AhyMS_ifiuqFhmks-s2CxKKSWWkrtaJeqWvAGiQ_wh0i8AuDh6RvKnHApig',
        'ut': 'FobyicMgeV6W21ICVIh67y2TdalzNIRdHh6UwIU-PHyOwFPXzPncgSsKJ2qXIFgvgxtvANYmJXUHCPD3tBIvfopl7NsepVBKFQucIcTwwlq-WX3qyvbPozoLToypptAjxUkKpVqGdUL6dks4Vtv1KKLXCmaAXp8mQrDOHpTHRZ8ft9gcUqPMUaAbnxmLu5qbISM7uGrJ2eSu7EROtLBVgwBhBZtzhNA0GzziXi8iq8h4fa763eyBwUxrtLUHrte9d4B-IaRwuRtmrYTnUmA_U7MpDN0Cg9SN',
        'st_si': '45897351155573',
        'waptgshowtime': '202128',
        'st_asi': 'delete',
        'cowCookie': 'true',
        'p_origin': 'https%3A%2F%2Fpassport2.eastmoney.com',
        'sid': '159309191',
        'uidal': '1002094027214364%e9%a3%8e%e4%b9%90%e5%b2%9a%e9%9b%85',
        'pi': '1002094027214364%3bm1002094027214364%3b%e9%a3%8e%e4%b9%90%e5%b2%9a%e9%9b%85%3bKkSBKC5DEQXUZK%2fEwwInj5WpbSR7S9kOZClStvOBj5vyQqwv2KUUkGsgekCzZfAp7PBnK10Vte4lIgkGg4e29UVyk8rldPKAxxCQZZB%2bFaU%2f%2bQIjCG2szv9umvRmfATQdFwMfSwM4LpINTBsihhyEuepC3aYX6qC6DijSw4dq2peQgoVVJiLtpJDnoH4sGuqGjWjS3VR%3bFq%2frXacfR4VaN3Wx18VNtjXw2KuVPNo5kOvrPHe%2bNVWyeVYEtjlWK7oBKWl%2bo75bImrRt7cx5ghJefp12JaZe5x%2fVT4ZDGpzWfGyyakddYf9QkR5GKET23%2fXOPVnJazum2ROhNUswfYRn6XX5iGKiAYjBYEToA%3d%3d',
        'vtpst': '|',
        'HAList': 'a-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Cd-hk-01024%2Cd-hk-06185%2Ca-sz-300042-%u6717%u79D1%u79D1%u6280%2Ca-sh-600916-N%u9EC4%u91D1%2Ca-sh-601818-%u5149%u5927%u94F6%u884C%2Ca-sz-002824-%u548C%u80DC%u80A1%u4EFD%2Ca-sz-002541-%u9E3F%u8DEF%u94A2%u6784%2Ca-sz-000723-%u7F8E%u9526%u80FD%u6E90',
        'st_psi': '20210208235349757-113300300813-2575167314',  # 20210208235349757-113300300813-2575167314
        'intellpositionL': '862px',
        'intellpositionT': '955px',
        'EMFUND1': 'null',
        'EMFUND2': 'null',
        'EMFUND3': 'null',
        'EMFUND4': 'null',
        'EMFUND5': 'null',
        'EMFUND6': 'null',
        'EMFUND7': 'null',
        'EMFUND8': 'null',
        'EMFUND9': '02-08 14:54:20@#$%u534E%u6CF0%u67CF%u745E%u6CAA%u6DF1300ETF@%23%24510300',
        'qgqp_b_id': '49621c65b51724aed8f10c0feea8ebdd',
        'st_pvi': '07634999118497',
        'st_sp': '2019-10-18%2023%3A34%3A34',
        'st_inirUrl': 'https%3A%2F%2Fwww.baidu.com%2Flink',
        'st_sn': '150',
    }

    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
    }

    response = req.get('http://push2.eastmoney.com/api/qt/clist/get'
                       , headers=headers, params=params,
                       cookies=cookies, verify=False)
    print('url:{}'.format(response.url))
    return response

def get_3_response(params):
    # 3日净流入数据
    cookies = {
        'cowminicookie': 'true',
        'em_hq_fls': 'js',
        'st_si': '81067005407350',
        'waptgshowtime': '202125',
        'st_asi': 'delete',
        'cowCookie': 'true',
        'qgqp_b_id': '49621c65b51724aed8f10c0feea8ebdd',
        'p_origin': 'https%3A%2F%2Fpassport2.eastmoney.com',
        'ct': 'YF2mZ_op_nsxQ6S0vjtqz7xZBug0NTW-Mm6Byp5_AN1rC_rdlYZ1xjaMxYGw83mcmWk_PvOgHooY5mVdwDQLWcvDJTfxh846lCMkqInLiT3TS937AhyMS_ifiuqFhmks-s2CxKKSWWkrtaJeqWvAGiQ_wh0i8AuDh6RvKnHApig',
        'ut': 'FobyicMgeV6W21ICVIh67y2TdalzNIRdHh6UwIU-PHyOwFPXzPncgSsKJ2qXIFgvgxtvANYmJXUHCPD3tBIvfopl7NsepVBKFQucIcTwwlq-WX3qyvbPozoLToypptAjxUkKpVqGdUL6dks4Vtv1KKLXCmaAXp8mQrDOHpTHRZ8ft9gcUqPMUaAbnxmLu5qbISM7uGrJ2eSu7EROtLBVgwBhBZtzhNA0GzziXi8iq8h4fa763eyBwUxrtLUHrte9d4B-IaRwuRtmrYTnUmA_U7MpDN0Cg9SN',
        'sid': '159309191',
        'uidal': '1002094027214364%e9%a3%8e%e4%b9%90%e5%b2%9a%e9%9b%85',
        'pi': '1002094027214364%3bm1002094027214364%3b%e9%a3%8e%e4%b9%90%e5%b2%9a%e9%9b%85%3bKkSBKC5DEQXUZK%2fEwwInj5WpbSR7S9kOZClStvOBj5vyQqwv2KUUkGsgekCzZfAp7PBnK10Vte4lIgkGg4e29UVyk8rldPKAxxCQZZB%2bFaU%2f%2bQIjCG2szv9umvRmfATQdFwMfSwM4LpINTBsihhyEuepC3aYX6qC6DijSw4dq2peQgoVVJiLtpJDnoH4sGuqGjWjS3VR%3bFq%2frXacfR4VaN3Wx18VNtjXw2KuVPNo5kOvrPHe%2bNVWyeVYEtjlWK7oBKWl%2bo75bImrRt7cx5ghJefp12JaZe5x%2fVT4ZDGpzWfGyyakddYf9QkR5GKET23%2fXOPVnJazum2ROhNUswfYRn6XX5iGKiAYjBYEToA%3d%3d',
        'vtpst': '|',
        'HAList': 'a-sh-601818-%u5149%u5927%u94F6%u884C%2Ca-sz-002824-%u548C%u80DC%u80A1%u4EFD%2Ca-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sz-002541-%u9E3F%u8DEF%u94A2%u6784%2Ca-sz-000723-%u7F8E%u9526%u80FD%u6E90',
        'intellpositionL': '862px',
        'intellpositionT': '1076px',
        'st_pvi': '07634999118497',
        'st_sp': '2019-10-18%2023%3A34%3A34',
        'st_inirUrl': 'https%3A%2F%2Fwww.baidu.com%2Flink',
        'st_sn': '25',
        'st_psi': '202102051813208-113300300813-8444984507',
    }

    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
    }

    response = req.get('http://push2.eastmoney.com/api/qt/clist/get'
                       , headers=headers, params=params,
                       cookies=cookies, verify=False)
    #print('url:{}'.format(response.url))
    return response

def get_response(params):
    cookies = {
        'waptgshowtime': '2020109',
        'st_si': '62033869304648',
        'st_asi': 'delete',
        'cowCookie': 'true',
        'qgqp_b_id': 'b6a504ec0746ecec06a8c9db5dde3bec',
        'intellpositionL': '249px',
        'intellpositionT': '755px',
        'st_pvi': '93530241304569',
        'st_sp': '2020-09-19^%^2017^%^3A34^%^3A43',
        'st_inirUrl': 'https^%^3A^%^2F^%^2Fwww.eastmoney.com^%^2F',
        'st_sn': '28',
        'st_psi': '20201009171102245-113300300813-9103840696',
    }

    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
    }

    response = req.get('http://push2.eastmoney.com/api/qt/clist/get', headers=headers, params=params,
                            cookies=cookies, verify=False)
    #print('respon:{}'.format(response.text))
    return response

def get_data(response):
    try:
        content = response.text
        data = json.loads(content)
    except Exception as ex:
        print('get_data抛异常:{}'.format(ex))
    # data = json.dumps(data)
    return data

def data_10_cleaning(data):
    # 清洗10天资金净流入数据
    # print('data:{}'.format(data))
    stock_code_list = jsonpath.jsonpath(data, '$..f12')
    name_list = jsonpath.jsonpath(data, '$..f14')
    latest_price_list = jsonpath.jsonpath(data, '$..f2')
    price_limit_list = jsonpath.jsonpath(data, '$..f160')
    # 主力净流入
    net_amount_list1 = jsonpath.jsonpath(data, '$..f174')
    net_proportion_list1 = jsonpath.jsonpath(data, '$..f175')
    # 超大单净流入
    net_amount_list2 = jsonpath.jsonpath(data, '$..f176')
    net_proportion_list2 = jsonpath.jsonpath(data, '$..f177')
    # 大单净流入
    net_amount_list3 = jsonpath.jsonpath(data, '$..f178')
    net_proportion_list3 = jsonpath.jsonpath(data, '$..f179')
    # 中单净流入
    net_amount_list4 = jsonpath.jsonpath(data, '$..f180')
    net_proportion_list4 = jsonpath.jsonpath(data, '$..f181')
    # 小单净流入
    net_amount_list5 = jsonpath.jsonpath(data, '$..f182')
    net_proportion_list5 = jsonpath.jsonpath(data, '$..f183')
    df = pd.DataFrame(stock_code_list, columns=['代码'])
    df['名称'] = name_list
    df['最新价'] = latest_price_list
    df['涨跌幅(%)'] = price_limit_list
    df['主力净流入-净额'] = net_amount_list1
    df['主力净流入-净占比(%)'] = net_proportion_list1
    df['超大单净流入-净额'] = net_amount_list2
    df['超大单净流入-净占比(%)'] = net_proportion_list2
    df['大单净流入-净额'] = net_amount_list3
    df['大单净流入-净占比(%)'] = net_proportion_list3
    df['中单净流入-净额'] = net_amount_list4
    df['中单净流入-净占比(%)'] = net_proportion_list4
    df['小单净流入-净额'] = net_amount_list5
    df['小单净流入-净占比(%)'] = net_proportion_list5
    # df['名称'] = name_list
    # df['close'] = latest_price_list
    # df['rate'] = price_limit_list
    # df['zhuliu-e'] = net_amount_list1
    # df['zhuliu-rate'] = net_proportion_list1
    # df['chaodd-e'] = net_amount_list2
    # df['chaodd-rate'] = net_proportion_list2
    # df['大单净流入-净额'] = net_amount_list3
    # df['大单净流入-净占比(%)'] = net_proportion_list3
    # df['中单净流入-净额'] = net_amount_list4
    # df['中单净流入-净占比(%)'] = net_proportion_list4
    # df['小单净流入-净额'] = net_amount_list5
    # df['小单净流入-净占比(%)'] = net_proportion_list5
    # print('my_df:{}'.format(df[['名称', 'close', 'rate', 'zhuliu-e', 'zhuliu-rate', 'chaodd-e', 'chaodd-rate']]))
    return df

def data_5_cleaning(data):
    # 清洗5天资金净流入数据
    #print('data:{}'.format(data))
    stock_code_list = jsonpath.jsonpath(data, '$..f12')
    print('stock_code_list:{}'.format(stock_code_list))
    name_list = jsonpath.jsonpath(data, '$..f14')
    latest_price_list = jsonpath.jsonpath(data, '$..f2')
    print('latest_price_list:{}'.format(latest_price_list))
    price_limit_list = jsonpath.jsonpath(data, '$..f109')
    print('price_limit_list:{}'.format(price_limit_list))
    # 主力净流入
    net_amount_list1 = jsonpath.jsonpath(data, '$..f164')
    net_proportion_list1 = jsonpath.jsonpath(data, '$..f165')
    # 超大单净流入
    net_amount_list2 = jsonpath.jsonpath(data, '$..f166')
    net_proportion_list2 = jsonpath.jsonpath(data, '$..f167')
    # 大单净流入
    net_amount_list3 = jsonpath.jsonpath(data, '$..f168')
    net_proportion_list3 = jsonpath.jsonpath(data, '$..f169')
    # 中单净流入
    net_amount_list4 = jsonpath.jsonpath(data, '$..f170')
    net_proportion_list4 = jsonpath.jsonpath(data, '$..f171')
    # 小单净流入
    net_amount_list5 = jsonpath.jsonpath(data, '$..f172')
    net_proportion_list5 = jsonpath.jsonpath(data, '$..f173')
    print('net_amount_list1:{}'.format(net_amount_list1))
    print('net_amount_list2:{}'.format(net_amount_list2))
    df = pd.DataFrame(stock_code_list, columns=['代码'])
    df['名称'] = name_list
    df['最新价'] = latest_price_list
    df['涨跌幅(%)'] = price_limit_list
    df['主力净流入-净额'] = net_amount_list1
    df['主力净流入-净占比(%)'] = net_proportion_list1
    df['超大单净流入-净额'] = net_amount_list2
    df['超大单净流入-净占比(%)'] = net_proportion_list2
    df['大单净流入-净额'] = net_amount_list3
    df['大单净流入-净占比(%)'] = net_proportion_list3
    df['中单净流入-净额'] = net_amount_list4
    df['中单净流入-净占比(%)'] = net_proportion_list4
    df['小单净流入-净额'] = net_amount_list5
    df['小单净流入-净占比(%)'] = net_proportion_list5
    return df

def data_3_cleaning(data):
    # 清洗3天资金净流入数据
    #print('data:{}'.format(data))
    stock_code_list = jsonpath.jsonpath(data, '$..f12')
    name_list = jsonpath.jsonpath(data, '$..f14')
    latest_price_list = jsonpath.jsonpath(data, '$..f2')
    price_limit_list = jsonpath.jsonpath(data, '$..f3')
    # 主力净流入
    net_amount_list1 = jsonpath.jsonpath(data, '$..f267')
    net_proportion_list1 = jsonpath.jsonpath(data, '$..f268')
    # 超大单净流入
    net_amount_list2 = jsonpath.jsonpath(data, '$..f269')
    net_proportion_list2 = jsonpath.jsonpath(data, '$..f270')
    # 大单净流入
    net_amount_list3 = jsonpath.jsonpath(data, '$..f271')
    net_proportion_list3 = jsonpath.jsonpath(data, '$..f272')
    # 中单净流入
    net_amount_list4 = jsonpath.jsonpath(data, '$..f273')
    net_proportion_list4 = jsonpath.jsonpath(data, '$..f274')
    # 小单净流入
    net_amount_list5 = jsonpath.jsonpath(data, '$..f275')
    net_proportion_list5 = jsonpath.jsonpath(data, '$..f276')
    df = pd.DataFrame(stock_code_list, columns=['代码'])
    df['名称'] = name_list
    df['最新价'] = latest_price_list
    df['涨跌幅(%)'] = price_limit_list
    df['主力净流入-净额'] = net_amount_list1
    df['主力净流入-净占比(%)'] = net_proportion_list1
    df['超大单净流入-净额'] = net_amount_list2
    df['超大单净流入-净占比(%)'] = net_proportion_list2
    df['大单净流入-净额'] = net_amount_list3
    df['大单净流入-净占比(%)'] = net_proportion_list3
    df['中单净流入-净额'] = net_amount_list4
    df['中单净流入-净占比(%)'] = net_proportion_list4
    df['小单净流入-净额'] = net_amount_list5
    df['小单净流入-净占比(%)'] = net_proportion_list5
    return df

def data_cleaning(data, page):
    stock_code_list = jsonpath.jsonpath(data, '$..f12')
    name_list = jsonpath.jsonpath(data, '$..f14')
    latest_price_list = jsonpath.jsonpath(data, '$..f2')
    price_limit_list = jsonpath.jsonpath(data, '$..f3')
    # 主力净流入
    net_amount_list1 = jsonpath.jsonpath(data, '$..f62')
    net_proportion_list1 = jsonpath.jsonpath(data, '$..f184')
    # 超大单净流入
    net_amount_list2 = jsonpath.jsonpath(data, '$..f66')
    net_proportion_list2 = jsonpath.jsonpath(data, '$..f69')
    # 大单净流入
    net_amount_list3 = jsonpath.jsonpath(data, '$..f72')
    net_proportion_list3 = jsonpath.jsonpath(data, '$..f75')
    # 中单净流入
    net_amount_list4 = jsonpath.jsonpath(data, '$..f78')
    net_proportion_list4 = jsonpath.jsonpath(data, '$..f81')
    # 小单净流入
    net_amount_list5 = jsonpath.jsonpath(data, '$..f84')
    net_proportion_list5 = jsonpath.jsonpath(data, '$..f87')
    df = pd.DataFrame(stock_code_list, columns=['代码'])
    df['名称'] = name_list
    df['最新价'] = latest_price_list
    df['涨跌幅(%)'] = price_limit_list
    df['主力净流入-净额'] = net_amount_list1
    df['主力净流入-净占比(%)'] = net_proportion_list1
    df['超大单净流入-净额'] = net_amount_list2
    df['超大单净流入-净占比(%)'] = net_proportion_list2
    df['大单净流入-净额'] = net_amount_list3
    df['大单净流入-净占比(%)'] = net_proportion_list3
    df['中单净流入-净额'] = net_amount_list4
    df['中单净流入-净占比(%)'] = net_proportion_list4
    df['小单净流入-净额'] = net_amount_list5
    df['小单净流入-净占比(%)'] = net_proportion_list5

    return df

def get_10_net_trade_data(max_acount=10):
    # 获取10天资金净流入数据
    this_res_df = pd.DataFrame()
    for page in range(1, max_acount):
        try:
            params = create_n_params(page)
            response = get_n_response(params)
            data = get_data(response)
            if data['data'] == None: break
            df = data_10_cleaning(data)
            if this_res_df.empty:
                this_res_df = df.copy()
            else:
                this_res_df = pd.concat([this_res_df, df], axis=0)
        except Exception as ex:
            continue
    return this_res_df

def get_5_net_trade_data(max_acount=10):
    # 获取5天资金净流入数据
    this_res_df = pd.DataFrame()
    st_psi = '20210209000929936-113300300813-1536072674'
    fields = 'f12,f14,f2,f109,f164,f165,f166,f167,f168,f169,f170,f171,f172,f173,f257,f258,f124'
    for page in range(1, max_acount):
        try:
            params = create_n_params(page, fid='f164', fields=fields)
            response = get_n_response(params, st_psi=st_psi, st_sn='152')
            # print('respon.text:{}'.format(response.text))
            data = get_data(response)
            if data['data'] == None: break
            df = data_5_cleaning(data)
            if this_res_df.empty:
                this_res_df = df.copy()
            else:
                this_res_df = pd.concat([this_res_df, df], axis=0)
        except Exception as ex:
            continue
    return this_res_df

def get_3_net_trade_data(max_acount=10):
    # 获取3天资金净流入数据
    this_res_df = pd.DataFrame()
    fields = 'f12,f14,f2,f127,f267,f268,f269,f270,f271,f272,f273,f274,f275,f276,f257,f258,f124'
    st_psi = '20210209000929936-113300300813-1536072674'
    for page in range(1, max_acount):
        try:
            params = create_n_params(page, fid='f267', fields=fields)
            response = get_n_response(params, st_psi=st_psi, st_sn='152')
            data = get_data(response)
            if data['data'] == None:break
            df = data_3_cleaning(data)
            if this_res_df.empty:
                this_res_df = df.copy()
            else:
                this_res_df = pd.concat([this_res_df, df], axis=0)
        except Exception as ex:
            continue
    return this_res_df

def get_net_trade_data(max_acount=2000):
    # 获取A股净流入数据
    this_res_df = pd.DataFrame()
    for page in range(1, max_acount):
        try:
            params = create_params(page)
            response = get_response(params)
            data = get_data(response)
            if data['data'] == None: break
            df = data_cleaning(data, page=page)
            if this_res_df.empty:
                this_res_df = df.copy()
            else:
                this_res_df = pd.concat([this_res_df, df], axis=0)
        except Exception as ex:
            continue
    return this_res_df

## 个股历史资金净流入数据
def create_his_net_capital_params(code):
    params = {
        'lmt': '0^',
        'klt': '101^',
        'secid': '{}'.format(code),
        'ut': 'b2884a393a59ad64002292a3e90d46a5',
        #'fs': 'm:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,m:1+t:3+f:!2',
        'fields1': 'f1,f2,f3,f7',
        'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65',
        #'cb': 'jQuery18307739865615069035_1602234656657^'
        '_': '1612750504965',
    }
    # value = str(page) + '^'
    # params['pn'] = value
    # print(params)
    return params

def get_his_net_capital_response(params):
    # get历史净流入数据
    cookies = {
        'cowminicookie': 'true',
        'em_hq_fls': 'js',
        'st_si': '45897351155573',
        'waptgshowtime': '202128',
        'st_asi': 'delete',
        'cowCookie': 'true',
        'qgqp_b_id': '49621c65b51724aed8f10c0feea8ebdd',
        'p_origin': 'https%3A%2F%2Fpassport2.eastmoney.com',
        'ct': 'YF2mZ_op_nsxQ6S0vjtqz7xZBug0NTW-Mm6Byp5_AN1rC_rdlYZ1xjaMxYGw83mcmWk_PvOgHooY5mVdwDQLWcvDJTfxh846lCMkqInLiT3TS937AhyMS_ifiuqFhmks-s2CxKKSWWkrtaJeqWvAGiQ_wh0i8AuDh6RvKnHApig',
        'ut': 'FobyicMgeV6W21ICVIh67y2TdalzNIRdHh6UwIU-PHyOwFPXzPncgSsKJ2qXIFgvgxtvANYmJXUHCPD3tBIvfopl7NsepVBKFQucIcTwwlq-WX3qyvbPozoLToypptAjxUkKpVqGdUL6dks4Vtv1KKLXCmaAXp8mQrDOHpTHRZ8ft9gcUqPMUaAbnxmLu5qbISM7uGrJ2eSu7EROtLBVgwBhBZtzhNA0GzziXi8iq8h4fa763eyBwUxrtLUHrte9d4B-IaRwuRtmrYTnUmA_U7MpDN0Cg9SN',
        'sid': '159309191',
        'uidal': '1002094027214364%e9%a3%8e%e4%b9%90%e5%b2%9a%e9%9b%85',
        'pi': '1002094027214364%3bm1002094027214364%3b%e9%a3%8e%e4%b9%90%e5%b2%9a%e9%9b%85%3bKkSBKC5DEQXUZK%2fEwwInj5WpbSR7S9kOZClStvOBj5vyQqwv2KUUkGsgekCzZfAp7PBnK10Vte4lIgkGg4e29UVyk8rldPKAxxCQZZB%2bFaU%2f%2bQIjCG2szv9umvRmfATQdFwMfSwM4LpINTBsihhyEuepC3aYX6qC6DijSw4dq2peQgoVVJiLtpJDnoH4sGuqGjWjS3VR%3bFq%2frXacfR4VaN3Wx18VNtjXw2KuVPNo5kOvrPHe%2bNVWyeVYEtjlWK7oBKWl%2bo75bImrRt7cx5ghJefp12JaZe5x%2fVT4ZDGpzWfGyyakddYf9QkR5GKET23%2fXOPVnJazum2ROhNUswfYRn6XX5iGKiAYjBYEToA%3d%3d',
        'vtpst': '|',
        'HAList': 'a-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sh-600916-N%u9EC4%u91D1%2Ca-sh-601818-%u5149%u5927%u94F6%u884C%2Ca-sz-002824-%u548C%u80DC%u80A1%u4EFD%2Ca-sz-002541-%u9E3F%u8DEF%u94A2%u6784%2Ca-sz-000723-%u7F8E%u9526%u80FD%u6E90',
        'st_psi': '20210208101455207-111000300841-3442523035',
        'intellpositionL': '862px',
        'intellpositionT': '455px',
        'st_pvi': '07634999118497',
        'st_sp': '2019-10-18%2023%3A34%3A34',
        'st_inirUrl': 'https%3A%2F%2Fwww.baidu.com%2Flink',
        'st_sn': '10',
    }

    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
    }

    response = req.get('http://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get'
                       , headers=headers, params=params,
                       cookies=cookies, verify=False)
    print('url:{}'.format(response.url))
    return response

def data_his_net_capital_cleaning(data):
    # 清洗历史资金净流入数据
    CODE = data['data']['code']
    code = 'SH.' + CODE if CODE[0] == '6' else 'SZ.' + CODE
    name = data['data']['name']
    cap_data_list = list(data['data']['klines'])
    f_list = [data_cap.split(',')[:-2] for data_cap in cap_data_list]
    f_df = pd.DataFrame(f_list, columns=['date', '主力净流入-净额', '小单净流入-净额', '中单净流入-净额', '大单净流入-净额', '超大单净流入-净额', '主力净流入-净占比', '小单净流入-净占比', '中单净流入-净占比', '大单净流入-净占比', '超大单净流入-净占比', '最新价', '涨跌幅(%)'])
    f_df['code'] = code
    f_df['name'] = name
    return f_df

def get_his_net_capital_trade_data(code='SZ.000002'):
    # 获取历史资金净流入数据
    this_res_df = pd.DataFrame()
    code = re.sub('\D', '', code)
    try:
        code_ = '1.' + code if code[0] == '6' else '0.' + code
        params = create_his_net_capital_params(code_)
        response = get_his_net_capital_response(params)
        data = get_data(response)
        this_res_df = data_his_net_capital_cleaning(data)

    except Exception as ex:
        return this_res_df
    return this_res_df

########################个股资金净流入数据接口######################################

#↓↓↓↓↓北向资金数据#########################

######################板块###########################
def create_northbound_params(page, type = 'HSGT20_HYTJ_SUM', st = 'ShareSZ_ZC', ps='100'):
    params = {
        'type': '{}'.format(type),
        'token': '894050c76af8597a853f5b408b759f5d',
        'st': '{}'.format(st),  # ShareSZ_Chg_One
        'sr': '-1',
        'p': '{}'.format(page),
        'ps': '{}'.format(ps),
        #'js': '{pages:(tp),data:(x)}',
        'filter': "(DateType='1')",
        'rt': '53759291',
    }
    return params

def get_northbound_response(params, ct, st_sn = '107', st_psi = '20210208181044839-113300303602-3463249747', intellpositionT = '848px'):
    # 北向资金数据
    cookies = {
        'cowminicookie': 'true',
        'em_hq_fls': 'js',
        'st_si': '45897351155573',
        'waptgshowtime': '202128',
        'st_asi': 'delete',
        'cowCookie': 'true',
        'qgqp_b_id': '49621c65b51724aed8f10c0feea8ebdd',
        'p_origin': 'https%3A%2F%2Fpassport2.eastmoney.com',
        'ct': '{}'.format(ct),
        'ut': 'FobyicMgeV6W21ICVIh67y2TdalzNIRdHh6UwIU-PHyOwFPXzPncgSsKJ2qXIFgvgxtvANYmJXUHCPD3tBIvfopl7NsepVBKFQucIcTwwlq-WX3qyvbPozoLToypptAjxUkKpVqGdUL6dks4Vtv1KKLXCmaAXp8mQrDOHpTHRZ8ft9gcUqPMUaAbnxmLu5qbISM7uGrJ2eSu7EROtLBVgwBhBZtzhNA0GzziXi8iq8h4fa763eyBwUxrtLUHrte9d4B-IaRwuRtmrYTnUmA_U7MpDN0Cg9SN',
        'sid': '159309191',
        'uidal': '1002094027214364%e9%a3%8e%e4%b9%90%e5%b2%9a%e9%9b%85',
        'pi': '1002094027214364%3bm1002094027214364%3b%e9%a3%8e%e4%b9%90%e5%b2%9a%e9%9b%85%3bKkSBKC5DEQXUZK%2fEwwInj5WpbSR7S9kOZClStvOBj5vyQqwv2KUUkGsgekCzZfAp7PBnK10Vte4lIgkGg4e29UVyk8rldPKAxxCQZZB%2bFaU%2f%2bQIjCG2szv9umvRmfATQdFwMfSwM4LpINTBsihhyEuepC3aYX6qC6DijSw4dq2peQgoVVJiLtpJDnoH4sGuqGjWjS3VR%3bFq%2frXacfR4VaN3Wx18VNtjXw2KuVPNo5kOvrPHe%2bNVWyeVYEtjlWK7oBKWl%2bo75bImrRt7cx5ghJefp12JaZe5x%2fVT4ZDGpzWfGyyakddYf9QkR5GKET23%2fXOPVnJazum2ROhNUswfYRn6XX5iGKiAYjBYEToA%3d%3d',
        'vtpst': '|',
        'HAList': 'a-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sz-300042-%u6717%u79D1%u79D1%u6280%2Ca-sh-600916-N%u9EC4%u91D1%2Ca-sh-601818-%u5149%u5927%u94F6%u884C%2Ca-sz-002824-%u548C%u80DC%u80A1%u4EFD%2Ca-sz-002541-%u9E3F%u8DEF%u94A2%u6784%2Ca-sz-000723-%u7F8E%u9526%u80FD%u6E90',
        'EMFUND1': 'null',
        'EMFUND2': 'null',
        'EMFUND3': 'null',
        'EMFUND4': 'null',
        'EMFUND5': 'null',
        'EMFUND6': 'null',
        'EMFUND7': 'null',
        'EMFUND8': 'null',
        'EMFUND9': '02-08 14:54:20@#$%u534E%u6CF0%u67CF%u745E%u6CAA%u6DF1300ETF@%23%24510300',
        'st_psi': '{}'.format(st_psi),  #
        'intellpositionL': '862px',
        'intellpositionT': '{}'.format(intellpositionT),  # 2155px
        'st_pvi': '07634999118497',
        'st_sp': '2019-10-18%2023%3A34%3A34',
        'st_inirUrl': 'https%3A%2F%2Fwww.baidu.com%2Flink',
        'st_sn': '{}'.format(st_sn),  # 119
    }

    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
    }

    response = req.get('http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get'
                       , headers=headers, params=params,
                       cookies=cookies, verify=False)
    # print('url:{}'.format(response.url))
    return response

def data_northbound_cleaning(data):
    # 清洗北向资金数据
    hy_code_list = jsonpath.jsonpath(data, '$..HYCode')
    hy_name_list = jsonpath.jsonpath(data, '$..HYName')
    date_list = jsonpath.jsonpath(data, '$..HdDate')
    # 涨跌幅
    zdf_list = jsonpath.jsonpath(data, '$..Zdf')
    # 股票只数【北向资金今日增持估计】
    zc_amount_list1 = jsonpath.jsonpath(data, '$..ZC_Count')
    # 股票只数【北向资金今日持股】
    count_list1 = jsonpath.jsonpath(data, '$..Count')
    # 占北向资金比【北向资金今日持股】
    sharehold_list2 = jsonpath.jsonpath(data, '$..ShareHold_Chg_GZ')
    # 市值【北向资金今日增持估计】
    share_sz_list2 = jsonpath.jsonpath(data, '$..ShareSZ_ZC')
    # 市值增幅 【北向资金今日增持估计】
    sharehold_zc_list3 = jsonpath.jsonpath(data, '$..ShareHold_ZC_Chg')
    # 占板块比%  【北向资金今日增持估计】
    sharehold_zc_chg_bk_list3 = jsonpath.jsonpath(data, '$..ShareHold_ZC_Chg_BK')
    # 占北向资金比%  【北向资金今日增持估计】
    sharehold_zc_chg_gz_list4 = jsonpath.jsonpath(data, '$..ShareHold_ZC_Chg_GZ')
    # 市值【北向资金今日持股】
    sharesz_gz_list4 = jsonpath.jsonpath(data, '$..ShareSZ_GZ')
    # 增持市值最大的个股code【今日增持最大股】
    max_sz_code_list5 = jsonpath.jsonpath(data, '$..Max_SZ_Code')
    # 增持市值最大的个股name【今日增持最大股】
    maz_sz_name_list5 = jsonpath.jsonpath(data, '$..Max_SZ_Name')
    # 减持市值最大个股code【今日减持最大股】
    min_sz_code_list5 = jsonpath.jsonpath(data, '$..Min_SZ_Code')
    # 减持市值最大个股name【今日减持最大股】
    min_sz_name_list5 = jsonpath.jsonpath(data, '$..Min_SZ_Name')

    df = pd.DataFrame(hy_code_list, columns=['code'])
    df['name'] = hy_name_list
    df['rate'] = zdf_list
    df['股票只数【北向资金今日增持估计】'] = zc_amount_list1
    df['股票只数【北向资金今日持股】'] = count_list1    # 行业code
    df['占北向资金比【北向资金今日持股】'] = sharehold_list2
    df['市值【北向资金今日增持估计】'] = share_sz_list2
    df['市值增幅 【北向资金今日增持估计】'] = sharehold_zc_list3
    df['占板块比% 【北向资金今日增持估计】'] = sharehold_zc_chg_bk_list3
    df['占北向资金比% 【北向资金今日增持估计】'] = sharehold_zc_chg_gz_list4
    df['市值【北向资金今日持股】'] = sharesz_gz_list4
    df['增持市值最大的个股code【今日增持最大股】'] = max_sz_code_list5
    df['增持市值最大的个股name【今日增持最大股】'] = maz_sz_name_list5
    df['减持市值最大个股code【今日减持最大股】'] = min_sz_code_list5
    df['减持市值最大个股name【今日减持最大股】'] = min_sz_name_list5
    df['date'] = date_list

    return df

def get_northbound_industry_net_trade_data(max_acount=5):
    # 获取北向资金流入A股市场的数据
    this_res_df = pd.DataFrame()
    ps = '100'
    ct = 'YF2mZ_op_nsxQ6S0vjtqz7xZBug0NTW-Mm6Byp5_AN1rC_rdlYZ1xjaMxYGw83mcmWk_PvOgHooY5mVdwDQLWcvDJTfxh846lCMkqInLiT3TS937AhyMS_ifiuqFhmks-s2CxKKSWWkrtaJeqWvAGiQ_wh0i8AuDh6RvKnHApig; ut=FobyicMgeV6W21ICVIh67y2TdalzNIRdHh6UwIU-PHyOwFPXzPncgSsKJ2qXIFgvgxtvANYmJXUHCPD3tBIvfopl7NsepVBKFQucIcTwwlq-WX3qyvbPozoLToypptAjxUkKpVqGdUL6dks4Vtv1KKLXCmaAXp8mQrDOHpTHRZ8ft9gcUqPMUaAbnxmLu5qbISM7uGrJ2eSu7EROtLBVgwBhBZtzhNA0GzziXi8iq8h4fa763eyBwUxrtLUHrte9d4B-IaRwuRtmrYTnUmA_U7MpDN0Cg9SN'
    for page in range(1, max_acount):
        try:
            params = create_northbound_params(page, ps)
            response = get_northbound_response(params, ct)
            data = get_data(response)
            if len(data) == 0: break
            df = data_northbound_cleaning(data)
            if this_res_df.empty:
                this_res_df = df.copy()
            else:
                this_res_df = pd.concat([this_res_df, df], axis=0)
        except Exception as ex:
            continue
    return this_res_df

######################板块###########################

######################个股###########################
def data_northbound_code_cleaning(data):
    # 清洗北向资金数据
    hy_code_list = jsonpath.jsonpath(data, '$..HYCode')
    stock_name_list = jsonpath.jsonpath(data, '$..SName')
    hy_name_list = jsonpath.jsonpath(data, '$..HYName')
    close_list = jsonpath.jsonpath(data, '$..NewPrice')
    date_list = jsonpath.jsonpath(data, '$..HdDate')
    # 行业板块
    industry_list = jsonpath.jsonpath(data, '$..HYName')
    # 地域板块
    province_list1 = jsonpath.jsonpath(data, '$..DQName')
    # 涨跌幅
    Zdf_list1 = jsonpath.jsonpath(data, '$..Zdf')
    # 今日持股数
    ShareHold_list2 = jsonpath.jsonpath(data, '$..ShareHold')
    # 今日持股市值
    ShareSZ_list2 = jsonpath.jsonpath(data, '$..ShareSZ')
    # 今日持股占流动市值比
    LTZB_list3 = jsonpath.jsonpath(data, '$..LTZB')
    # 今日持股占总股数比
    ZZB_list3 = jsonpath.jsonpath(data, '$..ZZB')
    # 今日增持估计股数
    ShareHold_Chg_One_list4 = jsonpath.jsonpath(data, '$..ShareHold_Chg_One')
    # 今日增持估计市值
    ShareSZ_Chg_One_list4 = jsonpath.jsonpath(data, '$..ShareSZ_Chg_One')
    # 今日增持估计--市值增幅
    ShareSZ_Chg_Rate_One_list5 = jsonpath.jsonpath(data, '$..ShareSZ_Chg_Rate_One')
    # 今日增持估计--占流通股比
    LTZB_One_list5 = jsonpath.jsonpath(data, '$..LTZB_One')
    # # 今日增持估计--占总股比
    ZZB_One_list5 = jsonpath.jsonpath(data, '$..ZZB_One')

    df = pd.DataFrame(hy_code_list, columns=['code'])
    df['stock_name'] = stock_name_list
    df['name'] = hy_name_list
    df['close'] = close_list
    df['行业板块'] = industry_list
    df['地域板块'] = province_list1
    df['涨跌幅'] = Zdf_list1    # 行业code
    df['今日持股数'] = ShareHold_list2
    df['今日持股市值'] = ShareSZ_list2
    df['今日持股占流动市值比'] = LTZB_list3
    df['今日持股占总股数比'] = ZZB_list3
    df['今日增持估计股数'] = ShareHold_Chg_One_list4
    df['今日增持估计市值'] = ShareSZ_Chg_One_list4
    df['今日增持估计--市值增幅'] = ShareSZ_Chg_Rate_One_list5
    df['今日增持估计--占流通股比'] = LTZB_One_list5
    df['今日增持估计--占总股比'] = ZZB_One_list5
    df['date'] = date_list
    return df

def get_northbound_code_net_trade_data(max_acount=100):
    # 获取北向资金流入A股市场的数据
    this_res_df = pd.DataFrame()
    imT = '2155px'
    st_sn = '119'
    st = 'ShareSZ_Chg_One'
    st_spi = '20210208204935945-113300303605-1756976206'
    type = 'HSGT20_GGTJ_SUM'
    ct = 'YF2mZ_op_nsxQ6S0vjtqz7xZBug0NTW-Mm6Byp5_AN1rC_rdlYZ1xjaMxYGw83mcmWk_PvOgHooY5mVdwDQLWcvDJTfxh846lCMkqInLiT3TS937AhyMS_ifiuqFhmks-s2CxKKSWWkrtaJeqWvAGiQ_wh0i8AuDh6RvKnHApig'
    for page in range(1, max_acount):
        try:
            params = create_northbound_params(page, type, st)
            response = get_northbound_response(params, ct, st_sn=st_sn, st_psi=st_spi, intellpositionT=imT)
            data = get_data(response)
            if len(data) == 0: break
            df = data_northbound_code_cleaning(data)
            if this_res_df.empty:
                this_res_df = df.copy()
            else:
                this_res_df = pd.concat([this_res_df, df], axis=0)
        except Exception as ex:
            continue
    return this_res_df


######################个股###########################

#↑↑↑↑↑北向资金数据#########################

#↓↓↓↓↓融资融券余额########################
def create_rzrq_params(page, type_='RPTA_RZRQ_LSHJ', _='1612845502290', ps='500'):
    params = {
        'type': '{}'.format(type_),
        'sty': 'ALL',
        'source': 'WEB',
        'st': 'dim_date',
        'sr': '-1',
        'p': '{}'.format(page),
        'ps': '{}'.format(ps),
        'filter': '',
        '_': '{}'.format(_),  # 1612763862192
    }
    return params

def get_rzrq_response(params, st_sn = '18', st_psi = '20210209125848514-113300301652-5188950394', intellpositionT = '1255px'):
    # 北向资金数据
    cookies = {
        'cowminicookie': 'true',
        'em_hq_fls': 'js',
        'st_si': '38729278707190',
        'waptgshowtime': '202129',
        'st_asi': 'delete',
        'cowCookie': 'true',
        'qgqp_b_id': '49621c65b51724aed8f10c0feea8ebdd',
        'p_origin': 'https%3A%2F%2Fpassport2.eastmoney.com',
        'ct': 'YF2mZ_op_nsxQ6S0vjtqz7xZBug0NTW-Mm6Byp5_AN1rC_rdlYZ1xjaMxYGw83mcmWk_PvOgHooY5mVdwDQLWcvDJTfxh846lCMkqInLiT3TS937AhyMS_ifiuqFhmks-s2CxKKSWWkrtaJeqWvAGiQ_wh0i8AuDh6RvKnHApig',
        'ut': 'FobyicMgeV6W21ICVIh67y2TdalzNIRdHh6UwIU-PHyOwFPXzPncgSsKJ2qXIFgvgxtvANYmJXUHCPD3tBIvfopl7NsepVBKFQucIcTwwlq-WX3qyvbPozoLToypptAjxUkKpVqGdUL6dks4Vtv1KKLXCmaAXp8mQrDOHpTHRZ8ft9gcUqPMUaAbnxmLu5qbISM7uGrJ2eSu7EROtLBVgwBhBZtzhNA0GzziXi8iq8h4fa763eyBwUxrtLUHrte9d4B-IaRwuRtmrYTnUmA_U7MpDN0Cg9SN',
        'sid': '159309191',
        'uidal': '1002094027214364%e9%a3%8e%e4%b9%90%e5%b2%9a%e9%9b%85',
        'pi': '1002094027214364%3bm1002094027214364%3b%e9%a3%8e%e4%b9%90%e5%b2%9a%e9%9b%85%3bKkSBKC5DEQXUZK%2fEwwInj5WpbSR7S9kOZClStvOBj5vyQqwv2KUUkGsgekCzZfAp7PBnK10Vte4lIgkGg4e29UVyk8rldPKAxxCQZZB%2bFaU%2f%2bQIjCG2szv9umvRmfATQdFwMfSwM4LpINTBsihhyEuepC3aYX6qC6DijSw4dq2peQgoVVJiLtpJDnoH4sGuqGjWjS3VR%3bFq%2frXacfR4VaN3Wx18VNtjXw2KuVPNo5kOvrPHe%2bNVWyeVYEtjlWK7oBKWl%2bo75bImrRt7cx5ghJefp12JaZe5x%2fVT4ZDGpzWfGyyakddYf9QkR5GKET23%2fXOPVnJazum2ROhNUswfYRn6XX5iGKiAYjBYEToA%3d%3d',
        'vtpst': '|',
        'HAList': 'a-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Cd-hk-01024%2Cd-hk-06185%2Ca-sz-300042-%u6717%u79D1%u79D1%u6280%2Ca-sh-600916-N%u9EC4%u91D1%2Ca-sh-601818-%u5149%u5927%u94F6%u884C%2Ca-sz-002824-%u548C%u80DC%u80A1%u4EFD%2Ca-sz-002541-%u9E3F%u8DEF%u94A2%u6784%2Ca-sz-000723-%u7F8E%u9526%u80FD%u6E90',
        'EMFUND1': 'null',
        'EMFUND2': 'null',
        'EMFUND3': 'null',
        'EMFUND4': 'null',
        'EMFUND5': 'null',
        'EMFUND6': 'null',
        'EMFUND7': 'null',
        'EMFUND8': 'null',
        'EMFUND9': '02-08 14:54:20@#$%u534E%u6CF0%u67CF%u745E%u6CAA%u6DF1300ETF@%23%24510300',
        'st_psi': '{}'.format(st_psi),  #
        'intellpositionL': '862px',
        'intellpositionT': '{}'.format(intellpositionT),  # 2155px
        'st_pvi': '07634999118497',
        'st_sp': '2019-10-18%2023%3A34%3A34',
        'st_inirUrl': 'https%3A%2F%2Fwww.baidu.com%2Flink',
        'st_sn': '{}'.format(st_sn),  # 119
        'JSESSIONID': '257A1C60C3C5683C576FF6774802282F',
    }

    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
    }

    response = req.get('http://datacenter.eastmoney.com/api/data/get'
                       , headers=headers, params=params,
                       cookies=cookies, verify=False)
    # print('url:{}'.format(response.url))
    return response

def data_rzrq_cleaning(data):
    # 清洗北向资金数据

    DIM_DATE_list = jsonpath.jsonpath(data, '$..DIM_DATE')
    # 融券余额
    RQYE_list = jsonpath.jsonpath(data, '$..RQYE')
    # 融券余量
    RQYL_list = jsonpath.jsonpath(data, '$..RQYL')
    # 融券卖出量1D
    RQMCL_list = jsonpath.jsonpath(data, '$..RQMCL')
    # 融券卖出量3D
    RQMCL3D_list1 = jsonpath.jsonpath(data, '$..RQMCL3D')
    # 融券卖出量5D
    RQMCL5D_list1 = jsonpath.jsonpath(data, '$..RQMCL5D')
    # 融券卖出量10D
    RQMCL10D_list2 = jsonpath.jsonpath(data, '$..RQMCL10D')
    # 融券偿还量1D
    RQCHL_list3 = jsonpath.jsonpath(data, '$..RQCHL')
    # 融券偿还量3D
    RQCHL3D_list3 = jsonpath.jsonpath(data, '$..RQCHL3D')
    # 融券偿还量5D
    RQCHL5D_list3 = jsonpath.jsonpath(data, '$..RQCHL5D')
    # 融券偿还量10D
    RQCHL10D_list3 = jsonpath.jsonpath(data, '$..RQCHL10D')
    # 融券净卖出股 RQJMG
    RQJMG_list2 = jsonpath.jsonpath(data, '$..RQJMG')
    # 融券净卖出股 RQJMG3D
    RQJMG3D_list2 = jsonpath.jsonpath(data, '$..RQJMG3D')
    # 融券净卖出股 RQJMG5D
    RQJMG5D_list2 = jsonpath.jsonpath(data, '$..RQJMG5D')
    # 融券净卖出股 RQJMG10D
    RQJMG10D_list2 = jsonpath.jsonpath(data, '$..RQJMG10D')

    # 融资余额
    RZYE_list = jsonpath.jsonpath(data, '$..RZYE')
    # 融资余额占流通市值占比
    RZYEZB_list = jsonpath.jsonpath(data, '$..RZYEZB')
    # 融资买入额
    RZMRE_list = jsonpath.jsonpath(data, '$..RZMRE')
    # 融资买入额3D
    RZMRE3D_list1 = jsonpath.jsonpath(data, '$..RZMRE3D')
    # 融资买入额5D
    RZMRE5D_list1 = jsonpath.jsonpath(data, '$..RZMRE5D')
    # 融资买入额10D
    RZMRE10D_list2 = jsonpath.jsonpath(data, '$..RZMRE10D')
    # 融资偿还额1D
    RZCHE_list3 = jsonpath.jsonpath(data, '$..RZCHE')
    # 融资偿还额3D
    RZCHE3D_list3 = jsonpath.jsonpath(data, '$..RZCHE3D')
    # 融资偿还额5D
    RZCHE5D_list3 = jsonpath.jsonpath(data, '$..RZCHE5D')
    # 融资偿还额10D
    RZCHE10D_list3 = jsonpath.jsonpath(data, '$..RZCHE10D')
    # 融资净买入额
    RZJME_list3 = jsonpath.jsonpath(data, '$..RZJME')
    # 融资净买入额3D
    RZJME3D_list3 = jsonpath.jsonpath(data, '$..RZJME3D')
    # 融资净买入额5D
    RZJME5D_list3 = jsonpath.jsonpath(data, '$..RZJME5D')
    # 融资净买入额10D
    RZJME10D_list3 = jsonpath.jsonpath(data, '$..RZJME10D')
    # 融资买入额
    RZMRE_list3 = jsonpath.jsonpath(data, '$..RZMRE')
    # 融资买入额3D
    RZMRE3D_list3 = jsonpath.jsonpath(data, '$..RZMRE3D')
    # 融资买入额5D
    RZMRE5D_list3 = jsonpath.jsonpath(data, '$..RZMRE5D')
    # 融资买入额10D
    RZMRE10D_list3 = jsonpath.jsonpath(data, '$..RZMRE10D')
    # 融资融券余额
    RZRQYE_list3 = jsonpath.jsonpath(data, '$..RZRQYE')
    # 融资融券余额差额
    RZRQYECZ_list3 = jsonpath.jsonpath(data, '$..RZRQYECZ')
    df = pd.DataFrame(DIM_DATE_list, columns=['date'])
    df['融资余额'] = RZYE_list
    df['融资余额占流通市值占比'] = RZYEZB_list
    df['融资买入额'] = RZMRE_list
    df['融资买入额3D'] = RZMRE3D_list1
    df['融资买入额5D'] = RZMRE5D_list1
    df['融资买入额10D'] = RZMRE10D_list2
    df['融资偿还额1D'] = RZCHE_list3  # 行业code
    df['融资偿还额3D'] = RZCHE3D_list3
    df['融资偿还额5D'] = RZCHE5D_list3
    df['融资偿还额10D'] = RZCHE10D_list3
    df['融资净买入额'] = RZJME_list3
    df['融资净买入额3D'] = RZJME3D_list3
    df['融资净买入额5D'] = RZJME5D_list3
    df['融资净买入额10D'] = RZJME10D_list3
    df['融资买入额'] = RZMRE_list3
    df['融资买入额3D'] = RZMRE3D_list3
    df['融资买入额5D'] = RZMRE5D_list3
    df['融资买入额10D'] = RZMRE10D_list3
    df['融券余额'] = RQYE_list
    df['融券余量'] = RQYL_list
    df['融券卖出量1D'] = RQMCL_list
    df['融券卖出量3D'] = RQMCL3D_list1
    df['融券卖出量5D'] = RQMCL5D_list1
    df['融券卖出量10D'] = RQMCL10D_list2
    df['融券偿还量1D'] = RQCHL_list3
    df['融券偿还量3D'] = RQCHL3D_list3
    df['融券偿还量5D'] = RQCHL5D_list3
    df['融券偿还量10D'] = RQCHL10D_list3
    df['融券净卖出股'] = RQJMG_list2
    df['融券净卖出股3D'] = RQJMG3D_list2
    df['融券净卖出股5D'] = RQJMG5D_list2
    df['融券净卖出股10D'] = RQJMG10D_list2
    df['融资融券余额'] = RZRQYE_list3
    df['融资融券余额差额'] = RZRQYECZ_list3
    return df

def get_rzrq_data(max_acount=5):
    # 获取北向资金流入A股市场的数据
    this_res_df = pd.DataFrame()
    ps = '100'
    for page in range(1, max_acount):
        try:
            params = create_rzrq_params(page, ps=ps)
            response = get_rzrq_response(params)
            data = get_data(response)
            if len(data) == 0: break
            df = data_rzrq_cleaning(data)
            if this_res_df.empty:
                this_res_df = df.copy()
            else:
                this_res_df = pd.concat([this_res_df, df], axis=0)
        except Exception as ex:
            continue
    return this_res_df


#↑↑↑↑↑融资融券余额########################

########################个股实时行情盘口数据接口######################################

####  1  0: 未知 #  2  1: 股票名字  #  3  2: 股票代码  #  4  3: 当前价格  #  5  4: 昨收  #  6  5: 今开 #  7  6: 成交量（手）
    #  8  7: 外盘  #  9  8: 内盘  # 10  9: 买一  # 11 10: 买一量（手）  # 12 11-18: 买二 买五  # 13 19: 卖一  # 14 20: 卖一量
    # 15 21-28: 卖二 卖五 # 16 29: 最近逐笔成交  # 17 30: 时间  # 18 31: 涨跌  # 19 32: 涨跌%  # 20 33: 最高  # 21 34: 最低
    # 22 35: 价格/成交量（手）/成交额  # 23 36: 成交量（手） # 24 37: 成交额（万）  # 25 38: 换手率  # 26 39: 市盈率  # 27 40:
    # 28 41: 最高  # 29 42: 最低  # 30 43: 振幅 # 31 44: 流通市值  # 32 45: 总市值 # 33 46: 市净率 # 34 47: 涨停价 # 35 48: 跌停价
### 腾讯接口 http://qt.gtimg.cn/q=sh600519 查看返回数据是以 ~ 分割字符串中内容

def get_quote_data(code='sz000001'):
    # 获取个股的实时行情盘口数据
    code = code.replace('.', '')
    code = code.lower()
    url_ = 'http://qt.gtimg.cn/q={}'.format(code)
    respon = req.get(url=url_)
    respon.encoding = respon.apparent_encoding
    respon = respon.text
    respon = respon.split('~')
    cols = ['code_namber', 'name', 'code', 'last_price', 'pre_price', 'open', 'trade_vol', 'out_pan', 'in_pan',
            'bid_1_price', 'bid_1_vol', 'bid_2_price', 'bid_2_vol', 'bid_3_price', 'bid_3_vol',
            'bid_4_price', 'bid_4_vol', 'bid_5_price', 'bid_5_vol', 'ask_1_price', 'ask_1_vol',
            'ask_2_price', 'ask_2_vol', 'ask_3_price', 'ask_3_vol', 'ask_4_price', 'ask_4_vol',
            'ask_5_price', 'ask_5_vol', 'date', 'pct_value', 'pct_rate', 'high', 'low',
            'price/trade_vol/trade_money', 'trade_vol', 'trade_money', 'tur_rate', 'PE', 'high', 'low',
            'zhenfu', 'cir_market', 'total_market', 'PS', 'zt_price', 'dt_price']
    respon = list(filter(lambda x: x != '', respon))
    respon = list(filter(lambda x: x != ' ', respon))
    respon = respon[:47]
    df = pd.DataFrame(respon, cols)
    df = df.T
    df = df[['name', 'code', 'last_price', 'pre_price', 'open', 'trade_vol', 'out_pan', 'in_pan',
            'bid_1_price', 'bid_1_vol', 'bid_2_price', 'bid_2_vol', 'bid_3_price', 'bid_3_vol',
            'bid_4_price', 'bid_4_vol', 'bid_5_price', 'bid_5_vol', 'ask_1_price', 'ask_1_vol',
            'ask_2_price', 'ask_2_vol', 'ask_3_price', 'ask_3_vol', 'ask_4_price', 'ask_4_vol',
            'ask_5_price', 'ask_5_vol', 'date', 'pct_value', 'pct_rate', 'high', 'low',
            'trade_vol', 'trade_money', 'tur_rate', 'PE', 'high', 'low',
            'zhenfu', 'cir_market', 'total_market', 'PS', 'zt_price', 'dt_price']]
    return df
########################个股实时行情盘口数据接口######################################

###########################个股历史行情数据接口######################################

def get_a_codes_by_req():
    # 通过爬虫获取网页上全A的股票代码
    # sz_code_path = 'https://www.banban.cn/gupiao/list_sz.html'
    # sh_code_path = 'https://www.banban.cn/gupiao/list_sh.html'
    # cyb_code_path = 'https://www.banban.cn/gupiao/list_cyb.html'
    # respon_sz_codes = req_url(sz_code_path)
    # time.sleep(2)
    # respon_sh_codes = req_url(sh_code_path)
    # respon_cyb_codes = req_url(cyb_code_path)
    # respon_sz_codes.extend(respon_sh_codes)
    # respon_sz_codes.extend(respon_cyb_codes)
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
    if code[:2] == 'sh':code = '0' + code[2:]
    else:
        code = '1' + code[2:]
    url_ = 'http://quotes.money.163.com/service/chddata.html?code={}&start={}&end={}'.format(code, start_date, end_date)
    print('url_:{}'.format(url_))
    respon = req.get(url=url_)
    respon.encoding = respon.apparent_encoding
    respon = respon.text
    #print('respon11111:{}'.format(respon))
    #print('2的1W次方:{}'.format(2 ** 10000))
    respon = list(respon.split('\r\n'))
    res_df = pd.DataFrame(respon)
    np_arr = np.array(res_df.values)
    np_arr = np.array(list(filter(lambda x: x[0] != '', np_arr)))
    #cols = np_arr[0][0].split(',')   # 列名
    # date	open	high	close	low	volume	turnover	code
    cols = ['date', 'code', 'name', 'close', 'high', 'low', 'open', 'PRE_CLOSE', 'CHG', 'PCHG', 'turnover', 'volume', 'VOL_MONEY', 'MARKET', 'CIR_MARKET', 'TRADE_NUM']
    #print('cols:{}'.format(cols))
    np_arr_list = np_arr[1:]
    np_arr_list = [nparr[0].split(',') for nparr in np_arr_list]
    res_11_df = pd.DataFrame(np_arr_list, columns=cols)

    return res_11_df

def func_callback(fun1):
    return fun1()

def all_get_index_code_method(index_code):
    # 根据指定的index_code获取对应的一揽子股票
    the_dic_ = {'000300': get_hs300_codes, '000016': get_sz50_codes, '000905': get_zz500_codes, '000906': get_zz800_codes, 'ALLSTOCKS': get_a_codes_by_req}
    return list(func_callback(the_dic_[index_code]))

def get_stock_price_old(codes, start, end):
    # 获取股票行情
    res_df = pd.DataFrame()
    start_d = time.time()
    for cd in codes:
        time.sleep(0.2)  # 频率过快会被屏蔽
        try:
            df = get_a_queto_data(start, end, cd)  #ts.get_hist_data(cd, start=start, end=end)
            #df['code'] = cd
            if res_df.empty:
                res_df = df.copy()
            else:
                res_df = pd.concat([res_df, df], axis=0)
        except Exception as e:
            print('合约:{},抛异常:{}'.format(cd, e))
            continue
    start_e = time.time()
    print('获取股票行情部分,耗时:{}s'.format(round(start_e-start_d)))
    return res_df

def get_his_a_codes_data(date_count=365, th_code='ALLSTOCKS'):
    # 获取全A股票的历史数据
    '''
    date_count: 获取数据的时间长度(默认是一年)
    th_code:获取的指数[000016/000300/000905/000906](默认是全市场)
    '''
    today = datetime.datetime.now()
    pre_date = datetime.datetime.strftime(today + datetime.timedelta(days=0), '%Y-%m-%d')
    pre_1_y_date = datetime.datetime.strftime(today + datetime.timedelta(days=-date_count), '%Y-%m-%d')

    # 【沪深300/中证500/上证50/中证800/创业板/全A】
    cho_index_codes = all_get_index_code_method(th_code)  # 获取除全A以外的指数成分股
    # 获取历史行情数据 ##
    price_df = get_stock_price(cho_index_codes, pre_1_y_date,
                               pre_date)
    price_df = price_df.sort_index(ascending=True)
    price_df['code'] = ['SH.' + cd[1:] if cd[0] == '6' else 'SZ.' + cd[1:] for cd in price_df['code']]

    return price_df

def avg_list_func(listTemp, n):
    # 平分list,每n个一组
    for i in np.arange(0, len(listTemp), n):
        yield listTemp[i:i + n]

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

def get_stock_price(codes, start, end):
    # 获取股票行情
    std0 = time.time()
    n = 500  # 20-->937.4 # 500-->876.2  # 100-->890.8  # 200-->966.2
    all_code_list = list(avg_list_func(codes, n))
    par_cls = partial(get_stock_price_thread, start=start, end=end)
    pool = ThreadPool()
    res_data_list = pool.map(par_cls, all_code_list)
    result_df = pd.concat(res_data_list)
    print('res_data:{}'.format(result_df))
    print('多进程耗时:{}s'.format(round(time.time() - std0, 3)))
    return result_df
###########################个股历史行情数据接口######################################


######################港股财务数据##########################
def _get_pagedata(freq='q', code='00700', page=5):
    # 获取雪球页面财务数据
                # https://stock.xueqiu.com/v5/stock/finance/hk/indicator.json?symbol=00700&type=Q4&is_detail=true&count=5&timestamp=
    if freq == 'y':
        Url_ = 'https://stock.xueqiu.com/v5/stock/finance/hk/indicator.json?symbol={}&type=Q4&is_detail=true&count=5&timestamp='.format(code)  # 年报
    elif freq == 'q':
        Url_ = 'https://stock.xueqiu.com/v5/stock/finance/hk/indicator.json?symbol={}&type=Q2&is_detail=true&count=5&timestamp='.format(code)  # 半年报
    else:
        Url_ = 'https://stock.xueqiu.com/v5/stock/finance/hk/indicator.json?symbol={}&type=Q4&is_detail=true&count=5&timestamp='.format(code)  # 年报
    print(Url_)

    header = {
        "access-control-allow-credentials": 'true',
        'access-control-allow-headers': 'Origin, X-Requested-With, Content-Type, Accept',
        'access-control-allow-methods': 'GET, POST, OPTIONS, DELETE',
        'access-control-allow-origin': 'https://xueqiu.com',
        'cache-control': 'private, no-store, no-cache, must-revalidate, max-age=0',
        "content-encoding": 'gzip',
        "content-type": 'application/json;charset=UTF-8',
        "date": 'Wed, 10 Mar 2021 14:29:09 GMT',
        "p3p": 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT',
        "server": 'openresty',
        "trace-id": 'eaf8eae91a222895',
        "vary": 'Accept-Encoding',
        "x-application-context": 'xueqiu-stock-api-rpc:production',
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
    }
    params = {
        'symbol': '{}'.format(code),
        'type': '{}'.format('Q4' if freq == 'y' else 'Q2'),
        'is_detail': 'true',
        'count': '{}'.format(page),
        'timestamp': '',
    }
    cookies = {
        'device_id': 'c2d77de33af1254b3987f20f7909a68d',
        's': 'ck14to7cil',
        'xq_a_token': 'a4b3e3e158cfe9745b677915691ecd794b4bf2f9',
        'xqat': 'a4b3e3e158cfe9745b677915691ecd794b4bf2f9',
        'xq_r_token': 'b80d3232bf315f8710d36ad2370bc777b24d5001',
        'xq_id_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTYxNzc2MzQxOCwiY3RtIjoxNjE1Mzg2MzI5MDA2LCJjaWQiOiJkOWQwbjRBWnVwIn0.E7_hHA7pr17sS_aFbozK8DYtGEgM2hfYGQM46L6O6SwkXD4hn2WwUAEKMAfO4ilrIHFxfd7cJJ6jYXAv7RMKcqGx-dHMeiJjtyJWcCwwcefNKV0Fx32xNGXNBtlH55epAgNW5pXHVCyQ5QHhhDp_GRE5MjJZ85zVo6StjrVXnqwJ7YTHBpMEHrIhXWEOvAZ3WAS_UFw-XMAbmj5zpzWYpw5OdyOxnhvVpc0p9GNWmWFJXxzlsAfbnzhZnHQIM_tEdaMdzrLkwuN6wpqeU22iJVgsN1TJ22d5y6Bs-GUspGtyeWODwWms793Q0OTyUJm0yLfA6_cam-ktlYg1-hycDQ',
        'u': '521615386379392',
        'Hm_lvt_1db88642e346389874251b5a1eded6e3': '1613806974,1615217431,1615302882,1615386381',
        'Hm_lpvt_1db88642e346389874251b5a1eded6e3': '1615386396'
    }
    respon = req.get(url='https://stock.xueqiu.com/v5/stock/finance/hk/indicator.json', headers=header, cookies=cookies, params=params)
    print(respon)
    res_txt = (respon.text).replace('jQuery112407285217582388686_1611985850544(', '')
    res_txt = res_txt.replace(');', '')

    data = json.loads(res_txt)
    target_df = data_change(data, code)
    #print(target_df)
    return target_df

def data_change(data, code):
    # 在json文本中提取需要的数据
    print('data:{}'.format(data))
    # code
    currency_name_list = jsonpath.jsonpath(data, '$..currency_name')
    print('currency_name_list:{}'.format(currency_name_list))
    # name
    name_list = jsonpath.jsonpath(data, '$..quote_name')
    print('name_list:{}'.format(name_list))
    # 收盘价
    annual_settle_date_list = jsonpath.jsonpath(data, '$..annual_settle_date')
    print('annual_settle_date_list:{}'.format(annual_settle_date_list))
    # report_name
    report_name_list = jsonpath.jsonpath(data, '$..report_name')
    print('report_name_list:{}'.format(report_name_list))
    # report_date
    report_date_list = jsonpath.jsonpath(data, '$..report_date')
    # # month_num
    month_num_list1 = jsonpath.jsonpath(data, '$..month_num')
    # ed
    ed_list1 = jsonpath.jsonpath(data, '$..ed')
    # tto  营收/营收同比增长
    tto_list2 = jsonpath.jsonpath(data, '$..tto')
    tto_value_list = [n[0] for n in tto_list2]
    tto_rate_list = [n[1] for n in tto_list2]
    print('tto_value_list:{}'.format(tto_value_list))
    print('tto_rate_list:{}'.format(tto_rate_list))

    # gpm 毛利率
    gpm_list2 = jsonpath.jsonpath(data, '$..gpm')
    gpm_value_list = [n[0] for n in gpm_list2]
    gpm_rate_list = [n[1] for n in gpm_list2]
    print('gpm_value_list:{}'.format(gpm_value_list))
    print('gpm_rate_list:{}'.format(gpm_rate_list))
    # cro 流动比率
    cro_list2 = jsonpath.jsonpath(data, '$..cro')
    cro_value_list = [n[0] for n in cro_list2]
    cro_rate_list = [n[1] for n in cro_list2]
    print('cro_value_list:{}'.format(cro_value_list))
    print('cro_rate_list:{}'.format(cro_rate_list))
    # qro 速动比率
    qro_list2 = jsonpath.jsonpath(data, '$..qro')
    qro_value_list = [n[0] for n in qro_list2]
    qro_rate_list = [n[1] for n in qro_list2]
    print('qro_value_list:{}'.format(qro_value_list))
    print('qro_rate_list:{}'.format(qro_rate_list))
    # ivcvspd 存货转换周期
    ivcvspd_list2 = jsonpath.jsonpath(data, '$..ivcvspd')
    ivcvspd_value_list = [n[0] for n in ivcvspd_list2]
    ivcvspd_rate_list = [n[1] for n in ivcvspd_list2]
    print('ivcvspd_value_list:{}'.format(ivcvspd_value_list))
    print('ivcvspd_rate_list:{}'.format(ivcvspd_rate_list))
    # beps 基本每股收益
    beps_list2 = jsonpath.jsonpath(data, '$..beps')
    beps_value_list = [n[0] for n in beps_list2]
    beps_rate_list = [n[1] for n in beps_list2]
    print('beps_value_list:{}'.format(beps_value_list))
    print('beps_rate_list:{}'.format(beps_rate_list))
    # beps_aju  基本每股收益_调整后
    beps_aju_list2 = jsonpath.jsonpath(data, '$..beps_aju')
    beps_aju_value_list = [n[0] for n in beps_aju_list2]
    beps_aju_rate_list = [n[1] for n in beps_aju_list2]
    print('beps_aju_value_list:{}'.format(beps_value_list))
    print('beps_aju_rate_list:{}'.format(beps_aju_rate_list))
    # bps  每股净资产
    bps_list2 = jsonpath.jsonpath(data, '$..bps')
    bps_value_list = [n[0] for n in bps_list2]
    bps_rate_list = [n[1] for n in bps_list2]
    print('bps_value_list:{}'.format(bps_value_list))
    print('bps_rate_list:{}'.format(bps_rate_list))
    # opps  每股营业利润
    opps_list2 = jsonpath.jsonpath(data, '$..opps')
    opps_value_list = [n[0] for n in opps_list2]
    opps_rate_list = [n[1] for n in opps_list2]
    print('opps_value_list:{}'.format(opps_value_list))
    print('opps_rate_list:{}'.format(opps_rate_list))
    # plobtxps 每股利润总额
    plobtxps_list2 = jsonpath.jsonpath(data, '$..plobtxps')
    plobtxps_value_list = [n[0] for n in plobtxps_list2]
    plobtxps_rate_list = [n[1] for n in plobtxps_list2]
    print('plobtxps_value_list:{}'.format(plobtxps_value_list))
    print('plobtxps_rate_list:{}'.format(plobtxps_rate_list))
    # ploashh  净利润
    ploashh_list2 = jsonpath.jsonpath(data, '$..ploashh')
    ploashh_value_list = [n[0] for n in ploashh_list2]
    ploashh_rate_list = [n[1] for n in ploashh_list2]
    print('ploashh_value_list:{}'.format(ploashh_value_list))
    print('ploashh_rate_list:{}'.format(ploashh_rate_list))
    # roe  ROE
    roe_list2 = jsonpath.jsonpath(data, '$..roe')
    roe_value_list = [n[0] for n in roe_list2]
    roe_rate_list = [n[1] for n in roe_list2]
    print('roe_value_list:{}'.format(roe_value_list))
    print('roe_rate_list:{}'.format(roe_rate_list))
    # rota  ROA
    rota_list2 = jsonpath.jsonpath(data, '$..rota')
    rota_value_list = [n[0] for n in rota_list2]
    rota_rate_list = [n[1] for n in rota_list2]
    print('rota_value_list:{}'.format(rota_value_list))
    print('rota_rate_list:{}'.format(rota_rate_list))
    # tlia_ta  资产负债率
    tlia_ta_list2 = jsonpath.jsonpath(data, '$..tlia_ta')
    tlia_ta_value_list = [n[0] for n in tlia_ta_list2]
    tlia_ta_rate_list = [n[1] for n in tlia_ta_list2]
    print('tlia_ta_value_list:{}'.format(tlia_ta_value_list))
    print('tlia_ta_rate_list:{}'.format(tlia_ta_rate_list))
    # tsrps 每股营业收入
    tsrps_list2 = jsonpath.jsonpath(data, '$..tsrps')
    tsrps_value_list = [n[0] for n in tsrps_list2]
    tsrps_rate_list = [n[1] for n in tsrps_list2]
    print('tsrps_value_list:{}'.format(tsrps_value_list))
    print('tsrps_rate_list:{}'.format(tsrps_rate_list))
    # apycvspd 应付账款转换周期
    apycvspd_list2 = jsonpath.jsonpath(data, '$..apycvspd')
    apycvspd_value_list = [n[0] for n in apycvspd_list2]
    apycvspd_rate_list = [n[1] for n in apycvspd_list2]
    print('apycvspd_value_list:{}'.format(apycvspd_value_list))
    print('apycvspd_rate_list:{}'.format(apycvspd_rate_list))
    # arbcvspd 应收账款转换周期
    arbcvspd_list2 = jsonpath.jsonpath(data, '$..arbcvspd')
    arbcvspd_value_list = [n[0] for n in arbcvspd_list2]
    arbcvspd_rate_list = [n[1] for n in arbcvspd_list2]
    print('arbcvspd_value_list:{}'.format(arbcvspd_value_list))
    print('arbcvspd_rate_list:{}'.format(arbcvspd_rate_list))
    # ncfps 每股现金流净额
    ncfps_list2 = jsonpath.jsonpath(data, '$..ncfps')
    ncfps_value_list = [n[0] for n in ncfps_list2]
    ncfps_rate_list = [n[1] for n in ncfps_list2]
    print('ncfps_value_list:{}'.format(ncfps_value_list))
    print('ncfps_rate_list:{}'.format(ncfps_rate_list))
    # nocfps 每股经营现金流
    nocfps_list2 = jsonpath.jsonpath(data, '$..nocfps')
    nocfps_value_list = [n[0] for n in nocfps_list2]
    nocfps_rate_list = [n[1] for n in nocfps_list2]
    print('nocfps_value_list:{}'.format(nocfps_value_list))
    print('nocfps_rate_list:{}'.format(nocfps_rate_list))

    # ncfps 每股现金流净额
    ncfps_list2 = jsonpath.jsonpath(data, '$..ncfps')
    ncfps_value_list = [n[0] for n in ncfps_list2]
    ncfps_rate_list = [n[1] for n in ncfps_list2]
    print('ncfps_value_list:{}'.format(ncfps_value_list))
    print('ncfps_rate_list:{}'.format(ncfps_rate_list))

    # ninvcfps 每股投资现金流
    ninvcfps_list2 = jsonpath.jsonpath(data, '$..ninvcfps')
    ninvcfps_value_list = [n[0] for n in ninvcfps_list2]
    ninvcfps_rate_list = [n[1] for n in ninvcfps_list2]
    print('ninvcfps_value_list:{}'.format(ninvcfps_value_list))
    print('ninvcfps_rate_list:{}'.format(ninvcfps_rate_list))

    # nfcgcfps 每股筹资现金流
    nfcgcfps_list2 = jsonpath.jsonpath(data, '$..nfcgcfps')
    nfcgcfps_value_list = [n[0] for n in nfcgcfps_list2]
    nfcgcfps_rate_list = [n[1] for n in nfcgcfps_list2]
    print('nfcgcfps_value_list:{}'.format(nfcgcfps_value_list))
    print('nfcgcfps_rate_list:{}'.format(nfcgcfps_rate_list))

    df = pd.DataFrame(report_name_list, columns=['report_name'])
    df['tto'] = tto_value_list
    df['tto_rate'] = tto_rate_list
    df['gpm'] = gpm_value_list
    df['gpm_rate'] = gpm_rate_list
    df['cro'] = cro_value_list
    df['cro_rate'] = cro_rate_list
    df['qro'] = qro_value_list
    df['qro_rate'] = qro_rate_list
    df['ivcvspd'] = ivcvspd_value_list
    df['ivcvspd_rate'] = ivcvspd_rate_list
    df['beps'] = beps_value_list
    df['beps_rate'] = beps_rate_list
    df['beps_aju'] = beps_aju_value_list
    df['beps_aju_rate'] = beps_aju_rate_list
    df['bps'] = bps_value_list
    df['bps_rate'] = bps_rate_list
    df['opps'] = opps_value_list
    df['opps'] = opps_rate_list
    df['plobtxps'] = plobtxps_value_list
    df['plobtxps_rate'] = plobtxps_rate_list
    df['ploashh'] = ploashh_value_list
    df['ploashh_rate'] = ploashh_rate_list
    df['roe'] = roe_value_list
    df['roe_rate'] = roe_rate_list
    df['roa'] = rota_value_list
    df['roa_rate'] = rota_rate_list
    df['tlia_ta'] = tlia_ta_value_list
    df['tlia_ta_rate'] = tlia_ta_rate_list
    df['tsrps'] = tsrps_value_list
    df['tsrps_rate'] = tsrps_rate_list
    df['apycvspd'] = apycvspd_value_list
    df['apycvspd_rate'] = apycvspd_rate_list
    df['arbcvspd'] = arbcvspd_value_list
    df['arbcvspd_rate'] = arbcvspd_rate_list
    df['ncfps'] = ncfps_value_list
    df['ncfps_rate'] = ncfps_rate_list
    df['nocfps'] = nocfps_value_list
    df['nocfps_rate'] = nocfps_rate_list
    df['ncfps'] = ncfps_value_list
    df['ncfps_rate'] = ncfps_rate_list
    df['ninvcfps'] = ninvcfps_value_list
    df['ninvcfps_rate'] = ninvcfps_rate_list
    df['code'] = code
    df['name'] = name_list[0]
    df.set_index('report_name', inplace=True)
    df = df.T
    return df

def get_hk_main_finance_data(code='00700', freq='q'):
    # freq = y 年度/ freq =q 季度
    # 主要财务数据
    return _get_pagedata(freq, code)

def get_hk_income_finance_data(code='00700', freq='y'):
    # 利润表
    pass

def get_hk_balance_finance_data(code='00700', freq='y'):
    # 资产负债表
    pass

def get_hk_cash_flow_finance_data(code='00700', freq='y'):


######################港股财务数据##########################

if __name__ == '__main__':
    #df = get_zz800_codes()  # 000908
    #df = get_a_codes()
    #df = get_quote_data()
    #df = get_10_net_trade_data()
    #df = get_industry_codes()
    #df = get_code_base_finance_year_data()
    #df = get_code_base_finance_bgq_data()
    #df = get_code_finance_year_data_xjll()
    #df = get_all_codes_finance_bgq_data_xjll(['SZ.000001', 'SZ.000002'])
    #df = get_his_net_capital_trade_data()
    #df = get_st_stock_codes()
    #df = get_3_net_trade_data()
    #df = get_northbound_net_trade_data()
    #df = get_northbound_code_net_trade_data()
    # df = get_his_hbgy_capital_data()
    df = get_rzrq_data()
    print(df)