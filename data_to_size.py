import readAndSave
from functools import partial


def search_data(data, height=None, weight=None):
    if height + 5 > int(data['104']) >= height - 5:# 이런 범위도 나중에 분석해봐야함.
        if weight == None: #아무것도 안적었을 때
            return True
        elif weight + 0.5 > float(data['510']) >= weight - 0.5:
            return True
    return False


def guess_upper_size(num, data):
    """0-어깨 1-가슴 2-팔 3-허리"""
    func_list = ['height', 'shoulder', 'chest', 'arm', 'waist']
    criteria_list = {
        'shoulder' : [395, 410, 425, 440, 460, 480, 500], # 애매 기준
        'chest' : [840, 850, 930, 1010, 1080, 1200, 1280],
        'arm' : [560, 565, 585, 600, 615, 625, 625], # 애매 기준
        'waist' : [720, 760, 840, 920, 1000, 1080, 1160],
        'height': [1650, 1650, 1750, 2000, 2100, 2100, 2100], # 일단 작은걸로 되개 하자.2000은 그냥 의미없음
    }
    size_names = ["XS", "S", "M", "L", "XL", "XXL", "XXXL"]

    def guess(criterias):
        for criteria, name in zip(criterias, size_names):
            if data <= criteria:
                return name
        return size_names[-1]#엄청 크면 제일큰 사이즈로

    return guess(criteria_list[func_list[num]])


def get_top_hw_filtered_dict(height, weight, filtered_surveys):
    #?????????? hw_filtered_surveys = list(filter(partial(search_data, height=height, weight=weight), surveys)) #surveys밖에 있는데도 돌아가네??????
    hw_filtered_surveys = list(filter(partial(search_data, height=height, weight=weight), filtered_surveys))
    if len(hw_filtered_surveys) ==0: return False# 데이터 없으면 그냥 False

    # 104 키 317 어깨너비 208 가슴둘레 233 팔길이 212 배꼽수준허리둘레 211 허리둘레 유니클로가 허리둘레야
    # 이거 바꾸면 func_list max(size_num_list[i] for i in 다 바꿔야함)
    few_parameter_surveys = [[int(person[s]) for s in ['104', '317', '208', '233', '211']]
                             for person in hw_filtered_surveys]

    #어깨 가슴 팔 허리 기준으로 계산(상체)
    guess_parameter_sizes = [[guess_upper_size(parameter_num, parameter_data)
                             for parameter_num, parameter_data in enumerate(few_parameter_survey)]
                             for few_parameter_survey in few_parameter_surveys]

    return guess_parameter_sizes


def guess_lower_size(num, data):
    func_list = ['waist', 'crotch', 'thigh', 'length', 'hem', 'hip']
    criteria_list = {
        'waist': [680, 700, 730, 760, 790, 820, 840, 865, 880, 910, 950, 1000],
        'crotch': [215, 220, 220, 230, 230, 230, 235, 240, 240, 240, 250, 255],
        'thigh': [270, 280, 280, 290, 300, 300, 310, 310, 320, 330, 340, 360],  # 애매 기준
        'length': [950, 960, 970, 980, 990, 1000, 1020, 1030, 1004, 1050, 1050, 1060, 1080],
        'hem': [155, 160, 160, 160, 170, 170, 170, 180, 180, 185, 185, 190],
        'hip' : [865, 890, 915, 940, 965, 990, 1015, 1040, 1065, 1090, 1130, 1180],# 일단 작은걸로 되개 하자.2000은 그냥 의미없음V
    }
    size_names = ["27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "38", "40"]

    def guess(criterias):
        for criteria, name in zip(criterias, size_names):
            if data <= criteria:
                return name
        return size_names[-1] # 엄청 크면 제일 큰 사이즈로

    return guess(criteria_list[func_list[num]])


def get_bottom_hw_filtered_dict(height, weight, filtered_surveys):
    #?????????? hw_filtered_surveys = list(filter(partial(search_data, height=height, weight=weight), surveys)) #surveys밖에 있는데도 돌아가네??????
    hw_filtered_surveys = list(filter(partial(search_data, height=height, weight=weight), filtered_surveys))
    if len(hw_filtered_surveys) ==0: return False# 데이터 없으면 그냥 False

    # ['waist', 'crotch', 'thigh', 'length', 'hem', 'hip']
    # 211 허리둘레 ?115 엉덩뼈가시높이(발 길이도 있어-이건 그냥 비율로) 419 넙다리둘레 128 샅높이(나중에 빼야함) 424 종아리 최소둘레 214 엉덩이
    # 이거 바꾸면 func_list max(size_num_list[i] for i in 다 바꿔야함)
    few_parameter_surveys = []
    for i, person in enumerate(hw_filtered_surveys):
        few_parameter_survey = []
        for s in ['211', '115', '419', '128', '424', '214']:
            # 밑위를 구하기(엉덩뼈가시높이-넙다리둘레)- 이거 이상행....
            if s == '128':
                crotch_len = int(person['115'])-int(person['128'])
                few_parameter_survey.append(crotch_len)
            else:
                few_parameter_survey.append(int(person[s]))
        few_parameter_surveys.append(few_parameter_survey)

    #어깨 가슴 팔 허리 기준으로 계산(상체) - 사이즈로 바꾸는 부분 제거
    # guess_parameter_sizes = [[guess_lower_size(parameter_num, parameter_data)
    #                          for parameter_num, parameter_data in enumerate(few_parameter_survey)]
    #                          for few_parameter_survey in few_parameter_surveys]
    #
    return few_parameter_surveys

if __name__ == "__main__":
    surveys = readAndSave.read_json('man_size.json','utf8')

    height_list = [int(survey['104']) for survey in surveys]
    height_min, height_max = min(height_list)//10 * 10, max(height_list)//10 * 10 # 1774->1770

    hw_filtered_dict = {}
    for height in range(height_min, height_max + 10, 10):#10mm씩 키 검색
        print('height{}'.format(height))
        height_filtered_list = list(filter(partial(search_data, height=height), surveys))
        if len(height_filtered_list) == 0: continue # 키 자료 없으면 안뽑기

        # 키 안에 있는 몸무게 데이터 접근
        weight_list = [float(height_filtered['510']) for height_filtered in height_filtered_list]
        weight_min, weight_max = round(min(weight_list)), round(max(weight_list))
        print('weight min{}, max {}'.format(weight_min, weight_max))

        hw_filtered_dict[height] ={}
        if weight_min == weight_max: # 자료가 하나밖에 없다면(하나만 있으면 range 문이 안돌아가므로)
            weight = weight_min
            hw_filtered_dict[height][weight] = get_bottom_hw_filtered_dict(height, weight, height_filtered_list)
            continue
        for weight in range(weight_min, weight_max, 1):
            # 없는 몸무게도 일단 들어가는 문제
            data = get_bottom_hw_filtered_dict(height, weight, height_filtered_list)
            if data:  # data가 빈 데이터가 아니라면
                hw_filtered_dict[height][weight] = data

    """
    surveys = readAndSave.read_json('man_size.json', 'utf8')

    height_list = [int(survey['104']) for survey in surveys]
    height_min, height_max = min(height_list) // 10 * 10, max(height_list) // 10 * 10  # 1774->1770

    hw_filtered_dict = {}
    for height in range(height_min, height_max + 10, 10):  # 10mm씩 키 검색
        print('height{}'.format(height))
        height_filtered_list = list(filter(partial(search_data, height=height), surveys))
        if len(height_filtered_list) == 0: continue  # 키 자료 없으면 안뽑기

        # 키 안에 있는 몸무게 데이터 접근
        weight_list = [float(height_filtered['510']) for height_filtered in height_filtered_list]
        weight_min, weight_max = round(min(weight_list)), round(max(weight_list))
        print('weight min{}, max {}'.format(weight_min, weight_max))

        hw_filtered_dict[height] = {}
        if weight_min == weight_max:  # 자료가 하나밖에 없다면(하나만 있으면 range 문이 안돌아가므로)
            weight = weight_min
            hw_filtered_dict[height][weight] = get_top_hw_filtered_dict(height, weight, height_filtered_list)
            continue
        for weight in range(weight_min, weight_max, 1):
            # 없는 몸무게도 일단 들어가는 문제
            data = get_top_hw_filtered_dict(height, weight, height_filtered_list)
            if data:  # data가 빈 데이터가 아니라면
                hw_filtered_dict[height][weight] = data
    """

    """바지로 바뀌면 위에 guess_uper_size만 바꾸면 된다"""
    readAndSave.save_json(hw_filtered_dict, 'bottom_hw_filtered_survey.json', 'utf8')