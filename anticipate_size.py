import readAndSave
import scipy as sp
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


def size_str_to_num(size_list):
    # 사이즈 숫자로 변환해서 계산하기 편하게 하기
    size_name = ["XS", "S", "M", "L", "XL", "XXL", "XXXL"]

    return [size_name.index(param_size) for param_size in size_list]


def draw_2d_dot(except_x=0, except_y=0, all_data={}):
    """기존에 있는 데이터를 [키, 몸무게] 리스트로 변환하기"""
    # {1770:{70:..}
    xy_tuple = [[int(x), int(y)] for x in all_data.keys() for y in all_data[x].keys()]

    # 제외할 키, 몸무게(2개짜리 이상 구할때)
    if [except_x, except_y] in xy_tuple:
        del_index = xy_tuple.index([except_x, except_y])
        del xy_tuple[del_index]

    return xy_tuple


def find_close_distance(height, weight, all_data):
    # http://stackoverflow.com/questions/1401712/how-can-the-euclidean-distance-be-calculated-with-numpy
    """유클리드 거리 짧은거 찾기"""

    # 사용자와 이미 있는 자료들의 데이터 점
    user = np.array([height, weight])
    other_users = np.array(draw_2d_dot(height, weight, all_data))

    # 데이터 점 중에 가장 가까운 점 찾기
    deltas = other_users - user
    dist = np.einsum('ij,ij->i', deltas, deltas)  # deltas 값 제곱
    index = np.argmin(dist)  # 거기서 최소 index?

    return other_users[index].tolist()


# 자료가 두 개 이상이 될때까지
def str_to_int_find_good_data(height, weight, hw_filtered_sizes):
    """데이터가 없을때는 가까운 데이터 가져오기. 가져온 데이터가 한개라면 가까운 데이터 가져오기"""

    try:
        hw_filtered_size_nums = [size_str_to_num(a_person)
                                 for a_person in hw_filtered_sizes[str(height)][str(weight)]]

        def find_another_data():
            """2개 이하의 데이터가 있을 때 가까운 값에서 하나 더 찾아오기"""
            """# 큰 데이터가 너무 왔다갔다 하는거 아닌가... 싶다 문제문제~~~"""
            another_height, another_weight = find_close_distance(height, weight, hw_filtered_sizes)

            another_data = [size_str_to_num(a_person)
                            for a_person in hw_filtered_sizes[str(another_height)][str(another_weight)]]

            hw_filtered_size_nums.extend(another_data)

        if len(hw_filtered_size_nums) < 2:
            find_another_data()

        return hw_filtered_size_nums

    except KeyError:
        """데이터가 없을 때"""
        assumed_height, assumed_weight = find_close_distance(height, weight, hw_filtered_sizes)
        # 재귀 함수를 했으면 return 도 해줘야지 여기서 끝나는게 아닌데
        return str_to_int_find_good_data(assumed_height, assumed_weight, hw_filtered_sizes)


def int_find_good_data(height, weight, hw_filtered_sizes):
    """데이터가 없을때는 가까운 데이터 가져오기. 가져온 데이터가 한개라면 가까운 데이터 가져오기"""
    """줄 두줄 바뀌는건데 어떻게 잘 할 방법 없을까?(데코레이터)"""
    try:
        hw_filtered_size_nums = [a_person
                                 for a_person in hw_filtered_sizes[str(height)][str(weight)]]

        def find_another_data():
            """2개 이하의 데이터가 있을 때 가까운     값에서 하나 더 찾아오기"""
            """# 큰 데이터가 너무 왔다갔다 하는거 아닌가... 싶다 문제문제~~~"""
            another_height, another_weight = find_close_distance(height, weight, hw_filtered_sizes)

            another_data = [a_person
                            for a_person in hw_filtered_sizes[str(another_height)][str(another_weight)]]

            hw_filtered_size_nums.extend(another_data)

        if len(hw_filtered_size_nums) < 2:
            find_another_data()

        return hw_filtered_size_nums

    except KeyError:
        """데이터가 없을 때"""
        assumed_height, assumed_weight = find_close_distance(height, weight, hw_filtered_sizes)
        # 재귀 함수를 했으면 return 도 해줘야지 여기서 끝나는게 아닌데
        return str_to_int_find_good_data(assumed_height, assumed_weight, hw_filtered_sizes)


def guess_size_by_question(qna, sizes_each_parameter, data_error=0.05):
    """이미 잘라진 사이즈가 주어졌을때 질문에 따라서 작다고 하면 '확률상 유의미하면' 작은걸로"""
    suggest_size = []
    for i, parameter in enumerate(sizes_each_parameter):
        if len(set(parameter)) == 1:  # 자료 종류가 하나라면
            suggest_size.append(parameter[0])  # 그냥 자료 붙이기
        else:  # 종류가 여러개라면 질문에 맞춰서
            if qna[i] == 1:
                size = Counter(parameter).most_common(1)[0][0]
                suggest_size.append(size)
            elif qna[i] == 2:  # 크다고 답했다면
                size = max(parameter)
                size = size-1 if size_p_value(size, parameter) < data_error else size
                suggest_size.append(size)
            elif qna[i] == 0:
                size = min(parameter)
                size = size + 1 if size_p_value(size, parameter) < data_error else size
                suggest_size.append(size)

    return suggest_size


def get_median(a):
    a_len = len(a)                # 배열 요소들의 전체 개수 구하기
    if a_len == 0: return None  # 빈 배열은 에러 반환
    a_center = int(a_len / 2)     # 요소 개수의 절반값 구하기

    if a_len % 2 == 1:   # 요소 개수가 홀수면
        return a[a_center]   # 홀수 개수인 배열에서는 중간 요소를 그대로 반환
    else:
        return (a[a_center - 1] + a[a_center]) / 2.0 # 짝수 개 요소는, 중간 두 수의 평균 반환


def guess_int_by_question(qna, sizes_each_parameter, data_error=0.05):
    """바지는 길이라서 최빈값은 의미가 없엉 ㅜㅜ 최빈값만 정리하기? medium으로"""
    """질문에 따라서 작다고 하면 '확률상 유의미하면' 작은걸로"""
    suggest_size = []
    for i, parameter in enumerate(sizes_each_parameter):
        if len(set(parameter)) == 1:  # 자료 종류가 하나라면
            suggest_size.append(parameter[0])  # 그냥 자료 붙이기
        else:  # 종류가 여러개라면 질문에 맞춰서
            sorted_param = sorted(parameter)
            if qna[i] == 1:
                size = get_median(sorted_param) # 중앙값
                suggest_size.append(size)
            elif qna[i] == 2:  # 크다고 답했다면
                # 해당값이 말이 될때까지 찾기
                size = find_size_under_significance(sorted_param, start_index=-1, data_error=data_error)
                suggest_size.append(size)
            elif qna[i] == 0:
                size = find_size_under_significance(sorted_param, start_index=0, data_error=data_error)
                suggest_size.append(size)

    return suggest_size


def find_size_under_significance(sorted_data, start_index=0, data_error=0.05):
    """적당 확률 찾을때까지 돌리기"""
    test_data = sorted_data[start_index]

    while size_p_value(test_data, sorted_data) < data_error:  # error 허용범위를 넘는다면
        # 0이면 1씩 커지고 -1이면 1씩 작아지고
        print(sorted_data)
        start_index = start_index+1 if start_index >= 0 else start_index-1
        test_data = sorted_data[start_index]
        print(test_data)
    return test_data


def size_p_value(size, parameter, direction='left'):
    """t분포표 만들고 p value 리턴하기"""
    # 자유도, 기댓값, 표준편차 계산(이건 데이터가 다를때 해야되는 거겠지)
    parameter_basic_info = [len(parameter) - 1, np.mean(parameter), np.std(parameter)]

    xx = np.linspace(min(parameter), max(parameter), 100)  # 그래프 범위

    rv = sp.stats.t(df=parameter_basic_info[0], loc=parameter_basic_info[1], scale=parameter_basic_info[2])
    plt.plot(xx, rv.pdf(xx))  # xx의 범위의 그래프르 stats pdf(probability density function)의 해당 값을 y값으로
    # plt.show()
    if direction == 'left':
        return rv.pdf(size)
    elif direction == 'right':
        return rv.sf(size)


def size_to_real(size_list):
    """다시 실측값으로 바꾸기"""
    func_list = ['height', 'shoulder', 'chest', 'arm', 'waist']
    # ["XS", "S", "M", "L", "XL", "XXL", "XXXL"]
    criteria_list = {
        'shoulder': [395, 410, 425, 440, 460, 480, 500],  # 애매 기준
        'chest': [840, 850, 930, 1010, 1080, 1200, 1280],
        'arm': [560, 565, 585, 600, 615, 625, 625],  # 애매 기준
        'waist': [720, 760, 840, 920, 1000, 1080, 1160],
        'height': [1650, 1650, 1750, 2000, 2100, 2100, 2100],  # 일단 작은걸로 되개 하자.2000은 그냥 의미없음
    }

    each_par_real = {}
    for i, size in enumerate(size_list):
        parameter_size_list = criteria_list[func_list[i]]
        each_par_real[func_list[i]] = parameter_size_list[size]

    return each_par_real


"""하의도 여기서는 딱히 바꿀 것이 없을거"""
if __name__ == "__main__":
    """상의"""
    # # 바뀌는 파트
    # hw_filtered_sizes = readAndSave.read_json('hw_filtered_survey.json', 'utf8')
    # user_height = 1770
    # user_weight = 70
    #
    # # 괜찮은 사이즈를 찾고 글자 데이터를 숫자로 바꾸기
    # hw_filtered_size_nums = str_to_int_find_good_data(user_height, user_weight, hw_filtered_sizes)
    # # 몸 부위별로 모으기
    # size_each_parameter = [[one_person[parameter]
    #                         for one_person in hw_filtered_size_nums] for parameter in range(5)]
    #
    # """예상 사이즈 추천하기"""
    # # 답변에 따라서
    # # ['height', 'shoulder', 'chest', 'arm', 'waist'] 순서 / 1 은 보통 0이 SMALL
    # question = [1, 0, 2, 1, 1]  # ~하면 가 남는 편이다
    # suggested_size = guess_size_by_question(question, size_each_parameter)
    # suggested_real = size_to_real(suggested_size)
    # print(suggested_size)

    """하의"""
    # 바뀌는 파트
    hw_filtered_sizes = readAndSave.read_json('bottom_hw_filtered_survey.json', 'utf8')
    user_height = 1770
    user_weight = 70

    # 괜찮은 사이즈를 찾고 글자 데이터를 숫자로 바꾸기
    hw_filtered_size_nums = int_find_good_data(user_height, user_weight, hw_filtered_sizes)
    # 몸 부위별로 모으기
    size_each_parameter = [[one_person[parameter]
                            for one_person in hw_filtered_size_nums] for parameter in range(5)]

    """예상 사이즈 추천하기"""
    # 답변에 따라서
    # ['waist', 'crotch', 'thigh', 'length', 'hem', 'hip'] 순서
    question = [0, 1, 2, 1, 1, 2]  # ~하면 가 남는 편이다
    suggested_size = guess_int_by_question(question, size_each_parameter) # 숫자니까..
    # suggested_real = size_to_real(suggested_size)
    print(suggested_size)
