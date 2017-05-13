import readAndSave
from functools import partial

def data_min_to_max():
    pass
def search_data(data, height=None, weight=None):
    if height + 10 > int(data['104']) > height - 10:# 이런 범위도 나중에 분석해봐야함.
        if weight == None: #아무것도 안적었을 때
            return True
        elif weight + 0.5 > float(data['510']) > weight - 0.5:
            return True
    return False


def guess_size(num, data):
    """0-어깨 1-가슴 2-팔 3-허리"""
    func_list = ['height', 'shoulder', 'chest', 'arm', 'waist']
    criteria_list = {
        'shoulder' : [395, 410, 425, 440, 460, 480, 500],
        'chest' : [840, 850, 930, 1010, 1080, 1200, 1280],
        'arm' : [560, 565, 585, 600, 615, 625, 625],
        'waist' : [720, 760, 840, 920, 1000, 1080, 1160],
        'height': [1650, 1650, 1750, 2000, 2100, 2100, 2100], # 일단 작은걸로 되개 하자.2000은 그냥 의미없음
    }
    size_names = ["XS", "S", "M", "L", "XL", "XXL", "XXXL"]

    def guess(criterias):
        for criteria, name in zip(criterias, size_names):
            if data <= criteria:
                return name
        return size_names[-1]

    return guess(criteria_list[func_list[num]])


def aggregate_size(size_list):
    #사이즈 숫자로 변환해서 계산하기 편하게 하기
    size_name = ["XS", "S", "M", "L", "XL", "XXL", "XXXL"]
    size_num_list = [size_name.index(size) for size in size_list]

    return size_name[max(size_num_list[i] for i in [0, 1, 2, 4])] #팔 길이는 일단 빼기

def get_hw_filtered_dict(height, weight, filtered_surveys):
    #?????????? hw_filtered_surveys = list(filter(partial(search_data, height=height, weight=weight), surveys)) #surveys밖에 있는데도 돌아가네??????
    hw_filtered_surveys = list(filter(partial(search_data, height=height, weight=weight), filtered_surveys))
    if len(hw_filtered_surveys) ==0: return False# 데이터 없으면 그냥 False

    # 104 키317 어깨너비 208 가슴둘레 233 팔길이 212 배꼽수준허리둘레 211 허리둘레
    # 이거 바꾸면 func_list max(size_num_list[i] for i in 다 바꿔야함
    few_parameter_surveys = [[int(person[s]) for s in ['104', '317', '208', '233', '211']]
                             for person in hw_filtered_surveys]

    #어깨 가슴 팔 허리 기준으로 계산
    guess_parameter_sizes = [[guess_size(parameter_num, parameter_data)
                             for parameter_num, parameter_data in enumerate(few_parameter_survey)]
                             for few_parameter_survey in few_parameter_surveys]

    return guess_parameter_sizes


if __name__ == "__main__":
    surveys = readAndSave.read_json('man_size.json','utf8')

    height_list = [int(survey['104']) for survey in surveys]
    height_min, height_max = min(height_list)//10 * 10, max(height_list)//10 * 10 # 1774->1770

    hw_filtered_dict = {}
    for height in range(height_min, height_max + 10, 10):#10mm씩 키 검색
        print(height)
        height_filtered_list = list(filter(partial(search_data, height=height), surveys))
        if len(height_filtered_list) == 0: continue # 키 자료 없으면 안뽑기

        weight_list = [float(height_filtered['510']) for height_filtered in height_filtered_list]
        weight_min, weight_max = round(min(weight_list)) , round(max(weight_list))
        print(weight_min, weight_max)

        hw_filtered_dict[height]={}
        if weight_min == weight_max: # 자료가 하나밖에 없다면
            weight = weight_min
            hw_filtered_dict[height][weight] = get_hw_filtered_dict(height, weight, height_filtered_list)
            continue
        for weight in range(weight_min, weight_max, 1):
            # 없는 몸무게도 일단 들어가는 문제
            data = get_hw_filtered_dict(height, weight, height_filtered_list)
            if data: # data가 빈 데이터가 아니라면
                hw_filtered_dict[height][weight] = data


readAndSave.save_json(hw_filtered_dict, 'hw_filtered_dict.json', 'utf8')

#에상 하는 부분 제거
# print(guess_parameter_sizes)
# aggregate_sizes = [aggregate_size(guess_parameter_size) for guess_parameter_size in guess_parameter_sizes]
# print(len(list(filter(lambda x: x=="M",aggregate_sizes))))
# #data랑 예상 결과값 합치기!
# train_data = zip(few_parameter_surveys,aggregate_sizes)
# print(list(train_data))