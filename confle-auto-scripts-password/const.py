# -*- coding: UTF-8 -*-
import os

class Const:
    def __init__(self):

        # 共通
        self.HOME_DIR = os.path.dirname(os.path.abspath(__file__))  # ホームディレクトリ
        
        # コマンド
        self.VPN_CONNECT_PID_CMD = "ps au | grep -v grep | grep vpn_connect.py | wc -l"
        
        # API URL
        self.JIRA_API_URL_BASE = "xxxxxxxxxx/jira"
        self.JIRA_API_CHK = "rest/api/2/myself"
        self.JIRA_CHANGE_PASSWD = "rest/api/2/myself/password"
        self.JIRA_CHANGE_PASSWD_T = "rest/api/2/user/password"

        # VPN
        self.XXXX_VPN_URL = "https://xxxxxxxxxxxxxx" # VPNアクセスパス
        self.XXXX_VPN_INFO = {
            "user": "xxxxxxxxx",
            "password": "xxxxxxxx"
        }

        # CONFLE(JIRA)
        self.CONFLE_JIRA_USER = {
            "user": "xxxxxxxx"
        }
        
        self.CONFLE_JIRA_INFO = {
            "Content-Type": "application/json"
        }
        
        self.CONFLE_JIRA_TEST = {
            "Content-Type": "text/html"
        }
        
        self.CONFLE_PUT_INFO = {
            "username": "xxxxxxxx",
            "key": "xxxxxxxxxxxxxxxxx"
        }
        
        self.CONFLE_JIRA_PASSWORD = self.HOME_DIR + "/last_password.list"
        
        # SNS TOPIC SUBJECT
        self.SUBJECT_PASSWORD_CHANGE = "パスワード変更成功"
        self.SUBJECT_VPN_UNCONNECT = "VPN接続失敗"
        self.SUBJECT_API_UNCONNECT = "API接続失敗"
        self.SUBJECT_OTHER_UNCONNECT = "予期せぬエラー"
        
        # SNS ARN
        self.SNS_ARN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        
        # SNS Default Messages
        self.SNS_DEFAULT_MESSAGES = "各位\n \nお疲れ様です。オタクです。\n"
        self.SNS_CHANGEOK_MESSAGES = "\nパスワードが無事変更されました。パスワードは下記です\n"
        self.SNS_VPNNG_MESSAGES = "\nVPN接続が失敗しました。確認してください。\n"
        self.SNS_APING_MESSAGES = "\nAPIのアクセスが失敗しました。\n"
        self.SNS_PASSWORNG_MESSAGES = "\nパスワード変更失敗しました。\n"
