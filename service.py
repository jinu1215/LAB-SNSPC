#, encoding='utf-8' -*- coding: utf-8 -*-
import csv
import json
import boto3
import requests
import xmltodict
import datetime
import logging
import sys
import config

reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def _utf8(v):
    if isinstance(v, unicode):
        v = v.encode('utf-8')
    return v


def _naver_shop_search(params):
    payload = dict()
    for key, value in params.iteritems():
        payload[key] = _utf8(value)
    response = requests.get(config.naver_api_url, params=payload)
    return response.status_code, response.text

def get_naver_shop_product_code(shop, code_list):
    result = dict()
    params = {
        "target": "shop",
        "key": config.naver_api_key,
        "display": 100,
        "sort": "sim",
        "start": 1,
    }

    for code in code_list:
        params["query"] = code + " " + shop
        try:
            status, body = _naver_shop_search(params)
            if status == 200:
                data = json.loads(json.dumps(xmltodict.parse(body)))
                result[code] = dict()
                result[code]['code'] = list()
                result[code]['title'] = list()

                print int(data['rss']['channel']['total'])
                if int(data['rss']['channel']['total']) > 0:
                    items = data['rss']['channel']['item']
                    if isinstance(items, list):
                        for item in items:
                            if item["mallName"]  == shop:
                                result[code]['code'].append(item['productId'])
                                result[code]['title'].append(item['title'])
                    else:
                        if item["mallName"]  == shop:
                            result[code]['code'].append(item['productId'])
                            result[code]['title'].append(item['title'])
                        else:
                            result[code]['code'].append("Not searched")
                            result[code]['title'].append("Not searched")
                else:
                    result[code]['code'].append("Not searched")
                    result[code]['title'].append("Not searched")
        except Exception as e:
            result[code]['code'].append("searche error")
            result[code]['title'].append("searche error")
            logger.error(e)
            logger.error(code)
            logger.error(data)

    return result


def create_csv_file(filename, shop, data):
    windows_bom = "\xEF\xBB\xBF"
    with open(filename, 'w') as csvfile:
        csvfile.write(windows_bom)
        fieldnames = ['your shop', 'title', 'naver']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key in data.keys():
            index = 0
            for value in data[key]['code']:
                writer.writerow({"your shop": key,
                                 "title": data[key]['title'][index],
                                 "naver": value})
                index += 1


def handler(event, context):
    # Your code goes here!
    shop = event.get(u'shop')
    codes = event.get(u'codes')
    code_list = codes.split(',')

    result = get_naver_shop_product_code(shop, code_list)
    file_name = "result_" + datetime.datetime.utcnow().isoformat() + ".csv"
    file_path = "/tmp/" + file_name
    create_csv_file(file_path, shop, result)

    s3_client = boto3.client('s3')
    upload_path = config.s3_file_prefix+file_name
    s3_client.upload_file(file_path, config.s3_bucket, upload_path)
    url = s3_client.generate_presigned_url('get_object',
                                           Params={
                                               'Bucket': config.s3_bucket,
                                               'Key': upload_path
                                           })
    return {"location": url}
