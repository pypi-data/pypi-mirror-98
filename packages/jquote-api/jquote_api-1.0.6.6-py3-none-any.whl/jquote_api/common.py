# -*- coding: UTF-8 –*-

def get_hk_fin_hearder(trace_id='eaf8eae91a222895',date_='Wed, 10 Mar 2021 14:29:09 GMT'):
    # 公有hearder
    header = {
        "access-control-allow-credentials": 'true',
        'access-control-allow-headers': 'Origin, X-Requested-With, Content-Type, Accept',
        'access-control-allow-methods': 'GET, POST, OPTIONS, DELETE',
        'access-control-allow-origin': 'https://xueqiu.com',
        'cache-control': 'private, no-store, no-cache, must-revalidate, max-age=0',
        "content-encoding": 'gzip',
        "content-type": 'application/json;charset=UTF-8',
        "date": '{}'.format(date_),
        "p3p": 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT',
        "server": 'openresty',
        "trace-id": '{}'.format(trace_id),
        "vary": 'Accept-Encoding',
        "x-application-context": 'xueqiu-stock-api-rpc:production',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
    }
    return header

def get_hk_fin_params(freq='y',code='00700',page=8):
     return {
        'symbol': '{}'.format(code),
        'type': '{}'.format('Q4' if freq == 'y' else 'Q2'),
        'is_detail': 'true',
        'count': '{}'.format(page),
        'timestamp': '',
    }