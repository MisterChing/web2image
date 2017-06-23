#!/usr/bin/env python
import sys
import os
import hashlib
import json
from cgi import parse_qs, escape
from app.gen_image import *
from conf.config import *

def application(environ, start_response):
    param_dict = parse_qs(environ['QUERY_STRING'])
    url = param_dict.get('url', [''])[0]
    url = escape(url)
    des_path = generate_path()
    des_file = des_path + '/' + createMD5(str(time.time())) + '.jpg'
    if not url:
        st = False
    else:
        st = phantomjs_generate_image(url, des_file)
        #  st = chrome_generate_image(url, des_file)
    data = {}
    if st == True:
        status = '200 OK'
        response_headers = [('Content-type','application/json; charset=utf-8')]
        data['errno'] = 0
        data['data'] = {}
        data['data']['url'] = des_file.replace(BASE_IMG_PATH.rstrip('/') + '/', BASE_IMG_HOST.rstrip('/') + '/')
    else:
        status = '200 OK'
        response_headers = [('Content-type','application/json; charset=utf-8')]
        data['errno'] = 1000
        data['data'] = {}
        data['data']['url'] = ''

    output = json.dumps(data)
    start_response(status, response_headers)
    return [output]


def generate_path():
    base_path = BASE_IMG_PATH.rstrip('/') + '/'
    dynamic_path = time.strftime("%Y/%m/%d", time.localtime(time.time()))
    des_path = base_path + dynamic_path
    try:
        if not os.path.exists(des_path):
            os.makedirs(des_path, 0755)
        return des_path
    except IOError as ex:
        print e
        return ''

def createMD5(str=''):
    m = hashlib.md5()
    m.update(str)
    new_str = m.hexdigest()
    return new_str
