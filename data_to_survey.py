import readAndSave
from functools import partial


def search_data(data, height=None, weight=None):
    if height + 5 > int(data['104']) >= height - 5:  # 이런 범위도 나중에 분석해봐야함.
        if weight == None:  # 아무것도 안적었을 때
            return True
        elif weight + 0.5 > float(data['510']) >= weight - 0.5:
            return True
    return False


def get_top_hw_filtered_dict(height, weight, filtered_surveys):
    #?????????? hw_filtered_surveys = list(filter(partial(search_data, height=height, weight=weight), surveys)) #surveys밖에 있는데도 돌아가네??????
    hw_filtered_surveys = list(filter(partial(search_data, height=height, weight=weight), filtered_surveys))
    if len(hw_filtered_surveys) ==0: return False  # 데이터 없으면 그냥 False

    # 104 키 317 어깨너비 208 가슴둘레 233 팔길이 212 배꼽수준허리둘레 211 허리둘레 유니클로가 허리둘레야
    # 이거 바꾸면 func_list max(size_num_list[i] for i in 다 바꿔야함)
    few_parameter_surveys = [[int(person[s]) for s in ['104', '317', '208', '233', '211']]
                             for person in hw_filtered_surveys]

    return few_parameter_surveys


def get_bottom_hw_filtered_dict(height, weight, filtered_surveys):
    #?????????? hw_filtered_surveys = list(filter(partial(search_data, height=height, weight=weight), surveys)) #surveys밖에 있는데도 돌아가네??????
    hw_filtered_surveys = list(filter(partial(search_data, height=height, weight=weight), filtered_surveys))
    if len(hw_filtered_surveys) == 0: return False  # 데이터 없으면 그냥 False

    # ['waist', 'crotch', 'thigh', 'length', 'hem', 'hip', 'crotch_height', 'middle_thigh', 'knee', 'calf']
    # 211 허리둘레 241 배꼽수준 샅앞뒤길이 419 넙다리둘레
    # 115 엉덩뼈가시높이(발 길이도 있어-이건 그냥 비율로) 424 종아리 최소둘레 214 엉덩이
    # 128 샅높이 420 넙다리 중간둘레 421 무릎둘레 423 장딴지 둘레
    # 이거 바꾸면 func_list max(size_num_list[i] for i in 다 바꿔야함)
    few_parameter_surveys = []
    for i, person in enumerate(hw_filtered_surveys):
        few_parameter_survey = []
        for s in ['211', '241', '419', '115', '424', '214', '128', '420', '421', '423']:
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
            elif s == '115':  # 전체 길이(100)에서 발목높이(6)로 계싼
                pant_len = int(person['115'])/50*47
                few_parameter_survey.append(round(pant_len))
            else:
                few_parameter_survey.append(int(person[s]))
        few_parameter_surveys.append(few_parameter_survey)

    return few_parameter_surveys


def get_whole_body_hw_filtered_dict(height, weight, filtered_surveys):
    hw_filtered_surveys = list(filter(partial(search_data, height=height, weight=weight), filtered_surveys))
    if len(hw_filtered_surveys) == 0: return False  # 데이터 없으면 그냥 False

    # ['shoulder', 'chest', 'arm', 'waist'
    # 'bottom_waist', 'crotch', 'thigh', 'length', 'hem', 'hip',
    # 'crotch_height', 'middle_thigh', 'knee', 'calf']

    few_parameter_surveys = []
    for i, person in enumerate(hw_filtered_surveys):
        few_parameter_survey = []
        param_list = ['317', '208', '233', '211',  # 317 어깨너비 208 가슴둘레 233 팔길이 211 허리둘레
                      '211-2', '241', '419', '115', '424', '214',  # 241 배꼽수준 샅앞뒤길이 419 넙다리둘레 115 엉덩뼈가시높이 424 종아리 최소둘레 214 엉덩이
                      '128', '420', '421', '423', '209']  # 128 샅높이 420 넙다리 중간둘레 421 무릎둘레 423 장딴지 둘레 209 젖가슴둘레
        for s in param_list:
            # 밑위를 구하기(엉덩뼈가시높이-넙다리둘레)- 이거 이상행....
            if s == '241':
                # 샅전체-2(배꼽수준-엉덩뼈)
                crotch_total_len = int(person['241'])-2*(int(person['114'])-int(person['115']))
                # 앞샅길이(10:7 비율)
                front_crotch = crotch_total_len*7/17
                few_parameter_survey.append(round(front_crotch))
            elif s == '211-2':
                # 허리둘레를 실제 바지 허리둘레로 계산 9:10 정도?
                pant_waist_len = int(person['211'])/9*10
                few_parameter_survey.append(round(pant_waist_len))
            elif s == '115':  # 전체 길이(100)에서 발목높이(6)로 계싼
                pant_len = int(person['115'])/50*47
                few_parameter_survey.append(round(pant_len))
            else:
                few_parameter_survey.append(int(person[s]))
        few_parameter_surveys.append(few_parameter_survey)

    return few_parameter_surveys


def main_function(sex_file, func):
    surveys = readAndSave.read_json(sex_file, 'utf8')

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
            hw_filtered_dict[height][weight] = func(height, weight, height_filtered_list)
            continue
        for weight in range(weight_min, weight_max+1, 1):
            # 없는 몸무게도 일단 들어가는 문제
            data = func(height, weight, height_filtered_list)
            if data:  # data 가 빈 데이터가 아니라면
                hw_filtered_dict[height][weight] = data

    return hw_filtered_dict


if __name__ == "__main__":
    func = get_whole_body_hw_filtered_dict
    save_file_name = 'whole_hw_filtered_survey_man_woman.json'

    man_hw_filtered_dict = main_function(sex_file='man_size.json', func=func)
    woman_hw_filtered_dict = main_function(sex_file='woman_size.json', func=func)

    hw_filtered_dict = {'man': man_hw_filtered_dict, 'woman': woman_hw_filtered_dict}

    readAndSave.save_json(hw_filtered_dict, save_file_name, 'utf8')


