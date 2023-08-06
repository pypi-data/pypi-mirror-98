#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import pandas as pd
import requests as req
import jsonpath
from PaHKStockXueQiuFinanceData.common import *

def _get_pagedata(freq='q', code='00700', page=8):
    # 获取雪球页面财务数据
    # https://stock.xueqiu.com/v5/stock/finance/hk/indicator.json?symbol=00700&type=Q4&is_detail=true&count=5&timestamp=

    header1 = get_hk_fin_hearder(freq=freq, code=code, page=8)
    print('header1:{}'.format(header1))

    params = get_hk_fin_params(code=code, page=page)

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

    res_txt = (respon.text).replace('jQuery112407285217582388686_1611985850544(', '')
    res_txt = res_txt.replace(');', '')

    data = json.loads(res_txt)
    target_df = data_change(data, code)
    #print(target_df)
    return target_df

def data_change(data, code):
    # 在json文本中提取需要的数据
    # code
    currency_name_list = jsonpath.jsonpath(data, '$..currency_name')
    # name
    name_list = jsonpath.jsonpath(data, '$..quote_name')
    # 收盘价
    annual_settle_date_list = jsonpath.jsonpath(data, '$..annual_settle_date')
    # report_name
    report_name_list = jsonpath.jsonpath(data, '$..report_name')
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
    # gpm 毛利率
    gpm_list2 = jsonpath.jsonpath(data, '$..gpm')
    gpm_value_list = [n[0] for n in gpm_list2]
    gpm_rate_list = [n[1] for n in gpm_list2]
    # cro 流动比率
    cro_list2 = jsonpath.jsonpath(data, '$..cro')
    cro_value_list = [n[0] for n in cro_list2]
    cro_rate_list = [n[1] for n in cro_list2]
    # qro 速动比率
    qro_list2 = jsonpath.jsonpath(data, '$..qro')
    qro_value_list = [n[0] for n in qro_list2]
    qro_rate_list = [n[1] for n in qro_list2]
    # ivcvspd 存货转换周期
    ivcvspd_list2 = jsonpath.jsonpath(data, '$..ivcvspd')
    ivcvspd_value_list = [n[0] for n in ivcvspd_list2]
    ivcvspd_rate_list = [n[1] for n in ivcvspd_list2]
    # beps 基本每股收益
    beps_list2 = jsonpath.jsonpath(data, '$..beps')
    beps_value_list = [n[0] for n in beps_list2]
    beps_rate_list = [n[1] for n in beps_list2]
    # beps_aju  基本每股收益_调整后
    beps_aju_list2 = jsonpath.jsonpath(data, '$..beps_aju')
    beps_aju_value_list = [n[0] for n in beps_aju_list2]
    beps_aju_rate_list = [n[1] for n in beps_aju_list2]
    # bps  每股净资产
    bps_list2 = jsonpath.jsonpath(data, '$..bps')
    bps_value_list = [n[0] for n in bps_list2]
    bps_rate_list = [n[1] for n in bps_list2]
    # opps  每股营业利润
    opps_list2 = jsonpath.jsonpath(data, '$..opps')
    opps_value_list = [n[0] for n in opps_list2]
    opps_rate_list = [n[1] for n in opps_list2]
    # plobtxps 每股利润总额
    plobtxps_list2 = jsonpath.jsonpath(data, '$..plobtxps')
    plobtxps_value_list = [n[0] for n in plobtxps_list2]
    plobtxps_rate_list = [n[1] for n in plobtxps_list2]
    # ploashh  净利润
    ploashh_list2 = jsonpath.jsonpath(data, '$..ploashh')
    ploashh_value_list = [n[0] for n in ploashh_list2]
    ploashh_rate_list = [n[1] for n in ploashh_list2]
    # roe  ROE
    roe_list2 = jsonpath.jsonpath(data, '$..roe')
    roe_value_list = [n[0] for n in roe_list2]
    roe_rate_list = [n[1] for n in roe_list2]
    # rota  ROA
    rota_list2 = jsonpath.jsonpath(data, '$..rota')
    rota_value_list = [n[0] for n in rota_list2]
    rota_rate_list = [n[1] for n in rota_list2]
    # tlia_ta  资产负债率
    tlia_ta_list2 = jsonpath.jsonpath(data, '$..tlia_ta')
    tlia_ta_value_list = [n[0] for n in tlia_ta_list2]
    tlia_ta_rate_list = [n[1] for n in tlia_ta_list2]
    # tsrps 每股营业收入
    tsrps_list2 = jsonpath.jsonpath(data, '$..tsrps')
    tsrps_value_list = [n[0] for n in tsrps_list2]
    tsrps_rate_list = [n[1] for n in tsrps_list2]
    # apycvspd 应付账款转换周期
    apycvspd_list2 = jsonpath.jsonpath(data, '$..apycvspd')
    apycvspd_value_list = [n[0] for n in apycvspd_list2]
    apycvspd_rate_list = [n[1] for n in apycvspd_list2]
    # arbcvspd 应收账款转换周期
    arbcvspd_list2 = jsonpath.jsonpath(data, '$..arbcvspd')
    arbcvspd_value_list = [n[0] for n in arbcvspd_list2]
    arbcvspd_rate_list = [n[1] for n in arbcvspd_list2]
    # ncfps 每股现金流净额
    ncfps_list2 = jsonpath.jsonpath(data, '$..ncfps')
    ncfps_value_list = [n[0] for n in ncfps_list2]
    ncfps_rate_list = [n[1] for n in ncfps_list2]
    # nocfps 每股经营现金流
    nocfps_list2 = jsonpath.jsonpath(data, '$..nocfps')
    nocfps_value_list = [n[0] for n in nocfps_list2]
    nocfps_rate_list = [n[1] for n in nocfps_list2]
    # ncfps 每股现金流净额
    ncfps_list2 = jsonpath.jsonpath(data, '$..ncfps')
    ncfps_value_list = [n[0] for n in ncfps_list2]
    ncfps_rate_list = [n[1] for n in ncfps_list2]
    # ninvcfps 每股投资现金流
    ninvcfps_list2 = jsonpath.jsonpath(data, '$..ninvcfps')
    ninvcfps_value_list = [n[0] for n in ninvcfps_list2]
    ninvcfps_rate_list = [n[1] for n in ninvcfps_list2]
    # nfcgcfps 每股筹资现金流
    nfcgcfps_list2 = jsonpath.jsonpath(data, '$..nfcgcfps')
    nfcgcfps_value_list = [n[0] for n in nfcgcfps_list2]
    nfcgcfps_rate_list = [n[1] for n in nfcgcfps_list2]
    df = pd.DataFrame(report_name_list, columns=['report_name'])
    df['nfcgcfps_value'] = nfcgcfps_value_list
    df['nfcgcfps_rate'] = nfcgcfps_rate_list
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
    cookies = {
           'xq_a_token': 'a4b3e3e158cfe9745b677915691ecd794b4bf2f9',
           'xqat': 'a4b3e3e158cfe9745b677915691ecd794b4bf2f9',
           'xq_r_token': 'b80d3232bf315f8710d36ad2370bc777b24d5001',
           'xq_id_token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTYxNzc2MzQxOCwiY3RtIjoxNjE1NjIyMTYxNTUxLCJjaWQiOiJkOWQwbjRBWnVwIn0.T6Xvdh8HdqA6KfoIBbnw2l6-qnQfpaOVLoaWlblfmB9JWVJ5QO1dz_aUMKwYHpcDH02Bi5705Ks27F-ppGypZA15bhyTTCiEeYlru47tRWNetHD7YjSTSu1BUg7n8YXX-2H-Ey2ObT5FNRHTN7c6Yoeo8aB_9kFsmyFjXrvNsMu-nP5_WZ1SiL7Rm4Q-_PD8IRyvIe4PxWfj4FAX-7nV7Hu694o0VbTGICQ8OFFXYCrYpJ_YCpE7hoXJhnNJ2wbmbz2hRfDdvo0hNCLJkr5j7g5EdIAKeQKyPvsFveHY0zUg9-M3-u4qt11qvQyHjB0AcA46lhVW2-cT-pAP_RCguw',
           'u': '781615622195200',
           'device_id': '24700f9f1986800ab4fcc880530dd0ed',
           'Hm_lvt_1db88642e346389874251b5a1eded6e3': '1615622197',
           'is_overseas': '0',
           's': 'cb1dgpvcul',
           'Hm_lpvt_1db88642e346389874251b5a1eded6e3': '1615622327',
    }
    params =get_hk_fin_params(freq=freq, code=code, page=8)
    header = get_hk_fin_hearder(trace_id='ad91103ba8e59899', date_='Sat, 13 Mar 2021 07:59:04 GMT')
    respon = req.get(url='https://stock.xueqiu.com/v5/stock/finance/hk/income.json', headers=header, cookies=cookies, params=params)
    content = respon.text
    data = json.loads(content)
    target_df = income_data_change(data, code)
    return target_df

def income_data_change(data, code):
    # 在json文本中提取需要的数据
    # code
    currency_name_list = jsonpath.jsonpath(data, '$..currency_name')
    # name
    name_list = jsonpath.jsonpath(data, '$..quote_name')
    # report_name
    report_name_list = jsonpath.jsonpath(data, '$..report_name')
    # report_date
    report_date_list = jsonpath.jsonpath(data, '$..report_date')
    # ploashh 本公司股本持有人应占溢利
    ploashh_list2 = jsonpath.jsonpath(data, '$..ploashh')
    ploashh_value_list = [n[0] for n in ploashh_list2]
    ploashh_rate_list = [n[1] for n in ploashh_list2]
    # otopeexp  其他经营开支
    otopeexp_list2 = jsonpath.jsonpath(data, '$..otopeexp')
    otopeexp_value_list = [n[0] for n in otopeexp_list2]
    otopeexp_rate_list = [n[1] for n in otopeexp_list2]
    print('otopeexp_value_list:{}'.format(otopeexp_value_list))
    print('otopeexp_rate_list:{}'.format(otopeexp_rate_list))

    # otiog  其他收入及收益
    otiog_list2 = jsonpath.jsonpath(data, '$..otiog')
    otiog_value_list = [n[0] for n in otiog_list2]
    otiog_rate_list = [n[1] for n in otiog_list2]

    # otcphio  其他全面收入
    otcphio_list2 = jsonpath.jsonpath(data, '$..otcphio')
    otcphio_value_list = [n[0] for n in otcphio_list2]
    otcphio_rate_list = [n[1] for n in otcphio_list2]

    # opeploinclfincost  扣除融资成本前之经营溢利
    opeploinclfincost_list2 = jsonpath.jsonpath(data, '$..opeploinclfincost')
    opeploinclfincost_value_list = [n[0] for n in opeploinclfincost_list2]
    opeploinclfincost_rate_list = [n[1] for n in opeploinclfincost_list2]

    # opeplo 经营溢利
    opeplo_list2 = jsonpath.jsonpath(data, '$..opeplo')
    opeplo_value_list = [n[0] for n in opeplo_list2]
    opeplo_rate_list = [n[1] for n in opeplo_list2]

    # nosplitems 非经营特殊项目
    nosplitems_list2 = jsonpath.jsonpath(data, '$..nosplitems')
    nosplitems_value_list = [n[0] for n in nosplitems_list2]
    nosplitems_rate_list = [n[1] for n in nosplitems_list2]

    # jtctletiascom 联营合营公司
    jtctletiascom_list2 = jsonpath.jsonpath(data, '$..jtctletiascom')
    jtctletiascom_value_list = [n[0] for n in jtctletiascom_list2]
    jtctletiascom_rate_list = [n[1] for n in jtctletiascom_list2]

    # gp 毛利
    gp_list2 = jsonpath.jsonpath(data, '$..gp')
    gp_value_list = [n[0] for n in gp_list2]
    gp_rate_list = [n[1] for n in gp_list2]

    # fcgcost 融资成本
    fcgcost_list2 = jsonpath.jsonpath(data, '$..fcgcost')
    fcgcost_value_list = [n[0] for n in fcgcost_list2]
    fcgcost_rate_list = [n[1] for n in fcgcost_list2]

    # divdbups_ajupd 每股股息
    divdbups_ajupd_list2 = jsonpath.jsonpath(data, '$..divdbups_ajupd')
    divdbups_ajupd_value_list = [n[0] for n in divdbups_ajupd_list2]
    divdbups_ajupd_rate_list = [n[1] for n in divdbups_ajupd_list2]

    # deps_aju 每股摊薄盈利
    deps_aju_list2 = jsonpath.jsonpath(data, '$..deps_aju')
    deps_aju_value_list = [n[0] for n in deps_aju_list2]
    deps_aju_rate_list = [n[1] for n in deps_aju_list2]

    # depaz 折旧及摊销
    depaz_list2 = jsonpath.jsonpath(data, '$..depaz')
    depaz_value_list = [n[0] for n in depaz_list2]
    depaz_rate_list = [n[1] for n in depaz_list2]

    # cmnshdiv 普通股股息
    cmnshdiv_list2 = jsonpath.jsonpath(data, '$..cmnshdiv')
    cmnshdiv_value_list = [n[0] for n in cmnshdiv_list2]
    cmnshdiv_rate_list = [n[1] for n in cmnshdiv_list2]

    # beps_aju 每股基本盈利
    beps_aju_list2 = jsonpath.jsonpath(data, '$..beps_aju')
    beps_aju_value_list = [n[0] for n in beps_aju_list2]
    beps_aju_rate_list = [n[1] for n in beps_aju_list2]

    # amtmiint 少数股东权益
    amtmiint_list2 = jsonpath.jsonpath(data, '$..amtmiint')
    amtmiint_value_list = [n[0] for n in amtmiint_list2]
    amtmiint_rate_list = [n[1] for n in amtmiint_list2]

    # amteqyhdcom 本公司股本持有人应占溢利
    amteqyhdcom_list2 = jsonpath.jsonpath(data, '$..amteqyhdcom')
    amteqyhdcom_value_list = [n[0] for n in amteqyhdcom_list2]
    amteqyhdcom_rate_list = [n[1] for n in amteqyhdcom_list2]

    # admexp 行政开支
    admexp_list2 = jsonpath.jsonpath(data, '$..admexp')
    admexp_value_list = [n[0] for n in admexp_list2]
    admexp_rate_list = [n[1] for n in admexp_list2]

    # # month_num
    month_num_list = jsonpath.jsonpath(data, '$..month_num')
    # ed
    ed_list1 = jsonpath.jsonpath(data, '$..ed')
    # tto  总营收/总营收同比增长
    tto_list2 = jsonpath.jsonpath(data, '$..tto')
    tto_value_list = [n[0] for n in tto_list2]
    tto_rate_list = [n[1] for n in tto_list2]

    # tcphio 全面收入总额
    tcphio_list2 = jsonpath.jsonpath(data, '$..tcphio')
    tcphio_value_list = [n[0] for n in tcphio_list2]
    tcphio_rate_list = [n[1] for n in tcphio_list2]

    # sr_ta 营业收入合计
    sr_ta_list2 = jsonpath.jsonpath(data, '$..sr_ta')
    sr_ta_value_list = [n[0] for n in sr_ta_list2]
    sr_ta_rate_list = [n[1] for n in sr_ta_list2]

    # slgdstexp 销售及分销开支
    slgdstexp_list2 = jsonpath.jsonpath(data, '$..slgdstexp')
    slgdstexp_value_list = [n[0] for n in slgdstexp_list2]
    slgdstexp_rate_list = [n[1] for n in slgdstexp_list2]

    # slgcost  销售成本
    slgcost_list2 = jsonpath.jsonpath(data, '$..slgcost')
    slgcost_value_list = [n[0] for n in slgcost_list2]
    slgcost_rate_list = [n[1] for n in slgcost_list2]

    # plocyr  除税后溢利
    plocyr_list2 = jsonpath.jsonpath(data, '$..plocyr')
    plocyr_value_list = [n[0] for n in plocyr_list2]
    plocyr_rate_list = [n[1] for n in plocyr_list2]

    # plobtx  除税前溢利
    plobtx_list2 = jsonpath.jsonpath(data, '$..plobtx')
    plobtx_value_list = [n[0] for n in plobtx_list2]
    plobtx_rate_list = [n[1] for n in plobtx_list2]

    # topeexp 经营开支总额
    topeexp_list2 = jsonpath.jsonpath(data, '$..topeexp')
    topeexp_value_list = [n[0] for n in topeexp_list2]
    topeexp_rate_list = [n[1] for n in topeexp_list2]

    # tipmcgpvs 减值及拨备
    tipmcgpvs_list2 = jsonpath.jsonpath(data, '$..tipmcgpvs')
    tipmcgpvs_value_list = [n[0] for n in tipmcgpvs_list2]
    tipmcgpvs_rate_list = [n[1] for n in tipmcgpvs_list2]
    print('currency_name_list:{}'.format(currency_name_list))

    df = pd.DataFrame(otopeexp_value_list, columns=['otopeexp_value_list'])
    df['otopeexp_rate'] = otopeexp_rate_list
    df['month_num_list'] = month_num_list
    df['ed_list'] = ed_list1
    df['topeexp_value'] = topeexp_value_list
    df['topeexp_rate'] = topeexp_rate_list
    df['tipmcgpvs_value'] = tipmcgpvs_value_list
    df['tipmcgpvs_rate'] = tipmcgpvs_rate_list
    df['sr_ta_rate'] = sr_ta_rate_list
    df['sr_ta_value'] = sr_ta_value_list
    df['tcphio_rate'] = tcphio_rate_list
    df['tcphio_value'] = tcphio_value_list
    df['slgcost_rate'] = slgcost_rate_list
    df['slgcost_value'] = slgcost_value_list
    df['slgdstexp_rate'] = slgdstexp_rate_list
    df['slgdstexp_value'] = slgdstexp_value_list
    df['plobtx_rate'] = plobtx_rate_list
    df['plobtx_value'] = plobtx_value_list
    df['plocyr_rate'] = plocyr_rate_list
    df['plocyr_value'] = plocyr_value_list
    df['tto'] = tto_value_list
    df['tto_rate'] = tto_rate_list
    df['report_name'] = report_name_list
    df['report_date'] = report_date_list
    df['admexp_rate'] = admexp_rate_list
    df['admexp_value'] = admexp_value_list
    df['amteqyhdcom_rate'] = amteqyhdcom_rate_list
    df['amteqyhdcom_value'] = amteqyhdcom_value_list
    df['amtmiint_value'] = amtmiint_value_list
    df['amtmiint_rate'] = amtmiint_rate_list
    df['cmnshdiv_rate'] = cmnshdiv_rate_list
    df['cmnshdiv_value'] = cmnshdiv_value_list
    df['beps_aju'] = beps_aju_value_list
    df['beps_aju_rate'] = beps_aju_rate_list
    df['depaz_rate'] = depaz_rate_list
    df['depaz_value'] = depaz_value_list
    df['deps_aju_rate'] = deps_aju_rate_list
    df['deps_aju_value'] = deps_aju_value_list
    df['divdbups_ajupd_rate'] = divdbups_ajupd_rate_list
    df['divdbups_ajupd_value'] = divdbups_ajupd_value_list
    df['ploashh'] = ploashh_value_list
    df['ploashh_rate'] = ploashh_rate_list
    df['fcgcost_rate'] = fcgcost_rate_list
    df['fcgcost_value'] = fcgcost_value_list
    df['gp_rate'] = gp_rate_list
    df['gp_value'] = gp_value_list
    df['jtctletiascom_rate'] = jtctletiascom_rate_list
    df['jtctletiascom_value'] = jtctletiascom_value_list
    df['nosplitems_rate'] = nosplitems_rate_list
    df['nosplitems_value'] = nosplitems_value_list
    df['opeplo_rate'] = opeplo_rate_list
    df['opeplo_value'] = opeplo_value_list
    df['opeploinclfincost_rate'] = opeploinclfincost_rate_list
    df['opeploinclfincost_value'] = opeploinclfincost_value_list
    df['otcphio_value'] = otcphio_value_list
    df['otcphio_rate'] = otcphio_rate_list
    df['otiog_rate'] = otiog_rate_list
    df['otiog_value'] = otiog_value_list
    df['code'] = code
    df['name'] = name_list[0]
    df['currency_name_list'] = currency_name_list[0]
    df.set_index('report_name', inplace=True)
    df = df.T
    return df

def get_hk_balance_finance_data(code='00700', freq='y', page=8):
    # 资产负债表
    cookies = {
        'xq_a_token': 'a4b3e3e158cfe9745b677915691ecd794b4bf2f9',
        'xqat': 'a4b3e3e158cfe9745b677915691ecd794b4bf2f9',
        'xq_r_token': 'b80d3232bf315f8710d36ad2370bc777b24d5001',
        'xq_id_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTYxNzc2MzQxOCwiY3RtIjoxNjE1NjIyMTYxNTUxLCJjaWQiOiJkOWQwbjRBWnVwIn0.T6Xvdh8HdqA6KfoIBbnw2l6-qnQfpaOVLoaWlblfmB9JWVJ5QO1dz_aUMKwYHpcDH02Bi5705Ks27F-ppGypZA15bhyTTCiEeYlru47tRWNetHD7YjSTSu1BUg7n8YXX-2H-Ey2ObT5FNRHTN7c6Yoeo8aB_9kFsmyFjXrvNsMu-nP5_WZ1SiL7Rm4Q-_PD8IRyvIe4PxWfj4FAX-7nV7Hu694o0VbTGICQ8OFFXYCrYpJ_YCpE7hoXJhnNJ2wbmbz2hRfDdvo0hNCLJkr5j7g5EdIAKeQKyPvsFveHY0zUg9-M3-u4qt11qvQyHjB0AcA46lhVW2-cT-pAP_RCguw',
        'u': '781615622195200',
        'device_id': '24700f9f1986800ab4fcc880530dd0ed',
        'Hm_lvt_1db88642e346389874251b5a1eded6e3': '1615622197',
        'is_overseas': '0',
        's': 'cb1dgpvcul',
        'Hm_lpvt_1db88642e346389874251b5a1eded6e3': '1615622327',
    }
    params = get_hk_fin_params(freq=freq, code=code, page=page)
    header = get_hk_fin_hearder(trace_id='bef5f4d99b4e04bc', date_='Sat, 13 Mar 2021 09:51:18 GMT')
    respon = req.get(url='https://stock.xueqiu.com/v5/stock/finance/hk/balance.json', headers=header, cookies=cookies,
                     params=params)
    content = respon.text
    data = json.loads(content)
    target_df = balance_data_change(data, code)
    return target_df

def balance_data_change(data, code):
    # 在json文本中提取需要的数据
    #print('data:{}'.format(data))
    # currency_name
    currency_name_list = jsonpath.jsonpath(data, '$..currency_name')
    # quote_name
    quote_name_list = jsonpath.jsonpath(data, '$..quote_name')
    # report_name
    report_name_list = jsonpath.jsonpath(data, '$..report_name')
    # report_date
    report_date_list = jsonpath.jsonpath(data, '$..report_date')

    # otca  其他流动资产
    otca_list2 = jsonpath.jsonpath(data, '$..otca')
    otca_value_list = [n[0] for n in otca_list2]
    otca_rate_list = [n[1] for n in otca_list2]

    # month_num
    month_num_list1 = jsonpath.jsonpath(data, '$..month_num')
    # ed
    ed_list1 = jsonpath.jsonpath(data, '$..ed')
    # nalia 净资产
    nalia_list2 = jsonpath.jsonpath(data, '$..nalia')
    nalia_value_list = [n[0] for n in nalia_list2]
    nalia_rate_list = [n[1] for n in nalia_list2]

    # miint  少数股东权益
    miint_list2 = jsonpath.jsonpath(data, '$..miint')
    miint_value_list = [n[0] for n in miint_list2]
    miint_rate_list = [n[1] for n in miint_list2]

    # ltdt 长期债项
    ltdt_list2 = jsonpath.jsonpath(data, '$..ltdt')
    ltdt_value_list = [n[0] for n in ltdt_list2]
    ltdt_rate_list = [n[1] for n in ltdt_list2]

    # iv 存货
    iv_list2 = jsonpath.jsonpath(data, '$..iv')
    iv_value_list = [n[0] for n in iv_list2]
    iv_rate_list = [n[1] for n in iv_list2]

    # inv  投资
    inv_list2 = jsonpath.jsonpath(data, '$..inv')
    inv_value_list = [n[0] for n in inv_list2]
    inv_rate_list = [n[1] for n in inv_list2]

    # iga  无形资产
    iga_list2 = jsonpath.jsonpath(data, '$..iga')
    iga_value_list = [n[0] for n in iga_list2]
    iga_rate_list = [n[1] for n in iga_list2]

    # fxda  固定资产
    fxda_list2 = jsonpath.jsonpath(data, '$..fxda')
    fxda_value_list = [n[0] for n in fxda_list2]
    fxda_rate_list = [n[1] for n in fxda_list2]

    # fina  金融资产
    fina_list2 = jsonpath.jsonpath(data, '$..fina')
    fina_value_list = [n[0] for n in fina_list2]
    fina_rate_list = [n[1] for n in fina_list2]

    # diftatclia 总资产减流动负债
    diftatclia_list2 = jsonpath.jsonpath(data, '$..diftatclia')
    diftatclia_value_list = [n[0] for n in diftatclia_list2]
    diftatclia_rate_list = [n[1] for n in diftatclia_list2]

    # clia  流动负债合计
    clia_list2 = jsonpath.jsonpath(data, '$..clia')
    clia_value_list = [n[0] for n in clia_list2]
    clia_rate_list = [n[1] for n in clia_list2]

    # cceq 现金及现金等价物
    cceq_list2 = jsonpath.jsonpath(data, '$..cceq')
    cceq_value_list = [n[0] for n in cceq_list2]
    cceq_rate_list = [n[1] for n in cceq_list2]

    # ca  流动资产合计
    ca_list2 = jsonpath.jsonpath(data, '$..ca')
    ca_value_list = [n[0] for n in ca_list2]
    ca_rate_list = [n[1] for n in ca_list2]

    # tnca  非流动资产合计
    tnca_list2 = jsonpath.jsonpath(data, '$..tnca')
    tnca_value_list = [n[0] for n in tnca_list2]
    tnca_rate_list = [n[1] for n in tnca_list2]

    # tlia  总负债
    tlia_list2 = jsonpath.jsonpath(data, '$..tlia')
    tlia_value_list = [n[0] for n in tlia_list2]
    tlia_rate_list = [n[1] for n in tlia_list2]

    # teqy  净资产
    teqy_list2 = jsonpath.jsonpath(data, '$..teqy')
    teqy_value_list = [n[0] for n in teqy_list2]
    teqy_rate_list = [n[1] for n in teqy_list2]

    # ta 总资产
    ta_list2 = jsonpath.jsonpath(data, '$..ta')
    ta_value_list = [n[0] for n in ta_list2]
    ta_rate_list = [n[1] for n in ta_list2]

    # stdt 短期债项
    stdt_list2 = jsonpath.jsonpath(data, '$..stdt')
    stdt_value_list = [n[0] for n in stdt_list2]
    stdt_rate_list = [n[1] for n in stdt_list2]

    # shpm 股份溢价
    shpm_list2 = jsonpath.jsonpath(data, '$..shpm')
    shpm_value_list = [n[0] for n in shpm_list2]
    shpm_rate_list = [n[1] for n in shpm_list2]

    # shhfd 股东权益
    shhfd_list2 = jsonpath.jsonpath(data, '$..shhfd')
    shhfd_value_list = [n[0] for n in shhfd_list2]
    shhfd_rate_list = [n[1] for n in shhfd_list2]

    # sd 日期
    sd_list2 = jsonpath.jsonpath(data, '$..sd')
    sd_value_list = [n[0] for n in sd_list2]
    sd_rate_list = [n[1] for n in sd_list2]

    # rpaculo 保留溢利
    rpaculo_list2 = jsonpath.jsonpath(data, '$..rpaculo')
    rpaculo_value_list = [n[0] for n in rpaculo_list2]
    rpaculo_rate_list = [n[1] for n in rpaculo_list2]

    # otstdt 其他短期负债
    otstdt_list2 = jsonpath.jsonpath(data, '$..otstdt')
    otstdt_value_list = [n[0] for n in otstdt_list2]
    otstdt_rate_list = [n[1] for n in otstdt_list2]

    # otrx 其他储备
    otrx_list2 = jsonpath.jsonpath(data, '$..otrx')
    otrx_value_list = [n[0] for n in otrx_list2]
    otrx_rate_list = [n[1] for n in otrx_list2]

    # otnca 其他非流动资产
    otnca_list2 = jsonpath.jsonpath(data, '$..otnca')
    otnca_value_list = [n[0] for n in otnca_list2]
    otnca_rate_list = [n[1] for n in otnca_list2]

    # otltlia 其他长期负债
    otltlia_list2 = jsonpath.jsonpath(data, '$..otltlia')
    otltlia_value_list = [n[0] for n in otltlia_list2]
    otltlia_rate_list = [n[1] for n in otltlia_list2]

    # trpy 应付账款
    trpy_list2 = jsonpath.jsonpath(data, '$..trpy')
    trpy_value_list = [n[0] for n in trpy_list2]
    trpy_rate_list = [n[1] for n in trpy_list2]

    # trx 总储备
    trx_list = jsonpath.jsonpath(data, '$..trx')
    trx_value_list = [n[0] for n in trx_list]
    trx_rate_list = [n[1] for n in trx_list]

    # trrb 应收账款
    trrb_list2 = jsonpath.jsonpath(data, '$..trrb')
    trrb_value_list = [n[0] for n in trrb_list2]
    trrb_rate_list = [n[1] for n in trrb_list2]

    # tnclia  非流动负债合计
    tnclia_list2 = jsonpath.jsonpath(data, '$..tnclia')
    tnclia_value_list = [n[0] for n in tnclia_list2]
    tnclia_rate_list = [n[1] for n in tnclia_list2]

    df = pd.DataFrame(ca_rate_list, columns=['ca_rate'])
    df['trx_value'] = trx_value_list
    df['trrb_rate'] = trrb_rate_list
    df['tnclia_value'] = tnclia_value_list
    df['tnclia_rate'] = tnclia_rate_list
    df['rpaculo_value'] = rpaculo_value_list
    df['rpaculo_rate'] = rpaculo_rate_list
    df['otstdt_value'] = otstdt_value_list
    df['otstdt_rate'] = otstdt_rate_list
    df['trpy_value'] = trpy_value_list
    df['trpy_rate'] = trpy_rate_list
    df['otltlia_value'] = otltlia_value_list
    df['otltlia_rate'] = otltlia_rate_list
    df['otnca_rate'] = otnca_rate_list
    df['otnca_value'] = otnca_value_list
    df['otrx_rate'] = otrx_rate_list
    df['otrx_value'] = otrx_value_list
    df['sd_rate'] = sd_rate_list
    df['sd_value'] = sd_value_list
    df['shhfd_value'] = shhfd_value_list
    df['shhfd_rate'] = shhfd_rate_list
    df['shpm_rate'] = shpm_rate_list
    df['shpm_value'] = shpm_value_list
    df['stdt_rate'] = stdt_rate_list
    df['stdt_value'] = stdt_value_list
    df['ta_value'] = ta_value_list
    df['ta_rate'] = ta_rate_list
    df['teqy_rate'] = teqy_rate_list
    df['teqy_value'] = teqy_value_list
    df['tlia_rate'] = tlia_rate_list
    df['tlia_value'] = tlia_value_list
    df['tnca_value'] = tnca_value_list
    df['tnca_rate'] = tnca_rate_list
    df['ca_value'] = ca_value_list
    df['cceq_value'] = cceq_value_list
    df['cceq_rate'] = cceq_rate_list
    df['clia_rate'] = clia_rate_list
    df['clia_value'] = clia_value_list
    df['diftatclia_rate'] = diftatclia_rate_list
    df['diftatclia_value'] = diftatclia_value_list
    df['fina_rate'] = fina_rate_list
    df['fina_value'] = fina_value_list
    df['fxda_rate'] = fxda_rate_list
    df['fxda_value'] = fxda_value_list
    df['iga_rate'] = iga_rate_list
    df['iga_value'] = iga_value_list
    df['inv_rate'] = inv_rate_list
    df['inv_value'] = inv_value_list
    df['iv_value'] = iv_value_list
    df['iv_rate'] = iv_rate_list
    df['ltdt_rate'] = ltdt_rate_list
    df['ltdt_value'] = ltdt_value_list
    df['miint_rate'] = miint_rate_list
    df['miint_value'] = miint_value_list
    df['report_name'] = report_name_list
    df['report_date'] = report_date_list
    df['nalia_rate'] = nalia_rate_list
    df['nalia_value'] = nalia_value_list
    df['ed'] = ed_list1
    df['month_num'] = month_num_list1[0]
    df['otca_rate'] = otca_rate_list
    df['otca_value'] = otca_value_list
    df['code'] = code
    df['name'] = quote_name_list[0]
    df['currency_name_list'] = currency_name_list[0]
    df.set_index('report_name', inplace=True)
    df = df.T
    return df

def get_hk_cash_flow_finance_data(code='00700', freq='y', page=8):
    # 现金流量表
    cookies = {
        'xq_a_token': 'a4b3e3e158cfe9745b677915691ecd794b4bf2f9',
        'xqat': 'a4b3e3e158cfe9745b677915691ecd794b4bf2f9',
        'xq_r_token': 'b80d3232bf315f8710d36ad2370bc777b24d5001',
        'xq_id_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTYxNzc2MzQxOCwiY3RtIjoxNjE1NjIyMTYxNTUxLCJjaWQiOiJkOWQwbjRBWnVwIn0.T6Xvdh8HdqA6KfoIBbnw2l6-qnQfpaOVLoaWlblfmB9JWVJ5QO1dz_aUMKwYHpcDH02Bi5705Ks27F-ppGypZA15bhyTTCiEeYlru47tRWNetHD7YjSTSu1BUg7n8YXX-2H-Ey2ObT5FNRHTN7c6Yoeo8aB_9kFsmyFjXrvNsMu-nP5_WZ1SiL7Rm4Q-_PD8IRyvIe4PxWfj4FAX-7nV7Hu694o0VbTGICQ8OFFXYCrYpJ_YCpE7hoXJhnNJ2wbmbz2hRfDdvo0hNCLJkr5j7g5EdIAKeQKyPvsFveHY0zUg9-M3-u4qt11qvQyHjB0AcA46lhVW2-cT-pAP_RCguw',
        'u': '781615622195200',
        'device_id': '24700f9f1986800ab4fcc880530dd0ed',
        'Hm_lvt_1db88642e346389874251b5a1eded6e3': '1615622197',
        'is_overseas': '0',
        's': 'cb1dgpvcul',
        'Hm_lpvt_1db88642e346389874251b5a1eded6e3': '1615637371',
    }
    params = get_hk_fin_params(freq=freq, code=code, page=page)
    header = get_hk_fin_hearder(trace_id='f5a72a85fb47898f', date_='Sat, 13 Mar 2021 09:51:18 GMT')
    respon = req.get(url='https://stock.xueqiu.com/v5/stock/finance/hk/cash_flow.json', headers=header, cookies=cookies,
                     params=params)
    content = respon.text
    data = json.loads(content)
    target_df = cash_flow_data_change(data, code)
    return target_df

def cash_flow_data_change(data, code):
    # 在json文本中提取需要的数据
    #print('data:{}'.format(data))
    # currency_name
    currency_name_list = jsonpath.jsonpath(data, '$..currency_name')
    # quote_name
    quote_name_list = jsonpath.jsonpath(data, '$..quote_name')
    # report_name
    report_name_list = jsonpath.jsonpath(data, '$..report_name')
    # report_date
    report_date_list = jsonpath.jsonpath(data, '$..report_date')

    # month_num
    month_num_list1 = jsonpath.jsonpath(data, '$..month_num')
    # ed
    ed_list1 = jsonpath.jsonpath(data, '$..ed')

    # depaz 折旧及摊销
    depaz_list2 = jsonpath.jsonpath(data, '$..depaz')
    depaz_value_list = [n[0] for n in depaz_list2]
    depaz_rate_list = [n[1] for n in depaz_list2]

    # sd 日期
    sd_list2 = jsonpath.jsonpath(data, '$..sd')

    # dcinv 投资减少
    dcinv_list2 = jsonpath.jsonpath(data, '$..dcinv')
    dcinv_value_list = [n[0] for n in dcinv_list2]
    dcinv_rate_list = [n[1] for n in dcinv_list2]

    # cceqeyr  期末现金
    cceqeyr_list2 = jsonpath.jsonpath(data, '$..cceqeyr')
    cceqeyr_value_list = [n[0] for n in cceqeyr_list2]
    cceqeyr_rate_list = [n[1] for n in cceqeyr_list2]

    # cceqbegyr  期初现金
    cceqbegyr_list2 = jsonpath.jsonpath(data, '$..cceqbegyr')
    cceqbegyr_value_list = [n[0] for n in cceqbegyr_list2]
    cceqbegyr_rate_list = [n[1] for n in cceqbegyr_list2]

    # adtfxda  增添固定资产
    adtfxda_list2 = jsonpath.jsonpath(data, '$..adtfxda')
    adtfxda_value_list = [n[0] for n in adtfxda_list2]
    adtfxda_rate_list = [n[1] for n in adtfxda_list2]

    # fxdiodtinstr 定息或债项工具融资
    fxdiodtinstr_list2 = jsonpath.jsonpath(data, '$..fxdiodtinstr')
    fxdiodtinstr_value_list = [n[0] for n in fxdiodtinstr_list2]
    fxdiodtinstr_rate_list = [n[1] for n in fxdiodtinstr_list2]

    # eqyfin 股本融资
    eqyfin_list2 = jsonpath.jsonpath(data, '$..eqyfin')
    eqyfin_value_list = [n[0] for n in eqyfin_list2]
    eqyfin_rate_list = [n[1] for n in eqyfin_list2]

    # dsfxda 出售固定资产
    dsfxda_list2 = jsonpath.jsonpath(data, '$..dsfxda')
    dsfxda_value_list = [n[0] for n in dsfxda_list2]
    dsfxda_rate_list = [n[1] for n in dsfxda_list2]

    # divrc 已收股息
    divrc_list2 = jsonpath.jsonpath(data, '$..divrc')
    divrc_value_list = [n[0] for n in divrc_list2]
    divrc_rate_list = [n[1] for n in divrc_list2]

    # divp  已派股息
    divp_list2 = jsonpath.jsonpath(data, '$..divp')
    divp_value_list = [n[0] for n in divp_list2]
    divp_rate_list = [n[1] for n in divp_list2]

    # lnrpa  偿还贷款
    lnrpa_list2 = jsonpath.jsonpath(data, '$..lnrpa')
    lnrpa_value_list = [n[0] for n in lnrpa_list2]
    lnrpa_rate_list = [n[1] for n in lnrpa_list2]

    # intrc 已收利息
    intrc_list2 = jsonpath.jsonpath(data, '$..intrc')
    intrc_value_list = [n[0] for n in intrc_list2]
    intrc_rate_list = [n[1] for n in intrc_list2]

    # intp 已付利息
    intp_list2 = jsonpath.jsonpath(data, '$..intp')
    intp_value_list = [n[0] for n in intp_list2]
    intp_rate_list = [n[1] for n in intp_list2]

    # icinv  投资增加
    icinv_list2 = jsonpath.jsonpath(data, '$..icinv')
    icinv_value_list = [n[0] for n in icinv_list2]
    icinv_rate_list = [n[1] for n in icinv_list2]

    # icdccceq 现金净额
    icdccceq_list2 = jsonpath.jsonpath(data, '$..icdccceq')
    icdccceq_value_list = [n[0] for n in icdccceq_list2]
    icdccceq_rate_list = [n[1] for n in icdccceq_list2]

    # nicln 新增贷款
    nicln_list2 = jsonpath.jsonpath(data, '$..nicln')
    nicln_value_list = [n[0] for n in nicln_list2]
    nicln_rate_list = [n[1] for n in nicln_list2]

    # ncfrldpty_finact 与关连人士之现金流量_融资活动
    ncfrldpty_finact_list2 = jsonpath.jsonpath(data, '$..ncfrldpty_finact')
    ncfrldpty_finact_value_list = [n[0] for n in ncfrldpty_finact_list2]
    ncfrldpty_finact_rate_list = [n[1] for n in ncfrldpty_finact_list2]

    # ncfdchexrateot  汇率影响
    ncfdchexrateot_list2 = jsonpath.jsonpath(data, '$..ncfdchexrateot')
    ncfdchexrateot_value_list = [n[0] for n in ncfdchexrateot_list2]
    ncfdchexrateot_rate_list = [n[1] for n in ncfdchexrateot_list2]

    # rpafxdiodtinstr 偿还定息或债项工具
    rpafxdiodtinstr_list2 = jsonpath.jsonpath(data, '$..rpafxdiodtinstr')
    rpafxdiodtinstr_value_list = [n[0] for n in rpafxdiodtinstr_list2]
    rpafxdiodtinstr_rate_list = [n[1] for n in rpafxdiodtinstr_list2]

    # nocf 经营活动产生的现金流量净额
    nocf_list2 = jsonpath.jsonpath(data, '$..nocf')
    nocf_value_list = [n[0] for n in nocf_list2]
    nocf_rate_list = [n[1] for n in nocf_list2]

    # ninvcf 投资活动产生的现金流量净额
    ninvcf_list2 = jsonpath.jsonpath(data, '$..ninvcf')
    ninvcf_value_list = [n[0] for n in ninvcf_list2]
    ninvcf_rate_list = [n[1] for n in ninvcf_list2]

    # nfcgcf  融资活动产生的现金流量净额
    nfcgcf_list2 = jsonpath.jsonpath(data, '$..nfcgcf')
    nfcgcf_value_list = [n[0] for n in nfcgcf_list2]
    nfcgcf_rate_list = [n[1] for n in nfcgcf_list2]

    # txprf 退回或已缴税项
    txprf_list2 = jsonpath.jsonpath(data, '$..txprf')
    txprf_value_list = [n[0] for n in txprf_list2]
    txprf_rate_list = [n[1] for n in txprf_list2]

    df = pd.DataFrame(adtfxda_rate_list, columns=['adtfxda_rate'])
    df['rpafxdiodtinstr_rate'] = rpafxdiodtinstr_rate_list
    df['rpafxdiodtinstr_value'] = rpafxdiodtinstr_value_list
    df['txprf_value'] = txprf_value_list
    df['txprf_rate'] = txprf_rate_list
    df['icinv_value'] = icinv_value_list
    df['icinv_rate'] = icinv_rate_list
    df['intp_rate'] = intp_rate_list
    df['intp_value'] = intp_value_list
    df['intrc_rate'] = intrc_rate_list
    df['intrc_value'] = intrc_value_list
    df['lnrpa_rate'] = lnrpa_rate_list
    df['lnrpa_value'] = lnrpa_value_list
    df['ncfdchexrateot_rate'] = ncfdchexrateot_rate_list
    df['ncfdchexrateot_value'] = ncfdchexrateot_value_list
    df['ncfrldpty_finact_rate'] = ncfrldpty_finact_rate_list
    df['ncfrldpty_finact_value'] = ncfrldpty_finact_value_list
    df['nfcgcf_rate'] = nfcgcf_rate_list
    df['nfcgcf_value'] = nfcgcf_value_list
    df['nicln_value'] = nicln_value_list
    df['nicln_rate'] = nicln_rate_list
    df['ninvcf_value'] = ninvcf_value_list
    df['ninvcf_rate'] = ninvcf_rate_list
    df['nocf_rate'] = nocf_rate_list
    df['nocf_value'] = nocf_value_list
    df['divp_value'] = divp_value_list
    df['divp_rate'] = divp_rate_list
    df['divrc_value'] = divrc_value_list
    df['divrc_rate'] = divrc_rate_list
    df['dsfxda_value'] = dsfxda_value_list
    df['dsfxda_rate'] = dsfxda_rate_list
    df['eqyfin_value'] = eqyfin_value_list
    df['eqyfin_rate'] = eqyfin_rate_list
    df['fxdiodtinstr_value'] = fxdiodtinstr_value_list
    df['fxdiodtinstr_rate'] = fxdiodtinstr_rate_list
    df['icdccceq_value'] = icdccceq_value_list
    df['icdccceq_rate'] = icdccceq_rate_list
    df['adtfxda_value'] = adtfxda_value_list
    df['cceqbegyr_value'] = cceqbegyr_value_list
    df['cceqbegyr_rate'] = cceqbegyr_rate_list
    df['cceqeyr_rate'] = cceqeyr_rate_list
    df['cceqeyr_value'] = cceqeyr_value_list
    df['dcinv_rate'] = dcinv_rate_list
    df['dcinv_value'] = dcinv_value_list
    df['sd'] = sd_list2[0]
    df['depaz_rate'] = depaz_rate_list
    df['depaz_value'] = depaz_value_list
    df['ed'] = ed_list1[0]
    df['month_num'] = month_num_list1[0]
    df['code'] = code
    df['name'] = quote_name_list[0]
    df['report_name'] = report_name_list[0]
    df['currency_name_list'] = currency_name_list[0]
    df.set_index('report_name', inplace=True)
    df = df.T
    return df

if __name__ == '__main__':
    # 主要财务数据
    #df = get_hk_main_finance_data()
    # 利润表
    #df_income = get_hk_income_finance_data('00700', freq='y')
    # 资产负债表
    #df_balance = get_hk_balance_finance_data('00700', freq='y')
    # 现金流量表
    df_cash = get_hk_cash_flow_finance_data('00700', freq='y')
    print('df:{}'.format(df_cash))

