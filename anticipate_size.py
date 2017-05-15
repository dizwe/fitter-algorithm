import readAndSave
import scipy as sp
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt
hw_filtered_sizes = readAndSave.read_json('hw_filtered_dict.json', 'utf8')
# print(hw_filtered_sizes['1930'])
user_height= 1930
user_weight= 76

def size_str_to_num(size_list):
    #사이즈 숫자로 변환해서 계산하기 편하게 하기
    size_name = ["XS", "S", "M", "L", "XL", "XXL", "XXXL"]

    return [size_name.index(size) for size in size_list]

def compare_covariance():
    surveys = readAndSave.read_json('man_size.json', 'utf8')

    # 104 키317 어깨너비 208 가슴둘레 233 팔길이 212 배꼽수준허리둘레 211 허리둘레
    few_parameter_surveys = [[float(person[s]) for s in ['104', '510', '317', '208', '233', '211']]
                             for person in surveys]

    # parameter_surveys_list = list(zip(*few_parameter_surveys)) # zip으로 여러개 list를 한꺼번에 묶기
    parameter_surveys_list = np.array(few_parameter_surveys).T # 위에랑 똑같은 소리

    print(parameter_surveys_list)

    height_covariance = [np.corrcoef(parameter_surveys_list[0],
                                parameter_surveys_list[par_num]) for par_num in [2, 3, 4, 5]]
    weight_covariance = [np.corrcoef(parameter_surveys_list[1],
                                parameter_surveys_list[par_num]) for par_num in [2, 3, 4, 5]]

    print(height_covariance[1][0, 1])
    print(weight_covariance[1][0, 1])

compare_covariance()

# #숫자로 바꾸기
# hw_filtered_sizes = [size_str_to_num(size)
#                      for size in hw_filtered_sizes[str(user_height)][str(user_weight)]]
# print(hw_filtered_sizes)
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
