import readAndSave
import json
import urllib.request

def get_size_data():
    page_num = 0
    data_list = []
    base = 'http://www.ibtk.kr/ifbcBodySizeMale/ca39bec000a24d5bdf5b3d30742926ce'

    more_page = True
    while(more_page):
        page_info = '?model_query_pageable={"pageNumber":%d,"pageSize":100}'%(page_num)
        url = base + page_info
        data = json.loads(request_until_suceed(url))
        more_page = not data['lastPage']
        data_list.extend(data['content'])
        page_num += 1
        print(page_num)

    return data_list


def request_until_suceed(url):
    req = urllib.request.Request(url)
    success = False
    while success is False:
        try:
            response = urllib.request.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception as e:
            print(e)  # want to know what error it is
            print("Error for url %s" % (url))

    return response.read().decode(response.headers.get_content_charset())


size_data = get_size_data()
readAndSave.save_json(size_data,'man_size.json','utf8')

