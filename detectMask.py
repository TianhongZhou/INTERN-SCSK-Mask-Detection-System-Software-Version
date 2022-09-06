import json
import cv2
import numpy as np
import requests
from aip import AipBodyAnalysis
import wx_sdk
import base64


# read file from path
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


# define request sending function
def send_request(method, url, params=None, headers=None):
    method = str.upper(method)

    if method == "POST":
        return requests.post(url=url, data=params, headers=headers)
    elif method == "GET":
        return requests.get(url=url, params=params, headers=headers)
    else:
        return None


# function to convert image to base64string
def to_base_64_string(image_path):
    with open(image_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read())
    return b64_string


# function to use SNN API to detect mask
def snn_API_fingMask(image_path):
    base64String = to_base_64_string(image_path)
    # TODO
    method = ""  # POST, GET
    url = ""  # URL of SNN
    headers = None
    params = {
        "apikey": "",  # api key
        "file_name": "",  # file name
        "img": str(base64String),
    }

    # get response
    response = send_request(method=method, url=url, params=params, headers=headers)
    body = response.text
    result = json.loads(body)
    status = result["message"]

    if status == "SUCCESS":
        output = result["resultSet"][0][0]["label"]
    else:
        output = "request failed"

    return output


# function to use jd API to detect mask
def jd_API_fingMask(image_path):
    base64String = to_base_64_string(image_path)
    url = 'https://aiapi.jd.com/jdai/mask_detect'
    bodyStr = '{"imageBase64Str":' + str(base64String) + '}'
    params = {
        'type': 'json',
        'content': 'json string',
        'appkey': 'cc890785ffcd15db3c4f7ca78c6ad6f1',
        'secretkey': '6df8a31045b7ec9f747fcc7ec2dea902'
    }

    response = wx_sdk.wx_post_req(url, params, bodyStr=bodyStr)
    body = response.text
    result = json.loads(body)
    status_code = result["code"]

    if status_code == "12001":
        output = "image does not exist"
    elif status_code == "12002":
        output = "image format error"
    elif status_code == "12003":
        output = "image size error"
    elif status_code == "12004":
        output = "parameter does not exit"
    elif status_code == "12005":
        output = "parameter value is null"
    elif status_code == "13002":
        output = "time out"
    elif status_code == "13004":
        output = "no face detected"
    elif status_code == "10000":
        output = result["result"]
    else:
        output = status_code + " internel error"

    return output


# function to use baidu API to detect mask
def baidu_API_fingMask(image_path):
    # ID information
    APP_ID = "26474079"
    API_KEY = "fQXQXju5fACi7TBRKcZjuz5n"
    SECRET_KEY = "6oGUZgzqDxil9HTFhIBm3GldR2SlVvjR"
    client = AipBodyAnalysis(APP_ID, API_KEY, SECRET_KEY)
    image = get_file_content(image_path)

    # using body attribute
    client.bodyAttr(image)
    options = {"type": "face_mask"}

    # using parameter to detect body
    result_http = client.bodyAttr(image, options)

    if result_http["person_num"] > 0:
        if result_http["person_info"][0]["attributes"]["face_mask"]["name"] == "戴口罩":
            result = "Wearing mask"
        else:
            result = "No mask"
    else:
        result = "No human detected"

    return result
