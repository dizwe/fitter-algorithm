import readAndSave
import scipy as sp
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt
hw_filtered_sizes = readAndSave.read_json('hw_filtered_dict.json', 'utf8')
# print(hw_filtered_sizes['1930'])
user_height= 1900
user_weight= 30

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

    print(parameter_surveys_list)

    height_correlation = [np.corrcoef(parameter_surveys_list[0],
                                parameter_surveys_list[par_num]) for par_num in [2, 3, 4, 5]]
    weight_correlation = [np.corrcoef(parameter_surveys_list[1],
                                parameter_surveys_list[par_num]) for par_num in [2, 3, 4, 5]]

    print(height_correlation[2][0, 1])
    print(weight_correlation[2][0, 1])

    return height_correlation, weight_correlation

def rank_keys():
    #비효율적으로 생겼당
    surveys = readAndSave.read_json('hw_filtered_dict.json', 'utf8')

    sorted_height = sorted([int(height)
                           for height in surveys.keys()])

    sorted_weight = sorted(set([float(weight) # 중복제거
                                for height in surveys.keys()
                                for weight in surveys[height]]))

    hw_tuple = [[int(height), float(weight)]
                for height in surveys.keys()
                for weight in surveys[height]]


    return hw_tuple



def find_close_distance(height, weight):
    #http://stackoverflow.com/questions/1401712/how-can-the-euclidean-distance-be-calculated-with-numpy
    # 유클리드 거리 짧은거 찾기
    height_cor, weight_cor = compare_correlation()

    user = np.array([height, weight])
    #일단 키랑 몸무게 리스트들을 뽑아봐야겠군

    other_users = np.array(rank_keys())

    deltas = other_users-user # x는 x값끼리 y는 y값끼리
    dist = np.einsum('ij,ij->i', deltas, deltas) #deltas 값 제곱

    index = np.argmin(dist)#거기서 최소 index?
    print(other_users[index])




find_close_distance(user_height, user_weight)
# #숫자로 바꾸기
# try:
#     hw_filtered_sizes = [size_str_to_num(size)
#                          for size in hw_filtered_sizes[str(user_height)][str(user_weight)]]
# except KeyError:#실제로 없는 Key 라면?
#     # 일단 자료찾기
#     find_distance(user_height, user_weight)
#     print()
#
# #몸 부위별로 모으기
# size_each_parameter = [[one_person[parameter]
#                         for one_person in hw_filtered_sizes] for parameter in range(5)]
# print(size_each_parameter)
#
# #자유도, 기댓값, 표준편차 계산
# parameter_basic_info = [(len(parameter)-1, np.mean(parameter), np.std(parameter)) for parameter in size_each_parameter]
# print(parameter_basic_info)
# xx = np.linspace(0, 6, 100)
# rv = sp.stats.t(df=parameter_basic_info[4][0], loc=parameter_basic_info[4][1], scale=parameter_basic_info[4][2])
# plt.plot(xx, rv.pdf(xx))#xx의 범위의 그래프르 stats pdf(probability density function)의 해당 값을 y값으로
# print(rv.pdf(2))
# plt.show()
