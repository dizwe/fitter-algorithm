import readAndSave
from functools import partial


def search_data(data, height=None, weight=None):
    if height + 5 > int(data['104']) >= height - 5:# 이런 범위도 나중에 분석해봐야함.
        if weight == None: #아무것도 안적었을 때
            return True
        elif weight + 0.5 > float(data['510']) >= weight - 0.5:
            return True
    return False












