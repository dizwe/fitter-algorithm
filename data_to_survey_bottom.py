from data_to_size import *


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
    # 211 허리둘레 241 배꼽수준 샅앞뒤길이 419 넙다리둘레
    # 115 엉덩뼈가시높이(발 길이도 있어-이건 그냥 비율로) 424 종아리 최소둘레 214 엉덩이

    # 이거 바꾸면 func_list max(size_num_list[i] for i in 다 바꿔야함)
    few_parameter_surveys = []
    for i, person in enumerate(hw_filtered_surveys):
        few_parameter_survey = []
        for s in ['211', '241', '419', '115', '424', '214']:
            # 밑위를 구하기(엉덩뼈가시높이-넙다리둘레)- 이거 이상행....
            if s == '241':
                # 샅전체-2(배꼽수준-엉덩뼈)
                crotch_total_len = int(person['241'])-2*(int(person['114'])-int(person['115']))
                # 앞샅길이(10:7 비율)
                front_crotch = crotch_total_len*7/17
                few_parameter_survey.append(round(front_crotch))
            elif s == '211':
                # 허리둘레를 실제 바지 허리둘레로 계산 9:10 정도?
                pant_waist_len = int(person['211'])/9*10
                few_parameter_survey.append(round(pant_waist_len))
            elif s == '115':  # 전체 길이에서 엉덩뼈가시높이로 계싼
                pant_len = int(person['115'])/11*10
                few_parameter_survey.append(round(pant_len))
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


"""바지로 바뀌면 위에 guess_uper_size만 바꾸면 된다"""
readAndSave.save_json(hw_filtered_dict, 'bottom_hw_filtered_survey_test.json', 'utf8')