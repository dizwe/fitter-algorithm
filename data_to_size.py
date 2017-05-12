import readAndSave
from functools import partial

def search_data(data, height=None, weight=None):
    if height + 10 > int(data['104']) > height - 10:# 이런 범위도 나중에 분석해봐야함.
        if weight + 0.5 > float(data['510']) > weight - 0.5:
            return True
    return False


def guess_size(num, data):
    """0-어깨 1-가슴 2-팔 3-허리"""
    func_list = ['shoulder', 'chest', 'arm', 'waist']
    criteria_list = {
        'shoulder' : [395, 410, 425, 440, 460, 480, 500],
        'chest' : [840, 850, 930, 1010, 1080, 1200, 1280],
        'arm' : [560, 565, 585, 600, 615, 625, 625],
        'waist' : [720, 760, 840, 920, 1000, 1080, 1160],
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

    return size_name[max(size_num_list[i] for i in [0, 1, 3])] #팔 길이는 일단 빼기

surveys = readAndSave.read_json('man_size.json','utf8')
hw_filtered_surveys = list(filter(partial(search_data, height=1770, weight=70), surveys))

test =[[person[s] for s in ['104','510','317','208','233','212']] for person in hw_filtered_surveys]
print(test)

# 317 어깨너비 208 가슴둘레 233 팔길이 212 배꼽수준허리둘레 211 허리둘레
few_parameter_surveys =[[int(person[s]) for s in ['317','208','233','211']] for person in hw_filtered_surveys]
#어깨 가슴 팔 허리 기준으로 계산
guess_parameter_sizes = [[guess_size(parameter_num, parameter_data)
                        for parameter_num, parameter_data in enumerate(few_parameter_survey)]
                        for few_parameter_survey in few_parameter_surveys]
print(guess_parameter_sizes)
aggregate_sizes = [aggregate_size(guess_parameter_size) for guess_parameter_size in guess_parameter_sizes]

#data랑 예상 결과값 합치기!
train_data = zip(few_parameter_surveys,aggregate_sizes)
print(list(train_data))