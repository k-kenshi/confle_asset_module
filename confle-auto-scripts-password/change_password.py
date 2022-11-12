# coding:utf-8

# Basic Module
import os
import re
import sys
import time
import json
import boto3
import urllib3
import datetime
import requests
import subprocess
import urllib,urllib.request

from   subprocess import getoutput
from   requests.auth import HTTPBasicAuth
from   dateutil.relativedelta import relativedelta
from   urllib3.exceptions import InsecureRequestWarning

# Original Module
import const
import sns_dictionary

#####################################################################
# プロセスを確認する
# プロセスがない場合
# 終了 SNSを飛ばす(飛ばす)
# 
# 今現在のパスワードをlistから取得する
# 結合性を合わせる。一致していれば現在の月にフォーマットを合わせる
# プロセスがある場合、APIを実行する。パスワードは上記
# 変更結果を格納する。リストを更新する。
# 更新完了終えたらSNSで報告する
#
# 別処理でサーバをシャットダウンさせてリフレッシュ処理を行う

CONST = const.Const()

# API実行時のゴミエラー抑止
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#Common Data
user = CONST.CONFLE_JIRA_USER["user"]
headers_api = CONST.CONFLE_JIRA_INFO

def target_time():

    """
    
    時刻を得る
    :param None:
    :return (tuple): 時刻
    
    """
    today = datetime.datetime.now()
    date_format = "%Y%m"
    
    after_time = (today + datetime.timedelta(days=2)).strftime(date_format)
    today_time = today.strftime(date_format)
    
    before_month = today - relativedelta(months=1)
    before_time = before_month.strftime(date_format)
    return today_time,before_time

def vpn_pid_chk():
    
    out_put = int(getoutput(CONST.VPN_CONNECT_PID_CMD))
    return out_put

def jira_api_chk(*data_set):
    
    api_url = f"https://{CONST.JIRA_API_URL_BASE}/{CONST.JIRA_API_CHK}"
    
    if data_set[1] is "api_before_chk":
        password = "xxxxxxxxx"
    
    else:
        password = data_set[0]
     
    time.sleep(10)
    response = requests.get(api_url,data=None,auth=(user, password), headers=headers_api, verify=False)
    api_chk_return = response.status_code == requests.codes.ok
    
    return api_chk_return
    
def jira_api_connect(today_month,before_month):
    
    # メイン処理
    api_chk = jira_api_chk(today_month,"api_before_chk")
    
    # 200だけ許可する
    if api_chk is True:
        put_api = f"https://{CONST.JIRA_API_URL_BASE}/{CONST.JIRA_CHANGE_PASSWD}"
        data_dic = {}
        data_dic["password"] = "xxxx" + today_month
        data_dic["currentPassword"] = "xxxxxxx"
        data_refacter = json.dumps(data_dic)
            
        # requestsを利用してPUTできないのでコマンドラインで生成
        # try構文使う
        
        try:
            response = requests.put(put_api,data=data_refacter, auth=(user, password),verify=False, headers=headers_api, timeout=3)
            api_chk_return = response.status_code == requests.codes.ok
            return data_dic["password"]
            
        except Exception as e:
            print(e)
            #パスワード変えられない
            print("パスワード失敗")
            sns_dictionary.main("passcha_ng")
            sys.exit()
        
    # 40X系は弾く
    else:
        print("NG")
        # 例外処理としてSNSを飛ばす
        sns_dictionary.main("api_ng")

def main():

    # 時間取得
    get_target_time = target_time()
    print(get_target_time[0],get_target_time[1])
    
    # VPN接続チェック
    vpn_pid_chk_request = vpn_pid_chk()
    print(vpn_pid_chk_request)
    
    if vpn_pid_chk_request == 0:
        print("OWARI")
        # 例外処理としてSNSを飛ばす
        sns_dictionary.main("vpn_ng")
    
    else:
        api_put_action = jira_api_connect(get_target_time[0],get_target_time[1])
        
        # パスワード変更後の正常性確認
        change_pw_api_chk = jira_api_chk(api_put_action,"put_after_chk")
            
        if change_pw_api_chk is True:
            sns_dictionary.main("api_ok")
        else:
            # 例外処理としてSNSを飛ばす。
            sns_dictionary.main("error_outside")
            
if __name__ == '__main__':
    main()
