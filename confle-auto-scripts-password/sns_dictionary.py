# coding:utf-8

# Basic Module
import os
import re
import sys
import time
import json
import boto3

# Original Module
import const
CONST = const.Const()

def main(*result_tag):
    
    TOPIC_ARN = CONST.SNS_ARN
    msg = ""
    msg += CONST.SNS_DEFAULT_MESSAGES
    
    if result_tag[0] is "vpn_ng":
        msg += CONST.SNS_VPNNG_MESSAGES
        subject = CONST.SUBJECT_VPN_UNCONNECT
        
    if result_tag[0] is "api_ng":
        msg += CONST.SNS_APING_MESSAGES
        subject = CONST.SUBJECT_API_UNCONNECT
        
    if result_tag[0] is "passchange_ng":
        msg += CONST.SNS_CHANGEOK_MESSAGES
        subject = CONST.SUBJECT_PASSWORD_CHANGE
    
    if result_tag[0] is "api_ok":
        msg += CONST.SNS_CHANGEOK_MESSAGES
        subject = CONST.SUBJECT_PASSWORD_CHANGE

    else:
        msg += "\n例外エラー"
        subject = "例外エラー"
        
    client = boto3.client('sns', region_name='ap-northeast-1')
    
    request = {
        'TopicArn': TOPIC_ARN,
        'Message': msg,
        'Subject': subject
    }
    response = client.publish(**request)

if __name__ == '__main__':
    print("SNS用の外部モジュール")
