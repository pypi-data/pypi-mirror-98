# -*-coding:utf-8 -*-

"""
# File       : test.py
# Time       ：2021/3/16 6:14 下午
# Author     ：shen
# version    ：python 3.7
# Description：
"""
from datacenter_utils.logger import Logger
from datacenter_utils.redis_common import RedisObject
from datacenter_utils.mongo_common import MongoObject
from datacenter_utils.aws_s3 import download_s3, run_unzip_file, s3_list

if __name__ == '__main__':
    logger = Logger().logger
    logger.info('test')
    #################

    r = RedisObject(host='', port=6379)
    df = r.get_dataframe_from_redis('', ktype='d1')

    #################
    m = MongoObject(host='', port=27017, username='', password='', auth_db='')
    collection = m.client['']['']
    df_c = m.find_many_df(collection)

    #################
    aws_access_key_id = ''
    aws_secret_access_key = ''
    s3_bucket = ''
    s3_daily_path = {
        'level1_cn': 'feed/events/cn',
        'level1_us': 'feed/events/us',
        # 'level2_cn': 'feed/pro/cn',
        # 'level2_us': 'feed/pro/us',
        # 'level3_cn': 'feed/anticipated/cn',
        # 'level3_us': 'feed/anticipated/us',
    }

    local_daily_path = ''

    for pth in s3_daily_path.values():
        download_s3(pth,
                    s3_bucket,
                    aws_access_key_id,
                    aws_secret_access_key,
                    local_daily_path)
    run_unzip_file(local_daily_path)

    for pth in s3_daily_path.values():
        s3_list(pth,
                s3_bucket,
                aws_access_key_id,
                aws_secret_access_key)

