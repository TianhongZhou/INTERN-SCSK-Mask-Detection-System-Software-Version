#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx_sdk

url = 'http://ai.gw.jdcloud.com/wanxianga17/testai'
params = { 
    'type' : 'json',
    'content' : 'json string',
    'appkey' : 'aef164550413cde170bd5e07d0c22d57',
    'secretkey':'77f17703b63d14d115ed26d507f5a7fa',
}

response = wx_sdk.wx_post_req( url, params)
print( response.text )