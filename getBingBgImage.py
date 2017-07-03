# encoding: utf-8
import urllib
import urllib2
import re
import os
import time
import shutil
import glob

from config import *

from datetime import datetime
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}

def switch_time_zone():
    """
    切换时区到settings.TIME_ZONE
    """
    # settings.TIME_ZONE = "Asia/Shanghai"
    os.environ["TZ"] = "Asia/Shanghai"
    time.tzset()


try:
    request = urllib2.Request('http://cn.bing.com', headers=headers)
    response = urllib2.urlopen(request)
    content = response.read().decode('utf-8')
    pattern = re.compile('.*?url: "(.*?)",id:.*?',re.S)
    items = re.findall(pattern, content)

    for item in items:
        print 'image url:' + item #图片url
        item = item
        u = urllib.urlopen('http://cn.bing.com' + item)
        data = u.read()

        switch_time_zone()
        time = datetime.now()
        year = time.year
        month = time.month
        day = time.day

        about_pattern = re.compile('.*?rb/(.*?)_ZH.*?', re.S)
        about_items = re.findall(about_pattern, item)
        print  'about_items' + str(about_items)
        for about_item in about_items:
            print about_item #相关内容
        
        # filePath = '%s%s-%s-%s_%s.jpg' % (FILE_PATH, year, month, day, about_item)
        filePath = '%snew.jpg' % (FILE_PATH)
        print 'save_path:' + filePath
        f = open(filePath, 'wb')
        f.write(data)
        f.close()

        #把最新的图片在别处也保存一份
        # filePath2 = '%s%s-%s-%s_%s.jpg' % (ARCHIVE_FILE_PATH, year, month, day, about_item)
        # print 'save_path2:' + filePath2
        # f = open(filePath2, 'wb')
        # f.write(data)
        # f.close()
except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason

#图片地址格式:http://s.cn.bing.net/az/hprichbg/rb/MariaLenkDive_ZH-CN10833846465_1920x1080.jpg