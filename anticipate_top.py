from anticipate_size import *


def top_size_to_real(size_list):
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

if __name__ == "__main__":
    """상의"""
    # 바뀌는 파트
    hw_filtered_sizes = readAndSave.read_json('hw_filtered_dict_every_1cm.json', 'utf8')
    user_height = 1770
    user_weight = 70

    # 괜찮은 사이즈를 찾고 글자 데이터를 숫자로 바꾸기
    hw_filtered_size_nums = str_to_int_find_good_data(user_height, user_weight, hw_filtered_sizes)
    # 몸 부위별로 모으기
    size_each_parameter = [[one_person[parameter]
                            for one_person in hw_filtered_size_nums]
                           for parameter in range(len(hw_filtered_size_nums[0]))]

    """예상 사이즈 추천하기"""
    # 답변에 따라서
    # ['height', 'shoulder', 'chest', 'arm', 'waist'] 순서 / 1 은 보통 0이 SMALL
    question = [1, 0, 2, 1, 1]  # ~하면 가 남는 편이다
    suggested_size = guess_size_by_question(question, size_each_parameter)
    suggested_real = top_size_to_real(suggested_size)
    print(suggested_size)