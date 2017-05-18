import readAndSave
import scipy as sp
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

def size_str_to_num(size_list):
    #사이즈 숫자로 변환해서 계산하기 편하게 하기
    size_name = ["XS", "S", "M", "L", "XL", "XXL", "XXXL"]

    return [size_name.index(size) for size in size_list]



def draw_2d_dot(except_x=0, except_y=0):
    """기존에 있는 데이터를 [키, 몸무게] 리스트로 변환하기"""
    data = readAndSave.read_json('hw_filtered_dict.json', 'utf8')
    # {1770:{70:..}
    xy_tuple = [[int(x), int(y)] for x in data.keys() for y in data[x].keys()]

    #제외할 키, 몸무게(2개짜리 이상 구할때)
    if [except_x, except_y] in xy_tuple:
        del_index = xy_tuple.index([except_x, except_y])
        del xy_tuple[del_index]

    return xy_tuple



def find_close_distance(height, weight):
    #http://stackoverflow.com/questions/1401712/how-can-the-euclidean-distance-be-calculated-with-numpy
    """유클리드 거리 짧은거 찾기"""

    # 사용자와 이미 있는 자료들의 데이터 점
    user = np.array([height, weight])
    other_users = np.array(draw_2d_dot(height, weight))

    #데이터 점 중에 가장 가까운 점 찾기
    deltas = other_users - user
    dist = np.einsum('ij,ij->i', deltas, deltas) #deltas 값 제곱
    index = np.argmin(dist)#거기서 최소 index?

    return other_users[index].tolist()



"""자료가 두 개 이상이 될때까지"""
def find_good_data(user_height, user_weight, hw_filtered_sizes):
    """데이터가 없을때는 가까운 데이터 가져오기. 가져온 데이터가 한개라면 가까운 데이터 가져오기"""
    try:
        hw_filtered_size_nums = [size_str_to_num(size)
                                 for size in hw_filtered_sizes[str(user_height)][str(user_weight)]]

        def find_another_data():
            """2개 이하의 데이터가 있을 때 가까운 값에서 하나 더 찾아오기"""
            another_height, another_weight = find_close_distance(user_height, user_weight)

            another_data = [size_str_to_num(size)
                            for size in hw_filtered_sizes[str(another_height)][str(another_weight)]]

            hw_filtered_size_nums.extend(another_data)

        if len(hw_filtered_size_nums) < 2:
            find_another_data()

        return hw_filtered_size_nums

    except KeyError:
        """데이터가 없을 때"""
        assumed_height, assumed_weight = find_close_distance(user_height, user_weight)
        # 재귀 함수를 했으면 return도 해줘야지 여기서 끝나는게 아닌데
        return find_good_data(assumed_height, assumed_weight, hw_filtered_sizes)


def size_pdf(size, parameter):
    parameter_basic_info = [len(parameter) - 1, np.mean(parameter), np.std(parameter)]
    print(parameter_basic_info)
    xx = np.linspace(0, 6, 100)  # 그래프 범위
    print(i)

    rv = sp.stats.t(df=parameter_basic_info[0], loc=parameter_basic_info[1], scale=parameter_basic_info[2])
    plt.plot(xx, rv.pdf(xx))  # xx의 범위의 그래프르 stats pdf(probability density function)의 해당 값을 y값으로
    plt.draw()
    return rv.pdf(size) < 0.05



hw_filtered_sizes = readAndSave.read_json('hw_filtered_dict.json', 'utf8')
user_height = 1770
user_weight = 70

#괜찮은 사이즈를 찾고 글자 데이터를 숫자로 바꾸기
hw_filtered_size_nums = find_good_data(user_height, user_weight, hw_filtered_sizes)
#몸 부위별로 모으기
size_each_parameter = [[one_person[parameter]
                        for one_person in hw_filtered_size_nums] for parameter in range(5)]


#자유도, 기댓값, 표준편차 계산(이건 데이터가 다를때 해야되는 거겠지)
suggest_size = []
question = [None, 'Small', 'Small', 'Small', 'Big'] # ~하면 가 남는 편이다
# ['height', 'shoulder', 'chest', 'arm', 'waist'] 순서
for i, parameter in enumerate(size_each_parameter):
    if len(set(parameter)) == 1: # 자료 종류가 하나라면
        suggest_size.append(parameter[0]) # 그냥 자료 붙이기
    else:  # 종류가 여러개라면 질문에 맞춰서
        if question[i] is None:
            size = Counter(parameter).most_common(1)[0]
            suggest_size.append(size)
        elif question[i] == 'Big':
            size = max(parameter)
            size = size-1 if size_pdf(size, parameter)<0.05 else size
            suggest_size.append(size)
        elif question[i] == 'Small':
            size = min(parameter)
            size = size + 1 if size_pdf(size, parameter) < 0.05 else size
            suggest_size.append(size)

print(suggest_size)