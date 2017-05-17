import readAndSave
import scipy as sp
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt

hw_filtered_sizes = readAndSave.read_json('hw_filtered_dict.json', 'utf8')
user_height= 1900
user_weight= 60

def size_str_to_num(size_list):
    #사이즈 숫자로 변환해서 계산하기 편하게 하기
    size_name = ["XS", "S", "M", "L", "XL", "XXL", "XXXL"]

    return [size_name.index(size) for size in size_list]

def compare_correlation():
    """키~ 몸무게 제외 변수, 몸무게~ 키 제외 변수 상관계수 찾기"""
    surveys = readAndSave.read_json('man_size.json', 'utf8')

    # 104 키317 어깨너비 208 가슴둘레 233 팔길이 212 배꼽수준허리둘레 211 허리둘레
    few_parameter_surveys = [[float(person[s]) for s in ['104', '510', '317', '208', '233', '211']]
                             for person in surveys]

    # parameter_surveys_list = list(zip(*few_parameter_surveys)) # zip으로 여러개 list를 한꺼번에 묶기
    parameter_surveys_list = np.array(few_parameter_surveys).T # 위에랑 똑같은 소리

    height_correlation = [np.corrcoef(parameter_surveys_list[0],
                                parameter_surveys_list[par_num]) for par_num in [2, 3, 4, 5]]
    weight_correlation = [np.corrcoef(parameter_surveys_list[1],
                                parameter_surveys_list[par_num]) for par_num in [2, 3, 4, 5]]

    return height_correlation, weight_correlation


def find_close_distance_with_weight(height, weight, parameter_num):
    """각 파라미터와 키, 몸무게의 상관계수를 가중치로 계산"""
    #http://stackoverflow.com/questions/1401712/how-can-the-euclidean-distance-be-calculated-with-numpy
    # 유클리드 거리 짧은거 찾기
    height_cor, weight_cor = compare_correlation()

    # 여기 가중치가 커질수록 해당 값을 '보존'하려는게 커진다.
    hw_cor = [round(height_cor[parameter_num][0, 1], 1), round(weight_cor[parameter_num][0, 1], 1)]

    # 사용자와 이미 있는 자료들의 데이터 점
    user = np.array([height, weight])
    other_users = np.array(draw_2d_dot())

    #데이터 점 중에 가장 가까운 점 찾기
    deltas = np.multiply(hw_cor, other_users)-np.multiply(hw_cor, user)
    dist = np.einsum('ij,ij->i', deltas, deltas) #deltas 값 제곱
    index = np.argmin(dist)#거기서 최소 index?

    return other_users[index].tolist()


def draw_2d_dot():
    """기존에 있는 데이터를 [키, 몸무게] 리스트로 변환하기"""
    data = readAndSave.read_json('hw_filtered_dict.json', 'utf8')
    # {1770:{70:..}
    xy_tuple = [[int(x), int(y)] for x in data.keys() for y in data[x].keys()]

    return xy_tuple



def find_close_distance(height, weight):
    #http://stackoverflow.com/questions/1401712/how-can-the-euclidean-distance-be-calculated-with-numpy
    """유클리드 거리 짧은거 찾기"""

    # 사용자와 이미 있는 자료들의 데이터 점
    user = np.array([height, weight])
    other_users = np.array(draw_2d_dot())

    #데이터 점 중에 가장 가까운 점 찾기
    deltas = other_users - user
    dist = np.einsum('ij,ij->i', deltas, deltas) #deltas 값 제곱
    index = np.argmin(dist)#거기서 최소 index?

    return other_users[index].tolist()


#숫자로 바꾸기
try:
    # 하나만 있어도 문제가 되어야할듯(확률 계산이 불가능)
    hw_filtered_sizes = [size_str_to_num(size)
                         for size in hw_filtered_sizes[str(user_height)][str(user_weight)]]
    print(hw_filtered_sizes)
except KeyError:#실제로 없는 Key 라면?
    # 비슷한 자료 찾기
    assumed_height, assumed_weight = find_close_distance(user_height, user_weight)
    # 키는 소수점이 아니라 int가 되어야함(원래 float임)
    print(assumed_height, assumed_weight)
    hw_filtered_sizes = [size_str_to_num(size)
                         for size in hw_filtered_sizes[str(assumed_height)][str(assumed_weight)]]

    print(hw_filtered_sizes)

#몸 부위별로 모으기
size_each_parameter = [[one_person[parameter]
                        for one_person in hw_filtered_sizes] for parameter in range(5)]
print(size_each_parameter)

#자유도, 기댓값, 표준편차 계산
parameter_basic_info = [(len(parameter)-1, np.mean(parameter), np.std(parameter)) for parameter in size_each_parameter]
print(parameter_basic_info)
xx = np.linspace(0, 6, 100)
rv = sp.stats.t(df=parameter_basic_info[4][0], loc=parameter_basic_info[4][1], scale=parameter_basic_info[4][2])
plt.plot(xx, rv.pdf(xx))#xx의 범위의 그래프르 stats pdf(probability density function)의 해당 값을 y값으로
print(rv.pdf(2))
plt.show()
